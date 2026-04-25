import pandas as pd
import pytest

from scripts.transform import transform


def test_transform_creates_features():
    yellow_df = pd.DataFrame(
        {
            "tpep_pickup_datetime": [pd.Timestamp("2021-01-01 00:00:00")],
            "tpep_dropoff_datetime": [pd.Timestamp("2021-01-01 00:10:00")],
            "PULocationID": [1],
            "DOLocationID": [2],
            "trip_distance": [1.0],
            "fare_amount": [5.0],
            "passenger_count": [1],
            "RatecodeID": [1],
        }
    )

    green_df = pd.DataFrame(
        {
            "lpep_pickup_datetime": [pd.Timestamp("2021-01-01 00:00:00")],
            "lpep_dropoff_datetime": [pd.Timestamp("2021-01-01 00:10:00")],
            "PULocationID": [1],
            "DOLocationID": [2],
            "trip_distance": [1.0],
            "fare_amount": [5.0],
            "passenger_count": [1],
            "RatecodeID": [1],
        }
    )

    yellow_result, green_result = transform(yellow_df, green_df)

    assert "trip_id" in yellow_result.columns
    assert "trip_id" in green_result.columns
    assert yellow_result["trip_duration"].iloc[0] == 10.0
    assert green_result["pickup_hour"].iloc[0] == 0
    assert yellow_result["month"].iloc[0] == 1
    assert green_result["year"].iloc[0] == 2021


def test_transform_raises_for_empty_data():
    with pytest.raises(ValueError):
        transform(pd.DataFrame(), pd.DataFrame())
