import sqlite3
from contextlib import closing

import pytest

from price_test_support import isolated_price_db, phase8_test_scope


@pytest.fixture
def quality_db(_protected_flask_state):
    path = _protected_flask_state.db.path

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
