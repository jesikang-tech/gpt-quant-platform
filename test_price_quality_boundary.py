import sqlite3
from contextlib import closing

import pytest

from price_quality import check_price_quality


@pytest.mark.parametrize(
    "legacy,ohlcv",
    [
        (-100, 100),
        (100, -100),
        (None, 100),
        (100, None),
        (float("inf"), 100),
        (100, float("inf")),
        (float("nan"), 100),
    ],
)
def test_invalid_price_values(tmp_path, legacy, ohlcv):
    db = tmp_path / "invalid_prices.db"

    with closing(sqlite3.connect(db)) as conn:
        conn.executescript("""
            CREATE TABLE etf_prices (
                ticker TEXT, date TEXT, close_price REAL
            );
            CREATE TABLE etf_ohlcv_prices (
                ticker TEXT, date TEXT, close_price REAL
            );
        """)
        conn.execute(
            "INSERT INTO etf_prices VALUES ('TEST', '2026-09-16', ?)",
            (legacy,),
        )
        conn.execute(
            "INSERT INTO etf_ohlcv_prices VALUES ('TEST', '2026-09-16', ?)",
            (ohlcv,),
        )
        conn.commit()

    before = db.read_bytes()
    result = check_price_quality(db, "TEST", "2026-09-16")

    assert result["status"] == "INVALID_PRICE"
    assert result["price_source_verified"] is False
    assert db.read_bytes() == before


def test_both_sources_missing(tmp_path):
    db = tmp_path / "missing_sources.db"

    with closing(sqlite3.connect(db)) as conn:
        conn.executescript("""
            CREATE TABLE etf_prices (
                ticker TEXT, date TEXT, close_price REAL
            );
            CREATE TABLE etf_ohlcv_prices (
                ticker TEXT, date TEXT, close_price REAL
            );
        """)
        conn.commit()

    before = db.read_bytes()
    result = check_price_quality(db, "TEST", "2026-09-16")

    assert result["status"] == "MISSING_SOURCE"
    assert db.read_bytes() == before


def test_missing_database_is_not_created(tmp_path):
    db = tmp_path / "does_not_exist.db"

    with pytest.raises(sqlite3.OperationalError):
        check_price_quality(db, "TEST", "2026-09-16")

    assert not db.exists()


def test_matching_prices_are_not_source_verified(tmp_path):
    db = tmp_path / "matching.db"

    with closing(sqlite3.connect(db)) as conn:
        conn.executescript("""
            CREATE TABLE etf_prices (
                ticker TEXT, date TEXT, close_price REAL
            );
            CREATE TABLE etf_ohlcv_prices (
                ticker TEXT, date TEXT, close_price REAL
            );
            INSERT INTO etf_prices
                VALUES ('TEST', '2026-09-16', 100);
            INSERT INTO etf_ohlcv_prices
                VALUES ('TEST', '2026-09-16', 100);
        """)
        conn.commit()

    before = db.read_bytes()
    result = check_price_quality(db, "TEST", "2026-09-16")

    assert result["status"] == "MATCH"
    assert result["price_source_verified"] is False
    assert db.read_bytes() == before
