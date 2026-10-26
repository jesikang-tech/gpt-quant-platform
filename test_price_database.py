"""Price persistence and queries against an isolated synthetic database."""

import pytest

from price_test_support import isolated_price_db


def test_price_count_order_and_ticker_filter(isolated_price_db):
    from core.price_provenance_gate import PriceProvenanceRejected
    from repository import save_etf_price, get_etf_prices
    from database import get_connection

    prices = [
        ("2026-01-06", 103),
        ("2026-01-02", 100),
        ("2026-01-05", 101),
    ]

    # An unverified source must never gain persistence authorization.
    with pytest.raises(PriceProvenanceRejected):
        save_etf_price("111111", "2026-01-06", 103)

    conn = get_connection()
    try:
        assert conn.execute(
            "SELECT COUNT(*) FROM etf_prices"
        ).fetchone() == (0,)

        # Prepare trusted-by-construction synthetic fixture rows only
        # inside the isolated temporary test database.
        with conn:
            conn.executemany(
                "INSERT INTO etf_prices "
                "(ticker, date, close_price) VALUES (?, ?, ?)",
                [("111111", day, price) for day, price in prices]
                + [("222222", "2026-01-02", 999)],
            )

        assert conn.execute(
            "SELECT COUNT(*) FROM etf_prices WHERE ticker=?",
            ("111111",),
        ).fetchone() == (len(prices),)

        assert conn.execute(
            "SELECT date, close_price FROM etf_prices "
            "WHERE ticker=? ORDER BY date LIMIT 2",
            ("111111",),
        ).fetchall() == sorted(prices)[:2]
    finally:
        conn.close()

    assert get_etf_prices("111111") == sorted(prices)
