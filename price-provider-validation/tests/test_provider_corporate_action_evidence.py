"""Synthetic fail-closed K16 corporate-action declaration tests."""
from dataclasses import FrozenInstanceError, replace

import pytest

from price_provider_validation.provider_corporate_action_evidence import (
    CorporateActionDeclaration,
    CorporateActionEvidenceRejected,
    assess_corporate_action_declaration,
)
from price_provider_validation.provider_evidence import ProviderEvidence


def _evidence(provider="KIS"):
    return ProviderEvidence(
        provider=provider,
        ticker="005930",
        observation_date="2026-10-28",
        acquired_at="2026-10-29T09:00:00+09:00",
        source_locator="synthetic:unverified",
        content_sha256="a" * 64,
        adjustment="UNKNOWN",
    )


def _declaration(provider="KIS", **changes):
    values = dict(
        provider=provider,
        ticker="005930",
        observation_date="2026-10-28",
        action_date="2026-10-27",
        action_type="SPLIT",
        source_reference="synthetic:unverified-action",
    )
    values.update(changes)
    return CorporateActionDeclaration(**values)


@pytest.mark.parametrize("provider", ("KIS", "KIWOOM"))
@pytest.mark.parametrize("action_type", (
    "SPLIT",
    "REVERSE_SPLIT",
    "CASH_DIVIDEND",
    "STOCK_DIVIDEND",
))
def test_matching_declarations_never_certify(provider, action_type):
    result = assess_corporate_action_declaration(
        _evidence(provider),
        _declaration(provider, action_type=action_type),
    )
    assert result.status == "DENIED"
    assert result.response_adjustment == "UNKNOWN"
    assert result.reason == "CORPORATE_ACTION_NOT_INDEPENDENTLY_VERIFIED"
    for name in (
        "corporate_action_verified",
        "independently_verified",
        "adjustment_factor_verified",
        "analysis_authorized",
        "dashboard_authorized",
        "persistence_authorized",
        "database_rebuild_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(result, name) is False


@pytest.mark.parametrize("changes", (
    {"provider": "KIWOOM"},
    {"ticker": "000660"},
    {"observation_date": "2026-10-27"},
    {"action_type": "UNKNOWN"},
    {"action_type": ""},
    {"action_date": "2026-02-30"},
    {"action_date": "20261027"},
    {"action_date": 20261027},
    {"source_reference": ""},
    {"source_reference": " unverified "},
))
def test_invalid_or_mismatched_declaration_rejected(changes):
    with pytest.raises(CorporateActionEvidenceRejected):
        assess_corporate_action_declaration(
            _evidence(), _declaration(**changes)
        )


def test_invalid_evidence_rejected():
    bad = replace(_evidence(), acquired_at="invalid")
    with pytest.raises(CorporateActionEvidenceRejected):
        assess_corporate_action_declaration(bad, _declaration())


def test_invalid_evidence_type_rejected():
    with pytest.raises(CorporateActionEvidenceRejected):
        assess_corporate_action_declaration(object(), _declaration())


def test_invalid_declaration_type_rejected():
    with pytest.raises(CorporateActionEvidenceRejected):
        assess_corporate_action_declaration(_evidence(), object())


def test_direct_result_is_immutable():
    result = assess_corporate_action_declaration(
        _evidence(), _declaration()
    )
    with pytest.raises(FrozenInstanceError):
        result.corporate_action_verified = True


def test_unverified_adjustment_claim_does_not_certify():
    evidence = replace(_evidence(), adjustment="ADJUSTED")
    result = assess_corporate_action_declaration(evidence, _declaration())
    assert result.response_adjustment == "UNKNOWN"
    assert result.corporate_action_verified is False
    assert result.status == "DENIED"
