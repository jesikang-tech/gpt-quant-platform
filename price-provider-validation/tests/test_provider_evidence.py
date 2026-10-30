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

from hashlib import sha256
from price_provider_validation.provider_evidence import assess_raw_bytes_evidence_binding


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_raw_byte_binding_valid_remains_denied(provider):
    body = b"original daily response bytes"
    evidence = _evidence(provider=provider, content_sha256=sha256(body).hexdigest())
    decision = assess_raw_bytes_evidence_binding(_observation(provider), evidence, body)
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


def test_raw_byte_binding_modified_body_rejected():
    body = b"original daily response bytes"
    evidence = _evidence(content_sha256=sha256(body).hexdigest())
    with pytest.raises(ProviderEvidenceRejected, match="SHA256 mismatch"):
        assess_raw_bytes_evidence_binding(_observation(), evidence, body + b" changed")


@pytest.mark.parametrize("invalid", ["text", bytearray(b"raw"), None, 123])
def test_raw_byte_binding_non_bytes_rejected(invalid):
    body = b"original daily response bytes"
    evidence = _evidence(content_sha256=sha256(body).hexdigest())
    with pytest.raises(ProviderEvidenceRejected, match="must be bytes"):
        assess_raw_bytes_evidence_binding(_observation(), evidence, invalid)


def test_raw_byte_binding_identity_mismatch_rejected():
    body = b"original daily response bytes"
    evidence = _evidence(provider="KIWOOM", content_sha256=sha256(body).hexdigest())
    with pytest.raises(ProviderEvidenceRejected, match="Provider mismatch"):
        assess_raw_bytes_evidence_binding(_observation(), evidence, body)


@pytest.mark.parametrize("acquired_at", [
    "2026-10-27T23:59:59+09:00",
    "2026-10-27T00:00:00+09:00",
    "2026-10-27T14:59:59Z",
])
def test_acquisition_time_precedes_observation_date_rejected(acquired_at):
    with pytest.raises(
        ProviderEvidenceRejected,
        match="Acquisition precedes observation date",
    ):
        assess_provider_evidence(_evidence(acquired_at=acquired_at))


@pytest.mark.parametrize("acquired_at", [
    "2026-10-28T00:00:00+09:00",
    "2026-10-28T15:30:00+09:00",
    "2026-10-29T09:00:00+09:00",
    "2026-10-28T00:00:00Z",
])
def test_acquisition_time_on_or_after_observation_date_remains_denied(acquired_at):
    decision = assess_provider_evidence(_evidence(acquired_at=acquired_at))
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False
@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
@pytest.mark.parametrize("bad_fields", [
    (),
    ("100",),
    ("100", "110", "90", "105"),
    ("100", "110", "90", "105", "1000", "extra"),
    ["100", "110", "90", "105", "1000"],
    None,
])
def test_binding_rejects_forged_raw_field_structure(provider, bad_fields):
    observation = replace(_observation(provider), raw_fields=bad_fields)
    evidence = _evidence(provider=provider)

    with pytest.raises(ProviderEvidenceRejected, match="Invalid observation structure"):
        assess_observation_evidence_binding(observation, evidence)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_raw_byte_binding_rejects_forged_raw_field_structure(provider):
    body = b"original daily response bytes"
    observation = replace(_observation(provider), raw_fields=("100",))
    evidence = _evidence(
        provider=provider,
        content_sha256=sha256(body).hexdigest(),
    )

    with pytest.raises(ProviderEvidenceRejected, match="Invalid observation structure"):
        assess_raw_bytes_evidence_binding(observation, evidence, body)

@pytest.mark.parametrize("acquired_at", [
    "2026-10-28T00:30:00+14:00",
    "2026-10-27T14:59:59Z",
    "2026-10-27T09:59:59-05:00",
])
def test_acquisition_timezone_normalized_to_kst_rejects_earlier_instant(acquired_at):
    with pytest.raises(
        ProviderEvidenceRejected,
        match="Acquisition precedes observation date",
    ):
        assess_provider_evidence(_evidence(acquired_at=acquired_at))


@pytest.mark.parametrize("acquired_at", [
    "2026-10-27T15:00:00Z",
    "2026-10-27T10:00:00-05:00",
    "2026-10-28T00:00:00+09:00",
])
def test_acquisition_timezone_normalized_to_kst_accepts_boundary_without_authority(acquired_at):
    decision = assess_provider_evidence(_evidence(acquired_at=acquired_at))
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize("adjustment", ["UNKNOWN", "ADJUSTED", "UNADJUSTED"])
def test_evidence_adjustment_claim_never_grants_authority(adjustment):
    evidence = _evidence(adjustment=adjustment)
    decision = assess_observation_evidence_binding(_observation(), evidence)
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False

@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_matching_digest_does_not_certify_observation_origin(provider):
    # These bytes are deliberately unrelated to the observation's OHLCV.
    body = b"unrelated synthetic payload"
    observation = _observation(provider)
    evidence = _evidence(
        provider=provider,
        content_sha256=sha256(body).hexdigest(),
    )

    decision = assess_raw_bytes_evidence_binding(
        observation, evidence, body
    )

    assert decision.reason == "INDEPENDENT_PROVIDER_PROVENANCE_NOT_VERIFIED"
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False
