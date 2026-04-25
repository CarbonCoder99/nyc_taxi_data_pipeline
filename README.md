# NYC Taxi Data ETL Project

A production-ready ETL pipeline for NYC Yellow and Green Taxi trip data. This project extracts Parquet data from the NYC TLC public source, transforms the datasets, and loads them into PostgreSQL.

## What this project does

- Extracts Yellow and Green taxi trip data from the NYC TLC public Parquet files.
- Uses retries, schema validation, and configurable extraction ranges.
- Transforms raw data with feature extraction, deduplication, and validation.
- Loads cleaned records into PostgreSQL using idempotent merge semantics.
- Supports CLI parameters, logging, and CI-friendly tests.

## Repo structure

- `main.py`: orchestrates the ETL flow.
- `scripts/config.py`: logging and environment configuration.
- `scripts/extract.py`: downloads and validates Parquet datasets.
- `scripts/transform.py`: transforms and validates datasets.
- `scripts/load.py`: loads data into PostgreSQL with staging and duplicate handling.
- `tests/`: unit tests for extraction, transformation, and load helpers.
- `README.md`: project documentation.
- `.env.example`: example environment settings.
- `requirements.txt`: Python dependencies.

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
   pip install -r requirements.txt
   ```

## Configuration

Copy `.env.example` to `.env` and update values for your environment.

```env
DB_URL=postgresql://taxi_user:StrongPassword123@localhost:5432/nyc_taxi
LOG_LEVEL=INFO
```

## Run the ETL pipeline

1. Ensure PostgreSQL is running.
2. Ensure your virtual environment is activated.
3. Run the pipeline with default year/month ranges:

```bash
python main.py
```

4. Use CLI flags to control extraction range:

```bash
python main.py --start-year 2021 --end-year 2023 --start-month 1 --end-month 6 --colors yellow green
```

## Testing

Run unit tests with:

```bash
pytest -q
```

## Notes on tables and data

The pipeline writes to the following tables:

- `yellow_tripdata`
- `green_tripdata`

Each table includes:
- pickup / dropoff timestamps
- pickup and dropoff location IDs
- trip distance, fare amount, passenger count, and rate code
- computed `trip_duration`
- extracted `pickup_hour`, `pickup_day_of_week`, `month`, and `year`
- a stable `trip_id` primary key for idempotent loads

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

This project is intended for educational and data engineering practice. Use the NYC TLC data according to the official terms of service.