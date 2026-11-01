"""K14 offline deny-only certification requirements tests."""
from dataclasses import FrozenInstanceError

import pytest

from price_provider_validation.provider_certification_acceptance import (
    ProviderCertificationAcceptance,
    ProviderCertificationRejected,
    ProviderCertificationRequirements,
    assess_provider_certification_requirements,
)


FIELDS = (
    "source_evidence_present",
    "raw_binding_present",
    "adjustment_evidence_present",
    "calendar_evidence_present",
    "quality_evidence_present",
    "licensing_evidence_present",
)


def make_requirements(provider="KIS", **overrides):
    values = {name: False for name in FIELDS}
    values.update(overrides)
    return ProviderCertificationRequirements(provider=provider, **values)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_missing_all_requirements_remains_denied(provider):
    decision = assess_provider_certification_requirements(
        make_requirements(provider)
    )
    assert type(decision) is ProviderCertificationAcceptance
    assert decision.provider == provider
    assert decision.missing_requirements == FIELDS
    assert decision.status == "DENIED"
    assert decision.independently_verified is False


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_all_declared_requirements_still_never_authorize(provider):
    decision = assess_provider_certification_requirements(
        make_requirements(provider, **{name: True for name in FIELDS})
    )
    assert decision.missing_requirements == ()
    assert decision.status == "DENIED"
    assert decision.reason == "INDEPENDENT_CERTIFICATION_NOT_ESTABLISHED"
    for name in (
        "independently_verified",
        "analysis_authorized",
        "dashboard_authorized",
        "snapshot_authorized",
        "persistence_authorized",
        "database_rebuild_authorized",
        "live_api_execution_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(decision, name) is False


@pytest.mark.parametrize("missing_field", FIELDS)
def test_each_missing_requirement_is_reported(missing_field):
    values = {name: True for name in FIELDS}
    values[missing_field] = False
    decision = assess_provider_certification_requirements(
        make_requirements(**values)
    )
    assert decision.missing_requirements == (missing_field,)
    assert decision.status == "DENIED"


@pytest.mark.parametrize("bad", [None, "KIS", {}, object()])
def test_invalid_input_type_rejected(bad):
    with pytest.raises(ProviderCertificationRejected):
        assess_provider_certification_requirements(bad)


@pytest.mark.parametrize("provider", ["NAVER", "", None, 1, True])
def test_unsupported_provider_rejected(provider):
    with pytest.raises(ProviderCertificationRejected):
        assess_provider_certification_requirements(
            make_requirements(provider)
        )


@pytest.mark.parametrize("bad", [None, 0, 1, "True", [], {}])
def test_non_boolean_requirement_rejected(bad):
    with pytest.raises(ProviderCertificationRejected):
        assess_provider_certification_requirements(
            make_requirements(source_evidence_present=bad)
        )


def test_decision_is_immutable():
    decision = assess_provider_certification_requirements(
        make_requirements()
    )
    with pytest.raises(FrozenInstanceError):
        decision.analysis_authorized = True
