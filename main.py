import requests
import os
import time
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from scripts.extract import extract
from scripts.transform import transform
from scripts.load import load


load_dotenv()  # Load environment variables from a .env file

def main():
    start_year = 2021
    end_year = 2021
    start_month = 1
    end_month = 4
    
    # Loop through the specified years and months to extract, transform, and load data for each month
    for year in range(start_year, end_year + 1):
        for month in range(start_month, end_month + 1):
            try:
                # Extract data for the current year and month
                yellow_df, green_df = extract(year, month)
                # Only proceed with transformation and loading if at least one of the DataFrames is not empty
                if not yellow_df.empty or not green_df.empty:
                    yellow_df, green_df = transform(yellow_df, green_df)
                    load(yellow_df, green_df)
                else:
                    # Show a message if both DataFrames are empty, indicating that there is no data for the current year and month
                    print(f"No data for {year}-{month:02d}")


            # Handle specific exceptions to provide more informative error messages and ensure the pipeline continues running for other months/years
            except KeyError as e:
                print(f" Key Error for {year}-{month:02d}: {e}")
            except requests.RequestException as e:
                print(f"Connection Error for {year}-{month:02d}: {e}")
            except KeyboardInterrupt:
                print("❌ Keyboard interrupt. Exiting...")
                return
            except Exception as e:
                print(f"Error processing {year}-{month:02d}: {e}")


if __name__ == "__main__":
    main()

