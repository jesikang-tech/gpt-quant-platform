import os
import tempfile
from pathlib import Path

import config
import database
import repository

from core.period_analysis import get_period_analysis


def test_historical_replay_respects_analysis_date_and_is_deterministic():
    fd, db_path = tempfile.mkstemp(
        prefix="historical_replay_",
        suffix=".db"
    )
    os.close(fd)

    original_config_path = config.DATABASE_PATH
    original_database_path = database.DATABASE_PATH

    try:
        test_db_path = Path(db_path)

        config.DATABASE_PATH = test_db_path
        database.DATABASE_PATH = test_db_path

        database.init_database()

        conn = database.get_connection()
        cursor = conn.cursor()

        ticker = "TEST_REPLAY"
        analysis_date = "2026-06-12"

        prices = [
            ("2026-03-23", 100.0),
            ("2026-03-24", 101.0),
            ("2026-03-25", 102.0),
            ("2026-03-26", 103.0),
            ("2026-03-27", 104.0),
            ("2026-03-30", 105.0),
            ("2026-03-31", 106.0),
            ("2026-04-01", 107.0),
            ("2026-04-02", 108.0),
            ("2026-04-03", 109.0),
            ("2026-04-06", 110.0),
            ("2026-04-07", 111.0),
            ("2026-04-08", 112.0),
            ("2026-04-09", 113.0),
            ("2026-04-10", 114.0),
            ("2026-04-13", 115.0),
            ("2026-04-14", 116.0),
            ("2026-04-15", 117.0),
            ("2026-04-16", 118.0),
            ("2026-04-17", 119.0),
            ("2026-04-20", 120.0),
            ("2026-04-21", 121.0),
            ("2026-04-22", 122.0),
            ("2026-04-23", 123.0),
            ("2026-04-24", 124.0),
            ("2026-04-27", 125.0),
            ("2026-04-28", 126.0),
            ("2026-04-29", 127.0),
            ("2026-04-30", 128.0),
            ("2026-05-01", 129.0),
            ("2026-05-04", 130.0),
            ("2026-05-05", 131.0),
            ("2026-05-06", 132.0),
            ("2026-05-07", 133.0),
            ("2026-05-08", 134.0),
            ("2026-05-11", 135.0),
            ("2026-05-12", 136.0),
            ("2026-05-13", 137.0),
            ("2026-05-14", 138.0),
            ("2026-05-15", 139.0),
            ("2026-05-18", 140.0),
            ("2026-05-19", 141.0),
            ("2026-05-20", 142.0),
            ("2026-05-21", 143.0),
            ("2026-05-22", 144.0),
            ("2026-05-25", 145.0),
            ("2026-05-26", 146.0),
            ("2026-05-27", 147.0),
            ("2026-05-28", 148.0),
            ("2026-05-29", 149.0),
            ("2026-06-01", 150.0),
            ("2026-06-02", 151.0),
            ("2026-06-03", 152.0),
            ("2026-06-04", 153.0),
            ("2026-06-05", 154.0),
            ("2026-06-08", 155.0),
            ("2026-06-09", 156.0),
            ("2026-06-10", 157.0),
            ("2026-06-11", 158.0),
            ("2026-06-12", 159.0),
            ("2026-06-15", 999.0),
            ("2026-06-16", 1000.0),
            ("2026-06-17", 1001.0),
        ]

        cursor.executemany(
            """
            INSERT INTO etf_prices
            (
                ticker,
                date,
                close_price
            )
            VALUES (?, ?, ?)
            """,
            [
                (ticker, date, price)
                for date, price in prices
            ],
        )

        conn.commit()
        conn.close()

        rows = repository.get_etf_prices(
            ticker,
            analysis_date
        )

        assert rows
        assert rows[-1][0] == analysis_date
        assert all(
            row[0] <= analysis_date
            for row in rows
        )

        result_a = get_period_analysis(
            ticker,
            analysis_date
        )

        result_b = get_period_analysis(
            ticker,
            analysis_date
        )

        assert result_a == result_b
        assert result_a["analysis_date"] == analysis_date
        assert result_a["periods"]["60"]["status"] == "ANALYZED"

    finally:
        config.DATABASE_PATH = original_config_path
        database.DATABASE_PATH = original_database_path

        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass
