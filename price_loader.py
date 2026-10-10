from repository import (
    save_etf_price,
    get_all_price_data
)
import csv
from pathlib import Path


def load_price_data(price_list):
    """Reject legacy development price writes."""

    raise RuntimeError(
        "Development price writes are disabled. "
        "Use an isolated test database instead."
    )

def get_sample_price_data():

    return [

        {
            "ticker": "069500",
            "date": "2026-07-20",
            "close_price": 10000
        },

        {
            "ticker": "069500",
            "date": "2026-07-21",
            "close_price": 10200
        },

        {
            "ticker": "069500",
            "date": "2026-07-22",
            "close_price": 10500
        },

        {
            "ticker": "069500",
            "date": "2026-07-23",
            "close_price": 10800
        },

        {
            "ticker": "069500",
            "date": "2026-07-24",
            "close_price": 11000
        },

        {
            "ticker": "069500",
            "date": "2026-07-25",
            "close_price": 11300
        },

        {
            "ticker": "069500",
            "date": "2026-07-26",
            "close_price": 11600
        }

    ]



def get_csv_price_data(
    filename="price_data.csv"
):
    """
    CSV 가격 데이터 읽기
    """

    price_list = []


    path = Path(filename)


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)


        for row in reader:

            price_list.append(
                {
                    "ticker": row["ticker"],
                    "date": row["date"],
                    "close_price": float(row["close_price"])
                }
            )


    return price_list


def update_price_database(price_list):
    """Reject legacy development price updates."""

    raise RuntimeError(
        "Development price writes are disabled. "
        "Use an isolated test database instead."
    )

if __name__ == "__main__":
    raise SystemExit(
        "price_loader.py is a development-only data loader. "
        "Direct execution against the operational database is disabled."
    )
