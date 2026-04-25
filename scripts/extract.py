import logging
import pandas as pd
import requests
import time
from io import BytesIO
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

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


def extract(start_year=2021, end_year=2025, start_month=1, end_month=12, colors=None):
    if colors is None:
        colors = ["yellow", "green"]
    if not colors:
        raise ValueError("At least one color must be specified")

    years = _build_range(start_year, end_year, "year", 1900, 2100)
    months = _build_range(start_month, end_month, "month", 1, 12)

    logger.info("Starting extraction for years=%s months=%s colors=%s", years, months, colors)
    session = configure_http_session()
    yellow_dfs = []
    green_dfs = []

    for year in years:
        for month in months:
            for color in colors:
                url = get_url(year, month, color)
                df = fetch_parquet(session, url)
                if df is None:
                    continue
                if color == "yellow":
                    yellow_dfs.append(df)
                else:
                    green_dfs.append(df)
                time.sleep(1)

    yellow_df = pd.concat(yellow_dfs, ignore_index=True) if yellow_dfs else pd.DataFrame()
    green_df = pd.concat(green_dfs, ignore_index=True) if green_dfs else pd.DataFrame()

    logger.info(
        "Extraction completed: yellow_rows=%s green_rows=%s",
        len(yellow_df),
        len(green_df),
    )
    return yellow_df, green_df