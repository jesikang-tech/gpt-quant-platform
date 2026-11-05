"""Pure PPM credential storage precondition policy.

This module does not inspect Windows ACLs or perform filesystem operations.
Evidence inputs are advisory until produced by a trusted Windows adapter.
A positive decision is NOT permission to write credentials.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StorageOperation(str, Enum):
    ENROLL = "enroll"
    UPDATE_ATTEMPTS = "update_attempts"
    REPLACE_CREDENTIAL = "replace_credential"


@dataclass(frozen=True)
class StorageEvidence:
    outside_package: bool
    outside_install_tree: bool
    trusted_parent: bool
    protected_acl: bool
    exclusive_lock: bool
    atomic_replace_supported: bool
    current_record_valid: bool
    revision_matches: bool
    enrollment_authorized: bool
    replacement_authorized: bool


@dataclass(frozen=True)
class StorageDecision:
    eligible: bool
    reason: str


def assess_storage_preconditions(
    operation: object,
    evidence: object,
) -> StorageDecision:
    """Assess declared preconditions; never authorize filesystem writes."""

    if type(operation) is not StorageOperation:
        return StorageDecision(False, "INVALID_OPERATION")

    if type(evidence) is not StorageEvidence:
        return StorageDecision(False, "INVALID_EVIDENCE")

    fields = (
        evidence.outside_package,
        evidence.outside_install_tree,
        evidence.trusted_parent,
        evidence.protected_acl,
        evidence.exclusive_lock,
        evidence.atomic_replace_supported,
        evidence.current_record_valid,
        evidence.revision_matches,
        evidence.enrollment_authorized,
        evidence.replacement_authorized,
    )

    if any(type(value) is not bool for value in fields):
        return StorageDecision(False, "INVALID_EVIDENCE_FIELD")

    common = (
        evidence.outside_package
        and evidence.outside_install_tree
        and evidence.trusted_parent
        and evidence.protected_acl
        and evidence.exclusive_lock
        and evidence.atomic_replace_supported
    )

    if not common:
        return StorageDecision(False, "STORAGE_BOUNDARY_UNVERIFIED")

    if operation is StorageOperation.ENROLL:
        if not evidence.enrollment_authorized:
            return StorageDecision(False, "ENROLLMENT_AUTHORITY_MISSING")

        if evidence.current_record_valid:
            return StorageDecision(False, "EXISTING_CREDENTIAL_PRESENT")

        return StorageDecision(True, "PRECONDITIONS_DECLARED_ONLY")

    if not evidence.current_record_valid:
        return StorageDecision(False, "CURRENT_RECORD_INVALID")

    if not evidence.revision_matches:
        return StorageDecision(False, "REVISION_CONFLICT")

    if operation is StorageOperation.REPLACE_CREDENTIAL:
        if not evidence.replacement_authorized:
            return StorageDecision(False, "REPLACEMENT_AUTHORITY_MISSING")

    return StorageDecision(True, "PRECONDITIONS_DECLARED_ONLY")
