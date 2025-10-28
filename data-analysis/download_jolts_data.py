"""
Download JOLTS Healthcare Sector Data
Bureau of Labor Statistics - Job Openings and Labor Turnover Survey

This script downloads healthcare sector turnover data (burnout indicators)
from the BLS Public Data API.
"""

import requests
import pandas as pd
import json
from datetime import datetime
import time

# BLS API Configuration
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# JOLTS Healthcare Series IDs
# Healthcare and Social Assistance (NAICS 62)
SERIES_IDS = {
    'healthcare_quit_rate': 'JTS6200000000000000QUR',  # Quit rate (PRIMARY BURNOUT INDICATOR)
    'healthcare_quit_level': 'JTS6200000000000000QUL',  # Quit level (thousands)
    'healthcare_total_separations_rate': 'JTS6200000000000000TSR',  # Total separations rate
    'healthcare_hires_rate': 'JTS6200000000000000HIR',  # Hires rate
    'healthcare_job_openings_rate': 'JTS6200000000000000JOR',  # Job openings rate
    'healthcare_layoff_rate': 'JTS6200000000000000LDR',  # Layoffs & discharges rate
    'healthcare_other_separations_rate': 'JTS6200000000000000OSR',  # Other separations rate
    
    # Additional subsectors for comparison
    'hospitals_quit_rate': 'JTS6220000000000000QUR',  # Hospitals specifically
    'nursing_facilities_quit_rate': 'JTS6230000000000000QUR',  # Nursing & residential care
    'ambulatory_quit_rate': 'JTS6210000000000000QUR',  # Ambulatory healthcare services
}

def download_bls_data(series_ids, start_year=2019, end_year=2025):
    """
    Download data from BLS API for specified series IDs
    
    Args:
        series_ids: List of BLS series IDs
        start_year: Starting year for data
        end_year: Ending year for data
    
    Returns:
        Dictionary with series data
    """
    headers = {'Content-type': 'application/json'}
    
    # BLS API limits to 50 series per request
    data_dict = {}
    
    for i in range(0, len(series_ids), 50):
        batch = list(series_ids.values())[i:i+50]
        
        payload = json.dumps({
            "seriesid": batch,
            "startyear": str(start_year),
            "endyear": str(end_year)
        })
        
        print(f"Downloading batch {i//50 + 1}...")
        
        try:
            response = requests.post(BLS_API_URL, data=payload, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            
            if json_data['status'] == 'REQUEST_SUCCEEDED':
                for series in json_data['Results']['series']:
                    series_id = series['seriesID']
                    # Find the key name for this series ID
                    series_name = [k for k, v in series_ids.items() if v == series_id][0]
                    data_dict[series_name] = series['data']
                    print(f"  ✓ Downloaded {series_name}")
            else:
                print(f"  ✗ API Error: {json_data.get('message', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Request failed: {e}")
            
        # Rate limiting - be nice to BLS servers
        time.sleep(1)
    
    return data_dict

def process_jolts_data(data_dict):
    """
    Process raw BLS data into a clean DataFrame
    
    Args:
        data_dict: Dictionary of series data from BLS API
    
    Returns:
        pandas DataFrame with processed data
    """
    all_data = []
    
    for series_name, data_points in data_dict.items():
        for point in data_points:
            # Extract month from period (format: M01, M02, etc.)
            period = point.get('period', '')
            month = int(period.replace('M', '')) if period.startswith('M') else 1
            
            all_data.append({
                'series_name': series_name,
                'year': int(point['year']),
                'month': month,
                'value': float(point['value']),
            })
    
    df = pd.DataFrame(all_data)
    
    # Debug: Check what we have
    print(f"  DataFrame shape: {df.shape}")
    print(f"  Columns: {df.columns.tolist()}")
    if len(df) > 0:
        print(f"  Sample row: {df.iloc[0].to_dict()}")
    
    # Create date column
    df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2) + '-01')
    
    # Pivot to wide format
    df_wide = df.pivot(index='date', columns='series_name', values='value')
    df_wide = df_wide.reset_index()
    
    # Sort by date
    df_wide = df_wide.sort_values('date')
    
    # Add derived variables
    if 'healthcare_quit_rate' in df_wide.columns:
        # Calculate voluntary turnover as percentage of total separations
        if 'healthcare_total_separations_rate' in df_wide.columns:
            df_wide['voluntary_pct_of_separations'] = (
                df_wide['healthcare_quit_rate'] / df_wide['healthcare_total_separations_rate'] * 100
            )
    
    # Add time period indicators
    df_wide['pre_covid'] = df_wide['date'] < '2020-03-01'
    df_wide['during_covid'] = (df_wide['date'] >= '2020-03-01') & (df_wide['date'] < '2021-06-01')
    df_wide['post_covid'] = df_wide['date'] >= '2021-06-01'
    
    # Add year and month for analysis
    df_wide['year'] = df_wide['date'].dt.year
    df_wide['month'] = df_wide['date'].dt.month
    df_wide['quarter'] = df_wide['date'].dt.quarter
    
    return df_wide

def main():
    """Main execution function"""
    print("=" * 70)
    print("JOLTS Healthcare Sector Data Download")
    print("Bureau of Labor Statistics - Public Data API")
    print("=" * 70)
    print()
    
    # Download data from 2019 to present (captures pre-COVID baseline)
    print("📊 Downloading JOLTS data...")
    print(f"   Time period: 2019-2025")
    print(f"   Series count: {len(SERIES_IDS)}")
    print()
    
    data_dict = download_bls_data(SERIES_IDS, start_year=2019, end_year=2025)
    
    if not data_dict:
        print("\n❌ No data downloaded. Check your internet connection or API status.")
        return
    
    print()
    print("📈 Processing data...")
    df = process_jolts_data(data_dict)
    
    # Save to CSV
    output_file = 'jolts_healthcare_data.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Data saved to: {output_file}")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Date range: {df['date'].min().strftime('%Y-%m')} to {df['date'].max().strftime('%Y-%m')}")
    
    # Display summary statistics
    print()
    print("=" * 70)
    print("KEY BURNOUT INDICATORS - Summary Statistics")
    print("=" * 70)
    
    if 'healthcare_quit_rate' in df.columns:
        print(f"\n🔥 Healthcare Quit Rate (Primary Burnout Indicator):")
        print(f"   Mean: {df['healthcare_quit_rate'].mean():.2f}%")
        print(f"   Std Dev: {df['healthcare_quit_rate'].std():.2f}%")
        print(f"   Min: {df['healthcare_quit_rate'].min():.2f}% ({df.loc[df['healthcare_quit_rate'].idxmin(), 'date'].strftime('%Y-%m')})")
        print(f"   Max: {df['healthcare_quit_rate'].max():.2f}% ({df.loc[df['healthcare_quit_rate'].idxmax(), 'date'].strftime('%Y-%m')})")
        
        # Pre vs Post COVID comparison
        if 'pre_covid' in df.columns and 'post_covid' in df.columns:
            pre_mean = df[df['pre_covid']]['healthcare_quit_rate'].mean()
            post_mean = df[df['post_covid']]['healthcare_quit_rate'].mean()
            change = ((post_mean - pre_mean) / pre_mean) * 100
            
            print(f"\n📊 COVID-19 Impact:")
            print(f"   Pre-COVID mean: {pre_mean:.2f}%")
            print(f"   Post-COVID mean: {post_mean:.2f}%")
            print(f"   Change: {change:+.1f}%")
    
    # Compare subsectors
    print(f"\n🏥 Subsector Comparison (Most Recent Month):")
    latest = df.iloc[-1]
    if 'hospitals_quit_rate' in df.columns:
        print(f"   Hospitals: {latest.get('hospitals_quit_rate', 'N/A'):.2f}%")
    if 'nursing_facilities_quit_rate' in df.columns:
        print(f"   Nursing Facilities: {latest.get('nursing_facilities_quit_rate', 'N/A'):.2f}%")
    if 'ambulatory_quit_rate' in df.columns:
        print(f"   Ambulatory Care: {latest.get('ambulatory_quit_rate', 'N/A'):.2f}%")
    
    print()
    print("=" * 70)
    print("✅ JOLTS data download complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
