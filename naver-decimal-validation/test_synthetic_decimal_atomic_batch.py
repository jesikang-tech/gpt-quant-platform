"""Synthetic-only Decimal batch atomicity regression tests."""

import sqlite3
from decimal import Decimal

import pytest

from core.decimal_synthetic_bridge import DecimalPricePair
from core.synthetic_atomic_price_repository import SyntheticPriceWriteRejected
from core.synthetic_decimal_atomic_repository import (
    SyntheticDecimalWriteRejected,
    create_synthetic_decimal_schema,
    insert_synthetic_decimal_batch,
    insert_synthetic_decimal_pair,
)


def _pair(ticker, day, close="10.12345678901234567890"):
    return DecimalPricePair(
        ticker=ticker,
        observation_date=day,
        open_price=Decimal("10"),
        high_price=Decimal("11"),
        low_price=Decimal("9"),
        close_price=Decimal(close),
        volume=Decimal("100"),
    )


def _database():
    conn = sqlite3.connect(":memory:")
    create_synthetic_decimal_schema(conn)
    return conn


def _rows(conn, table):
    return conn.execute(
        f"SELECT * FROM {table} ORDER BY ticker, date"
    ).fetchall()


def test_batch_stores_multiple_pairs_atomically_with_exact_decimal():
    conn = _database()
    try:
        insert_synthetic_decimal_batch(
            conn,
            [
                _pair("AAA", "2026-01-02"),
                _pair("BBB", "2026-01-05"),
            ],
        )

        prices = _rows(conn, "synthetic_decimal_prices")
        ohlcv = _rows(conn, "synthetic_decimal_ohlcv")

        assert len(prices) == len(ohlcv) == 2
        assert prices[0][2] == "10.12345678901234567890"
        assert ohlcv[0][5] == prices[0][2]
        assert ohlcv[1][5] == prices[1][2]
        assert not conn.in_transaction
    finally:
        conn.close()


def test_duplicate_input_key_rejected_without_writes():
    conn = _database()
    try:
        pair = _pair("AAA", "2026-01-02")

        with pytest.raises(
            SyntheticDecimalWriteRejected,
            match="Duplicate synthetic batch key",
        ):
            insert_synthetic_decimal_batch(conn, [pair, pair])

        assert _rows(conn, "synthetic_decimal_prices") == []
        assert _rows(conn, "synthetic_decimal_ohlcv") == []
    finally:
        conn.close()


def test_existing_database_key_failure_rolls_back_entire_batch():
    conn = _database()
    try:
        insert_synthetic_decimal_pair(
            conn, _pair("BBB", "2026-01-05")
        )

        before_prices = _rows(conn, "synthetic_decimal_prices")
        before_ohlcv = _rows(conn, "synthetic_decimal_ohlcv")

        with pytest.raises(sqlite3.IntegrityError):
            insert_synthetic_decimal_batch(
                conn,
                [
                    _pair("AAA", "2026-01-02"),
                    _pair("BBB", "2026-01-05"),
                ],
            )

        assert _rows(conn, "synthetic_decimal_prices") == before_prices
        assert _rows(conn, "synthetic_decimal_ohlcv") == before_ohlcv
        assert not conn.in_transaction
    finally:
        conn.close()


def test_later_invalid_pair_rejected_before_any_write():
    conn = _database()
    try:
        invalid = _pair("BBB", "2026-01-05", close="12")

        with pytest.raises(
            SyntheticDecimalWriteRejected,
            match="Invalid OHLC range",
        ):
            insert_synthetic_decimal_batch(
                conn,
                [_pair("AAA", "2026-01-02"), invalid],
            )

        assert _rows(conn, "synthetic_decimal_prices") == []
        assert _rows(conn, "synthetic_decimal_ohlcv") == []
    finally:
        conn.close()


@pytest.mark.parametrize("pairs", [[], (), None, {}])
def test_empty_or_unsupported_batch_rejected(pairs):
    conn = _database()
    try:
        with pytest.raises(
            SyntheticDecimalWriteRejected,
            match="Nonempty explicit synthetic batch required",
        ):
            insert_synthetic_decimal_batch(conn, pairs)

        assert _rows(conn, "synthetic_decimal_prices") == []
    finally:
        conn.close()


def test_file_backed_database_is_rejected(tmp_path):
    conn = sqlite3.connect(tmp_path / "synthetic.db")
    try:
        with pytest.raises(SyntheticPriceWriteRejected):
            insert_synthetic_decimal_batch(
                conn, [_pair("AAA", "2026-01-02")]
            )
    finally:
        conn.close()
def test_later_ohlcv_insert_failure_rolls_back_whole_batch():
    conn = _database()
    try:
        # Seed only OHLCV for the later key. Its PRICE insert can succeed,
        # but its OHLCV insert must fail on the existing primary key.
        later = _pair("BBB", "2026-01-05")
        conn.execute(
            "INSERT INTO synthetic_decimal_ohlcv VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                later.ticker,
                later.observation_date,
                "10",
                "11",
                "9",
                str(later.close_price),
                "100",
            ),
        )
        conn.commit()

        before_prices = _rows(conn, "synthetic_decimal_prices")
        before_ohlcv = _rows(conn, "synthetic_decimal_ohlcv")

        with pytest.raises(sqlite3.IntegrityError):
            insert_synthetic_decimal_batch(
                conn,
                [
                    _pair("AAA", "2026-01-02"),
                    later,
                ],
            )

        assert _rows(conn, "synthetic_decimal_prices") == before_prices
        assert _rows(conn, "synthetic_decimal_ohlcv") == before_ohlcv
        assert not conn.in_transaction
    finally:
        conn.close()


def test_existing_transaction_is_rejected_without_rollback():
    conn = _database()
    try:
        conn.execute("BEGIN")
        assert conn.in_transaction

        with pytest.raises(
            SyntheticPriceWriteRejected,
            match="Existing transaction prohibited",
        ):
            insert_synthetic_decimal_batch(
                conn,
                [_pair("AAA", "2026-01-02")],
            )

        # The caller's transaction remains under caller ownership.
        assert conn.in_transaction
        conn.rollback()

        assert _rows(conn, "synthetic_decimal_prices") == []
        assert _rows(conn, "synthetic_decimal_ohlcv") == []
    finally:
        conn.close()
