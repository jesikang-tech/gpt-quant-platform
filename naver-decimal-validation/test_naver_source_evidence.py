"""Focused synthetic tests for the fail-closed NAVER evidence contract."""

from dataclasses import FrozenInstanceError, replace

import pytest

from core.naver_source_evidence import (
    AcquisitionContext,
    ClaimedProvider,
    EvidenceReference,
    NaverSourceEvidence,
    NaverSourceEvidenceDecision,
    NaverSourceEvidenceRejected,
    ObservationIdentity,
    assess_naver_source_evidence,
)


def _reference(**changes):
    return replace(
        EvidenceReference(
            evidence_id="synthetic-1",
            evidence_type="RESPONSE_RECORD",
            asserted_provider="NAVER",
            issuer="caller",
            locator="https://example.invalid/synthetic",
            digest="not-a-trust-anchor",
        ),
        **changes,
    )


def _evidence(*references, **changes):
    value = NaverSourceEvidence(
        claimed_provider=ClaimedProvider("NAVER"),
        acquisition=AcquisitionContext(
            method="SYNTHETIC", acquired_at="2026-09-16T00:00:00Z",
            source_url="https://example.invalid/synthetic",
        ),
        observation=ObservationIdentity(
            ticker="069500", observation_date="2026-09-16",
            content_sha256="caller-supplied-hash",
        ),
        references=references or (_reference(),),
    )
    return replace(value, **changes)


def _assert_every_use_denied(decision):
    assert decision.status == "BLOCKED"
    assert decision.analysis_authorized is False
    assert decision.dashboard_authorized is False
    assert decision.portfolio_authorized is False
    assert decision.snapshot_authorized is False
    assert decision.persistence_authorized is False


def test_self_declared_metadata_never_verifies_provenance():
    decision = assess_naver_source_evidence(
        _evidence(caller_claims_verified=True),
    )
    assert decision.evidence_state == "SELF_DECLARED_ONLY"
    assert decision.reason == "SELF_DECLARED_EVIDENCE_ONLY"
    _assert_every_use_denied(decision)


def test_forged_independent_label_fails_without_trust_anchor():
    forged = _reference(
        issuer="attacker", verification_basis="INDEPENDENT_ATTESTATION",
        locator="https://naver.example.invalid/looks-official",
        digest="0" * 64,
    )
    decision = assess_naver_source_evidence(_evidence(forged))
    assert decision.evidence_state == "UNVERIFIABLE"
    assert decision.reason == "INDEPENDENT_TRUST_ANCHOR_UNAVAILABLE"
    _assert_every_use_denied(decision)


@pytest.mark.parametrize("invalid", [None, {}, "NAVER", True])
def test_absent_or_wrong_envelope_is_rejected(invalid):
    with pytest.raises(
        NaverSourceEvidenceRejected,
        match="Absent or malformed source evidence",
    ):
        assess_naver_source_evidence(invalid)


def test_empty_references_are_rejected():
    with pytest.raises(NaverSourceEvidenceRejected, match="Absent evidence"):
        assess_naver_source_evidence(_evidence(references=()))


def test_malformed_reference_is_rejected():
    with pytest.raises(NaverSourceEvidenceRejected, match="Malformed evidence"):
        assess_naver_source_evidence(_evidence(_reference(digest="  bad  ")))


def test_conflicting_provider_evidence_is_rejected():
    with pytest.raises(NaverSourceEvidenceRejected, match="Conflicting provider"):
        assess_naver_source_evidence(
            _evidence(_reference(asserted_provider="OTHER")),
        )


def test_duplicate_evidence_id_with_conflicting_contents_is_rejected():
    with pytest.raises(NaverSourceEvidenceRejected, match="Conflicting evidence"):
        assess_naver_source_evidence(
            _evidence(_reference(), _reference(digest="different")),
        )


def test_contract_is_immutable():
    evidence = _evidence()
    with pytest.raises(FrozenInstanceError):
        evidence.caller_claims_verified = True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("status", "VERIFIED"),
        ("analysis_authorized", True),
        ("dashboard_authorized", True),
        ("portfolio_authorized", True),
        ("snapshot_authorized", True),
        ("persistence_authorized", True),
    ],
)
def test_authorization_fields_cannot_be_forged_at_construction(field, value):
    with pytest.raises(TypeError):
        NaverSourceEvidenceDecision(
            reason="forged",
            evidence_state="UNVERIFIABLE",
            **{field: value},
        )


def test_verified_evidence_state_cannot_be_forged_at_construction():
    with pytest.raises(NaverSourceEvidenceRejected, match="Invalid evidence state"):
        NaverSourceEvidenceDecision(
            reason="forged",
            evidence_state="VERIFIED",
        )
