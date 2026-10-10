import sqlite3
from contextlib import closing

import pytest

from price_quality import rank_price_quality_dates


def test_rank_price_quality_dates(tmp_path):
    db = tmp_path / "daily_ranking.db"

    with closing(sqlite3.connect(db)) as conn:
        conn.executescript("""
            CREATE TABLE etf_prices (
                ticker TEXT NOT NULL,
                date TEXT NOT NULL,
                close_price REAL NOT NULL,
                PRIMARY KEY (ticker, date)
            );

            CREATE TABLE etf_ohlcv_prices (
                ticker TEXT NOT NULL,
                date TEXT NOT NULL,
                close_price REAL,
                PRIMARY KEY (ticker, date)
            );

            INSERT INTO etf_prices VALUES
                ('A', '2026-07-28', 101),
                ('B', '2026-07-28', 102),
                ('C', '2026-07-28', 100),
                ('A', '2026-07-29', 100),
                ('B', '2026-07-29', 100),
                ('W', '2026-07-25', 100);

            INSERT INTO etf_ohlcv_prices VALUES
                ('A', '2026-07-28', 100),
                ('B', '2026-07-28', 100),
                ('C', '2026-07-28', 100),
                ('A', '2026-07-29', 100),
                ('B', '2026-07-29', 100);
        """)
        conn.commit()

    before = db.read_bytes()

    result = rank_price_quality_dates(db, limit=3)

    assert len(result) == 3
    assert result[0]["date"] == "2026-07-28"
    assert result[0]["total"] == 3
    assert result[0]["MISMATCH"] == 2
    assert result[0]["mismatch_rate"] == pytest.approx(2 / 3)
    assert result[0]["price_source_verified"] is False

    assert result[1]["date"] == "2026-07-25"
    assert result[1]["MISSING_SOURCE"] == 1
    assert result[1]["MISMATCH"] == 0

    assert result[2]["date"] == "2026-07-29"
    assert result[2]["MISMATCH"] == 0

    assert db.read_bytes() == before


def test_rank_price_quality_dates_missing_database(tmp_path):
    db = tmp_path / "missing.db"

    with pytest.raises(sqlite3.OperationalError):
        rank_price_quality_dates(db)

    assert not db.exists()
