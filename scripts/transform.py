import hashlib
import pandas as pd

def generate_trip_hash(row, prefix):
    """
    Generate a unique hash for each trip based on key columns
    
    """
    # Convert key columns to string and concatenate, handling datetime objects
    pickup_col = 'tpep_pickup_datetime' if 'tpep_pickup_datetime' in row else 'lpep_pickup_datetime'
    dropoff_col = 'tpep_dropoff_datetime' if 'tpep_dropoff_datetime' in row else 'lpep_dropoff_datetime'
    
    # Convert datetime to ISO format string if it's a datetime object
    pickup_time = row[pickup_col].isoformat() if hasattr(row[pickup_col], 'isoformat') else str(row[pickup_col])
    dropoff_time = row[dropoff_col].isoformat() if hasattr(row[dropoff_col], 'isoformat') else str(row[dropoff_col])
    
    key_data = f"{pickup_time}|{dropoff_time}|{row['PULocationID']}|{row['DOLocationID']}|{row['trip_distance']}|{row['fare_amount']}"
    # Create SHA256 hash and take first 16 characters for shorter key
    return prefix + hashlib.sha256(key_data.encode()).hexdigest()[:16]

# TRANSFORM LOGIC
def transform(yellow_df, green_df):
    # Select only the relevant columns for analysis and database storage
    yellow_df = yellow_df[['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'trip_distance', 'fare_amount', 'passenger_count', 'RatecodeID']].copy()
    green_df = green_df[['lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'trip_distance', 'fare_amount', 'passenger_count', 'RatecodeID']].copy()


    # Calculate trip duration in minutes for both yellow and green taxi data and round to 1 decimal place
    yellow_df["trip_duration"] = (yellow_df["tpep_dropoff_datetime"] - yellow_df["tpep_pickup_datetime"]).dt.total_seconds() / 60
    yellow_df["trip_duration"] = yellow_df["trip_duration"].round(1)
    
    green_df["trip_duration"] = (green_df["lpep_dropoff_datetime"] - green_df["lpep_pickup_datetime"]).dt.total_seconds() / 60
    green_df["trip_duration"] = green_df["trip_duration"].round(1)

    # Remove duplicates and handle missing values in both datasets
    yellow_df.drop_duplicates(inplace=True)
    yellow_df.dropna(inplace=True)

    green_df.dropna(inplace=True)
    green_df.drop_duplicates(inplace=True)


    # extract pick-up hour and pick up day of week from the pickup datetime column for both yellow and green taxi data
    yellow_df["pickup_hour"] = yellow_df["tpep_pickup_datetime"].dt.hour
    yellow_df["pickup_day_of_week"] = yellow_df["tpep_pickup_datetime"].dt.day_of_week
    yellow_df["month"] = yellow_df["tpep_pickup_datetime"].dt.month
    yellow_df["year"] = yellow_df["tpep_pickup_datetime"].dt.year

    green_df["pickup_hour"] = green_df["lpep_pickup_datetime"].dt.hour
    green_df["pickup_day_of_week"] = green_df["lpep_pickup_datetime"].dt.day_of_week
    green_df["month"] = green_df["lpep_pickup_datetime"].dt.month
    green_df["year"] = green_df["lpep_pickup_datetime"].dt.year

    # Generate primary keys for both datasets
    yellow_df['trip_id'] = yellow_df.apply(lambda row: generate_trip_hash(row, 'Y'), axis=1)
    green_df['trip_id'] = green_df.apply(lambda row: generate_trip_hash(row, 'G'), axis=1)

    
    return yellow_df, green_df