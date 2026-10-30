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
