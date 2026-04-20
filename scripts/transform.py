import pandas as pd


# TRANSFORM LOGIC
def transform(yellow_df, green_df):
    # Select only the relevant columns for analysis and database storage
    yellow_df = yellow_df[['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'trip_distance', 'fare_amount', 'passenger_count', 'RatecodeID']]
    green_df = green_df[['lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'trip_distance', 'fare_amount', 'passenger_count', 'RatecodeID']] 


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
    
    return yellow_df, green_df