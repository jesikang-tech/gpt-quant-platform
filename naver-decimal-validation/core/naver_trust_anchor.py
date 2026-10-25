"""Pure, fail-closed acquisition trust-anchor contract for NAVER evidence.

The evidence envelope contains caller claims.  A trust anchor is a separate
configuration concern and cannot be derived from provider names, URLs,
timestamps, hashes, issuer labels, or verification flags in that envelope.

No independently established NAVER acquisition anchor is available here, so
this module intentionally has no successful verification path.
"""

from dataclasses import dataclass, field

from core.naver_source_evidence import (
    NaverSourceEvidence,
    ObservationIdentity,
    assess_naver_source_evidence,
)


class NaverTrustAnchorRejected(ValueError):
    """Trust requirements or supplied anchor material are invalid."""


@dataclass(frozen=True)
class TrustedAcquisitionRequirements:
    """Policy expectations kept separate from the evidence being assessed."""

    expected_observation: ObservationIdentity
    required_provider: str = field(default="NAVER", init=False)


@dataclass(frozen=True)
class ExternalTrustAnchor:
    """Opaque external configuration, not an issuer or evidence claim.

    ``independently_verified`` must remain false until a real verifier and
    anchor are specified outside this contract.  Setting it is not a shortcut
    to verification and is rejected as a forged/unsupported state.
    """

    anchor_id: str
    authority: str
    verification_method: str
    independently_verified: bool = False


@dataclass(frozen=True)
class NaverTrustAnchorDecision:
    reason: str
    source_evidence_state: str
    status: str = field(default="DENIED", init=False)
    verified: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    database_rebuild_authorized: bool = field(default=False, init=False)

    def __post_init__(self):
        if self.reason == "INDEPENDENT_TRUST_ANCHOR_UNVERIFIED":
            object.__setattr__(self, "status", "UNVERIFIABLE")
        if self.source_evidence_state not in {
            "SELF_DECLARED_ONLY", "UNVERIFIABLE",
        }:
            raise NaverTrustAnchorRejected("Invalid source evidence state")


def _required_text(value, name):
    if type(value) is not str or not value or value != value.strip():
        raise NaverTrustAnchorRejected("Malformed " + name)


def _validate_requirements(requirements):
    if type(requirements) is not TrustedAcquisitionRequirements:
        raise NaverTrustAnchorRejected("Absent or malformed requirements")
    identity = requirements.expected_observation
    if type(identity) is not ObservationIdentity:
        raise NaverTrustAnchorRejected("Malformed expected observation identity")
    for name, value in (
        ("expected ticker", identity.ticker),
        ("expected observation date", identity.observation_date),
        ("expected content hash", identity.content_sha256),
    ):
        _required_text(value, name)


def _validate_anchor(anchor):
    if type(anchor) is not ExternalTrustAnchor:
        raise NaverTrustAnchorRejected("Malformed external trust anchor")
    for name, value in (
        ("anchor id", anchor.anchor_id),
        ("anchor authority", anchor.authority),
        ("anchor verification method", anchor.verification_method),
    ):
        _required_text(value, name)
    if type(anchor.independently_verified) is not bool:
        raise NaverTrustAnchorRejected("Malformed anchor verification state")
    if anchor.independently_verified:
        raise NaverTrustAnchorRejected(
            "Verified external trust anchor is unsupported"
        )


def assess_naver_trust_anchor(evidence, requirements, *, trust_anchor=None):
    """Assess evidence without allowing caller claims to manufacture trust."""

    _validate_requirements(requirements)
    if type(evidence) is not NaverSourceEvidence:
        raise NaverTrustAnchorRejected("Absent or malformed source evidence")

    # Delegate envelope, reference, and contradiction checks to the existing
    # evidence contract instead of reproducing that contract here.
    evidence_decision = assess_naver_source_evidence(evidence)

    if evidence.claimed_provider.name != requirements.required_provider:
        raise NaverTrustAnchorRejected("Unexpected claimed provider")
    if evidence.observation != requirements.expected_observation:
        raise NaverTrustAnchorRejected("Mismatched observation identity")

    if trust_anchor is None:
        return NaverTrustAnchorDecision(
            reason="INDEPENDENT_TRUST_ANCHOR_MISSING",
            source_evidence_state=evidence_decision.evidence_state,
        )

    _validate_anchor(trust_anchor)
    return NaverTrustAnchorDecision(
        reason="INDEPENDENT_TRUST_ANCHOR_UNVERIFIED",
        source_evidence_state=evidence_decision.evidence_state,
    )
