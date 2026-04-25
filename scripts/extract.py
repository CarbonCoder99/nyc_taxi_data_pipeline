import requests
import pandas as pd
import time
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def get_url(year, month, color):
    """Generate the URL for the parquet file."""
    return f"https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-{month}.parquet"

def fetch_parquet(url):
    """Fetch and load parquet data from URL into a DataFrame."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_parquet(BytesIO(response.content))
        filename = url.split('/')[-1]
        print(f"{filename} loaded successfully.")
        return df
    except requests.RequestException as e:
        print(f"Connection Error: Error pulling data from {url}")
        return None

# EXTRACT LOGIC
def extract(start_year=2021, end_year=2025, start_month=1, end_month=12):
    years = [str(y) for y in range(start_year, end_year + 1)]
    months = [f"{m:02d}" for m in range(start_month, end_month + 1)]
    
    yellow_dfs = []
    green_dfs = []
    
    for year in years:
        for month in months:
            for color in ['yellow', 'green']:
                url = get_url(year, month, color)
                df = fetch_parquet(url)
                if df is not None:
                    if color == 'yellow':
                        yellow_dfs.append(df)
                    elif color == 'green':
                        green_dfs.append(df)
                time.sleep(1)  # Delay to avoid overwhelming the server
    
    # Concatenate all DataFrames (if any were loaded)
    yellow_df = pd.concat(yellow_dfs, ignore_index=True) if yellow_dfs else pd.DataFrame()
    green_df = pd.concat(green_dfs, ignore_index=True) if green_dfs else pd.DataFrame()
    
    return yellow_df, green_df