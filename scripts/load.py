import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()  # Load environment variables from a .env file

# LOAD LOGIC
def load(yellow_df, green_df):
    # Load each parquet file into a postgres database

    DB_URL = os.getenv("DB_URL")  # Get the database URL from environment variables
    if DB_URL:
        print("✅ Found Database URL, attempting to connect...")
        try:
            engine = create_engine(DB_URL)
            # Test database connection
            with engine.connect() as conn:
                print("🔗 Database connection successful!")
            
            # create tables and load data into the database
            with engine.connect() as conn:
                conn.execute(text("""
                             CREATE TABLE IF NOT EXISTS yellow_tripdata_2021_2025(
                                tpep_pickup_datetime TIMESTAMP,
                                tpep_dropoff_datetime TIMESTAMP,
                                PULocationID INTEGER,
                                DOLocationID INTEGER,
                                trip_distance FLOAT,
                                fare_amount FLOAT,
                                passenger_count INTEGER,
                                RatecodeID INTEGER,
                                trip_duration FLOAT,
                                pickup_hour INTEGER,
                                pickup_day_of_week INTEGER
                             )
                             
                             """))
                
                conn.execute(text("""
                             CREATE TABLE IF NOT EXISTS green_tripdata_2021_2025(
                                lpep_pickup_datetime TIMESTAMP,
                                lpep_dropoff_datetime TIMESTAMP,
                                PULocationID INTEGER,
                                DOLocationID INTEGER,
                                trip_distance FLOAT,
                                fare_amount FLOAT,
                                passenger_count INTEGER,
                                RatecodeID INTEGER,
                                trip_duration FLOAT,
                                pickup_hour INTEGER,
                                pickup_day_of_week INTEGER
                             )
                             
                             """))

            yellow_df.to_sql('yellow_tripdata_2021_2025', engine, if_exists='replace', index=False)
            green_df.to_sql('green_tripdata_2021_2025', engine, if_exists='replace', index=False)

            print("🚀 DATABASE SUCCESS: Data pushed to PostgreSQL!")
        except Exception as e:
            print(f"❌ DATABASE ERROR: {e}")
