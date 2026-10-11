"""Verify sample price insertion using an isolated temporary database."""

import sqlite3
from contextlib import closing
import pytest
from price_test_support import isolated_price_db, phase8_test_scope


SAMPLE_PRICES = [
    10000,
    10200,
    10500,
    10800,
    11000,
    11300,
    11600,
]


def test_sample_price_insertion():
    db_path = _scope.db.path

    with closing(sqlite3.connect(db_path)) as conn:
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

        rows = [
            ("069500", f"2026-07-{20 + i}", price)
            for i, price in enumerate(SAMPLE_PRICES)
        ]

        conn.executemany(
                """
                INSERT INTO etf_prices
                    (ticker, date, close_price)
                VALUES (?, ?, ?)
                """,
            rows,
        )

        actual = conn.execute(
                """
                SELECT close_price
                FROM etf_prices
                WHERE ticker = ?
                ORDER BY date
                """,
            ("069500",),
        ).fetchall()

    assert [row[0] for row in actual] == SAMPLE_PRICES


@pytest.fixture(autouse=True)
def _protected_flask_state(isolated_price_db, monkeypatch):
    with phase8_test_scope(isolated_price_db) as scope:
        import sys
        monkeypatch.setattr(sys.modules[__name__], "_scope", scope, raising=False)
        config_before = dict(scope.api.app.config)
        auth_path_before = scope.api.AUTH_CONFIG_PATH
        # Preserve the original custom etf_prices schema.
        scope.db.path.unlink()
        try:
            yield scope
        finally:
            scope.api.app.config.clear()
            scope.api.app.config.update(config_before)
            scope.api.AUTH_CONFIG_PATH = auth_path_before


if __name__ == "__main__":
    raise SystemExit("Run this protected contract with pytest.")
