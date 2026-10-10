"""Verify sample price insertion using an isolated temporary database."""

import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory


SAMPLE_PRICES = [
    10000,
    10200,
    10500,
    10800,
    11000,
    11300,
    11600,
]


def test_sample_price_insertion():
    with TemporaryDirectory() as directory:
        db_path = Path(directory) / "sample_prices.db"

        with closing(sqlite3.connect(db_path)) as conn:
            conn.execute(
                """
                CREATE TABLE etf_prices (
                    ticker TEXT NOT NULL,
                    date TEXT NOT NULL,
                    close_price REAL NOT NULL,
                    PRIMARY KEY (ticker, date)
                )
                """
            )

            rows = [
                ("069500", f"2026-07-{20 + i}", price)
                for i, price in enumerate(SAMPLE_PRICES)
            ]

            conn.executemany(
                """
                INSERT INTO etf_prices
                    (ticker, date, close_price)
                VALUES (?, ?, ?)
                """,
                rows,
            )

            actual = conn.execute(
                """
                SELECT close_price
                FROM etf_prices
                WHERE ticker = ?
                ORDER BY date
                """,
                ("069500",),
            ).fetchall()

        assert [row[0] for row in actual] == SAMPLE_PRICES


if __name__ == "__main__":
    test_sample_price_insertion()
    print("Sample price insertion test: PASS")
