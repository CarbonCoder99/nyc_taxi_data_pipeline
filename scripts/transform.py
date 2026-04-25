import hashlib
import logging
import pandas as pd

logger = logging.getLogger(__name__)

YELLOW_COLUMNS = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "trip_distance",
    "fare_amount",
    "passenger_count",
    "RatecodeID",
]

GREEN_COLUMNS = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "trip_distance",
    "fare_amount",
    "passenger_count",
    "RatecodeID",
]


def generate_trip_hash(row, prefix):
    pickup_col = "tpep_pickup_datetime" if "tpep_pickup_datetime" in row else "lpep_pickup_datetime"
    dropoff_col = "tpep_dropoff_datetime" if "tpep_dropoff_datetime" in row else "lpep_dropoff_datetime"

    pickup_time = (
        row[pickup_col].isoformat()
        if hasattr(row[pickup_col], "isoformat")
        else str(row[pickup_col])
    )
    dropoff_time = (
        row[dropoff_col].isoformat()
        if hasattr(row[dropoff_col], "isoformat")
        else str(row[dropoff_col])
    )

    key_data = (
        f"{pickup_time}|{dropoff_time}|{row['PULocationID']}|{row['DOLocationID']}|"
        f"{row['trip_distance']}|{row['fare_amount']}"
    )
    return prefix + hashlib.sha256(key_data.encode()).hexdigest()[:16]


def _validate_input(df, required_columns, color_name):
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"{color_name} dataframe missing required columns: {missing}")


def _transform_dataframe(df, color):
    if color == "yellow":
        required_columns = YELLOW_COLUMNS
        pickup_col = "tpep_pickup_datetime"
        dropoff_col = "tpep_dropoff_datetime"
        prefix = "Y"
    else:
        required_columns = GREEN_COLUMNS
        pickup_col = "lpep_pickup_datetime"
        dropoff_col = "lpep_dropoff_datetime"
        prefix = "G"

    _validate_input(df, required_columns, color)
    df = df[required_columns].copy()

    df["trip_duration"] = (
        df[dropoff_col] - df[pickup_col]
    ).dt.total_seconds() / 60
    df["trip_duration"] = df["trip_duration"].round(1)

    df.dropna(inplace=True)
    df = df[df["trip_duration"] >= 0]
    df.drop_duplicates(inplace=True)

    df["pickup_hour"] = df[pickup_col].dt.hour
    df["pickup_day_of_week"] = df[pickup_col].dt.day_of_week
    df["month"] = df[pickup_col].dt.month
    df["year"] = df[pickup_col].dt.year
    df["trip_id"] = df.apply(lambda row: generate_trip_hash(row, prefix), axis=1)

    logger.info("%s records transformed: %s rows", color, len(df))
    return df


def transform(yellow_df, green_df):
    if yellow_df.empty and green_df.empty:
        raise ValueError("No data provided to transform")

    transformed_yellow = _transform_dataframe(yellow_df, "yellow") if not yellow_df.empty else pd.DataFrame()
    transformed_green = _transform_dataframe(green_df, "green") if not green_df.empty else pd.DataFrame()

    return transformed_yellow, transformed_green