"""Synthetic regression tests for the provider analysis denial boundary."""

from dataclasses import replace

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
    prepare_raw_observation,
)
from price_provider_validation.provider_evidence import ProviderEvidenceDecision
from price_provider_validation.trading_day_certification import (
    TradingDayCertificationDecision,
)
from price_provider_validation.provider_analysis_boundary import (
    assess_provider_analysis_boundary,
)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_valid_structural_provider_still_denied(provider):
    observation = prepare_raw_observation(
        provider, "005930", "2026-10-29",
        ("100", "110", "90", "105", "1000"),
    )
    evidence = ProviderEvidenceDecision(
        reason="INDEPENDENT_PROVIDER_PROVENANCE_NOT_VERIFIED"
    )
    trading_day = TradingDayCertificationDecision(
        structural_status="CANDIDATE",
        structural_reason="STRUCTURALLY_VALID_UNVERIFIED",
        structural_trading_day_eligible=True,
    )

    decision = assess_provider_analysis_boundary(
        observation, evidence, trading_day
    )

    assert decision.provider == provider
    assert decision.ticker == "005930"
    assert decision.observation_date == "2026-10-29"
    assert decision.status == "BLOCKED"
    assert decision.analysis_authorized is False
    assert decision.dashboard_authorized is False
    assert decision.snapshot_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("status", "VERIFIED"),
        ("independently_verified", True),
        ("analysis_authorized", True),
        ("persistence_authorized", True),
    ],
)
def test_forged_evidence_authority_rejected(field, value):
    observation = prepare_raw_observation(
        "KIS", "005930", "2026-10-29",
        ("100", "110", "90", "105", "1000"),
    )
    evidence = replace(
        ProviderEvidenceDecision(reason="UNVERIFIED"),
        **{field: value},
    )
    trading_day = TradingDayCertificationDecision(
        "CANDIDATE", "STRUCTURALLY_VALID_UNVERIFIED", True
    )

    with pytest.raises(ProviderObservationRejected):
        assess_provider_analysis_boundary(observation, evidence, trading_day)


@pytest.mark.parametrize(
    "field,value",
    [
        ("status", "VERIFIED"),
        ("official_trading_day_verified", True),
        ("analysis_authorized", True),
        ("persistence_authorized", True),
    ],
)
def test_forged_trading_day_authority_rejected(field, value):
    observation = prepare_raw_observation(
        "KIWOOM", "005930", "2026-10-29",
        ("100", "110", "90", "105", "1000"),
    )
    evidence = ProviderEvidenceDecision(reason="UNVERIFIED")
    trading_day = replace(
        TradingDayCertificationDecision(
            "CANDIDATE", "STRUCTURALLY_VALID_UNVERIFIED", True
        ),
        **{field: value},
    )

    with pytest.raises(ProviderObservationRejected):
        assess_provider_analysis_boundary(observation, evidence, trading_day)


@pytest.mark.parametrize(
    "invalid_index",
    [0, 1, 2],
)
def test_invalid_input_types_rejected(invalid_index):
    values = [
        prepare_raw_observation(
            "KIS", "005930", "2026-10-29",
            ("100", "110", "90", "105", "1000"),
        ),
        ProviderEvidenceDecision(reason="UNVERIFIED"),
        TradingDayCertificationDecision(
            "CANDIDATE", "STRUCTURALLY_VALID_UNVERIFIED", True
        ),
    ]
    values[invalid_index] = object()

    with pytest.raises(ProviderObservationRejected):
        assess_provider_analysis_boundary(*values)


def test_adjustment_escalation_rejected():
    observation = replace(
        prepare_raw_observation(
            "KIS", "005930", "2026-10-29",
            ("100", "110", "90", "105", "1000"),
        ),
        adjustment="ADJUSTED",
    )
    evidence = ProviderEvidenceDecision(reason="UNVERIFIED")
    trading_day = TradingDayCertificationDecision(
        "CANDIDATE", "STRUCTURALLY_VALID_UNVERIFIED", True
    )

    with pytest.raises(ProviderObservationRejected):
        assess_provider_analysis_boundary(
            observation, evidence, trading_day
        )
