"""Isolated synthetic integration of existing Replay and Factor engines."""

from datetime import date, timedelta
from decimal import Decimal
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
