"""Isolated synthetic integration of existing Replay and Factor engines."""

from datetime import date, timedelta
from decimal import Context, Decimal, localcontext
from pathlib import Path
import ast
import importlib.util
import sys
import types

import pytest


def _load_replay_without_database(monkeypatch):
    root = Path(__file__).resolve().parents[1]

    database_stub = types.ModuleType("database")

    def forbidden_connection():
        raise AssertionError("DATABASE_ACCESS_FORBIDDEN")

    database_stub.get_connection = forbidden_connection

    with monkeypatch.context() as patch:
        patch.setitem(sys.modules, "database", database_stub)

        factor_spec = importlib.util.spec_from_file_location(
            "_synthetic_replay_factor",
            root / "factor_engine.py",
        )
        factor = importlib.util.module_from_spec(factor_spec)

        # Read literal configuration without executing config.py.
        required = {
            "MIN_RETURN_3M",
            "MIN_UPTREND_RATIO",
            "MIN_REQUIRED_PRICE_DATA",
        }
        tree = ast.parse(
            (root / "config.py").read_text(encoding="utf-8")
        )
        values = {}

        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in required:
                    if target.id in values:
                        raise AssertionError("Duplicate configuration constant")
                    values[target.id] = ast.literal_eval(node.value)

        if set(values) != required:
            raise AssertionError("Required configuration constants missing")

        config = types.ModuleType("config")
        for name, value in values.items():
            setattr(config, name, value)
        patch.setitem(sys.modules, "config", config)

        factor_spec.loader.exec_module(factor)
        patch.setitem(sys.modules, "factor_engine", factor)

        replay_spec = importlib.util.spec_from_file_location(
            "_synthetic_replay_engine",
            root / "historical_replay.py",
        )
        replay = importlib.util.module_from_spec(replay_spec)
        replay_spec.loader.exec_module(replay)

    monkeypatch.setitem(sys.modules, "database", database_stub)
    replay.get_connection = forbidden_connection
    return replay.HistoricalReplayEngine


def _synthetic_prices():
    current = date(2026, 1, 1)
    rows = []

    while len(rows) < 70:
        if current.weekday() < 5:
            rows.append((
                current.isoformat(),
                Decimal("100") + Decimal(len(rows)),
            ))
        current += timedelta(days=1)

    return tuple(rows)


def test_replay_decimal_calculation_without_database(monkeypatch):
    engine_type = _load_replay_without_database(monkeypatch)
    prices = _synthetic_prices()
    analysis_date = prices[-1][0]

    assert len(prices) == 70
    assert all(type(close) is Decimal for _, close in prices)

    engine = engine_type(analysis_date)
    engine._get_historical_prices = lambda ticker: list(prices)

    result = engine._evaluate_ticker("SYNTHETIC_REPLAY")

    assert result is not None
    assert result["ticker"] == "SYNTHETIC_REPLAY"
    assert result["analysis_date"] == analysis_date
    assert result["trading_days"] == 70
    assert result["return_rate"] > 15
    assert result["uptrend_ratio"] >= 70
    assert result["final_score"] > 0


def test_replay_database_access_is_denied(monkeypatch):
    engine_type = _load_replay_without_database(monkeypatch)
    engine = engine_type("2026-03-11")

    with pytest.raises(AssertionError, match="DATABASE_ACCESS_FORBIDDEN"):
        engine._get_historical_prices("SYNTHETIC_REPLAY")


@pytest.fixture
def synthetic_decimal_replay_repository():
    from contextlib import closing
    import sqlite3
    from core.naver_decimal_price_pipeline import prepare_naver_decimal_price_pair
    from core.synthetic_decimal_atomic_repository import (
        create_synthetic_decimal_schema,
        insert_synthetic_decimal_batch,
    )

    # These weekday labels are synthetic fixtures, not an exchange calendar.
    with localcontext(Context(prec=50)):
        prices = tuple((day, close + Decimal("0.00000000000000000001"))
                       for day, close in _synthetic_prices())
        pairs = tuple(prepare_naver_decimal_price_pair(
            "SYNTHETIC_REPLAY", day,
            {"Open": close, "High": close, "Low": close, "Close": close,
             "Volume": Decimal("1000")},
            adjustment="UNADJUSTED",
        ) for day, close in prices)
    with closing(sqlite3.connect(":memory:")) as conn:
        create_synthetic_decimal_schema(conn)
        insert_synthetic_decimal_batch(conn, pairs)
        yield conn, prices


def test_repository_decimal_series_reaches_existing_replay(
    monkeypatch, synthetic_decimal_replay_repository,
):
    from core.synthetic_decimal_atomic_repository import read_synthetic_replay_prices

    engine_type = _load_replay_without_database(monkeypatch)
    conn, prices = synthetic_decimal_replay_repository
    ticker = "SYNTHETIC_REPLAY"
    analysis_date = prices[-1][0]
    engine = engine_type(analysis_date)
    with pytest.raises(AssertionError, match="^DATABASE_ACCESS_FORBIDDEN$"):
        engine._get_historical_prices(ticker)

    series = read_synthetic_replay_prices(conn, ticker=ticker, analysis_date=analysis_date)
    assert len(series) == 70
    assert type(series) is tuple
    assert series == prices
    assert [close.as_tuple() for _, close in series] == [close.as_tuple() for _, close in prices]
    assert all(type(close) is Decimal for _, close in series)
    assert series[0][1] != Decimal(str(float(series[0][1])))
    calls = []

    def synthetic_historical_prices(requested_ticker):
        calls.append(requested_ticker)
        assert requested_ticker == ticker
        return series

    engine._get_historical_prices = synthetic_historical_prices
    changes = conn.total_changes
    result = engine._evaluate_ticker(ticker)
    assert calls == [ticker]
    assert result is not None
    assert result["ticker"] == ticker
    assert result["analysis_date"] == analysis_date
    assert result["trading_days"] == 70
    assert type(result["return_rate"]) is Decimal
    assert result["return_rate"] > 15
    assert result["uptrend_ratio"] == 100.0
    assert result["final_score"] == 100.0
    assert conn.total_changes == changes
    assert not conn.in_transaction


def test_repository_close_text_mismatch_blocks_replay_evaluation(
    monkeypatch, synthetic_decimal_replay_repository,
):
    from core.synthetic_decimal_atomic_repository import (
        SyntheticDecimalWriteRejected,
        read_synthetic_replay_prices,
    )

    engine_type = _load_replay_without_database(monkeypatch)
    conn, prices = synthetic_decimal_replay_repository
    ticker = "SYNTHETIC_REPLAY"
    analysis_date = prices[-1][0]
    assert read_synthetic_replay_prices(conn, ticker=ticker, analysis_date=analysis_date) == prices
    original_text = str(prices[0][1])
    changed_text = original_text + "0"
    assert changed_text != original_text
    assert Decimal(changed_text) == Decimal(original_text)
    assert str(Decimal(changed_text)) == changed_text
    conn.execute(
        "UPDATE synthetic_decimal_prices SET close_price = ? WHERE ticker = ? AND date = ?",
        (changed_text, ticker, prices[0][0]),
    )
    conn.commit()
    engine = engine_type(analysis_date)
    evaluation_calls = []
    original_evaluate = engine._evaluate_ticker

    def recording_evaluate(requested_ticker):
        evaluation_calls.append(requested_ticker)
        return original_evaluate(requested_ticker)

    with monkeypatch.context() as patch:
        patch.setattr(engine, "_evaluate_ticker", recording_evaluate)
        with pytest.raises(
            SyntheticDecimalWriteRejected, match="^PRICE/OHLCV close TEXT mismatch$",
        ):
            series = read_synthetic_replay_prices(conn, ticker=ticker, analysis_date=analysis_date)
            engine._get_historical_prices = lambda requested_ticker: series
            engine._evaluate_ticker(ticker)
    assert evaluation_calls == []
    assert not conn.in_transaction
    with pytest.raises(AssertionError, match="^DATABASE_ACCESS_FORBIDDEN$"):
        engine._get_historical_prices(ticker)
