"""Synthetic contract tests for the read-only quality decision adapter."""

import pytest

from price_integrity_decision import PriceIntegrityRejected
from price_quality_decision_adapter import (
    assess_daily_quality_summary,
    assess_overall_quality_summary,
)


def quality_summary(**changes):
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


def test_overall_matching_rows_remain_unauthorized():
    decision = assess_overall_quality_summary(
        quality_summary(weekend_rows=0)
    )
    assert decision.status == "CONSISTENT_UNVERIFIED"
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


def test_daily_matching_rows_remain_unauthorized():
    decision = assess_daily_quality_summary(
        quality_summary(date="2026-09-16")
    )
    assert decision.status == "CONSISTENT_UNVERIFIED"
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "field", ["MISMATCH", "MISSING_SOURCE", "INVALID_PRICE"]
)
def test_overall_quality_failure_blocks(field):
    values = quality_summary(MATCH=2, weekend_rows=0)
    values[field] = 1
    decision = assess_overall_quality_summary(values)
    assert decision.status == "BLOCKED"
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "field", ["MISMATCH", "MISSING_SOURCE", "INVALID_PRICE"]
)
def test_daily_quality_failure_blocks(field):
    values = quality_summary(MATCH=2, date="2026-09-16")
    values[field] = 1
    decision = assess_daily_quality_summary(values)
    assert decision.status == "BLOCKED"
    assert decision.analysis_authorized is False


def test_overall_requires_weekend_count():
    with pytest.raises(PriceIntegrityRejected):
        assess_overall_quality_summary(quality_summary())


@pytest.mark.parametrize("weekends", [-1, 4, True, "0"])
def test_overall_rejects_invalid_weekend_count(weekends):
    with pytest.raises(PriceIntegrityRejected):
        assess_overall_quality_summary(
            quality_summary(weekend_rows=weekends)
        )


@pytest.mark.parametrize("day", [None, "", 20260916, False])
def test_daily_rejects_missing_or_invalid_date(day):
    with pytest.raises(PriceIntegrityRejected):
        assess_daily_quality_summary(
            quality_summary(date=day)
        )


@pytest.mark.parametrize("verified", [True, 1, "verified"])
def test_source_verification_escalation_is_rejected(verified):
    with pytest.raises(PriceIntegrityRejected):
        assess_daily_quality_summary(
            quality_summary(
                date="2026-09-16",
                price_source_verified=verified,
            )
        )


def test_empty_overall_dataset_is_blocked():
    decision = assess_overall_quality_summary(
        quality_summary(total=0, MATCH=0, weekend_rows=0)
    )
    assert decision.status == "BLOCKED"
    assert decision.reason == "EMPTY_DATASET"


def test_empty_daily_dataset_is_blocked():
    decision = assess_daily_quality_summary(
        quality_summary(total=0, MATCH=0, date="2026-09-16")
    )
    assert decision.status == "BLOCKED"
    assert decision.reason == "EMPTY_DATASET"


def test_adapters_do_not_mutate_input():
    overall = quality_summary(weekend_rows=0)
    daily = quality_summary(date="2026-09-16")
    original_overall = dict(overall)
    original_daily = dict(daily)

    assess_overall_quality_summary(overall)
    assess_daily_quality_summary(daily)

    assert overall == original_overall
    assert daily == original_daily


@pytest.mark.parametrize("value", [None, [], (), "invalid", 3])
def test_adapters_reject_non_mapping_input(value):
    with pytest.raises(PriceIntegrityRejected):
        assess_overall_quality_summary(value)
    with pytest.raises(PriceIntegrityRejected):
        assess_daily_quality_summary(value)
