import sqlite3
from contextlib import closing

import pytest

from price_test_support import isolated_price_db
@pytest.fixture(autouse=True)
def _reset_quality_test_database(isolated_price_db):
    """Reset only the fixture-owned temporary database."""
    isolated_price_db.path.unlink()
from price_quality import check_price_quality

def _create_quality_test_tables(conn):
    """Create minimal synthetic tables for price-quality boundary tests."""
    conn.executescript("""
        CREATE TABLE etf_prices (
            ticker TEXT, date TEXT, close_price REAL
        );
        CREATE TABLE etf_ohlcv_prices (
            ticker TEXT, date TEXT, close_price REAL
        );
    """)



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
def test_invalid_price_values(isolated_price_db, legacy, ohlcv):
    db = isolated_price_db.path

    with closing(sqlite3.connect(db)) as conn:
        _create_quality_test_tables(conn)
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


def test_both_sources_missing(isolated_price_db):
    db = isolated_price_db.path

    with closing(sqlite3.connect(db)) as conn:
        _create_quality_test_tables(conn)
        conn.commit()

    before = db.read_bytes()
    result = check_price_quality(db, "TEST", "2026-09-16")

    assert result["status"] == "MISSING_SOURCE"
    assert db.read_bytes() == before


def test_missing_database_is_not_created(isolated_price_db):
    db = isolated_price_db.path

    with pytest.raises(sqlite3.OperationalError):
        check_price_quality(db, "TEST", "2026-09-16")

    assert not db.exists()


def test_matching_prices_are_not_source_verified(isolated_price_db):
    db = isolated_price_db.path

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
