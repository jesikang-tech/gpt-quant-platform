"""Synthetic K21 execution authorization denial tests."""
from dataclasses import FrozenInstanceError, replace

import pytest

from price_provider_validation.provider_certification_acceptance import (
    ProviderCertificationRequirements,
    assess_provider_certification_requirements,
)
from price_provider_validation.provider_license_purpose import (
    ProviderLicenseRequirements,
    assess_provider_license_purpose,
)
from price_provider_validation.provider_usage_policy import UsagePurpose
from price_provider_validation.provider_execution_authorization import (
    ProviderExecutionRejected,
    assess_provider_execution_authorization,
    invoke_provider_execution,
)


def _inputs(provider="KIWOOM"):
    certification = assess_provider_certification_requirements(
        ProviderCertificationRequirements(
            provider=provider,
            source_evidence_present=True,
            raw_binding_present=True,
            adjustment_evidence_present=True,
            calendar_evidence_present=True,
            quality_evidence_present=True,
            licensing_evidence_present=True,
        )
    )
    license_decision = assess_provider_license_purpose(
        ProviderLicenseRequirements(
            provider=provider,
            purpose=UsagePurpose.PERSONAL_OWN_ASSET,
            official_terms_present=True,
            license_document_present=True,
            provider_identity_bound=True,
            purpose_scope_documented=True,
            redistribution_scope_documented=True,
            commercial_scope_documented=True,
            official_reply_reviewed=True,
        )
    )
    return certification, license_decision


def _assert_denied(decision):
    assert decision.status == "DENIED"
    for name in (
        "independently_verified",
        "api_execution_authorized",
        "analysis_authorized",
        "dashboard_authorized",
        "snapshot_authorized",
        "persistence_authorized",
        "redistribution_authorized",
        "database_rebuild_authorized",
        "live_api_execution_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(decision, name) is False


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_all_declared_requirements_still_denied(provider):
    certification, license_decision = _inputs(provider)
    decision = assess_provider_execution_authorization(
        certification, license_decision
    )
    assert decision.provider == provider
    assert decision.certification_status == "DENIED"
    assert decision.license_status == "DENIED"
    _assert_denied(decision)


def test_mismatched_provider_rejected():
    certification, _ = _inputs("KIS")
    _, license_decision = _inputs("KIWOOM")
    with pytest.raises(ProviderExecutionRejected):
        assess_provider_execution_authorization(
            certification, license_decision
        )


@pytest.mark.parametrize(
    "field",
    [
        "independently_verified",
        "analysis_authorized",
        "dashboard_authorized",
        "snapshot_authorized",
        "persistence_authorized",
        "database_rebuild_authorized",
        "live_api_execution_authorized",
        "broker_execution_authorized",
    ],
)
def test_forged_certification_rejected(field):
    certification, license_decision = _inputs()
    object.__setattr__(certification, field, True)
    with pytest.raises(ProviderExecutionRejected):
        assess_provider_execution_authorization(
            certification, license_decision
        )


@pytest.mark.parametrize(
    "field",
    [
        "independently_verified",
        "license_verified",
        "api_execution_authorized",
        "analysis_authorized",
        "dashboard_authorized",
        "snapshot_authorized",
        "persistence_authorized",
        "redistribution_authorized",
        "commercial_use_authorized",
        "database_rebuild_authorized",
        "broker_execution_authorized",
    ],
)
def test_forged_license_rejected(field):
    certification, license_decision = _inputs()
    object.__setattr__(license_decision, field, True)
    with pytest.raises(ProviderExecutionRejected):
        assess_provider_execution_authorization(
            certification, license_decision
        )


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_execution_callback_never_called(provider):
    certification, license_decision = _inputs(provider)
    decision = assess_provider_execution_authorization(
        certification, license_decision
    )
    calls = []

    def callback():
        calls.append("EXECUTED")

    with pytest.raises(ProviderExecutionRejected):
        invoke_provider_execution(decision, callback)
    assert calls == []


@pytest.mark.parametrize(
    "field",
    [
        "independently_verified",
        "api_execution_authorized",
        "analysis_authorized",
        "dashboard_authorized",
        "snapshot_authorized",
        "persistence_authorized",
        "redistribution_authorized",
        "database_rebuild_authorized",
        "live_api_execution_authorized",
        "broker_execution_authorized",
    ],
)
def test_forged_execution_decision_rejected(field):
    certification, license_decision = _inputs()
    decision = assess_provider_execution_authorization(
        certification, license_decision
    )
    object.__setattr__(decision, field, True)
    with pytest.raises(ProviderExecutionRejected):
        invoke_provider_execution(decision, lambda: None)


def test_invalid_callback_rejected():
    certification, license_decision = _inputs()
    decision = assess_provider_execution_authorization(
        certification, license_decision
    )
    with pytest.raises(ProviderExecutionRejected):
        invoke_provider_execution(decision, None)


def test_result_immutable():
    certification, license_decision = _inputs()
    decision = assess_provider_execution_authorization(
        certification, license_decision
    )
    with pytest.raises(FrozenInstanceError):
        decision.analysis_authorized = True


@pytest.mark.parametrize("invalid", [None, object(), "DENIED"])
def test_invalid_decision_type_rejected(invalid):
    with pytest.raises(ProviderExecutionRejected):
        invoke_provider_execution(invalid, lambda: None)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_repeated_execution_denial_never_invokes_callback(provider):
    certification, license_decision = _inputs(provider)
    decision = assess_provider_execution_authorization(
        certification, license_decision
    )
    calls = []

    def callback():
        calls.append("EXECUTED")

    for _ in range(3):
        with pytest.raises(ProviderExecutionRejected):
            invoke_provider_execution(decision, callback)

    assert calls == []
