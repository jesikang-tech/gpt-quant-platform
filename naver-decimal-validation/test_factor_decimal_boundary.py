"""Synthetic-only Decimal boundary contract for existing factor calculations."""

from decimal import Decimal
from pathlib import Path
import ast
import importlib.util
import sys
import types


def _load_existing_factor_engine():
    root = Path(__file__).resolve().parents[1]
    source = root / "factor_engine.py"

    # Read literal assignments without executing application config.py.
    # No application database, provider, or replay module is imported.
    required = {
        "MIN_RETURN_3M",
        "MIN_UPTREND_RATIO",
        "MIN_REQUIRED_PRICE_DATA",
    }
    config_tree = ast.parse(
        (root / "config.py").read_text(encoding="utf-8")
    )
    values = {}

    for node in config_tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in required:
                if target.id in values:
                    raise AssertionError(
                        f"Duplicate config constant: {target.id}"
                    )
                values[target.id] = ast.literal_eval(node.value)

    if set(values) != required:
        raise AssertionError(
            f"Missing config constants: {sorted(required - set(values))}"
        )

    config = types.ModuleType("config")
    for name, value in values.items():
        setattr(config, name, value)

    original_config = sys.modules.get("config")
    sys.modules["config"] = config

    try:
        spec = importlib.util.spec_from_file_location(
            "_synthetic_factor_decimal_boundary",
            source,
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if original_config is None:
            sys.modules.pop("config", None)
        else:
            sys.modules["config"] = original_config


def test_decimal_return_threshold_exact_and_adjacent():
    factor = _load_existing_factor_engine()
    start = Decimal("100")
    below = Decimal("114.999999999")
    exact = Decimal("115")
    above = Decimal("115.000000001")

    below_rate = factor.calculate_return(start, below)
    exact_rate = factor.calculate_return(start, exact)
    above_rate = factor.calculate_return(start, above)

    assert type(exact_rate) is Decimal
    assert below_rate < Decimal("15")
    assert exact_rate == Decimal("15")
    assert above_rate > Decimal("15")

    assert factor.calculate_return_score(below_rate) == 70
    assert factor.calculate_return_score(exact_rate) == 90
    assert factor.calculate_return_score(above_rate) == 90


def test_decimal_slope_threshold_exact_and_adjacent():
    factor = _load_existing_factor_engine()
    start = Decimal("100")

    assert factor.calculate_slope_score(
        [start, Decimal("114.999999999")]
    ) == 70

    assert factor.calculate_slope_score(
        [start, Decimal("115")]
    ) == 90

    assert factor.calculate_slope_score(
        [start, Decimal("115.000000001")]
    ) == 90


def test_decimal_trend_and_final_score():
    factor = _load_existing_factor_engine()

    prices = [
        Decimal("100.000000001"),
        Decimal("100.000000002"),
        Decimal("100.000000003"),
        Decimal("100.000000002"),
        Decimal("100.000000004"),
    ]

    assert factor.calculate_trend_score(prices) == 75
    assert factor.calculate_uptrend_ratio(prices) == 75.0

    assert factor.calculate_final_score(90, 75, 90) == 85.5


def test_decimal_etf_threshold_configuration_contract():
    factor = _load_existing_factor_engine()

    assert factor.MIN_RETURN_3M == 0.15
    assert factor.MIN_UPTREND_RATIO == 0.70
    assert factor.MIN_REQUIRED_PRICE_DATA == 60

    assert Decimal("15") >= factor.MIN_RETURN_3M * 100
    assert Decimal("14.999999999") < factor.MIN_RETURN_3M * 100
    assert Decimal("15.000000001") >= factor.MIN_RETURN_3M * 100
