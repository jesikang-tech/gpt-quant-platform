import sqlite3
from contextlib import closing
import pytest

from price_test_support import isolated_price_db
from price_quality import summarize_price_quality_by_date


def test_daily_price_quality_summary(isolated_price_db):
    db = isolated_price_db.path

    with closing(sqlite3.connect(db)) as conn:
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
                ('AAA', '2026-09-16', 100),
                ('BBB', '2026-09-16', 101),
                ('CCC', '2026-09-16', 100),
                ('DDD', '2026-09-16', 0);

            INSERT INTO etf_ohlcv_prices VALUES
                ('AAA', '2026-09-16', 100),
                ('BBB', '2026-09-16', 100),
                ('DDD', '2026-09-16', 100),
                ('EEE', '2026-09-16', 100);
        """)
        conn.commit()

    before = db.read_bytes()

    result = summarize_price_quality_by_date(
        db,
        "2026-09-16",
    )

    assert result["date"] == "2026-09-16"
    assert result["total"] == 5
    assert result["MATCH"] == 1
    assert result["MISMATCH"] == 1
    assert result["MISSING_SOURCE"] == 2
    assert result["INVALID_PRICE"] == 1

    assert db.read_bytes() == before


def test_daily_summary_null_and_missing_sources(isolated_price_db):
    db = isolated_price_db.path

    with closing(sqlite3.connect(db)) as conn:
        conn.executescript("""
            CREATE TABLE etf_prices (
                ticker TEXT, date TEXT, close_price REAL,
                PRIMARY KEY (ticker, date)
            );

            CREATE TABLE etf_ohlcv_prices (
                ticker TEXT, date TEXT, close_price REAL,
                PRIMARY KEY (ticker, date)
            );

            INSERT INTO etf_prices VALUES
                ('NULL_A', '2026-09-16', NULL),
                ('NULL_B', '2026-09-16', 100),
                ('ONLY_A', '2026-09-16', 100);

            INSERT INTO etf_ohlcv_prices VALUES
                ('NULL_A', '2026-09-16', 100),
                ('NULL_B', '2026-09-16', NULL),
                ('ONLY_B', '2026-09-16', 100);
        """)
        conn.commit()

    before = db.read_bytes()

    result = summarize_price_quality_by_date(
        db, "2026-09-16"
    )

    assert result["total"] == 4
    assert result["INVALID_PRICE"] == 2
    assert result["MISSING_SOURCE"] == 2
    assert result["MATCH"] == 0
    assert result["MISMATCH"] == 0
    assert result["price_source_verified"] is False
    assert db.read_bytes() == before


def test_daily_summary_missing_database_not_created(isolated_price_db):
    db = isolated_price_db.path

    import pytest

    with pytest.raises(sqlite3.OperationalError):
        summarize_price_quality_by_date(db, "2026-09-16")

    assert not db.exists()

@pytest.fixture(autouse=True)
def _reset_quality_test_database(isolated_price_db):
    """Reset only the fixture-owned temporary database."""
    isolated_price_db.path.unlink()
