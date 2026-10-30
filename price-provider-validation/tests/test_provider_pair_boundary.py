"""Offline fail-first tests for cross-provider comparison and denial."""

from dataclasses import replace

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
    prepare_raw_observation,
)
from price_provider_validation.provider_pair_boundary import (
    ProviderPairDecision,
    assess_provider_pair,
)


FIELDS = ("100", "110", "90", "105", "1000")


def _observation(provider, ticker="005930", day="2026-10-28", fields=FIELDS):
    return prepare_raw_observation(provider, ticker, day, fields)


def _assert_denied(decision):
    assert type(decision) is ProviderPairDecision
    assert decision.analysis_authorized is False
    assert decision.dashboard_authorized is False
    assert decision.snapshot_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "kis,kiwoom",
    [
        (None, None),
        (None, _observation("KIWOOM")),
        (_observation("KIS"), None),
    ],
)
def test_missing_observation_denied(kis, kiwoom):
    decision = assess_provider_pair(kis, kiwoom)
    assert decision.status == "MISSING"
    _assert_denied(decision)


@pytest.mark.parametrize(
    "changes",
    [
        {"ticker": "000660"},
        {"day": "2026-10-27"},
    ],
)
def test_identity_mismatch_denied(changes):
    decision = assess_provider_pair(
        _observation("KIS"),
        _observation("KIWOOM", **changes),
    )
    assert decision.status == "IDENTITY_MISMATCH"
    _assert_denied(decision)


@pytest.mark.parametrize("index", range(5))
def test_each_raw_field_mismatch_denied(index):
    changed = list(FIELDS)
    changed[index] = "999"

    decision = assess_provider_pair(
        _observation("KIS"),
        _observation("KIWOOM", fields=tuple(changed)),
    )

    assert decision.status == "PRICE_MISMATCH"
    _assert_denied(decision)


def test_identical_raw_fields_remain_unverified():
    decision = assess_provider_pair(
        _observation("KIS"),
        _observation("KIWOOM"),
    )
    assert decision.status == "MATCHED_UNVERIFIED"
    _assert_denied(decision)


@pytest.mark.parametrize(
    "kis,kiwoom",
    [
        (_observation("KIWOOM"), _observation("KIS")),
        (object(), _observation("KIWOOM")),
        (_observation("KIS"), object()),
        (_observation("KIS"), _observation("KIS")),
        (_observation("KIWOOM"), _observation("KIWOOM")),
    ],
)
def test_wrong_provider_or_type_rejected(kis, kiwoom):
    with pytest.raises(ProviderObservationRejected):
        assess_provider_pair(kis, kiwoom)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_adjustment_escalation_rejected(provider):
    changed = replace(
        _observation(provider),
        adjustment="ADJUSTED",
    )

    kis = changed if provider == "KIS" else _observation("KIS")
    kiwoom = changed if provider == "KIWOOM" else _observation("KIWOOM")

    with pytest.raises(ProviderObservationRejected):
        assess_provider_pair(kis, kiwoom)


@pytest.mark.parametrize(
    "kis,kiwoom",
    [
        (None, object()),
        (object(), None),
        (None, _observation("KIS")),
        (_observation("KIWOOM"), None),
    ],
)
def test_invalid_input_not_masked_by_missing_input(kis, kiwoom):
    with pytest.raises(ProviderObservationRejected):
        assess_provider_pair(kis, kiwoom)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_invalid_raw_field_shape_rejected(provider):
    changed = replace(
        _observation(provider),
        raw_fields=("100",),
    )

    kis = changed if provider == "KIS" else _observation("KIS")
    kiwoom = changed if provider == "KIWOOM" else _observation("KIWOOM")

    with pytest.raises(ProviderObservationRejected):
        assess_provider_pair(kis, kiwoom)


def test_pair_decision_has_no_source_selection_or_fallback():
    decision = assess_provider_pair(
        _observation("KIS"),
        _observation("KIWOOM"),
    )

    assert not hasattr(decision, "selected_provider")
    assert not hasattr(decision, "fallback_provider")
    assert not hasattr(decision, "preferred_provider")
    _assert_denied(decision)

@pytest.mark.parametrize(
    "changes",
    [
        {"ticker": ""},
        {"ticker": " 005930"},
        {"ticker": "005930 "},
        {"observation_date": ""},
        {"observation_date": "2026-02-30"},
        {"observation_date": "20261028"},
        {"observation_date": "2026-10-28 "},
    ],
)
@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_mutated_observation_identity_rejected(provider, changes):
    changed = replace(_observation(provider), **changes)
    kis = changed if provider == "KIS" else _observation("KIS")
    kiwoom = changed if provider == "KIWOOM" else _observation("KIWOOM")

    with pytest.raises(ProviderObservationRejected):
        assess_provider_pair(kis, kiwoom)


@pytest.mark.parametrize(
    "changes",
    [
        {"ticker": ""},
        {"observation_date": "2026-02-30"},
    ],
)
@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_mutated_observation_rejected_even_if_other_missing(provider, changes):
    changed = replace(_observation(provider), **changes)
    kis = changed if provider == "KIS" else None
    kiwoom = changed if provider == "KIWOOM" else None

    with pytest.raises(ProviderObservationRejected):
        assess_provider_pair(kis, kiwoom)
