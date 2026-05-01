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
def extract(year, month):
    month_str = f"{month:02d}"
    
    yellow_df = pd.DataFrame()
    green_df = pd.DataFrame()
    
    for color in ['yellow', 'green']:
        url = get_url(year, month_str, color)
        df = fetch_parquet(url)
        if df is not None:
            if color == 'yellow':
                yellow_df = df
            elif color == 'green':
                green_df = df
        time.sleep(1)  # Delay to avoid overwhelming the server
    
    return yellow_df, green_df