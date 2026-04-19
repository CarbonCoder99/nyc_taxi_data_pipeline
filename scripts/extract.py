import requests
import pandas as pd
import time
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

# EXTRACT LOGIC
def extract():
    global yellow_df, green_df
    yellow_trip_data_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet"
    green_trip_data_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2026-01.parquet"

    url_list = [yellow_trip_data_url, green_trip_data_url]



    for i in url_list:
        # catch any errors that occur during the download process and print an error message
        try:            
            response = requests.get(i)
            response.raise_for_status()  # Check if the request was successful

            if response.status_code == 200:
                filename = i.split('/')[-1]
            # with open(f"./files/{filename}", "wb") as file:
            #     file.write(response.content)
            # print(f"{filename} downloaded successfully.")
            
                if "yellow" in filename:
                    yellow_df = pd.read_parquet(BytesIO(response.content))
                    print(f"{filename} loaded into DataFrame successfully.")
                elif "green" in filename:
                    green_df = pd.read_parquet(BytesIO(response.content))
                    print(f"{filename} loaded into DataFrame successfully.")

        except requests.RequestException as e:
            print(f"Error downloading {i}: {e}")
            continue
        
        time.sleep(1)  # Adding a delay to avoid overwhelming the machine with requests
    return yellow_df, green_df
