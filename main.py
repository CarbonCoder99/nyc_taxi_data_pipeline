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
    try:
        yellow_df, green_df = extract()
        yellow_df, green_df = transform(yellow_df, green_df)
        load(yellow_df, green_df)
    except KeyError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

