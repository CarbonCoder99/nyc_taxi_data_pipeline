import argparse
import logging
import sys

from dotenv import load_dotenv
from scripts.config import configure_logging
from scripts.extract import extract
from scripts.load import load
from scripts.transform import transform


def parse_args():
    parser = argparse.ArgumentParser(description="Run the NYC Taxi ETL pipeline")
    parser.add_argument("--start-year", type=int, default=2021, help="First year to extract")
    parser.add_argument("--end-year", type=int, default=2025, help="Last year to extract")
    parser.add_argument("--start-month", type=int, default=1, help="First month to extract")
    parser.add_argument("--end-month", type=int, default=12, help="Last month to extract")
    parser.add_argument(
        "--colors",
        nargs="+",
        choices=["yellow", "green"],
        default=["yellow", "green"],
        help="Taxi colors to include",
    )
    return parser.parse_args()


def main():
    load_dotenv()
    configure_logging()
    logger = logging.getLogger(__name__)

    args = parse_args()
    logger.info("Pipeline started with args=%s", args)

    try:
        yellow_df, green_df = extract(
            start_year=args.start_year,
            end_year=args.end_year,
            start_month=args.start_month,
            end_month=args.end_month,
            colors=args.colors,
        )
        yellow_df, green_df = transform(yellow_df, green_df)
        load(yellow_df, green_df)
        logger.info("Pipeline finished successfully")
    except Exception as exc:
        logger.exception("Pipeline failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()

