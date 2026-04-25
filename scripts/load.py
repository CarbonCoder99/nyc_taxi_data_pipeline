import logging
import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
logger = logging.getLogger(__name__)

YELLOW_TABLE = "yellow_tripdata"
GREEN_TABLE = "green_tripdata"

TABLE_SCHEMAS = {
    YELLOW_TABLE: """
        CREATE TABLE IF NOT EXISTS yellow_tripdata(
            trip_id VARCHAR(17) PRIMARY KEY,
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
            pickup_day_of_week INTEGER,
            month INTEGER,
            year INTEGER
        )
    """,
    GREEN_TABLE: """
        CREATE TABLE IF NOT EXISTS green_tripdata(
            trip_id VARCHAR(17) PRIMARY KEY,
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
            pickup_day_of_week INTEGER,
            month INTEGER,
            year INTEGER
        )
    """,
}


def get_db_url():
    db_url = os.getenv("DB_URL")
    if not db_url:
        raise ValueError("DB_URL is not set. Set a DB_URL environment variable before running the pipeline.")
    return db_url


def get_db_engine(db_url, retries=3, delay=2):
    engine = create_engine(db_url, pool_pre_ping=True)
    last_exception = None
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                logger.info("Database connection successful on attempt %s", attempt)
            return engine
        except Exception as exc:
            last_exception = exc
            logger.warning("Database connection failed on attempt %s: %s", attempt, exc)
            time.sleep(delay * attempt)

    raise ConnectionError(f"Unable to connect to database after {retries} attempts") from last_exception


def _create_table(conn, table_name):
    conn.execute(text(TABLE_SCHEMAS[table_name]))
    logger.info("Ensured table exists: %s", table_name)


def _load_dataframe(engine, df, table_name):
    if df.empty:
        logger.info("Skipping empty dataframe for %s", table_name)
        return

    df = df.drop_duplicates(subset=["trip_id"]).copy()
    staging_table = f"{table_name}_staging"

    with engine.begin() as conn:
        _create_table(conn, table_name)

        df.to_sql(staging_table, con=conn, if_exists="replace", index=False, method="multi")
        logger.info("Wrote %s rows to staging table %s", len(df), staging_table)

        insert_sql = text(
            f"INSERT INTO {table_name} SELECT * FROM {staging_table} "
            f"ON CONFLICT (trip_id) DO NOTHING"
        )
        result = conn.execute(insert_sql)
        logger.info(
            "Merged staging data into %s, rows affected=%s",
            table_name,
            result.rowcount,
        )

        conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}"))
        logger.info("Dropped staging table %s", staging_table)


def load(yellow_df, green_df):
    db_url = get_db_url()
    engine = get_db_engine(db_url)

    if not yellow_df.empty:
        _load_dataframe(engine, yellow_df, YELLOW_TABLE)
    else:
        logger.info("No yellow data to load")

    if not green_df.empty:
        _load_dataframe(engine, green_df, GREEN_TABLE)
    else:
        logger.info("No green data to load")

    logger.info("Database load completed")
