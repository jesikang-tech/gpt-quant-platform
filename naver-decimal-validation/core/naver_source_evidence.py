"""Pure, fail-closed NAVER source-provenance evidence contract.

This module records claims and evidence references.  It deliberately has no
trust-anchor registry, signature verifier, provider client, or I/O capability,
so it cannot produce a verified provenance state.
"""

from dataclasses import dataclass, field


class NaverSourceEvidenceRejected(ValueError):
    """Source evidence is malformed, conflicting, or unverifiable."""


@dataclass(frozen=True)
class ClaimedProvider:
    name: str


@dataclass(frozen=True)
class AcquisitionContext:
    method: str
    acquired_at: str
    source_url: str


@dataclass(frozen=True)
class ObservationIdentity:
    ticker: str
    observation_date: str
    content_sha256: str


@dataclass(frozen=True)
class EvidenceReference:
    evidence_id: str
    evidence_type: str
    asserted_provider: str
    issuer: str
    locator: str
    digest: str
    verification_basis: str = "SELF_DECLARED"


@dataclass(frozen=True)
class NaverSourceEvidence:
    claimed_provider: ClaimedProvider
    acquisition: AcquisitionContext
    observation: ObservationIdentity
    references: tuple
    caller_claims_verified: bool = False


@dataclass(frozen=True)
class NaverSourceEvidenceDecision:
    reason: str
    evidence_state: str
    status: str = field(default="BLOCKED", init=False)
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    portfolio_authorized: bool = field(default=False, init=False)
    snapshot_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)

    def __post_init__(self):
        if self.evidence_state not in {"SELF_DECLARED_ONLY", "UNVERIFIABLE"}:
            raise NaverSourceEvidenceRejected("Invalid evidence state")


def _required_text(value, field):
    if type(value) is not str or not value or value != value.strip():
        raise NaverSourceEvidenceRejected("Malformed " + field)


def _validate_contract(evidence):
    if type(evidence) is not NaverSourceEvidence:
        raise NaverSourceEvidenceRejected("Absent or malformed source evidence")
    if type(evidence.claimed_provider) is not ClaimedProvider:
        raise NaverSourceEvidenceRejected("Malformed claimed provider")
    if type(evidence.acquisition) is not AcquisitionContext:
        raise NaverSourceEvidenceRejected("Malformed acquisition context")
    if type(evidence.observation) is not ObservationIdentity:
        raise NaverSourceEvidenceRejected("Malformed observation identity")
    if type(evidence.references) is not tuple or not evidence.references:
        raise NaverSourceEvidenceRejected("Absent evidence references")
    if type(evidence.caller_claims_verified) is not bool:
        raise NaverSourceEvidenceRejected("Malformed caller verification claim")

    _required_text(evidence.claimed_provider.name, "claimed provider")
    for field, value in (
        ("acquisition method", evidence.acquisition.method),
        ("acquisition timestamp", evidence.acquisition.acquired_at),
        ("source URL", evidence.acquisition.source_url),
        ("ticker", evidence.observation.ticker),
        ("observation date", evidence.observation.observation_date),
        ("content hash", evidence.observation.content_sha256),
    ):
        _required_text(value, field)

    seen = {}
    for reference in evidence.references:
        if type(reference) is not EvidenceReference:
            raise NaverSourceEvidenceRejected("Malformed evidence reference")
        for field, value in (
            ("evidence id", reference.evidence_id),
            ("evidence type", reference.evidence_type),
            ("asserted provider", reference.asserted_provider),
            ("issuer", reference.issuer),
            ("evidence locator", reference.locator),
            ("evidence digest", reference.digest),
            ("verification basis", reference.verification_basis),
        ):
            _required_text(value, field)
        if reference.verification_basis not in {
            "SELF_DECLARED", "INDEPENDENT_ATTESTATION",
        }:
            raise NaverSourceEvidenceRejected("Malformed verification basis")
        if reference.asserted_provider != evidence.claimed_provider.name:
            raise NaverSourceEvidenceRejected("Conflicting provider evidence")
        fingerprint = (
            reference.evidence_type,
            reference.asserted_provider,
            reference.issuer,
            reference.locator,
            reference.digest,
            reference.verification_basis,
        )
        previous = seen.setdefault(reference.evidence_id, fingerprint)
        if previous != fingerprint:
            raise NaverSourceEvidenceRejected("Conflicting evidence reference")


def assess_naver_source_evidence(evidence):
    """Validate the envelope, then deny trust without an independent anchor.

    Provider names, timestamps, URLs, hashes, evidence labels, and caller
    booleans remain claims.  None can establish verified provenance here.
    """

    _validate_contract(evidence)
    has_independent_claim = any(
        reference.verification_basis == "INDEPENDENT_ATTESTATION"
        for reference in evidence.references
    )
    if has_independent_claim:
        return NaverSourceEvidenceDecision(
            reason="INDEPENDENT_TRUST_ANCHOR_UNAVAILABLE",
            evidence_state="UNVERIFIABLE",
        )
    return NaverSourceEvidenceDecision(
        reason="SELF_DECLARED_EVIDENCE_ONLY",
        evidence_state="SELF_DECLARED_ONLY",
    )
