# NYC Taxi Data ETL Project

A lightweight ETL pipeline for NYC Yellow and Green Taxi trip data. This project extracts Parquet data from the NYC TLC public source, transforms the datasets, and loads them into PostgreSQL.

## What this project does

- Extracts Yellow and Green taxi trip data from the NYC TLC public Parquet files.
- Transforms the raw data by selecting key columns, calculating trip duration, removing duplicates, dropping missing rows, and extracting pickup time features.
- Loads the cleaned data into PostgreSQL tables `yellow_tripdata_2021_2025` and `green_tripdata_2021_2025`.

## Repo structure

- `main.py`: orchestrates the ETL flow.
- `scripts/extract.py`: downloads and reads the Parquet datasets.
- `scripts/transform.py`: selects columns, computes duration, drops duplicates, and adds time features.
- `scripts/load.py`: connects to PostgreSQL and writes the processed data.
- `notebook.ipynb`: optional notebook version for exploration and prototyping.
- `README.md`: project documentation.

## Prerequisites

- Python 3.8 or newer
- PostgreSQL 12+ (or compatible)
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

### Option 1: Install PostgreSQL on Windows

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

### Option 2: Use PostgreSQL with Docker

If you prefer Docker instead of native installation, run:

```bash
docker run --name nyc-taxi-postgres -e POSTGRES_USER=taxi_user -e POSTGRES_PASSWORD=StrongPassword123 -e POSTGRES_DB=nyc_taxi -p 5432:5432 -d postgres:latest
```

Then verify:

```bash
docker ps
```

### Configure the project connection

Create a `.env` file in the project root with the connection string:

```env
DB_URL=postgresql://taxi_user:StrongPassword123@localhost:5432/nyc_taxi
```

> If PostgreSQL uses a non-default port, update `5432` to the correct port.

## Run the ETL pipeline

1. Ensure PostgreSQL is running.
2. Ensure your virtual environment is activated.
3. Run:

```bash
python main.py
```

The ETL flow will:
- download Yellow and Green Parquet files for years 2021–2025,
- transform the records,
- write the cleaned tables into PostgreSQL.

## Notes on tables and data

The pipeline writes to the following tables:

- `yellow_tripdata_2021_2025`
- `green_tripdata_2021_2025`

Each table includes:
- pickup / dropoff timestamps
- pickup and dropoff location IDs
- trip distance, fare amount, passenger count, and rate code
- computed `trip_duration`
- extracted `pickup_hour` and `pickup_day_of_week`
- extracted `month` and `year`

## Troubleshooting

- If `python main.py` fails with a database error, verify `DB_URL` and confirm PostgreSQL is reachable.
- If Parquet load fails, ensure `pyarrow` is installed.
- If the ETL does not find data, confirm your internet connection and that the NYC TLC URL is reachable.

## Data source

NYC Taxi and Limousine Commission (TLC) trip data is downloaded from:
- `https://d37ci6vzurychx.cloudfront.net/trip-data/`

Example files:
- `yellow_tripdata_2021-01.parquet`
- `green_tripdata_2021-01.parquet`

## License

This repository is intended for educational and data engineering practice. Use the NYC TLC data according to the official terms of service.