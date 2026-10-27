"""Pure rejection checks for declarations. No issuer or signature verifier exists."""

from .contracts import EvidenceProvenance, Result, Status
from .validation import valid_artifact_id


def assess_evidence_trust(
    provenance: object, *, expected_subject_id: object, now: object,
) -> Result:
    """Never returns PASS. Caller-supplied identity/time cannot establish trust.

    Timestamps are nonnegative integer UTC Unix seconds (bool is rejected).
    No system clock, issuer allowlist, verification flag, or trust callback is used.
    """
    if type(provenance) is not EvidenceProvenance:
        return Result(Status.FAIL, ("invalid_provenance_contract",))
    if not valid_artifact_id(expected_subject_id):
        return Result(Status.FAIL, ("invalid_expected_subject",))
    if not valid_artifact_id(provenance.source_id) or not valid_artifact_id(provenance.subject_id):
        return Result(Status.FAIL, ("invalid_provenance_identity",))
    if any(type(value) is not int or value < 0 for value in (
        provenance.issued_at, provenance.expires_at, now,
    )):
        return Result(Status.FAIL, ("invalid_provenance_time",))
    if provenance.subject_id != expected_subject_id:
        return Result(Status.FAIL, ("evidence_subject_mismatch",))
    if provenance.expires_at <= provenance.issued_at:
        return Result(Status.FAIL, ("invalid_validity_window",))
    if provenance.issued_at > now:
        return Result(Status.FAIL, ("evidence_from_future",))
    if now >= provenance.expires_at:
        return Result(Status.FAIL, ("evidence_expired",))
    return Result(Status.UNVERIFIED, (
        "issuer_and_signature_unverified", "declared_time_unverified",
    ))
