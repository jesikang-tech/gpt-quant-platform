"""Synthetic API response safety tests."""

from dataclasses import replace

import pytest

from core.naver_raw_observation import prepare_naver_raw_observation
from core.naver_analysis_boundary import assess_naver_analysis_observation
from core.naver_analysis_response import (
    NaverAnalysisResponseRejected,
    build_naver_analysis_response,
)


RAW_ROW = "20260916|9680|9715|9621|9676|252142"


def make_decision():
    observation = prepare_naver_raw_observation("069500", RAW_ROW)
    return assess_naver_analysis_observation(observation)


def test_blocked_response_contract():
    response = build_naver_analysis_response(make_decision())
    assert response["status"] == "BLOCKED"
    assert response["reason"] == "UNVERIFIED_ADJUSTMENT_AND_PROVENANCE"
    assert response["provider"] == "NAVER"


def test_all_authorizations_are_false():
    response = build_naver_analysis_response(make_decision())
    assert response["analysis_authorized"] is False
    assert response["dashboard_authorized"] is False
    assert response["persistence_authorized"] is False


def test_identity_is_preserved():
    response = build_naver_analysis_response(make_decision())
    assert response["ticker"] == "069500"
    assert response["observation_date"] == "2026-09-16"


def test_no_price_or_investment_fields():
    response = build_naver_analysis_response(make_decision())
    forbidden = {
        "open", "high", "low", "close", "volume",
        "price", "final_score", "ranking",
        "portfolio", "market_regime", "market_strategy",
    }
    assert forbidden.isdisjoint(response)


@pytest.mark.parametrize("invalid", [None, {}, [], "BLOCKED", 123])
def test_invalid_decision_rejected(invalid):
    with pytest.raises(
        NaverAnalysisResponseRejected,
        match="INVALID_DECISION",
    ):
        build_naver_analysis_response(invalid)


@pytest.mark.parametrize(
    "changes",
    [
        {"status": "AUTHORIZED"},
        {"analysis_authorized": True},
        {"dashboard_authorized": True},
        {"persistence_authorized": True},
        {"provider": "OTHER"},
        {"reason": "VERIFIED"},
    ],
)
def test_unauthorized_promotion_rejected(changes):
    decision = replace(make_decision(), **changes)
    with pytest.raises(
        NaverAnalysisResponseRejected,
        match="UNEXPECTED_ANALYSIS_AUTHORIZATION",
    ):
        build_naver_analysis_response(decision)
