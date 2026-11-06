"""Synthetic tests for the Ver1.1 Kiwoom reference policy."""

from dataclasses import FrozenInstanceError

import pytest

from price_provider_validation.kiwoom_price_reference_policy import (
    assess_kiwoom_price_reference_policy,
)


def test_reference_policy_adopts_kiwoom_for_ver11():
    decision = assess_kiwoom_price_reference_policy()
    assert decision.provider == "KIWOOM"
    assert decision.platform_version == "1.1"
    assert decision.reference_policy == "OFFICIAL_REST_API"
    assert decision.personal_scope_reported is True
    assert decision.ka10086_price_basis == "ORIGINAL_PRICE_REPORTED"
    assert decision.ka10081_price_basis == "API_GUIDE_REVIEW_REQUIRED"
    assert decision.hts_numeric_equivalence_required is False
    assert decision.analysis_authorized is True
    assert decision.dashboard_authorized is True


def test_reference_policy_never_grants_execution_authority():
    decision = assess_kiwoom_price_reference_policy()
    for field in (
        "trading_calendar_verified",
        "response_provenance_verified",
        "api_execution_authorized",
        "snapshot_authorized",
        "persistence_authorized",
        "database_rebuild_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(decision, field) is False


def test_reference_policy_is_immutable():
    decision = assess_kiwoom_price_reference_policy()
    with pytest.raises(FrozenInstanceError):
        decision.provider = "KIS"
