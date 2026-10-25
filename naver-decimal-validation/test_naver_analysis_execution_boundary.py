"""Executable fail-closed contract tests; no operational imports or DB."""

from dataclasses import replace

import pytest

from core.naver_raw_observation import prepare_naver_raw_observation
from core.naver_analysis_boundary import assess_naver_analysis_observation
from core.naver_analysis_response import build_naver_analysis_response
from core.price_provenance_gate import (
    PriceProvenanceRejected,
    assess_price_provenance,
    require_analysis_authorization,
)


RAW_ROW = "20260916|9680|9715|9621|9676|252142"


def test_unverified_observation_cannot_enter_analysis():
    observation = prepare_naver_raw_observation("069500", RAW_ROW)
    decision = assess_naver_analysis_observation(observation)

    assert decision.status == "BLOCKED"
    assert decision.analysis_authorized is False
    assert decision.dashboard_authorized is False
    assert decision.persistence_authorized is False

    provenance = assess_price_provenance(
        provider=observation.provider,
        adjustment=observation.adjustment,
    )

    with pytest.raises(PriceProvenanceRejected):
        require_analysis_authorization(provenance)


@pytest.mark.parametrize(
    "field",
    [
        "analysis_authorized",
        "dashboard_authorized",
        "persistence_authorized",
    ],
)
def test_forged_approval_cannot_reach_response(field):
    observation = prepare_naver_raw_observation("069500", RAW_ROW)
    decision = assess_naver_analysis_observation(observation)
    forged = replace(decision, **{field: True})

    with pytest.raises(ValueError):
        build_naver_analysis_response(forged)


def test_blocked_response_never_exposes_prices_or_scores():
    observation = prepare_naver_raw_observation("069500", RAW_ROW)
    decision = assess_naver_analysis_observation(observation)
    response = build_naver_analysis_response(decision)

    assert response["status"] == "BLOCKED"
    assert response["analysis_authorized"] is False

    forbidden = {
        "open", "high", "low", "close", "volume",
        "price", "final_score", "ranking",
        "portfolio", "market_regime", "market_strategy",
    }

    assert forbidden.isdisjoint(response)
