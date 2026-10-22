"""Offline tests for the NAVER Decimal price pipeline."""

from decimal import Decimal

import pytest

from core.naver_decimal_price_pipeline import (
    prepare_naver_decimal_price_pair,
)


def valid_values():
    return {
        "Open": "9775",
        "High": "9810",
        "Low": "9715",
        "Close": "9770",
        "Volume": "123456",
    }


def test_naver_price_pair_preserves_decimal_values():
    pair = prepare_naver_decimal_price_pair(
        "0008S0",
        "2026-09-16",
        valid_values(),
        adjustment="UNADJUSTED",
    )

    assert pair.close_price == Decimal("9770")
    assert pair.open_price == Decimal("9775")
    assert pair.high_price == Decimal("9810")


def test_naver_price_pair_rejects_float_values():
    values = valid_values()
    values["Close"] = 9770.0

    with pytest.raises(ValueError):
        prepare_naver_decimal_price_pair(
            "0008S0",
            "2026-09-16",
            values,
            adjustment="UNADJUSTED",
        )


def test_naver_price_pair_rejects_invalid_ohlc():
    values = valid_values()
    values["Close"] = "9900"

    with pytest.raises(ValueError):
        prepare_naver_decimal_price_pair(
            "0008S0",
            "2026-09-16",
            values,
            adjustment="UNADJUSTED",
        )


def test_naver_price_pair_rejects_unknown_adjustment():
    with pytest.raises(ValueError):
        prepare_naver_decimal_price_pair(
            "0008S0",
            "2026-09-16",
            valid_values(),
            adjustment="UNKNOWN",
        )

def test_naver_price_rows_share_exact_close():
    from core.naver_decimal_price_pipeline import (
        prepare_naver_price_rows,
    )

    price_row, ohlcv_row = prepare_naver_price_rows(
        "0008S0",
        "2026-09-16",
        valid_values(),
        adjustment="UNADJUSTED",
    )

    assert price_row[0] == ohlcv_row[0]
    assert price_row[1] == ohlcv_row[1]
    assert price_row[2] == ohlcv_row[5]
    assert price_row[2] is ohlcv_row[5]
    assert type(price_row[2]) is Decimal


def test_naver_price_rows_reject_invalid_observation():
    from core.naver_decimal_price_pipeline import (
        prepare_naver_price_rows,
    )

    values = valid_values()
    values["Low"] = "9900"

    with pytest.raises(ValueError):
        prepare_naver_price_rows(
            "0008S0",
            "2026-09-16",
            values,
            adjustment="UNADJUSTED",
        )

def test_naver_atomic_decimal_storage():
    import sqlite3

    from core.synthetic_decimal_atomic_repository import (
        create_synthetic_decimal_schema,
        insert_synthetic_decimal_pair,
    )

    pair = prepare_naver_decimal_price_pair(
        "0008S0",
        "2026-09-16",
        valid_values(),
        adjustment="UNADJUSTED",
    )

    with sqlite3.connect(":memory:") as conn:
        create_synthetic_decimal_schema(conn)
        insert_synthetic_decimal_pair(conn, pair)

        price = conn.execute(
            "SELECT close_price FROM synthetic_decimal_prices"
        ).fetchone()

        ohlcv = conn.execute(
            "SELECT close_price FROM synthetic_decimal_ohlcv"
        ).fetchone()

        assert price == ("9770",)
        assert ohlcv == price


def test_naver_atomic_decimal_duplicate_preserves_existing_rows():
    import sqlite3

    from core.synthetic_decimal_atomic_repository import (
        create_synthetic_decimal_schema,
        insert_synthetic_decimal_pair,
    )

    pair = prepare_naver_decimal_price_pair(
        "0008S0",
        "2026-09-16",
        valid_values(),
        adjustment="UNADJUSTED",
    )

    with sqlite3.connect(":memory:") as conn:
        create_synthetic_decimal_schema(conn)
        insert_synthetic_decimal_pair(conn, pair)

        with pytest.raises(sqlite3.IntegrityError):
            insert_synthetic_decimal_pair(conn, pair)

        price_count = conn.execute(
            "SELECT COUNT(*) FROM synthetic_decimal_prices"
        ).fetchone()[0]

        ohlcv_count = conn.execute(
            "SELECT COUNT(*) FROM synthetic_decimal_ohlcv"
        ).fetchone()[0]

        assert price_count == 1
        assert ohlcv_count == 1


def test_naver_rejects_unverified_adjustment_contract():
    from core.naver_decimal_price_pipeline import (
        prepare_naver_decimal_price_pair,
    )

    with pytest.raises(ValueError):
        prepare_naver_decimal_price_pair(
            "0008S0",
            "2026-09-16",
            valid_values(),
            adjustment="UNVERIFIED",
        )


def test_naver_rejects_float_precision_boundary():
    from core.naver_decimal_price_pipeline import (
        prepare_naver_price_rows,
    )

    values = valid_values()
    values["Close"] = 9770.0

    with pytest.raises(ValueError):
        prepare_naver_price_rows(
            "0008S0",
            "2026-09-16",
            values,
            adjustment="UNADJUSTED",
        )


def test_naver_analysis_integration_remains_denied():
    from core.naver_decimal_price_pipeline import (
        prepare_naver_analysis_rows,
    )

    with pytest.raises(
        RuntimeError,
        match="UNVERIFIED_ANALYSIS_COMPATIBILITY_DENIED",
    ):
        prepare_naver_analysis_rows(
            "0008S0",
            "2026-09-16",
            valid_values(),
            adjustment="UNADJUSTED",
        )


def test_naver_raw_row_preserves_exact_decimal():
    from core.naver_decimal_price_pipeline import (
        prepare_naver_raw_decimal_pair,
    )

    pair = prepare_naver_raw_decimal_pair(
        "0008S0",
        "20260916|9775|9810|9715|9770|123456",
        adjustment="UNADJUSTED",
    )

    assert pair.observation_date == "2026-09-16"
    assert pair.close_price == Decimal("9770")
    assert type(pair.close_price) is Decimal


def test_naver_raw_row_rejects_invalid_date():
    from core.naver_decimal_price_pipeline import (
        parse_naver_raw_ohlcv_row,
    )

    with pytest.raises(ValueError):
        parse_naver_raw_ohlcv_row(
            "20260230|9775|9810|9715|9770|123456"
        )


def test_naver_raw_row_rejects_invalid_price_range():
    from core.naver_decimal_price_pipeline import (
        prepare_naver_raw_decimal_pair,
    )

    with pytest.raises(ValueError):
        prepare_naver_raw_decimal_pair(
            "0008S0",
            "20260916|9775|9810|9715|9900|123456",
            adjustment="UNADJUSTED",
        )


def test_naver_raw_row_rejects_float_input():
    from core.naver_decimal_price_pipeline import (
        parse_naver_raw_ohlcv_row,
    )

    with pytest.raises(ValueError):
        parse_naver_raw_ohlcv_row(
            9770.0
        )


def test_naver_raw_row_rejects_unverified_adjustment():
    from core.naver_decimal_price_pipeline import (
        prepare_naver_raw_decimal_pair,
    )

    with pytest.raises(ValueError):
        prepare_naver_raw_decimal_pair(
            "0008S0",
            "20260916|9775|9810|9715|9770|123456",
            adjustment="UNVERIFIED",
        )