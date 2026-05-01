# NYC Taxi Data ETL Project

A sequential ETL pipeline for NYC Yellow and Green Taxi trip data. This project extracts Parquet data from the NYC TLC public source, processes it month-by-month, and loads it into PostgreSQL.

## What this project does

- **Extracts** Yellow and Green taxi trip data from NYC TLC public Parquet files one month at a time.
- **Transforms** raw data by selecting key columns, calculating trip duration, removing duplicates, dropping missing rows, and extracting pickup time features.
- **Loads** cleaned data into PostgreSQL tables `yellow_tripdata_2021_2025` and `green_tripdata_2021_2025`.
- **Processes sequentially** by year and month, allowing for granular error handling and progress tracking.

## Repo structure

- `main.py`: Orchestrates the ETL flow with year/month configuration and error handling.
- `scripts/extract.py`: Contains `get_url()`, `fetch_parquet()`, and `extract(year, month)` functions to download and read a single month of Parquet data.
- `scripts/transform.py`: Transforms data by selecting columns, computing duration, dropping duplicates, and adding time features.
- `scripts/load.py`: Connects to PostgreSQL and writes processed data.
- `.env`: Environment file for storing the database connection URL.
- `README.md`: Project documentation.

## Prerequisites

- Python 3.8 or newer
- PostgreSQL 12+ (or compatible, e.g., Supabase)
- Internet access to download NYC taxi data

## Python setup

1. Create and activate a virtual environment (recommended):

   Windows PowerShell:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Windows Command Prompt:
   ```cmd
   python -m venv .venv
   .\.venv\Scripts\activate.bat
   ```

2. Install required Python packages:
   ```bash
   pip install requests pandas sqlalchemy python-dotenv pyarrow
   ```

   Note: `pyarrow` is required for reading Parquet files with `pandas`.

## PostgreSQL setup

This section covers installing PostgreSQL on Windows and configuring a database for the ETL pipeline.

### Install PostgreSQL on Windows

1. Download PostgreSQL:
   - Visit: https://www.postgresql.org/download/windows/
   - Download the installer from EnterpriseDB.

2. Run the installer and follow these steps:
   - Select the installation directory.
   - Choose a data directory.
   - Set a PostgreSQL superuser password.
   - Keep the default port `5432` unless you need a different port.
   - Install pgAdmin if you want a GUI tool.

3. Confirm the PostgreSQL service is running:
   - Open Services and verify `postgresql-x64-*` is running.
   - Or use PowerShell:
     ```powershell
     Get-Service | Where-Object Name -Like 'postgres*'
     ```

4. Create a database and user role:
   - Open `psql` or pgAdmin.
   - Create a database and user role with SQL:
     ```sql
     CREATE DATABASE nyc_taxi;
     CREATE USER taxi_user WITH PASSWORD 'StrongPassword123';
     GRANT ALL PRIVILEGES ON DATABASE nyc_taxi TO taxi_user;
     ```

5. Verify the connection:
   ```bash
   psql -h localhost -p 5432 -U taxi_user -d nyc_taxi
   ```

### Configure the project connection

Create a `.env` file in the project root with the connection string. For local PostgreSQL or Supabase:

**Local PostgreSQL:**
```env
DB_URL=postgresql://taxi_user:StrongPassword123@localhost:5432/nyc_taxi
```

**Supabase:**
```env
DB_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT.supabase.co:5432/postgres
```

> If PostgreSQL uses a non-default port, update the port number accordingly.

## Run the ETL pipeline

The pipeline processes data month-by-month. Configure the year and month range in `main.py`:

```python
start_year = 2021
end_year = 2021
start_month = 1
end_month = 12  # Adjust as needed
```

Then run:

```bash
python main.py
```

### How it works

For each month in the specified range, the pipeline will:
1. Extract Yellow and Green taxi data for that month from NYC TLC Parquet files
2. Transform the records (drop nulls, remove duplicates, compute features)
3. Load the cleaned data into PostgreSQL
4. Continue to the next month

This month-by-month approach provides:
- **Granular error handling**: If one month fails, others can still be processed
- **Better progress tracking**: See which months have completed
- **Flexible scheduling**: Process months in smaller batches if needed

## Notes on tables and data

The pipeline writes to the following tables:

- `yellow_tripdata_2021_2025`: Yellow taxi trip data
- `green_tripdata_2021_2025`: Green taxi trip data

Each table includes:
- `trip_id`: Unique trip identifier (generated from trip details)
- Pickup/dropoff timestamps (`tpep_pickup_datetime`, `lpep_pickup_datetime`, etc.)
- Pickup and dropoff location IDs (`pulocationid`, `dolocationid`)
- `trip_distance`, `fare_amount`, `passenger_count`, `ratecodeid`
- `trip_duration`: Calculated trip duration in minutes
- `pickup_hour`, `pickup_day_of_week`: Extracted time features
- `month`, `year`: Extracted date features

## Troubleshooting

- If `python main.py` fails with a database error, verify `DB_URL` in `.env` and confirm the database is reachable.
- If Parquet load fails, ensure `pyarrow` is installed.
- If the ETL does not find data, confirm your internet connection and that NYC TLC URLs are reachable.
- For connection timeouts with remote databases (e.g., Supabase), check firewall/network rules.

## Data source

NYC Taxi and Limousine Commission (TLC) trip data is downloaded from:
- `https://d37ci6vzurychx.cloudfront.net/trip-data/`

Example files:
- `yellow_tripdata_2021-01.parquet`
- `green_tripdata_2021-01.parquet`

## License

This project is intended for educational and data engineering practice. Use the NYC TLC data according to the official terms of service.