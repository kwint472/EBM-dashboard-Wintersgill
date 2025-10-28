"""
Simple JOLTS Healthcare Data Download Script
Downloads quit rates and turnover data from BLS
"""

import pandas as pd
import requests
import time

# BLS API Configuration
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# Healthcare sector series
SERIES_IDS = {
    'quit_rate': 'JTS6200000000000000QUR',  # Healthcare quit rate
    'separations': 'JTS6200000000000000TSR',  # Total separations
    'hires': 'JTS6200000000000000HIR',  # Hires rate  
}

def download_data():
    """Download data from BLS API"""
    print("=" * 60)
    print("JOLTS Healthcare Data Download")
    print("=" * 60)
    print()
    
    # Prepare request
    headers = {'Content-type': 'application/json'}
    data = {
        "seriesid": list(SERIES_IDS.values()),
        "startyear": "2019",
        "endyear": "2025"
    }
    
    print("Downloading from BLS API...")
    response = requests.post(BLS_API_URL, json=data, headers=headers)
    
    if response.status_code != 200:
        print(f"ERROR: API returned status {response.status_code}")
        return None
    
    json_data = response.json()
    
    if json_data['status'] != 'REQUEST_SUCCEEDED':
        print(f"ERROR: {json_data.get('message', 'Unknown error')}")
        return None
    
    print("Download successful!")
    return json_data

def process_data(json_data):
    """Process JSON into DataFrame"""
    print("\nProcessing data...")
    
    # Debug: Show structure
    print(f"Keys in Results: {json_data['Results'].keys()}")
    print(f"Number of series: {len(json_data['Results']['series'])}")
    
    all_rows = []
    
    for series in json_data['Results']['series']:
        series_id = series['seriesID']
        data_points = series.get('data', [])
        
        print(f"\nSeries {series_id}: {len(data_points)} data points")
        
        # Find the friendly name
        series_name = None
        for name, sid in SERIES_IDS.items():
            if sid == series_id:
                series_name = name
                break
        
        if not series_name:
            series_name = series_id
        
        for datapoint in data_points:
            year = int(datapoint['year'])
            period = datapoint['period']
            
            # Only process monthly data (M01-M12)
            if not period.startswith('M'):
                continue
            
            month = int(period[1:])
            value = float(datapoint['value'])
            
            all_rows.append({
                'year': year,
                'month': month,
                'series': series_name,
                'value': value
            })
    
    print(f"\nTotal rows collected: {len(all_rows)}")
    
    # Create DataFrame
    if not all_rows:
        print("ERROR: No data rows created")
        return None
    
    df = pd.DataFrame(all_rows)
    print(f"Created DataFrame with {len(df)} rows")
    print(f"Columns: {df.columns.tolist()}")
    
    # Create date column  
    df['date'] = pd.to_datetime(
        df['year'].astype(str) + '-' + 
        df['month'].astype(str).apply(lambda x: str(x).zfill(2)) + '-01'
    )
    
    # Pivot to wide format
    df_wide = df.pivot(index='date', columns='series', values='value')
    df_wide = df_wide.reset_index()
    df_wide = df_wide.sort_values('date')
    
    # Add year and month columns
    df_wide['year'] = df_wide['date'].dt.year
    df_wide['month'] = df_wide['date'].dt.month
    
    # Add COVID period indicators
    df_wide['pre_covid'] = (df_wide['date'] < '2020-03-01')
    df_wide['during_covid'] = ((df_wide['date'] >= '2020-03-01') & (df_wide['date'] < '2021-06-01'))
    df_wide['post_covid'] = (df_wide['date'] >= '2021-06-01')
    
    print(f"Processed {len(df_wide)} monthly observations")
    print(f"Date range: {df_wide['date'].min()} to {df_wide['date'].max()}")
    
    return df_wide

def main():
    # Download
    json_data = download_data()
    if not json_data:
        return
    
    # Process
    df = process_data(json_data)
    if df is None or len(df) == 0:
        print("No data to save")
        return
    
    # Save
    output_file = 'jolts_healthcare_data.csv'
    df.to_csv(output_file, index=False)
    print(f"\nData saved to: {output_file}")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"\nTotal months: {len(df)}")
    print(f"\nAverage quit rate: {df['quit_rate'].mean():.2f}%")
    print(f"Max quit rate: {df['quit_rate'].max():.2f}% ({df[df['quit_rate'] == df['quit_rate'].max()]['date'].values[0]})")
    print(f"Min quit rate: {df['quit_rate'].min():.2f}% ({df[df['quit_rate'] == df['quit_rate'].min()]['date'].values[0]})")
    
    # COVID comparison
    print("\nCOVID-19 IMPACT:")
    print(f"Pre-COVID avg quit rate: {df[df['pre_covid']]['quit_rate'].mean():.2f}%")
    print(f"Post-COVID avg quit rate: {df[df['post_covid']]['quit_rate'].mean():.2f}%")
    change = df[df['post_covid']]['quit_rate'].mean() - df[df['pre_covid']]['quit_rate'].mean()
    print(f"Change: {change:+.2f} percentage points")
    
    print("\n" + "=" * 60)
    print("Download complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
