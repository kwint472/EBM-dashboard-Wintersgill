"""
Create Sample JOLTS and FEVS Data for Dashboard Demo
This creates realistic sample data based on actual trends
"""

import pandas as pd
import numpy as np

def create_sample_jolts_data():
    """Create sample JOLTS healthcare turnover data"""
    
    # Create monthly date range
    dates = pd.date_range('2019-01-01', '2024-12-01', freq='MS')
    
    np.random.seed(42)  # For reproducibility
    
    # Realistic baseline and trends
    # Pre-COVID: ~2.5% quit rate
    # COVID spike: +0.8% 
    # Post-COVID elevated: ~3.0%
    
    data = []
    for date in dates:
        year = date.year
        month = date.month
        
        # Base quit rate
        base_rate = 2.5
        
        # COVID impact
        if date >= pd.Timestamp('2020-03-01') and date < pd.Timestamp('2020-06-01'):
            # Initial drop (uncertainty)
            covid_effect = -0.5
        elif date >= pd.Timestamp('2020-06-01') and date < pd.Timestamp('2021-01-01'):
            # Gradual increase
            covid_effect = 0.3
        elif date >= pd.Timestamp('2021-01-01'):
            # "Great Resignation" - sustained high quit rates
            covid_effect = 0.7 + 0.2 * np.sin((date.year - 2021) * 2 * np.pi / 3)
        else:
            covid_effect = 0
        
        # Seasonal variation
        seasonal = 0.2 * np.sin(month * 2 * np.pi / 12)
        
        # Random noise
        noise = np.random.normal(0, 0.15)
        
        quit_rate = base_rate + covid_effect + seasonal + noise
        
        # Total separations (quits + layoffs + other)
        total_sep = quit_rate * 1.4  # Quits are ~70% of separations
        
        # Hires rate (slightly higher to account for growth)
        hires = quit_rate * 1.1 + np.random.normal(0, 0.1)
        
        data.append({
            'date': date,
            'year': year,
            'month': month,
            'Healthcare_Quit_Rate': round(quit_rate, 2),
            'Healthcare_Total_Separations': round(total_sep, 2),
            'Healthcare_Hires_Rate': round(hires, 2),
            'pre_covid': date < pd.Timestamp('2020-03-01'),
            'during_covid': (date >= pd.Timestamp('2020-03-01')) & (date < pd.Timestamp('2021-06-01')),
            'post_covid': date >= pd.Timestamp('2021-06-01')
        })
    
    df = pd.DataFrame(data)
    return df

def create_sample_fevs_data():
    """Create sample FEVS leadership and burnout data"""
    
    years = range(2019, 2025)
    
    np.random.seed(43)
    
    data = []
    for year in years:
        # Leadership effectiveness (scale 1-5, higher = better)
        # Slight decline during COVID
        base_leadership = 3.5
        
        if year <= 2019:
            leadership_adj = 0.1
        elif year in [2020, 2021]:
            # COVID stress on leadership
            leadership_adj = -0.3
        else:
            # Gradual recovery but not to baseline
            leadership_adj = -0.1
        
        leadership = base_leadership + leadership_adj + np.random.normal(0, 0.15)
        
        # Burnout/dissatisfaction (scale 1-5, higher = more burnout)
        # Inverse relationship with leadership
        base_burnout = 2.8
        
        if year <= 2019:
            burnout_adj = -0.2
        elif year in [2020, 2021]:
            # COVID burnout spike
            burnout_adj = 0.8
        else:
            # Remains elevated
            burnout_adj = 0.4
        
        burnout = base_burnout + burnout_adj + np.random.normal(0, 0.2)
        
        data.append({
            'year': year,
            'leadership_effectiveness_index': round(leadership, 2),
            'burnout_dissatisfaction_index': round(burnout, 2),
            'n_responses': np.random.randint(8000, 12000)  # Sample size
        })
    
    df = pd.DataFrame(data)
    return df

def combine_datasets():
    """Combine JOLTS and FEVS data"""
    
    print("=" * 60)
    print("CREATING SAMPLE INTEGRATED DATASET")
    print("JOLTS Healthcare Turnover + FEVS Leadership/Burnout")
    print("=" * 60)
    print()
    
    # Create sample data
    print("Creating sample JOLTS data (monthly)...")
    jolts = create_sample_jolts_data()
    print(f"  {len(jolts)} monthly observations")
    
    print("Creating sample FEVS data (annual)...")
    fevs = create_sample_fevs_data()
    print(f"  {len(fevs)} annual observations")
    
    # For integration, calculate annual averages of JOLTS
    print("\nAggregating JOLTS to annual level...")
    jolts_annual = jolts.groupby('year').agg({
        'Healthcare_Quit_Rate': 'mean',
        'Healthcare_Total_Separations': 'mean',
        'Healthcare_Hires_Rate': 'mean',
    }).reset_index()
    
    # Merge datasets
    print("Merging datasets on year...")
    combined = pd.merge(jolts_annual, fevs, on='year', how='inner')
    
    # Add derived variables
    combined['turnover_leadership_ratio'] = (
        combined['Healthcare_Quit_Rate'] / combined['leadership_effectiveness_index']
    )
    
    combined['burnout_quit_correlation'] = (
        combined['burnout_dissatisfaction_index'] * combined['Healthcare_Quit_Rate']
    )
    
    # Save files
    jolts.to_csv('jolts_healthcare_monthly.csv', index=False)
    fevs.to_csv('fevs_healthcare_annual.csv', index=False)
    combined.to_csv('combined_leadership_turnover.csv', index=False)
    
    print("\n" + "=" * 60)
    print("FILES CREATED:")
    print("=" * 60)
    print("1. jolts_healthcare_monthly.csv - Monthly turnover data")
    print("2. fevs_healthcare_annual.csv - Annual leadership/burnout data")
    print("3. combined_leadership_turnover.csv - Integrated analysis dataset")
    
    print("\n" + "=" * 60)
    print("INTEGRATED DATASET SUMMARY")
    print("=" * 60)
    print(f"\nYears covered: {combined['year'].min()} - {combined['year'].max()}")
    print(f"Observations: {len(combined)}")
    
    print("\n" + "-" * 60)
    print("KEY VARIABLES:")
    print("-" * 60)
    print("\nOUTCOME (Y) - Healthcare Worker Burnout:")
    print(f"  Quit Rate Mean: {combined['Healthcare_Quit_Rate'].mean():.2f}%")
    print(f"  Quit Rate Std: {combined['Healthcare_Quit_Rate'].std():.2f}%")
    print(f"  Burnout Index Mean: {combined['burnout_dissatisfaction_index'].mean():.2f}/5")
    
    print("\nPREDICTOR (X) - Leadership Interventions:")
    print(f"  Leadership Effectiveness Mean: {combined['leadership_effectiveness_index'].mean():.2f}/5")
    print(f"  Leadership Effectiveness Std: {combined['leadership_effectiveness_index'].std():.2f}")
    
    print("\n" + "-" * 60)
    print("CORRELATIONS:")
    print("-" * 60)
    corr_leadership_quit = combined['leadership_effectiveness_index'].corr(combined['Healthcare_Quit_Rate'])
    corr_burnout_quit = combined['burnout_dissatisfaction_index'].corr(combined['Healthcare_Quit_Rate'])
    corr_leadership_burnout = combined['leadership_effectiveness_index'].corr(combined['burnout_dissatisfaction_index'])
    
    print(f"Leadership ↔ Quit Rate: {corr_leadership_quit:.3f}")
    print(f"Burnout ↔ Quit Rate: {corr_burnout_quit:.3f}")
    print(f"Leadership ↔ Burnout: {corr_leadership_burnout:.3f}")
    
    print("\n" + "-" * 60)
    print("COVID-19 COMPARISON:")
    print("-" * 60)
    pre_covid = combined[combined['year'] < 2020]
    post_covid = combined[combined['year'] >= 2021]
    
    print(f"\nPre-COVID (2019):")
    print(f"  Avg Quit Rate: {pre_covid['Healthcare_Quit_Rate'].mean():.2f}%")
    print(f"  Avg Leadership: {pre_covid['leadership_effectiveness_index'].mean():.2f}/5")
    print(f"  Avg Burnout: {pre_covid['burnout_dissatisfaction_index'].mean():.2f}/5")
    
    print(f"\nPost-COVID (2021+):")
    print(f"  Avg Quit Rate: {post_covid['Healthcare_Quit_Rate'].mean():.2f}%")
    print(f"  Avg Leadership: {post_covid['leadership_effectiveness_index'].mean():.2f}/5")
    print(f"  Avg Burnout: {post_covid['burnout_dissatisfaction_index'].mean():.2f}/5")
    
    print(f"\nChanges:")
    quit_change = post_covid['Healthcare_Quit_Rate'].mean() - pre_covid['Healthcare_Quit_Rate'].mean()
    leadership_change = post_covid['leadership_effectiveness_index'].mean() - pre_covid['leadership_effectiveness_index'].mean()
    burnout_change = post_covid['burnout_dissatisfaction_index'].mean() - pre_covid['burnout_dissatisfaction_index'].mean()
    
    print(f"  Quit Rate: {quit_change:+.2f} percentage points")
    print(f"  Leadership: {leadership_change:+.2f} points")
    print(f"  Burnout: {burnout_change:+.2f} points")
    
    print("\n" + "=" * 60)
    print("DASHBOARD INTEGRATION READY!")
    print("=" * 60)
    print("\nNOTE: This is SAMPLE DATA for demonstration.")
    print("Replace with actual JOLTS and FEVS data when available.")
    print("\nFor real data:")
    print("  JOLTS: https://data.bls.gov/cgi-bin/srgate")
    print("  FEVS: https://www.opm.gov/fevs/public-data-file/")
    
    return combined

if __name__ == "__main__":
    df = combine_datasets()
