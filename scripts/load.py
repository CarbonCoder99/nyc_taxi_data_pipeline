import os
import hashlib
from io import StringIO
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
                                trip_id VARCHAR(20) PRIMARY KEY,
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
                                trip_id VARCHAR(20) PRIMARY KEY,
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

            yellow_columns = [
                'trip_id',
                'tpep_pickup_datetime',
                'tpep_dropoff_datetime',
                'pulocationid',
                'dolocationid',
                'trip_distance',
                'fare_amount',
                'passenger_count',
                'ratecodeid',
                'trip_duration',
                'pickup_hour',
                'pickup_day_of_week',
                'month',
                'year'
            ]

            green_columns = [
                'trip_id',
                'lpep_pickup_datetime',
                'lpep_dropoff_datetime',
                'pulocationid',
                'dolocationid',
                'trip_distance',
                'fare_amount',
                'passenger_count',
                'ratecodeid',
                'trip_duration',
                'pickup_hour',
                'pickup_day_of_week',
                'month',
                'year'
            ]

            # Load data using COPY for efficient bulk ingestion
            with psycopg2.connect(DB_URL) as conn:
                # Set statement timeout to 10 minutes (600000 ms) to handle large data loads
                conn.cursor().execute("SET statement_timeout = 600000")
                cur = conn.cursor()

                # Load yellow taxi data
                try:
                    buffer = StringIO()
                    yellow_df.to_csv(buffer, index=False, header=False, columns=yellow_columns)
                    buffer.seek(0)
                    cur.copy_from(buffer, 'yellow_tripdata_2021_2025', sep=',', columns=yellow_columns)
                    conn.commit()
                    print("✅ Yellow taxi data loaded successfully!")
                except Exception as e:
                    if "duplicate key value" in str(e).lower() or "unique constraint" in str(e).lower():
                        print("⚠️  Some yellow taxi records already exist (duplicates skipped)")
                        conn.rollback()
                    else:
                        print(f"❌ Error loading yellow taxi data: {e}")
                        conn.rollback()
                        raise

                # Load green taxi data
                try:
                    buffer = StringIO()
                    green_df.to_csv(buffer, index=False, header=False, columns=green_columns)
                    buffer.seek(0)
                    cur.copy_from(buffer, 'green_tripdata_2021_2025', sep=',', columns=green_columns)
                    conn.commit()
                    print("✅ Green taxi data loaded successfully!")
                except Exception as e:
                    if "duplicate key value" in str(e).lower() or "unique constraint" in str(e).lower():
                        print("⚠️  Some green taxi records already exist (duplicates skipped)")
                        conn.rollback()
                    else:
                        print(f"❌ Error loading green taxi data: {e}")
                        conn.rollback()
                        raise
            
            print("🚀 DATABASE SUCCESS: Data pushed to DATABASE!")

        except Exception as e:
            print(f"❌ DATABASE ERROR: {e}")
