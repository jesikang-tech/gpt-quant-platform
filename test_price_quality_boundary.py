import sqlite3
from contextlib import closing

import pytest

from price_test_support import isolated_price_db, phase8_test_scope


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
    db = _scope.db.path

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
    db = _scope.db.path

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
    db = _scope.db.path

    with pytest.raises(sqlite3.OperationalError):
        check_price_quality(db, "TEST", "2026-09-16")

    assert not db.exists()


def test_matching_prices_are_not_source_verified(tmp_path):
    db = _scope.db.path

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


@pytest.fixture(autouse=True)
def _protected_flask_state(isolated_price_db, monkeypatch):
    with phase8_test_scope(isolated_price_db) as scope:
        import sys
        from price_quality import check_price_quality
        target = sys.modules[__name__]
        for name, value in {"check_price_quality": check_price_quality, "_scope": scope}.items():
            monkeypatch.setattr(target, name, value, raising=False)
        config_before = dict(scope.api.app.config)
        auth_path_before = scope.api.AUTH_CONFIG_PATH
        # Keep the original legacy-only schemas and absent-DB contracts.
        scope.db.path.unlink()
        try:
            yield scope
        finally:
            scope.api.app.config.clear()
            scope.api.app.config.update(config_before)
            scope.api.AUTH_CONFIG_PATH = auth_path_before
