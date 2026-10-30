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
    evidence = ProviderEvidenceDecision(reason="UNVERIFIED")
    object.__setattr__(evidence, field, value)
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
@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_analysis_callback_never_executed(provider):
    from core.price_provenance_gate import PriceProvenanceRejected
    from price_provider_validation.provider_analysis_boundary import (
        invoke_provider_analysis,
    )

    observation = prepare_raw_observation(
        provider, "005930", "2026-10-29",
        ("100", "110", "90", "105", "1000"),
    )
    decision = assess_provider_analysis_boundary(
        observation,
        ProviderEvidenceDecision(reason="UNVERIFIED"),
        TradingDayCertificationDecision(
            "CANDIDATE", "STRUCTURALLY_VALID_UNVERIFIED", True
        ),
    )

    calls = []

    def callback():
        calls.append("EXECUTED")
        return "UNSAFE"

    with pytest.raises(PriceProvenanceRejected):
        invoke_provider_analysis(decision, callback)

    assert calls == []


@pytest.mark.parametrize(
    "field,value",
    [
        ("status", "AUTHORIZED"),
        ("analysis_authorized", True),
        ("dashboard_authorized", True),
        ("snapshot_authorized", True),
        ("persistence_authorized", True),
    ],
)
def test_forged_analysis_boundary_rejected(field, value):
    from price_provider_validation.provider_analysis_boundary import (
        ProviderAnalysisBoundaryDecision,
        invoke_provider_analysis,
    )

    decision = replace(
        ProviderAnalysisBoundaryDecision(
            provider="KIS",
            ticker="005930",
            observation_date="2026-10-29",
            status="BLOCKED",
            reason="UNVERIFIED",
        ),
        **{field: value},
    )

    calls = []

    with pytest.raises(ProviderObservationRejected):
        invoke_provider_analysis(
            decision, lambda: calls.append("EXECUTED")
        )

    assert calls == []


def test_invalid_analysis_decision_rejected():
    from price_provider_validation.provider_analysis_boundary import (
        invoke_provider_analysis,
    )

    with pytest.raises(ProviderObservationRejected):
        invoke_provider_analysis(object(), lambda: None)


def test_invalid_analysis_callback_rejected():
    from price_provider_validation.provider_analysis_boundary import (
        ProviderAnalysisBoundaryDecision,
        invoke_provider_analysis,
    )

    decision = ProviderAnalysisBoundaryDecision(
        provider="KIS",
        ticker="005930",
        observation_date="2026-10-29",
        status="BLOCKED",
        reason="UNVERIFIED",
    )

    with pytest.raises(ProviderObservationRejected):
        invoke_provider_analysis(decision, None)
