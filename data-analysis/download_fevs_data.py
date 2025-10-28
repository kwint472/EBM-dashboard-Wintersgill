"""
Download Federal Employee Viewpoint Survey (FEVS) Data
U.S. Office of Personnel Management

This script downloads FEVS data focusing on leadership quality indicators
and employee wellbeing/burnout measures from federal healthcare agencies.
"""

import pandas as pd
import requests
from io import StringIO
import os

# FEVS Public Data Files
# These are the most recent available datasets
FEVS_DATA_URLS = {
    '2023': 'https://www.opm.gov/fevs/public-data-file/2023/2023_FEVS_Gwide_Final_Data_File.csv',
    '2022': 'https://www.opm.gov/fevs/public-data-file/2022/2022_FEVS_Gwide_Final_Data_File.csv',
    '2021': 'https://www.opm.gov/fevs/public-data-file/2021/2021_FEVS_Gwide_Final_Data_File.csv',
    '2020': 'https://www.opm.gov/fevs/public-data-file/2020/2020_FEVS_Gwide_Final_Data_File.csv',
    '2019': 'https://www.opm.gov/fevs/public-data-file/2019/2019_FEVS_Gwide_Final_Data_File.csv',
}

# Healthcare-related agencies to filter
HEALTHCARE_AGENCIES = [
    'VH',   # Veterans Health Administration (VA Hospitals)
    'HE',   # Health and Human Services
    'CM',   # Centers for Medicare & Medicaid Services  
    'CD',   # Centers for Disease Control and Prevention
    'FD',   # Food and Drug Administration
    'IH',   # Indian Health Service
    'HR',   # Health Resources and Services Administration
    'NI',   # National Institutes of Health
    'SA',   # Substance Abuse and Mental Health Services Administration
]

# Key survey items related to leadership and burnout
# Q1-Q10: Leadership & Supervision
# Q40: Job Satisfaction
# Q69-Q71: Work-Life Balance (Burnout Indicators)

KEY_ITEMS = {
    # LEADERSHIP EFFECTIVENESS INDICATORS (X Variables)
    'Q51': 'My organization leaders maintain high standards of honesty and integrity',
    'Q53': 'In my organization, leaders generate high levels of motivation',
    'Q54': 'My organization\'s leaders maintain high communication effectiveness',
    'Q56': 'Managers promote communication among different work units',
    'Q60': 'Overall, how good a job do you feel is being done by your immediate supervisor',
    
    # BURNOUT & SATISFACTION INDICATORS (Y Variables)  
    'Q40': 'I recommend my organization as a good place to work',
    'Q69': 'How satisfied are you with your involvement in decisions that affect your work',
    'Q70': 'How satisfied are you with the information you receive about work',
    'Q71': 'How satisfied are you with the recognition you receive',
    'Q72': 'Considering everything, how satisfied are you with your job',
    'Q92': 'Considering everything, how satisfied are you with your pay',
    
    # WORK-LIFE & STRESS INDICATORS
    'DEMPBURNT': 'I feel burned out by my work',
    'DSTRESS': 'My work involves a great deal of stress',
    'DWORKLOAD': 'My workload is reasonable',
}

def download_fevs_year(year, url):
    """
    Download FEVS data for a specific year
    
    Args:
        year: Year of survey
        url: URL to CSV file
    
    Returns:
        pandas DataFrame with FEVS data
    """
    print(f"  Downloading {year} data...")
    
    try:
        # Try direct CSV download
        df = pd.read_csv(url, encoding='latin-1', low_memory=False)
        print(f"    ✓ {year}: {len(df)} responses")
        return df
        
    except Exception as e:
        print(f"    ✗ {year}: Download failed - {e}")
        print(f"    Note: Manual download may be required from OPM website")
        return None

def filter_healthcare_agencies(df, year):
    """
    Filter FEVS data to healthcare-related agencies
    
    Args:
        df: Full FEVS dataframe
        year: Survey year
    
    Returns:
        Filtered DataFrame with healthcare agencies only
    """
    if df is None:
        return None
    
    # Try different agency column names used across years
    agency_cols = ['AGENCY', 'DAGENCY', 'Agency', 'agency']
    agency_col = None
    
    for col in agency_cols:
        if col in df.columns:
            agency_col = col
            break
    
    if agency_col is None:
        print(f"    Warning: Could not find agency column in {year} data")
        return df
    
    # Filter to healthcare agencies
    healthcare_df = df[df[agency_col].isin(HEALTHCARE_AGENCIES)].copy()
    
    if len(healthcare_df) > 0:
        print(f"    ✓ Filtered to {len(healthcare_df)} healthcare agency responses")
        return healthcare_df
    else:
        print(f"    ⚠ No healthcare agencies found with codes {HEALTHCARE_AGENCIES}")
        return df  # Return full dataset if filter fails

def extract_key_variables(df, year):
    """
    Extract and rename key leadership and burnout variables
    
    Args:
        df: FEVS dataframe
        year: Survey year
    
    Returns:
        DataFrame with key variables only
    """
    if df is None:
        return None
    
    # Find which key items exist in this year's data
    available_items = [col for col in KEY_ITEMS.keys() if col in df.columns]
    
    if not available_items:
        print(f"    Warning: No key items found in {year} data")
        print(f"    Available columns: {list(df.columns[:20])}...")  # Show first 20
        return None
    
    # Extract key variables plus year identifier
    subset_df = df[available_items].copy()
    subset_df['year'] = int(year)
    
    print(f"    ✓ Extracted {len(available_items)} key variables")
    
    return subset_df

def aggregate_leadership_burnout_scores(df):
    """
    Create composite leadership and burnout indices
    
    Args:
        df: DataFrame with individual survey items
    
    Returns:
        DataFrame with aggregated scores
    """
    if df is None or len(df) == 0:
        return None
    
    # Leadership Effectiveness Composite (X Variable)
    leadership_items = ['Q51', 'Q53', 'Q54', 'Q56', 'Q60']
    available_leadership = [col for col in leadership_items if col in df.columns]
    
    if available_leadership:
        # Convert to numeric, handling string responses
        for col in available_leadership:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['leadership_effectiveness_index'] = df[available_leadership].mean(axis=1, skipna=True)
    
    # Burnout/Dissatisfaction Composite (Y Variable)
    burnout_items = ['Q40', 'Q69', 'Q70', 'Q71', 'Q72']
    available_burnout = [col for col in burnout_items if col in df.columns]
    
    if available_burnout:
        # Convert to numeric
        for col in available_burnout:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Reverse code so higher = more burnout (consistent with quit rate direction)
        # Original scale: 5=Very Satisfied, 1=Very Dissatisfied
        # Reversed: 5=Very Dissatisfied (high burnout), 1=Very Satisfied (low burnout)
        df['burnout_dissatisfaction_index'] = 6 - df[available_burnout].mean(axis=1, skipna=True)
    
    return df

def main():
    """Main execution function"""
    print("=" * 70)
    print("FEVS Healthcare Agency Data Download")
    print("U.S. Office of Personnel Management - Federal Employee Viewpoint Survey")
    print("=" * 70)
    print()
    
    print("📊 Target Variables:")
    print("   X (Leadership): Supervisor effectiveness, leadership integrity,")
    print("                   communication, motivation")
    print("   Y (Burnout): Job satisfaction, burnout, stress, workload,")
    print("               recognition, work-life balance")
    print()
    print("🏥 Healthcare Agencies:")
    print("   VA Hospitals, HHS, CDC, FDA, NIH, CMS, IHS, HRSA, SAMHSA")
    print()
    print("=" * 70)
    print()
    
    all_data = []
    
    for year, url in FEVS_DATA_URLS.items():
        print(f"📥 Processing {year}...")
        
        # Download
        df = download_fevs_year(year, url)
        
        if df is not None:
            # Filter to healthcare agencies
            df_healthcare = filter_healthcare_agencies(df, year)
            
            # Extract key variables
            df_subset = extract_key_variables(df_healthcare, year)
            
            if df_subset is not None:
                # Aggregate scores
                df_scores = aggregate_leadership_burnout_scores(df_subset)
                
                if df_scores is not None:
                    all_data.append(df_scores)
        
        print()
    
    if not all_data:
        print("\n❌ No data successfully downloaded.")
        print("\n📝 NOTE: FEVS data may require manual download from:")
        print("   https://www.opm.gov/fevs/public-data-file/")
        print("\n   If automatic download fails, please:")
        print("   1. Visit the URL above")
        print("   2. Download CSV files for 2019-2023")
        print("   3. Place them in the same directory as this script")
        print("   4. Run the manual processing script")
        return
    
    # Combine all years
    print("🔄 Combining data across years...")
    df_combined = pd.concat(all_data, ignore_index=True)
    
    # Calculate annual averages
    print("📊 Calculating annual aggregates...")
    
    annual_summary = df_combined.groupby('year').agg({
        'leadership_effectiveness_index': ['mean', 'std', 'count'],
        'burnout_dissatisfaction_index': ['mean', 'std', 'count']
    }).reset_index()
    
    annual_summary.columns = ['_'.join(col).strip('_') for col in annual_summary.columns.values]
    
    # Save outputs
    output_detail = 'fevs_healthcare_detailed.csv'
    output_summary = 'fevs_healthcare_annual_summary.csv'
    
    df_combined.to_csv(output_detail, index=False)
    annual_summary.to_csv(output_summary, index=False)
    
    print(f"\n✅ Data saved:")
    print(f"   Detailed: {output_detail} ({len(df_combined)} responses)")
    print(f"   Summary: {output_summary} ({len(annual_summary)} years)")
    
    # Display results
    print()
    print("=" * 70)
    print("HEALTHCARE FEDERAL EMPLOYEES - Leadership & Burnout Trends")
    print("=" * 70)
    print()
    print(annual_summary.to_string(index=False))
    
    print()
    print("=" * 70)
    print("✅ FEVS data download complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
