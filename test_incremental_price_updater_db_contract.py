import sqlite3

from collector.incremental_price_updater import IncrementalPriceUpdater


class _TestUpdater(IncrementalPriceUpdater):

    def __init__(self, conn):
        self._conn = conn
        self.price_collector = None

    def get_latest_price_date(self, ticker):
        row = self._conn.execute(
            """
            SELECT MAX(date)
            FROM etf_prices
            WHERE ticker = ?
            """,
            (ticker,),
        ).fetchone()

        return row[0] if row and row[0] else None


def build_test_db():
    conn = sqlite3.connect(":memory:")

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

    conn.executemany(
        """
        INSERT INTO etf_prices
        (ticker, date, close_price)
        VALUES (?, ?, ?)
        """,
        [
            ("069500", "2026-08-04", 100.0),
            ("069500", "2026-08-03", 99.0),
            ("305720", "2026-08-04", 200.0),
        ],
    )

    conn.commit()

    return conn


def test_latest_price_date_is_returned_per_ticker():
    conn = build_test_db()
    updater = _TestUpdater(conn)

    assert updater.get_latest_price_date("069500") == "2026-08-04"
    assert updater.get_latest_price_date("305720") == "2026-08-04"

    conn.close()


def test_missing_ticker_returns_none():
    conn = build_test_db()
    updater = _TestUpdater(conn)

    assert updater.get_latest_price_date("999999") is None

    conn.close()


def test_latest_date_does_not_cross_tickers():
    conn = build_test_db()

    conn.execute(
        """
        INSERT INTO etf_prices
        (ticker, date, close_price)
        VALUES (?, ?, ?)
        """,
        ("069500", "2026-07-31", 98.0),
    )
    conn.commit()

    updater = _TestUpdater(conn)

    assert updater.get_latest_price_date("069500") == "2026-08-04"
    assert updater.get_latest_price_date("305720") == "2026-08-04"

    conn.close()
import sqlite3

import collector.incremental_price_updater as updater_module
from collector.incremental_price_updater import IncrementalPriceUpdater


def build_temp_db(tmp_path):
    db_path = tmp_path / "price_test.db"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE etf_prices (
            ticker TEXT NOT NULL,
            date TEXT NOT NULL,
            close_price REAL NOT NULL,
            PRIMARY KEY (ticker, date)
        )
    """)
    conn.executemany("""
        INSERT INTO etf_prices
        (ticker, date, close_price)
        VALUES (?, ?, ?)
    """, [
        ("069500", "2026-08-03", 99.0),
        ("069500", "2026-08-04", 100.0),
        ("305720", "2026-08-04", 200.0),
    ])
    conn.commit()
    conn.close()
    return db_path


def test_real_get_latest_price_date_uses_isolated_db(tmp_path, monkeypatch):
    db_path = build_temp_db(tmp_path)

    def isolated_connection():
        return sqlite3.connect(db_path)

    monkeypatch.setattr(
        updater_module,
        "get_connection",
        isolated_connection,
    )

    updater = IncrementalPriceUpdater(price_collector=None)

    assert updater.get_latest_price_date("069500") == "2026-08-04"
    assert updater.get_latest_price_date("305720") == "2026-08-04"
    assert updater.get_latest_price_date("999999") is None
