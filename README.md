# NYC Taxi Data ETL Project

This project performs an ETL (Extract, Transform, Load) process on NYC Yellow and Green Taxi trip data for January 2026. It downloads the data from the official NYC Taxi and Limousine Commission (TLC) website, processes it, and loads it into a PostgreSQL database.

## Features

- **Extract**: Downloads Yellow and Green taxi trip data in Parquet format.
- **Transform**: Cleans the data by selecting relevant columns, calculating trip duration, removing duplicates, and handling missing values.
- **Load**: Inserts the processed data into PostgreSQL tables.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Required Python packages: `requests`, `pandas`, `sqlalchemy`, `python-dotenv`

## Setup

1. Clone or download this repository.

2. Install the required packages:
   ```
   pip install requests pandas sqlalchemy python-dotenv
   ```

3. Create a `.env` file in the project root with your PostgreSQL connection string:
   ```
   DB_URL=postgresql://username:password@localhost:5432/database_name
   ```

4. Ensure PostgreSQL is running and accessible.

## Usage

Run the ETL script:
```
python main.py
```

The script will:
- Download the data files if not present.
- Process the data.
- Load it into the database tables `yellow_tripdata_jan_2026` and `green_tripdata_jan_2026`.

## Project Structure

- `main.py`: Main ETL script.
- `notebook.ipynb`: Jupyter notebook version of the ETL process.
- `README.md`: Detailed description of Project Structure

## Data Source

Data is sourced from: https://d37ci6vzurychx.cloudfront.net/trip-data/

- Yellow Taxi: `yellow_tripdata_2026-01.parquet`
- Green Taxi: `green_tripdata_2026-01.parquet`

## License

This project is for educational purposes. Please refer to the NYC TLC data usage terms.