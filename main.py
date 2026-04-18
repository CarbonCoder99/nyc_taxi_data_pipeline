import requests
import os
import time
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()  # Load environment variables from a .env file

# Global variables for dataframes
# yellow_df = None
# green_df = None

# EXTRACT LOGIC
def extract():
    global yellow_df, green_df
    yellow_trip_data_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet"
    green_trip_data_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2026-01.parquet"

    url_list = [yellow_trip_data_url, green_trip_data_url]


    for i in url_list:
        response = requests.get(i)
        if response.status_code == 200:
            filename = i.split('/')[-1]
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"{filename} downloaded successfully.")
            if "yellow" in filename:
                yellow_df = pd.read_parquet(filename)
            elif "green" in filename:
                green_df = pd.read_parquet(filename)

        time.sleep(1)  # Adding a delay to avoid overwhelming the machine with requests


# TRANSFORM LOGIC
def transform():
    global yellow_df, green_df
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

    green_df["pickup_hour"] = green_df["lpep_pickup_datetime"].dt.hour
    green_df["pickup_day_of_week"] = green_df["lpep_pickup_datetime"].dt.day_of_week

# LOAD LOGIC
def load():
    global yellow_df, green_df
    # Load each parquet file into a postgres database using SQLAlchemy and psycopg2
    DB_URL = os.getenv("DB_URL")  # Get the database URL from environment variables
    if DB_URL:
        print("✅ Found Database URL, attempting to connect...")
        try:
            engine = create_engine(DB_URL)
            yellow_df.to_sql('yellow_tripdata_jan_2026', engine, if_exists='replace', index=False)
            green_df.to_sql('green_tripdata_jan_2026', engine, if_exists='replace', index=False)
            print("🚀 DATABASE SUCCESS: Data pushed to PostgreSQL!")
        except Exception as e:
            print(f"❌ DATABASE ERROR: {e}")


def main():
    extract()
    transform()
    load()

if __name__ == "__main__":
    main()

