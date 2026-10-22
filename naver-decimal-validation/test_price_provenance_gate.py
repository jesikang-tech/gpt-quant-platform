from dataclasses import FrozenInstanceError, replace

import pytest

from core.price_provenance_gate import (
    PriceProvenanceDecision,
    PriceProvenanceRejected,
    assess_price_provenance,
    require_analysis_authorization,
)


@pytest.mark.parametrize(
    "provider,adjustment",
    [
        ("NAVER", "UNKNOWN"),
        ("NAVER", "ADJUSTED"),
        ("NAVER", "UNADJUSTED"),
        ("FDR", "UNKNOWN"),
        (None, None),
        ("UNIDENTIFIED", "UNIDENTIFIED"),
    ],
)
def test_unverified_price_is_always_blocked(provider, adjustment):
    decision = assess_price_provenance(
        provider=provider,
        adjustment=adjustment,
    )
    assert decision.status == "BLOCKED"
    assert decision.reason == "PRICE_PROVENANCE_NOT_ESTABLISHED"
    assert decision.analysis_authorized is False
    assert decision.portfolio_authorized is False
    assert decision.dashboard_authorized is False
    assert decision.snapshot_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "provider,adjustment",
    [
        (True, "UNKNOWN"),
        (123, "UNKNOWN"),
        ("NAVER", True),
        ("NAVER", 123),
    ],
)
def test_invalid_claim_types_are_rejected(provider, adjustment):
    with pytest.raises(PriceProvenanceRejected):
        assess_price_provenance(
            provider=provider,
            adjustment=adjustment,
        )


def test_analysis_requires_verified_evidence():
    decision = assess_price_provenance(
        provider="NAVER",
        adjustment="UNKNOWN",
    )
    with pytest.raises(PriceProvenanceRejected):
        require_analysis_authorization(decision)


def test_forged_authorization_is_not_accepted():
    decision = replace(
        PriceProvenanceDecision(),
        analysis_authorized=True,
    )
    with pytest.raises(PriceProvenanceRejected):
        require_analysis_authorization(decision)


def test_arbitrary_mapping_cannot_authorize():
    with pytest.raises(PriceProvenanceRejected):
        require_analysis_authorization(
            {"analysis_authorized": True}
        )


def test_decision_is_immutable():
    decision = PriceProvenanceDecision()
    with pytest.raises(FrozenInstanceError):
        decision.status = "APPROVED"
