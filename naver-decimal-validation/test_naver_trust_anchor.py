"""Synthetic negative tests for the fail-closed NAVER trust anchor."""

from dataclasses import FrozenInstanceError, replace

import pytest

from core.naver_source_evidence import (
    AcquisitionContext,
    ClaimedProvider,
    EvidenceReference,
    NaverSourceEvidence,
    NaverSourceEvidenceRejected,
    ObservationIdentity,
)
from core.naver_trust_anchor import (
    ExternalTrustAnchor,
    NaverTrustAnchorDecision,
    NaverTrustAnchorRejected,
    TrustedAcquisitionRequirements,
    assess_naver_trust_anchor,
)


IDENTITY = ObservationIdentity("069500", "2026-09-16", "claimed-hash")
REQUIREMENTS = TrustedAcquisitionRequirements(IDENTITY)


def _reference(**changes):
    value = EvidenceReference(
        evidence_id="synthetic-1",
        evidence_type="RESPONSE_RECORD",
        asserted_provider="NAVER",
        issuer="caller",
        locator="https://example.invalid/synthetic",
        digest="caller-digest",
    )
    return replace(value, **changes)


def _evidence(*references, **changes):
    value = NaverSourceEvidence(
        claimed_provider=ClaimedProvider("NAVER"),
        acquisition=AcquisitionContext(
            method="SYNTHETIC",
            acquired_at="2026-09-16T00:00:00Z",
            source_url="https://example.invalid/synthetic",
        ),
        observation=IDENTITY,
        references=references or (_reference(),),
    )
    return replace(value, **changes)


def _assert_no_authority(decision):
    assert decision.verified is False
    assert decision.analysis_authorized is False
    assert decision.dashboard_authorized is False
    assert decision.persistence_authorized is False
    assert decision.database_rebuild_authorized is False


@pytest.mark.parametrize("status", ["VERIFIED", "PASS", "APPROVED"])
def test_decision_constructor_rejects_forbidden_statuses(status):
    with pytest.raises(TypeError):
        NaverTrustAnchorDecision(
            reason="caller-forged",
            status=status,
            source_evidence_state="SELF_DECLARED_ONLY",
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "verified",
        "analysis_authorized",
        "dashboard_authorized",
        "persistence_authorized",
        "database_rebuild_authorized",
    ],
)
def test_decision_constructor_rejects_authorization_forgery(field_name):
    with pytest.raises(TypeError):
        NaverTrustAnchorDecision(
            reason="caller-forged",
            source_evidence_state="SELF_DECLARED_ONLY",
            **{field_name: True},
        )


@pytest.mark.parametrize("state", ["VERIFIED", "PASS", "APPROVED"])
def test_decision_rejects_forbidden_source_evidence_states(state):
    with pytest.raises(NaverTrustAnchorRejected, match="source evidence state"):
        NaverTrustAnchorDecision(
            reason="caller-forged",
            source_evidence_state=state,
        )


def test_decision_is_immutable_and_fail_closed():
    decision = NaverTrustAnchorDecision(
        reason="caller-supplied",
        source_evidence_state="SELF_DECLARED_ONLY",
    )
    assert decision.status == "DENIED"
    _assert_no_authority(decision)
    with pytest.raises(FrozenInstanceError):
        decision.status = "VERIFIED"


def test_missing_anchor_is_denied():
    decision = assess_naver_trust_anchor(_evidence(), REQUIREMENTS)
    assert decision.status == "DENIED"
    assert decision.reason == "INDEPENDENT_TRUST_ANCHOR_MISSING"
    _assert_no_authority(decision)


def test_self_declared_issuer_is_not_an_external_anchor():
    decision = assess_naver_trust_anchor(
        _evidence(_reference(issuer="NAVER")), REQUIREMENTS,
    )
    assert decision.status == "DENIED"
    _assert_no_authority(decision)


def test_forged_verification_flags_are_rejected():
    forged_anchor = ExternalTrustAnchor(
        anchor_id="caller-anchor",
        authority="caller",
        verification_method="caller-assertion",
        independently_verified=True,
    )
    with pytest.raises(NaverTrustAnchorRejected, match="unsupported"):
        assess_naver_trust_anchor(
            _evidence(caller_claims_verified=True),
            REQUIREMENTS,
            trust_anchor=forged_anchor,
        )


def test_unverified_external_configuration_remains_unverifiable():
    anchor = ExternalTrustAnchor(
        anchor_id="opaque-config-id",
        authority="unestablished-authority",
        verification_method="unspecified-verifier",
    )
    decision = assess_naver_trust_anchor(
        _evidence(), REQUIREMENTS, trust_anchor=anchor,
    )
    assert decision.status == "UNVERIFIABLE"
    _assert_no_authority(decision)


def test_mismatched_observation_identity_is_rejected():
    other = replace(IDENTITY, content_sha256="different-claimed-hash")
    with pytest.raises(NaverTrustAnchorRejected, match="Mismatched observation"):
        assess_naver_trust_anchor(_evidence(observation=other), REQUIREMENTS)


def test_conflicting_references_are_rejected_by_existing_contract():
    with pytest.raises(NaverSourceEvidenceRejected, match="Conflicting evidence"):
        assess_naver_trust_anchor(
            _evidence(_reference(), _reference(digest="different")),
            REQUIREMENTS,
        )


@pytest.mark.parametrize(
    ("evidence", "requirements", "anchor"),
    [
        (None, REQUIREMENTS, None),
        (_evidence(), None, None),
        (_evidence(), TrustedAcquisitionRequirements(None), None),
        (_evidence(), REQUIREMENTS, "issuer=NAVER"),
    ],
)
def test_malformed_input_is_rejected(evidence, requirements, anchor):
    with pytest.raises(NaverTrustAnchorRejected, match="malformed|Malformed"):
        assess_naver_trust_anchor(
            evidence, requirements, trust_anchor=anchor,
        )


def test_forged_independent_reference_label_cannot_verify():
    forged = _reference(
        issuer="attacker",
        verification_basis="INDEPENDENT_ATTESTATION",
    )
    decision = assess_naver_trust_anchor(_evidence(forged), REQUIREMENTS)
    assert decision.status == "DENIED"
    assert decision.source_evidence_state == "UNVERIFIABLE"
    _assert_no_authority(decision)
