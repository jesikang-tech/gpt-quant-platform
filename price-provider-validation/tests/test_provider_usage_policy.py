"""Offline tests for fail-closed provider usage-purpose classification."""

import pytest

from price_provider_validation.provider_usage_policy import (
    UsagePurpose,
    assess_provider_usage,
)


def test_personal_purpose_requires_reviewed_reply():
    denied = assess_provider_usage(
        "KIWOOM", UsagePurpose.PERSONAL_OWN_ASSET
    )
    reviewed = assess_provider_usage(
        "KIWOOM",
        UsagePurpose.PERSONAL_OWN_ASSET,
        official_reply_reviewed=True,
    )
    assert denied.purpose_within_reported_scope is False
    assert reviewed.purpose_within_reported_scope is True


@pytest.mark.parametrize(
    "purpose",
    [
        UsagePurpose.THIRD_PARTY_DISTRIBUTION,
        UsagePurpose.COMMERCIAL_SERVICE,
    ],
)
def test_redistribution_and_commercial_use_remain_denied(purpose):
    result = assess_provider_usage(
        "KIWOOM", purpose, official_reply_reviewed=True
    )
    assert result.purpose_within_reported_scope is False


def test_purpose_scope_never_grants_operational_authority():
    result = assess_provider_usage(
        "KIWOOM",
        UsagePurpose.PERSONAL_OWN_ASSET,
        official_reply_reviewed=True,
    )
    assert result.independently_verified is False
    assert result.api_execution_authorized is False
    assert result.analysis_authorized is False
    assert result.persistence_authorized is False
    assert result.redistribution_authorized is False
    assert result.database_rebuild_authorized is False


@pytest.mark.parametrize("provider", ["KIS", "NAVER", "", None])
def test_other_providers_require_independent_review(provider):
    with pytest.raises(ValueError):
        assess_provider_usage(
            provider,
            UsagePurpose.PERSONAL_OWN_ASSET,
            official_reply_reviewed=True,
        )


@pytest.mark.parametrize("invalid", ["PERSONAL_OWN_ASSET", None, True])
def test_untyped_purpose_is_rejected(invalid):
    with pytest.raises(TypeError):
        assess_provider_usage(
            "KIWOOM", invalid, official_reply_reviewed=True
        )


@pytest.mark.parametrize("invalid", [1, "true", None])
def test_untyped_reply_review_is_rejected(invalid):
    with pytest.raises(TypeError):
        assess_provider_usage(
            "KIWOOM",
            UsagePurpose.PERSONAL_OWN_ASSET,
            official_reply_reviewed=invalid,
        )
