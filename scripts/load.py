import os
import hashlib
from dotenv import load_dotenv
import psycopg2

load_dotenv()  # Load environment variables from a .env file

# LOAD LOGIC
def load(yellow_df, green_df):
    # Load each parquet file into a postgres database

    DB_URL = os.getenv("DB_URL")  # Get the database URL from environment variables

    if DB_URL:
        print("✅ Found Database URL, attempting to connect...")
        try:
            # Test database connection, create tables, and load data into the database
            with psycopg2.connect(DB_URL) as conn:
                print("🔗 Database connection successful!")

                cur = conn.cursor()

                cur.execute("""
                             CREATE TABLE IF NOT EXISTS yellow_tripdata_2021_2025(
                                trip_id VARCHAR(17) PRIMARY KEY,
                                tpep_pickup_datetime TIMESTAMP,
                                tpep_dropoff_datetime TIMESTAMP,
                                pulocationid INTEGER,
                                dolocationid INTEGER,
                                trip_distance FLOAT,
                                fare_amount FLOAT,
                                passenger_count INTEGER,
                                ratecodeid INTEGER,
                                trip_duration FLOAT,
                                pickup_hour INTEGER,
                                pickup_day_of_week INTEGER,
                                month INTEGER,
                                year INTEGER
                             )
                             
                             """)
                
                cur.execute("""
                             CREATE TABLE IF NOT EXISTS green_tripdata_2021_2025(
                                trip_id VARCHAR(17) PRIMARY KEY,
                                lpep_pickup_datetime TIMESTAMP,
                                lpep_dropoff_datetime TIMESTAMP,
                                pulocationid INTEGER,
                                dolocationid INTEGER,
                                trip_distance FLOAT,
                                fare_amount FLOAT,
                                passenger_count INTEGER,
                                ratecodeid INTEGER,
                                trip_duration FLOAT,
                                pickup_hour INTEGER,
                                pickup_day_of_week INTEGER,
                                month INTEGER,
                                year INTEGER
                             )
                             
                             """)
                conn.commit()

                print("✅ Database tables created successfully!")

            # Normalize DataFrame column names to PostgreSQL lowercase defaults
            yellow_df.columns = yellow_df.columns.str.lower()
            green_df.columns = green_df.columns.str.lower()

            # Load data with duplicate handling
            try:
                yellow_df.to_sql('yellow_tripdata_2021_2025', DB_URL, if_exists='append', index=False)
                print("✅ Yellow taxi data loaded successfully!")
            except Exception as e:
                if "duplicate key value" in str(e).lower() or "unique constraint" in str(e).lower():
                    print("⚠️  Some yellow taxi records already exist (duplicates skipped)")
                else:
                    print(f"❌ Error loading yellow taxi data: {e}")
                    raise
            
            try:
                green_df.to_sql('green_tripdata_2021_2025', DB_URL, if_exists='append', index=False)
                print("✅ Green taxi data loaded successfully!")
            except Exception as e:
                if "duplicate key value" in str(e).lower() or "unique constraint" in str(e).lower():
                    print("⚠️  Some green taxi records already exist (duplicates skipped)")
                else:
                    print(f"❌ Error loading green taxi data: {e}")
                    raise
            
            print("🚀 DATABASE SUCCESS: Data pushed to DATABASE!")

        except Exception as e:
            print(f"❌ DATABASE ERROR: {e}")
