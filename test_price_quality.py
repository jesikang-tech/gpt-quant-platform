import sqlite3
from contextlib import closing

import pytest

from price_quality import check_price_quality


@pytest.fixture
def quality_db(tmp_path):
    path = tmp_path / "price_quality.db"

    with closing(sqlite3.connect(path)) as conn:
        conn.executescript("""
            CREATE TABLE etf_prices (
                ticker TEXT,
                date TEXT,
                close_price REAL,
                PRIMARY KEY (ticker, date)
            );

            CREATE TABLE etf_ohlcv_prices (
                ticker TEXT,
                date TEXT,
                close_price REAL,
                PRIMARY KEY (ticker, date)
            );

            INSERT INTO etf_prices VALUES
                ('MATCH', '2026-09-16', 100),
                ('DIFF', '2026-09-16', 101),
                ('MISSING', '2026-09-16', 100),
                ('INVALID', '2026-09-16', 0);

            INSERT INTO etf_ohlcv_prices VALUES
                ('MATCH', '2026-09-16', 100),
                ('DIFF', '2026-09-16', 100),
                ('INVALID', '2026-09-16', 100);
        """)
        conn.commit()

    return path


@pytest.mark.parametrize(
    "ticker, expected",
    [
        ("MATCH", "MATCH"),
        ("DIFF", "MISMATCH"),
        ("MISSING", "MISSING_SOURCE"),
        ("INVALID", "INVALID_PRICE"),
    ],
)
def test_price_quality_status(quality_db, ticker, expected):
    before = quality_db.read_bytes()

    result = check_price_quality(
        quality_db,
        ticker,
        "2026-09-16",
    )

    assert result["status"] == expected
    assert result["ticker"] == ticker
    assert result["date"] == "2026-09-16"
    assert quality_db.read_bytes() == before
