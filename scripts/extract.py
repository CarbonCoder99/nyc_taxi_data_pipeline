import requests
import pandas as pd
import time
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

<<<<<<< HEAD
COLOR_REQUIRED_COLUMNS = {
    "yellow": [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "PULocationID",
        "DOLocationID",
        "trip_distance",
        "fare_amount",
        "passenger_count",
        "RatecodeID",
    ],
    "green": [
        "lpep_pickup_datetime",
        "lpep_dropoff_datetime",
        "PULocationID",
        "DOLocationID",
        "trip_distance",
        "fare_amount",
        "passenger_count",
        "RatecodeID",
    ],
}


def configure_http_session(retries=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(["GET"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_url(year, month, color):
    return f"https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-{month}.parquet"


def validate_dataframe(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def fetch_parquet(session, url):
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        df = pd.read_parquet(BytesIO(response.content))

        required_columns = COLOR_REQUIRED_COLUMNS[
            "yellow" if "yellow" in url else "green"
        ]
        validate_dataframe(df, required_columns)

        logger.info("%s loaded successfully", url.split("/")[-1])
        return df
    except (requests.RequestException, ValueError, OSError) as exc:
        logger.warning("Failed to fetch %s: %s", url, exc)
        return None


def _build_range(start, end, name, min_value, max_value):
    if start < min_value or end > max_value or start > end:
        raise ValueError(
            f"{name} range must be between {min_value} and {max_value} and start <= end"
        )
    return [f"{value:02d}" for value in range(start, end + 1)] if name == "month" else [str(value) for value in range(start, end + 1)]


def extract(start_year=2021, end_year=2022, start_month=1, end_month=2, colors=None):
    if colors is None:
        colors = ["yellow", "green"]
    if not colors:
        raise ValueError("At least one color must be specified")

    years = _build_range(start_year, end_year, "year", 1900, 2100)
    months = _build_range(start_month, end_month, "month", 1, 12)

    logger.info("Starting extraction for years=%s months=%s colors=%s", years, months, colors)
    session = configure_http_session()
=======
# EXTRACT LOGIC
def extract(years=None, months=None):
    if years is None:
        years = ["2021", "2022", "2023", "2024", "2025"]
    if months is None:
        months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    
>>>>>>> parent of 0f6203e (fix: ensuring a production ready pipeline)
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