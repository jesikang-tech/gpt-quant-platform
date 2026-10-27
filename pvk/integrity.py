"""Compare supplied manifests without opening, hashing, or resolving files."""

import hmac

from .contracts import IntegrityClaim, ManifestRequirements, Result, Status
from .validation import valid_artifact_id, valid_sha256


def assess_integrity(claims: object) -> Result:
    if type(claims) is not tuple:
        return Result(Status.FAIL, ("invalid_manifest_contract",))
    if not claims:
        return Result(Status.UNVERIFIED, ("empty_manifest",))
    seen = set()
    failed = []
    pending = []
    for claim in claims:
        if type(claim) is not IntegrityClaim:
            return Result(Status.FAIL, ("invalid_integrity_contract",))
        if not valid_artifact_id(claim.artifact_id) or not valid_sha256(claim.expected_sha256):
            return Result(Status.FAIL, ("invalid_integrity_fields",))
        if claim.artifact_id in seen:
            return Result(Status.FAIL, ("duplicate_artifact",))
        seen.add(claim.artifact_id)
        if claim.observed_sha256 is None:
            pending.append("unverified:" + claim.artifact_id)
        elif not valid_sha256(claim.observed_sha256):
            return Result(Status.FAIL, ("invalid_observed_digest",))
        elif not hmac.compare_digest(claim.expected_sha256, claim.observed_sha256):
            failed.append("digest_mismatch:" + claim.artifact_id)
    if failed:
        return Result(Status.FAIL, tuple(failed + pending))
    if pending:
        return Result(Status.UNVERIFIED, tuple(pending))
    return Result(Status.PASS, ("supplied_digests_match",))


def assess_manifest(claims: object, requirements: object) -> Result:
    """Require exact membership, then compare digests. No trust or file access."""
    if type(requirements) is not ManifestRequirements:
        return Result(Status.FAIL, ("invalid_requirements_contract",))
    required = requirements.artifact_ids
    if type(required) is not tuple or not required:
        return Result(Status.FAIL, ("invalid_required_artifacts",))
    if any(not valid_artifact_id(item) for item in required):
        return Result(Status.FAIL, ("invalid_required_artifact_id",))
    if len(set(required)) != len(required):
        return Result(Status.FAIL, ("duplicate_required_artifact",))
    if type(claims) is not tuple:
        return Result(Status.FAIL, ("invalid_manifest_contract",))
    seen = set()
    errors = []
    for claim in claims:
        if type(claim) is not IntegrityClaim:
            return Result(Status.FAIL, ("invalid_integrity_contract",))
        if not valid_artifact_id(claim.artifact_id):
            return Result(Status.FAIL, ("invalid_integrity_fields",))
        if claim.artifact_id in seen:
            errors.append("duplicate_artifact:" + claim.artifact_id)
        if claim.artifact_id not in required:
            errors.append("unexpected_artifact:" + claim.artifact_id)
        seen.add(claim.artifact_id)
    errors.extend("missing_artifact:" + item for item in required if item not in seen)
    if errors:
        return Result(Status.FAIL, tuple(errors))
    return assess_integrity(claims)
