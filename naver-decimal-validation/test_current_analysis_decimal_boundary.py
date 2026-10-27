"""Synthetic Decimal regression for the existing current-analysis entry.

No application imports, operational database connections, or provider calls.
The real analysis function is extracted from source and supplied with isolated
dependencies. This test does not authorize NAVER data usage.
"""

import ast
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

import pytest

from test_factor_decimal_boundary import _load_existing_factor_engine


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "current_analysis.py"


def _load_analysis_function():
    tree = ast.parse(ANALYSIS.read_text(encoding="utf-8"))
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "get_current_analysis_data"
    ]
    assert len(functions) == 1

    factor = _load_existing_factor_engine()
    function = functions[0]
    function.decorator_list = []

    module = ast.Module(body=[function], type_ignores=[])
    ast.fix_missing_locations(module)

    def forbidden_database(*args, **kwargs):
        raise AssertionError("Operational database access is forbidden")

    namespace = {
        "Decimal": Decimal,
        "Optional": Optional,
        "_normalize_analysis_date": lambda value: "2026-09-04",
        "_get_period_config": lambda value: {
            "lookback_trading_days": 2,
            "return_threshold": 15.0,
        },
        "MIN_UPTREND_RATIO": 0.70,
        "get_all_etf_tickers": lambda: ["SYNTHETIC"],
        "_get_etf_name_map": lambda: {"SYNTHETIC": "Synthetic"},
        "get_etf_prices": forbidden_database,
        "calculate_return": factor.calculate_return,
        "calculate_return_score": factor.calculate_return_score,
        "calculate_trend_score": factor.calculate_trend_score,
        "calculate_slope_score": factor.calculate_slope_score,
        "calculate_uptrend_ratio": factor.calculate_uptrend_ratio,
        "_get_future_performance": lambda *args: (None, None, None),
        "_get_reality_test": lambda *args: {},
        "_get_close_only_reality_test": lambda *args: {},
    }

    exec(compile(module, str(ANALYSIS), "exec"), namespace)
    return SimpleNamespace(
        analyze=namespace["get_current_analysis_data"],
        namespace=namespace,
    )


@pytest.mark.parametrize(
    "closing,expected_pass",
    [
        ("114.999999999999999999", False),
        ("115", True),
        ("115.000000000000000001", True),
    ],
    ids=["strictly_below", "exact_threshold", "strictly_above"],
)
def test_current_analysis_decimal_selection_boundary(closing, expected_pass):
    subject = _load_analysis_function()

    def synthetic_prices(ticker, end_date):
        assert ticker == "SYNTHETIC"
        assert end_date == "2026-09-04"
        return [
            ("2026-09-03", Decimal("100")),
            ("2026-09-04", Decimal(closing)),
        ]

    subject.namespace["get_etf_prices"] = synthetic_prices

    result = subject.analyze(
        limit=1,
        analysis_date="2026-09-04",
        period="1m",
    )

    rows = result["current_score_top"]
    assert len(rows) == 1
    assert rows[0]["ticker"] == "SYNTHETIC"
    assert rows[0]["selection_pass"] is expected_pass
