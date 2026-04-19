import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()  # Load environment variables from a .env file

# LOAD LOGIC
def load(yellow_df, green_df):
    # Load each parquet file into a postgres database using SQLAlchemy and psycopg2
    DB_URL = os.getenv("DB_URL")  # Get the database URL from environment variables
    if DB_URL:
        print("✅ Found Database URL, attempting to connect...")
        try:
            engine = create_engine(DB_URL)
            # Test database connection
            with engine.connect() as conn:
                print("🔗 Database connection successful!")
            
            yellow_df.to_sql('yellow_tripdata_jan_2026', engine, if_exists='replace', index=False)
            green_df.to_sql('green_tripdata_jan_2026', engine, if_exists='replace', index=False)
            print("🚀 DATABASE SUCCESS: Data pushed to PostgreSQL!")
        except Exception as e:
            print(f"❌ DATABASE ERROR: {e}")
