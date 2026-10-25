"""Synthetic tests for the fail-closed price integrity decision."""

from dataclasses import FrozenInstanceError

import pytest

from price_integrity_decision import (
    PriceIntegrityDecision,
    PriceIntegrityRejected,
    assess_price_integrity,
)


def summary(**changes):
    values = {
        "total": 3,
        "MATCH": 3,
        "MISMATCH": 0,
        "MISSING_SOURCE": 0,
        "INVALID_PRICE": 0,
        "price_source_verified": False,
    }
    values.update(changes)
    return values


def test_matching_rows_remain_unverified_and_unauthorized():
    decision = assess_price_integrity(summary())

    assert decision.status == "CONSISTENT_UNVERIFIED"
    assert decision.total == 3
    assert decision.matched == 3
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


def test_empty_dataset_is_blocked():
    decision = assess_price_integrity(
        summary(total=0, MATCH=0)
    )
    assert decision.status == "BLOCKED"
    assert decision.reason == "EMPTY_DATASET"


@pytest.mark.parametrize(
    "field",
    ["MISMATCH", "MISSING_SOURCE", "INVALID_PRICE"],
)
def test_each_quality_failure_blocks(field):
    values = summary(MATCH=2)
    values[field] = 1

    decision = assess_price_integrity(values)

    assert decision.status == "BLOCKED"
    assert decision.reason == "PRICE_OHLCV_INCONSISTENT"
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "changes",
    [
        {"total": 4},
        {"MATCH": -1},
        {"MATCH": True},
        {"MISMATCH": 1.0},
        {"total": "3"},
        {"price_source_verified": True},
        {"price_source_verified": 0},
        {"weekend_rows": -1},
        {"weekend_rows": 4},
        {"weekend_rows": True},
    ],
)
def test_invalid_or_escalated_summary_is_rejected(changes):
    with pytest.raises(PriceIntegrityRejected):
        assess_price_integrity(summary(**changes))


@pytest.mark.parametrize(
    "value",
    [None, (), [], "invalid", 3],
)
def test_invalid_summary_type_is_rejected(value):
    with pytest.raises(PriceIntegrityRejected):
        assess_price_integrity(value)


def test_missing_required_field_is_rejected():
    values = summary()
    del values["MATCH"]

    with pytest.raises(PriceIntegrityRejected):
        assess_price_integrity(values)


def test_valid_weekend_count_does_not_authorize():
    decision = assess_price_integrity(
        summary(weekend_rows=1)
    )
    assert decision.status == "CONSISTENT_UNVERIFIED"
    assert decision.persistence_authorized is False


def test_decision_is_immutable():
    decision = assess_price_integrity(summary())

    assert isinstance(decision, PriceIntegrityDecision)

    with pytest.raises(FrozenInstanceError):
        decision.persistence_authorized = True


def test_input_summary_is_not_modified():
    values = summary()
    original = dict(values)

    assess_price_integrity(values)

    assert values == original
