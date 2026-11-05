"""Windows PPM credential storage security boundary.

This module is a pure assessment layer. It does not inspect the
filesystem, trust caller-provided claims as verified evidence,
or authorize credential file operations.

A future Windows adapter must independently establish each security
property using trusted OS handles under a controlled lock.
"""

from dataclasses import dataclass

from .storage_policy import (
    StorageDecision,
    StorageEvidence,
    StorageOperation,
    assess_storage_preconditions,
)
from .windows_credential_store import (
    WindowsStoreLocation,
    assess_windows_store_location,
)


@dataclass(frozen=True)
class WindowsSecurityEvidence:
    """Untrusted declaration until verified by a trusted OS adapter."""

    location: WindowsStoreLocation
    storage: StorageEvidence
    handle_path_verified: bool
    no_reparse_points: bool
    owner_verified: bool
    acl_verified: bool
    lock_verified: bool
    atomic_write_verified: bool


@dataclass(frozen=True)
class WindowsBoundaryDecision:
    eligible: bool
    reason: str


def assess_windows_storage_boundary(
    operation: object,
    evidence: object,
    *,
    platform: str | None = None,
) -> WindowsBoundaryDecision:
    """Assess declarations without granting filesystem authority."""

    if type(evidence) is not WindowsSecurityEvidence:
        return WindowsBoundaryDecision(False, "INVALID_WINDOWS_EVIDENCE")

    location_result = assess_windows_store_location(
        evidence.location,
        platform=platform,
    )

    if not location_result.eligible:
        return WindowsBoundaryDecision(
            False,
            "LOCATION_" + location_result.reason,
        )

    checks = (
        evidence.handle_path_verified,
        evidence.no_reparse_points,
        evidence.owner_verified,
        evidence.acl_verified,
        evidence.lock_verified,
        evidence.atomic_write_verified,
    )

    if any(type(value) is not bool for value in checks):
        return WindowsBoundaryDecision(False, "INVALID_SECURITY_FLAGS")

    if not all(checks):
        return WindowsBoundaryDecision(False, "WINDOWS_SECURITY_UNVERIFIED")

    storage_result: StorageDecision = assess_storage_preconditions(
        operation,
        evidence.storage,
    )

    if not storage_result.eligible:
        return WindowsBoundaryDecision(
            False,
            "STORAGE_" + storage_result.reason,
        )

    return WindowsBoundaryDecision(
        True,
        "DECLARED_PRECONDITIONS_ONLY",
    )
