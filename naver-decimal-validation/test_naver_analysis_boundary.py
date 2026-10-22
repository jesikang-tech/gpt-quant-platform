"""Synthetic tests for the NAVER analysis safety boundary."""

from dataclasses import replace

import pytest

from core.naver_raw_observation import prepare_naver_raw_observation
from core.naver_analysis_boundary import assess_naver_analysis_observation


RAW_ROW = "20260916|9680|9715|9621|9676|252142"


def make_observation():
    return prepare_naver_raw_observation("069500", RAW_ROW)


def test_unverified_naver_analysis_is_blocked():
    decision = assess_naver_analysis_observation(make_observation())
    assert decision.status == "BLOCKED"
    assert decision.analysis_authorized is False
    assert decision.dashboard_authorized is False
    assert decision.persistence_authorized is False


def test_block_reason_is_explicit():
    decision = assess_naver_analysis_observation(make_observation())
    assert decision.reason == "UNVERIFIED_ADJUSTMENT_AND_PROVENANCE"


def test_observation_identity_is_preserved():
    decision = assess_naver_analysis_observation(make_observation())
    assert decision.provider == "NAVER"
    assert decision.ticker == "069500"
    assert decision.observation_date == "2026-09-16"


@pytest.mark.parametrize("invalid", [None, {}, [], "NAVER", 123])
def test_invalid_observation_is_rejected(invalid):
    with pytest.raises(ValueError, match="INVALID_NAVER_OBSERVATION"):
        assess_naver_analysis_observation(invalid)


@pytest.mark.parametrize(
    "changes",
    [
        {"provider": "OTHER"},
        {"adjustment": "ADJUSTED"},
        {"provenance_verified": True},
        {"persistence_authorized": True},
    ],
)
def test_unexpected_trust_state_is_rejected(changes):
    observation = replace(make_observation(), **changes)
    with pytest.raises(ValueError, match="UNEXPECTED_NAVER_TRUST_STATE"):
        assess_naver_analysis_observation(observation)