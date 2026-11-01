"""Synthetic K20 provider license and purpose boundary tests."""
from dataclasses import FrozenInstanceError, replace

import pytest

from price_provider_validation.provider_usage_policy import UsagePurpose
from price_provider_validation.provider_license_purpose import (
    ProviderLicenseRejected,
    ProviderLicenseRequirements,
    assess_provider_license_purpose,
)


def _requirements(provider="KIWOOM",
                  purpose=UsagePurpose.PERSONAL_OWN_ASSET,
                  **changes):
    values = dict(
        provider=provider,
        purpose=purpose,
        official_terms_present=False,
        license_document_present=False,
        provider_identity_bound=False,
        purpose_scope_documented=False,
        redistribution_scope_documented=False,
        commercial_scope_documented=False,
        official_reply_reviewed=False,
    )
    values.update(changes)
    return ProviderLicenseRequirements(**values)


def _assert_denied(result):
    assert result.status == "DENIED"
    assert result.license_verified is False
    for name in (
        "independently_verified",
        "api_execution_authorized",
        "analysis_authorized",
        "dashboard_authorized",
        "snapshot_authorized",
        "persistence_authorized",
        "redistribution_authorized",
        "commercial_use_authorized",
        "database_rebuild_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(result, name) is False


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
@pytest.mark.parametrize("purpose", list(UsagePurpose))
def test_missing_license_evidence_denied(provider, purpose):
    result = assess_provider_license_purpose(
        _requirements(provider, purpose)
    )
    assert len(result.missing_requirements) == 6
    assert result.reported_personal_scope is False
    _assert_denied(result)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
@pytest.mark.parametrize("purpose", list(UsagePurpose))
def test_all_caller_flags_true_still_denied(provider, purpose):
    result = assess_provider_license_purpose(
        _requirements(
            provider,
            purpose,
            official_terms_present=True,
            license_document_present=True,
            provider_identity_bound=True,
            purpose_scope_documented=True,
            redistribution_scope_documented=True,
            commercial_scope_documented=True,
            official_reply_reviewed=True,
        )
    )
    assert result.missing_requirements == ()
    _assert_denied(result)


def test_kiwoom_personal_scope_is_not_legal_authorization():
    result = assess_provider_license_purpose(
        _requirements(
            "KIWOOM",
            UsagePurpose.PERSONAL_OWN_ASSET,
            official_reply_reviewed=True,
        )
    )
    assert result.reported_personal_scope is True
    _assert_denied(result)


def test_kis_requires_independent_scope_review():
    result = assess_provider_license_purpose(
        _requirements(
            "KIS",
            UsagePurpose.PERSONAL_OWN_ASSET,
            official_reply_reviewed=True,
        )
    )
    assert result.reported_personal_scope is False
    _assert_denied(result)


@pytest.mark.parametrize(
    "purpose",
    [
        UsagePurpose.THIRD_PARTY_DISTRIBUTION,
        UsagePurpose.COMMERCIAL_SERVICE,
    ],
)
def test_kiwoom_nonpersonal_purpose_remains_denied(purpose):
    result = assess_provider_license_purpose(
        _requirements(
            "KIWOOM",
            purpose,
            official_reply_reviewed=True,
        )
    )
    assert result.reported_personal_scope is False
    _assert_denied(result)


@pytest.mark.parametrize("provider", ["NAVER", "", None])
def test_unsupported_provider_rejected(provider):
    with pytest.raises(ProviderLicenseRejected):
        assess_provider_license_purpose(
            _requirements(provider=provider)
        )


@pytest.mark.parametrize("purpose", ["PERSONAL_OWN_ASSET", None, True])
def test_untyped_purpose_rejected(purpose):
    with pytest.raises(ProviderLicenseRejected):
        assess_provider_license_purpose(
            _requirements(purpose=purpose)
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "official_terms_present",
        "license_document_present",
        "provider_identity_bound",
        "purpose_scope_documented",
        "redistribution_scope_documented",
        "commercial_scope_documented",
        "official_reply_reviewed",
    ],
)
def test_invalid_boolean_declaration_rejected(field_name):
    requirements = replace(
        _requirements(),
        **{field_name: "true"},
    )
    with pytest.raises(ProviderLicenseRejected):
        assess_provider_license_purpose(requirements)


def test_result_is_immutable():
    result = assess_provider_license_purpose(_requirements())
    with pytest.raises(FrozenInstanceError):
        result.analysis_authorized = True
