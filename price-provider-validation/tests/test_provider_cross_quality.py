"""Synthetic K19 cross-provider quality integration tests."""
from dataclasses import FrozenInstanceError, replace

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
    prepare_raw_observation,
)
from price_provider_validation.provider_cross_quality import (
    assess_cross_provider_quality,
)


FIELDS = ("100", "110", "90", "105", "1000")


def _observation(provider, ticker="005930", day="2026-10-28",
                 fields=FIELDS):
    return prepare_raw_observation(provider, ticker, day, fields)


def _assert_denied(result):
    assert result.status == "DENIED"
    assert result.reason == (
        "CROSS_PROVIDER_INDEPENDENT_VERIFICATION_MISSING"
    )
    for name in (
        "independently_verified",
        "numerical_equivalence_verified",
        "adjustment_policy_verified",
        "official_trading_day_verified",
        "analysis_authorized",
        "dashboard_authorized",
        "snapshot_authorized",
        "persistence_authorized",
        "database_rebuild_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(result, name) is False

    for name in (
        "selected_provider",
        "preferred_provider",
        "fallback_provider",
    ):
        assert not hasattr(result, name)


def test_identical_raw_values_still_denied():
    result = assess_cross_provider_quality(
        _observation("KIS"),
        _observation("KIWOOM"),
    )
    assert result.pair_status == "MATCHED_UNVERIFIED"
    assert result.kis_structural_status is not None
    assert result.kiwoom_structural_status is not None
    _assert_denied(result)


@pytest.mark.parametrize("index", range(5))
def test_each_raw_field_mismatch_denied(index):
    changed = list(FIELDS)
    changed[index] = "999"
    result = assess_cross_provider_quality(
        _observation("KIS"),
        _observation("KIWOOM", fields=tuple(changed)),
    )
    assert result.pair_status == "PRICE_MISMATCH"
    _assert_denied(result)


@pytest.mark.parametrize(
    "change",
    [
        {"ticker": "000660"},
        {"day": "2026-10-27"},
    ],
)
def test_identity_mismatch_denied(change):
    result = assess_cross_provider_quality(
        _observation("KIS"),
        _observation("KIWOOM", **change),
    )
    assert result.pair_status == "IDENTITY_MISMATCH"
    _assert_denied(result)


@pytest.mark.parametrize(
    "kis,kiwoom",
    [
        (None, None),
        (None, _observation("KIWOOM")),
        (_observation("KIS"), None),
    ],
)
def test_missing_observation_denied(kis, kiwoom):
    result = assess_cross_provider_quality(kis, kiwoom)
    assert result.pair_status == "MISSING"
    _assert_denied(result)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_adjustment_escalation_rejected(provider):
    changed = replace(
        _observation(provider),
        adjustment="ADJUSTED",
    )
    kis = changed if provider == "KIS" else _observation("KIS")
    kiwoom = changed if provider == "KIWOOM" else _observation("KIWOOM")
    with pytest.raises(ProviderObservationRejected):
        assess_cross_provider_quality(kis, kiwoom)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_invalid_numeric_field_rejected(provider):
    changed = replace(
        _observation(provider),
        raw_fields=("bad", "110", "90", "105", "1000"),
    )
    kis = changed if provider == "KIS" else _observation("KIS")
    kiwoom = changed if provider == "KIWOOM" else _observation("KIWOOM")
    with pytest.raises(ProviderObservationRejected):
        assess_cross_provider_quality(kis, kiwoom)


def test_result_is_immutable():
    result = assess_cross_provider_quality(
        _observation("KIS"),
        _observation("KIWOOM"),
    )
    with pytest.raises(FrozenInstanceError):
        result.analysis_authorized = True
