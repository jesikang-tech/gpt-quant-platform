"""Offline fail-closed tests for untrusted provider evidence."""

import pytest

from price_provider_validation.provider_evidence import (
    ProviderEvidence,
    ProviderEvidenceRejected,
    assess_provider_evidence,
)


def _evidence(**overrides):
    values = dict(
        provider="KIS",
        ticker="005930",
        observation_date="2026-10-28",
        acquired_at="2026-10-29T09:00:00+09:00",
        source_locator="offline-fixture",
        content_sha256="a" * 64,
        adjustment="UNKNOWN",
    )
    values.update(overrides)
    return ProviderEvidence(**values)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_valid_shape_remains_denied(provider):
    decision = assess_provider_evidence(_evidence(provider=provider))
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize("changes", [
    {"provider": "NAVER"},
    {"provider": "kis"},
    {"acquired_at": "2026-10-29T09:00:00"},
    {"acquired_at": "invalid"},
    {"content_sha256": "abc"},
    {"content_sha256": "G" * 64},
    {"adjustment": "VERIFIED"},
    {"source_locator": ""},
])
def test_invalid_evidence_rejected(changes):
    with pytest.raises(ProviderEvidenceRejected):
        assess_provider_evidence(_evidence(**changes))


@pytest.mark.parametrize("bad_date", [
    "2026-02-30", "2026-13-01", "20261028", "invalid",
])
def test_invalid_observation_date_rejected(bad_date):
    with pytest.raises(ProviderEvidenceRejected):
        assess_provider_evidence(_evidence(observation_date=bad_date))

from dataclasses import replace
from price_provider_validation.provider_contract import prepare_raw_observation
from price_provider_validation.provider_evidence import assess_observation_evidence_binding


def _observation(provider="KIS"):
    return prepare_raw_observation(
        provider, "005930", "2026-10-28", ("100", "110", "90", "105", "1000")
    )


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_binding_valid_identity_remains_denied(provider):
    decision = assess_observation_evidence_binding(
        _observation(provider), _evidence(provider=provider)
    )
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize("changes", [
    {"provider": "KIWOOM"},
    {"ticker": "000660"},
    {"observation_date": "2026-10-27"},
])
def test_binding_identity_mismatch_rejected(changes):
    with pytest.raises(ProviderEvidenceRejected):
        assess_observation_evidence_binding(_observation(), _evidence(**changes))


def test_binding_adjustment_escalation_rejected():
    observation = replace(_observation(), adjustment="ADJUSTED")
    with pytest.raises(ProviderEvidenceRejected):
        assess_observation_evidence_binding(observation, _evidence())


def test_binding_invalid_observation_type_rejected():
    with pytest.raises(ProviderEvidenceRejected):
        assess_observation_evidence_binding(object(), _evidence())
