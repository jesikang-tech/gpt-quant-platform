"""Offline tests for fail-closed provider persistence entry."""
from dataclasses import replace

import pytest

from core.price_provenance_gate import PriceProvenanceRejected
from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
    prepare_raw_observation,
)
from price_provider_validation.provider_evidence import (
    ProviderEvidenceDecision,
)
from price_provider_validation.provider_persistence_entry import (
    invoke_provider_persistence,
)
from price_provider_validation.provider_usage_policy import (
    UsagePurpose,
    assess_provider_usage,
)
from price_provider_validation.trading_day_certification import (
    TradingDayCertificationDecision,
)


def _observation():
    return prepare_raw_observation(
        provider="KIWOOM",
        ticker="005930",
        observation_date="2026-10-30",
        raw_fields=("+100", "+110", "+90", "+105", "1000"),
    )


def _inputs():
    return {
        "observation": _observation(),
        "usage_decision": assess_provider_usage(
            "KIWOOM",
            UsagePurpose.PERSONAL_OWN_ASSET,
            official_reply_reviewed=True,
        ),
        "evidence_decision": ProviderEvidenceDecision(
            reason="SYNTHETIC_UNVERIFIED"
        ),
        "trading_day_decision": TradingDayCertificationDecision(
            reason="SYNTHETIC_UNVERIFIED"
        ),
    }


def _invoke(**changes):
    values = _inputs()
    values.update(changes)
    calls = []

    def callback():
        calls.append("CALLED")

    try:
        invoke_provider_persistence(
            persist_callback=callback,
            **values,
        )
    finally:
        assert calls == [], "Persistence callback must never execute"


def test_unverified_persistence_rejected_before_callback():
    with pytest.raises(PriceProvenanceRejected):
        _invoke()


@pytest.mark.parametrize(
    "field",
    [
        "independently_verified",
        "api_execution_authorized",
        "analysis_authorized",
        "persistence_authorized",
        "redistribution_authorized",
        "database_rebuild_authorized",
    ],
)
def test_usage_authority_escalation_rejected(field):
    values = _inputs()
    values["usage_decision"] = replace(
        values["usage_decision"], **{field: True}
    )
    with pytest.raises(ProviderObservationRejected):
        _invoke(**values)


@pytest.mark.parametrize(
    "field",
    [
        "independently_verified",
        "analysis_authorized",
        "persistence_authorized",
    ],
)
def test_evidence_authority_escalation_rejected(field):
    values = _inputs()
    object.__setattr__(values["evidence_decision"], field, True)
    with pytest.raises(ProviderObservationRejected):
        _invoke(**values)


@pytest.mark.parametrize(
    "field",
    [
        "official_trading_day_verified",
        "analysis_authorized",
        "persistence_authorized",
    ],
)
def test_trading_day_authority_escalation_rejected(field):
    values = _inputs()
    object.__setattr__(values["trading_day_decision"], field, True)
    with pytest.raises(ProviderObservationRejected):
        _invoke(**values)


@pytest.mark.parametrize(
    "field",
    [
        "observation",
        "usage_decision",
        "evidence_decision",
        "trading_day_decision",
    ],
)
def test_invalid_decision_types_rejected(field):
    with pytest.raises(ProviderObservationRejected):
        _invoke(**{field: object()})


def test_invalid_callback_rejected():
    values = _inputs()
    with pytest.raises(ProviderObservationRejected):
        invoke_provider_persistence(
            persist_callback=None,
            **values,
        )


def test_provider_mismatch_rejected():
    values = _inputs()
    values["usage_decision"] = replace(
        values["usage_decision"], provider="KIS"
    )
    with pytest.raises(ProviderObservationRejected):
        _invoke(**values)


def test_unverified_adjustment_cannot_be_relabelled():
    values = _inputs()
    values["observation"] = replace(
        values["observation"], adjustment="ADJUSTED"
    )
    with pytest.raises(ProviderObservationRejected):
        _invoke(**values)
