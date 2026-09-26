import sqlite3
from contextlib import closing

import pandas as pd
import pytest

import config
import database
import repository
from collector.price_collector import PriceCollector


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    path = tmp_path / "ohlcv.db"
    monkeypatch.setattr(config, "DATABASE_PATH", path)
    monkeypatch.setattr(database, "DATABASE_PATH", path)
    return path


def test_ohlcv_initialization_preserves_existing_close_table(isolated_db):
    with closing(sqlite3.connect(isolated_db)) as conn:
        conn.execute("CREATE TABLE etf_prices (ticker TEXT NOT NULL, date TEXT NOT NULL, "
                     "close_price REAL NOT NULL, PRIMARY KEY (ticker, date))")
        conn.execute("INSERT INTO etf_prices VALUES ('TEST', '2026-01-02', 100)")
        conn.commit()
        original_schema = conn.execute("SELECT sql FROM sqlite_master WHERE name='etf_prices'").fetchone()
    database.init_database()
    repository.save_etf_ohlcv_price("TEST", "2026-01-02", 99, 110, 95, 100, 1234)
    database.init_database()
    with closing(sqlite3.connect(isolated_db)) as conn:
        assert conn.execute("SELECT sql FROM sqlite_master WHERE name='etf_prices'").fetchone() == original_schema
        columns = conn.execute("PRAGMA table_info(etf_ohlcv_prices)").fetchall()
        assert [(row[1], row[2], row[3], row[5]) for row in columns] == [
            ("ticker", "TEXT", 1, 1), ("date", "TEXT", 1, 2),
            ("open_price", "REAL", 0, 0), ("high_price", "REAL", 0, 0),
            ("low_price", "REAL", 0, 0), ("close_price", "REAL", 0, 0),
            ("volume", "REAL", 0, 0),
        ]
    assert repository.get_etf_prices("TEST") == [("2026-01-02", 100.0)]
    assert repository.get_etf_ohlcv_prices("TEST") == [("2026-01-02", 99, 110, 95, 100, 1234)]


def test_ohlcv_roundtrip_update_filter_and_close_independence(isolated_db):
    database.init_database()
    repository.save_etf_price("TEST", "2026-01-02", 100)
    repository.save_etf_ohlcv_price("TEST", "2026-01-05", 100, 120, 98, 110, 200)
    repository.save_etf_ohlcv_price("TEST", "2026-01-02", 99, 115, 90, 101, 100)
    repository.save_etf_ohlcv_price("OTHER", "2026-01-02", high_price=999)
    assert repository.get_etf_ohlcv_prices("TEST", "2026-01-02") == [
        ("2026-01-02", 99, 115, 90, 101, 100)
    ]
    repository.save_etf_ohlcv_price("TEST", "2026-01-02", close_price=102)
    assert repository.get_etf_ohlcv_prices("TEST") == [
        ("2026-01-02", None, None, None, 102, None),
        ("2026-01-05", 100, 120, 98, 110, 200),
    ]
    assert repository.get_etf_ohlcv_prices("MISSING") == []
    assert repository.get_etf_prices("TEST") == [("2026-01-02", 100)]
    repository.save_etf_price("TEST", "2026-01-02", 103)
    assert repository.get_etf_prices("TEST", "2026-01-02") == [("2026-01-02", 103)]
    assert repository.get_etf_prices("TEST", "2026-01-01") == []
    assert repository.get_etf_ohlcv_prices("TEST")[0][4] == 102


@pytest.mark.parametrize("high", [120.0, None, float("nan"), pd.NA, "absent"])
def test_collector_saves_ohlcv_without_high_fallback(isolated_db, monkeypatch, high):
    database.init_database()
    values = {"Open": [99], "Low": [95], "Close": [100], "Volume": [1234], "Change": [0.01]}
    if not isinstance(high, str):
        values["High"] = [high]
    frame = pd.DataFrame(values, index=pd.to_datetime(["2026-01-02"]))
    collector = PriceCollector()
    monkeypatch.setattr(collector.provider, "get_price", lambda *args: frame)
    assert collector.collect("TEST", "2026-01-02", "2026-01-02") is frame
    expected_high = 120.0 if isinstance(high, float) and high == 120.0 else None
    assert repository.get_etf_ohlcv_prices("TEST") == [
        ("2026-01-02", 99, expected_high, 95, 100, 1234)
    ]
    assert repository.get_etf_prices("TEST") == [("2026-01-02", 100)]


@pytest.mark.parametrize("create_ohlcv", [False, True])
def test_replay_does_not_require_ohlcv(isolated_db, create_ohlcv):
    import current_analysis

    if create_ohlcv:
        database.init_database()
    else:
        with closing(sqlite3.connect(isolated_db)) as conn:
            conn.executescript(
                "CREATE TABLE etf_info (ticker TEXT PRIMARY KEY, name TEXT);"
                "CREATE TABLE etf_prices (ticker TEXT, date TEXT, close_price REAL,"
                "PRIMARY KEY(ticker, date));"
            )
    dates = pd.bdate_range("2026-01-01", periods=20).strftime("%Y-%m-%d").tolist()
    with closing(sqlite3.connect(isolated_db)) as conn:
        conn.execute("INSERT INTO etf_info (ticker, name) VALUES ('TEST', 'Test ETF')")
        conn.executemany("INSERT INTO etf_prices VALUES (?, ?, ?)",
                         [("TEST", day, 100 + index) for index, day in enumerate(dates)])
        conn.commit()
    before = isolated_db.read_bytes()
    result = current_analysis.get_current_analysis_data(analysis_date=dates[-1], period="1m")
    assert result["success"] is True
    assert result["current_score_top"][0]["price"] == 119
    assert result["current_score_top"][0]["return"] == 19
    assert result["db_write"] is False
    assert isolated_db.read_bytes() == before
