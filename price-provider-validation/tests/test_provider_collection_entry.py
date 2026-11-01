"""Synthetic tests for the fail-closed collection entry."""

from dataclasses import replace

import pytest

from price_provider_validation.provider_collection_entry import (
    invoke_provider_collection,
)
from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)
from price_provider_validation.provider_usage_policy import (
    UsageAssessment,
    UsagePurpose,
    assess_provider_usage,
)


def _usage():
    return assess_provider_usage(
        "KIWOOM",
        UsagePurpose.PERSONAL_OWN_ASSET,
        official_reply_reviewed=True,
    )


def _assert_denied_without_callback(usage):
    calls = []

    def collect_callback():
        calls.append("EXECUTED")
        return "UNSAFE"

    with pytest.raises(ProviderObservationRejected):
        invoke_provider_collection(usage, collect_callback)

    assert calls == []


def test_personal_usage_scope_does_not_grant_collection():
    usage = _usage()

    assert usage.purpose_within_reported_scope is True
    assert usage.api_execution_authorized is False
    _assert_denied_without_callback(usage)


@pytest.mark.parametrize(
    "purpose",
    [
        UsagePurpose.PERSONAL_OWN_ASSET,
        UsagePurpose.THIRD_PARTY_DISTRIBUTION,
        UsagePurpose.COMMERCIAL_SERVICE,
    ],
)
def test_all_usage_purposes_denied(purpose):
    usage = assess_provider_usage(
        "KIWOOM", purpose, official_reply_reviewed=True
    )
    _assert_denied_without_callback(usage)


@pytest.mark.parametrize(
    "field,value",
    [
        ("independently_verified", True),
        ("api_execution_authorized", True),
        ("analysis_authorized", True),
        ("persistence_authorized", True),
        ("redistribution_authorized", True),
        ("database_rebuild_authorized", True),
    ],
)
def test_forged_authority_rejected(field, value):
    usage = replace(_usage(), **{field: value})
    _assert_denied_without_callback(usage)


@pytest.mark.parametrize(
    "field,value",
    [
        ("provider", "KIS"),
        ("purpose", "PERSONAL_OWN_ASSET"),
        ("purpose_within_reported_scope", "True"),
    ],
)
def test_invalid_usage_identity_rejected(field, value):
    usage = replace(_usage(), **{field: value})
    _assert_denied_without_callback(usage)


@pytest.mark.parametrize(
    "invalid",
    [
        None,
        object(),
        "KIWOOM",
        {"api_execution_authorized": False},
    ],
)
def test_invalid_usage_types_rejected(invalid):
    _assert_denied_without_callback(invalid)


def test_invalid_callback_rejected():
    with pytest.raises(
        ProviderObservationRejected,
        match="Invalid collection callback",
    ):
        invoke_provider_collection(_usage(), None)


def test_direct_forged_usage_assessment_denied():
    usage = UsageAssessment(
        provider="KIWOOM",
        purpose=UsagePurpose.PERSONAL_OWN_ASSET,
        purpose_within_reported_scope=True,
        api_execution_authorized=True,
    )
    _assert_denied_without_callback(usage)
