import sqlite3
from contextlib import closing

from price_quality import summarize_price_quality_overall


def test_overall_price_quality_report(tmp_path):
    db = tmp_path / "quality_report.db"

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
                open_price REAL,
                high_price REAL,
                low_price REAL,
                close_price REAL,
                volume REAL,
                PRIMARY KEY (ticker, date)
            );

            INSERT INTO etf_prices VALUES
                ('MATCH', '2026-07-24', 100),
                ('DIFF', '2026-07-24', 101),
                ('WEEKEND', '2026-07-25', 200),
                ('INVALID', '2026-07-24', -1);

            INSERT INTO etf_ohlcv_prices VALUES
                ('MATCH', '2026-07-24', 100, 100, 100, 100, 1000),
                ('DIFF', '2026-07-24', 100, 102, 99, 100, 1000),
                ('INVALID', '2026-07-24', 100, 100, 100, 100, 1000),
                ('ONLY_OHLCV', '2026-07-24', 100, 100, 100, 100, 1000);
        """)
        conn.commit()

    before = db.read_bytes()

    report = summarize_price_quality_overall(db)

    assert report["total"] == 5
    assert report["MATCH"] == 1
    assert report["MISMATCH"] == 1
    assert report["MISSING_SOURCE"] == 2
    assert report["INVALID_PRICE"] == 1
    assert report["weekend_rows"] == 1
    assert report["price_source_verified"] is False

    assert db.read_bytes() == before


def test_overall_report_missing_database(tmp_path):
    import pytest

    db = tmp_path / "missing.db"

    with pytest.raises(sqlite3.OperationalError):
        summarize_price_quality_overall(db)

    assert not db.exists()
