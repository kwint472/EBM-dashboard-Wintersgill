"""
Download JOLTS Healthcare Data - Alternative Method
Uses direct file downloads from BLS website
"""

import pandas as pd
import requests
from io import StringIO

def download_jolts_data():
    """
    Download JOLTS data using direct file access
    """
    print("=" * 60)
    print("JOLTS Healthcare Turnover Data Download")
    print("Bureau of Labor Statistics")
    print("=" * 60)
    print()
    
    # BLS publishes data files we can download directly
    # Using the public data query tool export
    print("Attempting to download JOLTS healthcare data...")
    print()
    print("NOTE: If automatic download fails, please:")
    print("1. Visit https://data.bls.gov/cgi-bin/srgate")
    print("2. Series ID: JTS6200000000000000QUR (Healthcare Quit Rate)")
    print("3. Select years: 2019-2025")
    print("4. Download as CSV")
    print()
    
    # Try the new public data API (v2.0) without registration for single series
    base_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    
    # Healthcare series we want
    series = {
        'Healthcare Quit Rate': 'JTS6200000000000000QUR',
        'Healthcare Total Separations': 'JTS6200000000000000TSR',
        'Healthcare Hires Rate': 'JTS6200000000000000HIR',
    }
    
    all_data = []
    
    for name, series_id in series.items():
        print(f"Downloading {name}...")
        
        # Build URL with query parameters
        url = f"{base_url}{series_id}"
        
        try:
            # Try simple GET request
            params = {
                'startyear': '2019',
                'endyear': '2025',
                'registrationkey': ''  # Public API
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we got data
                if 'Results' in data and 'series' in data['Results']:
                    series_data = data['Results']['series']
                    if len(series_data) > 0 and 'data' in series_data[0]:
                        points = series_data[0]['data']
                        
                        for point in points:
                            if point['period'].startswith('M'):  # Monthly data
                                all_data.append({
                                    'series_name': name,
                                    'year': int(point['year']),
                                    'month': int(point['period'][1:]),
                                    'value': float(point['value'])
                                })
                        
                        print(f"  SUCCESS: Downloaded {len(points)} data points")
                    else:
                        print(f"  WARNING: No data in response")
                else:
                    print(f"  WARNING: Unexpected response format")
            else:
                print(f"  ERROR: Status code {response.status_code}")
                
        except Exception as e:
            print(f"  ERROR: {str(e)}")
    
    if not all_data:
        print("\n" + "=" * 60)
        print("AUTOMATIC DOWNLOAD FAILED")
        print("=" * 60)
        print("\nManual download instructions:")
        print("1. Go to: https://data.bls.gov/cgi-bin/srgate")
        print("2. Enter Series ID: JTS6200000000000000QUR")
        print("3. Select years 2019-2025")
        print("4. Format: Excel or CSV")
        print("5. Save as 'jolts_healthcare_quit_rate.csv' in this folder")
        print("\nFor additional context, also download:")
        print("  - JTS6200000000000000TSR (Total Separations)")
        print("  - JTS6200000000000000HIR (Hires Rate)")
        return None
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    df['date'] = pd.to_datetime(
        df['year'].astype(str) + '-' + 
        df['month'].astype(str).apply(lambda x: str(x).zfill(2)) + '-01'
    )
    
    # Pivot to wide format
    df_wide = df.pivot(index='date', columns='series_name', values='value')
    df_wide = df_wide.reset_index()
    df_wide = df_wide.sort_values('date')
    
    # Add time period indicators
    df_wide['year'] = df_wide['date'].dt.year
    df_wide['month'] = df_wide['date'].dt.month
    df_wide['pre_covid'] = (df_wide['date'] < '2020-03-01')
    df_wide['during_covid'] = ((df_wide['date'] >= '2020-03-01') & (df_wide['date'] < '2021-06-01'))
    df_wide['post_covid'] = (df_wide['date'] >= '2021-06-01')
    
    # Save
    output_file = 'jolts_healthcare_data.csv'
    df_wide.to_csv(output_file, index=False)
    
    print("\n" + "=" * 60)
    print("DATA DOWNLOADED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nFile saved: {output_file}")
    print(f"Observations: {len(df_wide)}")
    print(f"Date range: {df_wide['date'].min().strftime('%Y-%m')} to {df_wide['date'].max().strftime('%Y-%m')}")
    
    # Summary
    if 'Healthcare Quit Rate' in df_wide.columns:
        print("\n" + "-" * 60)
        print("HEALTHCARE WORKER TURNOVER SUMMARY")
        print("-" * 60)
        print(f"\nQuit Rate Statistics:")
        print(f"  Mean: {df_wide['Healthcare Quit Rate'].mean():.2f}%")
        print(f"  Std Dev: {df_wide['Healthcare Quit Rate'].std():.2f}%")
        print(f"  Min: {df_wide['Healthcare Quit Rate'].min():.2f}% ({df_wide[df_wide['Healthcare Quit Rate'] == df_wide['Healthcare Quit Rate'].min()]['date'].dt.strftime('%Y-%m').values[0]})")
        print(f"  Max: {df_wide['Healthcare Quit Rate'].max():.2f}% ({df_wide[df_wide['Healthcare Quit Rate'] == df_wide['Healthcare Quit Rate'].max()]['date'].dt.strftime('%Y-%m').values[0]})")
        
        # COVID comparison
        pre = df_wide[df_wide['pre_covid']]['Healthcare Quit Rate'].mean()
        post = df_wide[df_wide['post_covid']]['Healthcare Quit Rate'].mean()
        
        print(f"\nCOVID-19 Impact:")
        print(f"  Pre-COVID average (before Mar 2020): {pre:.2f}%")
        print(f"  Post-COVID average (after Jun 2021): {post:.2f}%")
        print(f"  Change: {post - pre:+.2f} percentage points ({((post - pre) / pre * 100):+.1f}%)")
    
    print("\n" + "=" * 60)
    
    return df_wide

if __name__ == "__main__":
    df = download_jolts_data()
    
    if df is None:
        print("\nPlease follow manual download instructions above.")
