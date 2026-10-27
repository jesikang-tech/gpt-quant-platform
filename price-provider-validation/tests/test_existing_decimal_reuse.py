"""Offline tests of the existing Decimal source contract.

No API calls, database access, persistence, or operational authorization.
"""

import importlib
from decimal import Decimal
from pathlib import Path

import pytest


@pytest.fixture
def decimal_contract(monkeypatch):
    repository = Path(__file__).resolve().parents[2]
    existing_root = repository / "naver-decimal-validation"

    if not (
        existing_root / "core" / "decimal_source_integration.py"
    ).is_file():
        pytest.fail("Existing Decimal contract missing")

    monkeypatch.syspath_prepend(str(existing_root))

    return importlib.import_module(
        "core.decimal_source_integration"
    )


def _values():
    return {
        "Open": "100.125",
        "High": "110.500",
        "Low": "90.000",
        "Close": "105.375",
        "Volume": "1000",
    }


def _prepare(contract, values):
    return contract.prepare_decimal_source_record(
        "005930",
        "2026-10-28",
        values,
        provider="KIS",
        adjustment="UNADJUSTED",
    )


def test_existing_decimal_precision_preserved(decimal_contract):
    record = _prepare(decimal_contract, _values())

    assert record.open_price == Decimal("100.125")
    assert record.close_price == Decimal("105.375")
    assert record.volume == Decimal("1000")


@pytest.mark.parametrize(
    "invalid_value",
    [1.25, True, "NaN", "-1"],
)
def test_existing_decimal_rejects_invalid_price(
    decimal_contract, invalid_value
):
    values = _values()
    values["Open"] = invalid_value

    with pytest.raises(decimal_contract.DecimalSourceRejected):
        _prepare(decimal_contract, values)


def test_existing_decimal_rejects_inconsistent_range(decimal_contract):
    values = _values()
    values["Low"] = "120"

    with pytest.raises(decimal_contract.DecimalSourceRejected):
        _prepare(decimal_contract, values)


def test_existing_decimal_comparison_remains_blocked(decimal_contract):
    record = _prepare(decimal_contract, _values())

    with pytest.raises(
        decimal_contract.DecimalSourceRejected,
        match="Trusted provenance verification not implemented",
    ):
        decimal_contract.classify_decimal_source_record(
            Decimal("100"),
            record,
            existing_evidence=record.evidence,
        )
