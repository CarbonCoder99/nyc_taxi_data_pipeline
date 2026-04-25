import requests
import pandas as pd
import time
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

# EXTRACT LOGIC
def extract(years=None, months=None):
    if years is None:
        years = ["2021", "2022", "2023", "2024", "2025"]
    if months is None:
        months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    
    yellow_dfs = []
    green_dfs = []
    
    for year in years:
        for month in months:
            yellow_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month}.parquet"
            green_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month}.parquet"
            
            for url in [yellow_url, green_url]:
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    
                    df = pd.read_parquet(BytesIO(response.content))
                    filename = url.split('/')[-1]
                    
                    if "yellow" in filename:
                        yellow_dfs.append(df)
                        print(f"{filename} loaded successfully.")
                    elif "green" in filename:
                        green_dfs.append(df)
                        print(f"{filename} loaded successfully.")
                        
                except requests.RequestException as e:
                    print(f"Connection Error: Error pulling data from {url}")
                    continue
                
                time.sleep(1)  # Delay to avoid overwhelming the server
    
    # Concatenate all DataFrames (if any were loaded)
    yellow_df = pd.concat(yellow_dfs, ignore_index=True) if yellow_dfs else pd.DataFrame()
    green_df = pd.concat(green_dfs, ignore_index=True) if green_dfs else pd.DataFrame()
    
    return yellow_df, green_df