import pandas as pd

from scripts.extract import extract, fetch_parquet, get_url


class DummyResponse:
    def __init__(self, content):
        self.content = content

    def raise_for_status(self):
        return None


class DummySession:
    def __init__(self, response):
        self.response = response

    def get(self, url, timeout=30):
        return self.response


def test_get_url():
    assert get_url("2021", "01", "yellow") == "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
    assert get_url("2023", "12", "green") == "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-12.parquet"


def test_fetch_parquet_success(monkeypatch):
    expected = pd.DataFrame(
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

    response = DummyResponse(expected.to_parquet())
    session = DummySession(response)
    monkeypatch.setattr("scripts.extract.pd.read_parquet", lambda *args, **kwargs: expected)

    df = fetch_parquet(session, "https://example.com/yellow_tripdata_2021-01.parquet")
    assert df.equals(expected)


def test_extract_range_builds_data(monkeypatch):
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

    def fake_fetch(session, url):
        return yellow_df if "yellow" in url else green_df

    monkeypatch.setattr("scripts.extract.fetch_parquet", fake_fetch)

    yellow_result, green_result = extract(
        start_year=2021,
        end_year=2021,
        start_month=1,
        end_month=1,
        colors=["yellow", "green"],
    )

    assert len(yellow_result) == 1
    assert len(green_result) == 1
