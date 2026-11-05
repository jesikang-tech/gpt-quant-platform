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

@dataclass(frozen=True)
class WindowsStorageExecutionDecision:
    """Actual execution authority, distinct from policy eligibility."""

    authorized: bool
    reason: str
    policy_eligible: bool


def assess_windows_storage_execution(
    operation: object,
    evidence: object,
    *,
    platform: str | None = None,
) -> WindowsStorageExecutionDecision:
    """Deny credential storage execution until trusted OS controls exist.

    Existing policy assessment is reused only for diagnostics.
    Caller-provided evidence, including all-true security flags,
    cannot authorize filesystem writes, replacement, or deletion.

    This function performs no filesystem or credential operations.
    """
    policy = assess_windows_storage_boundary(
        operation,
        evidence,
        platform=platform,
    )

    if not policy.eligible:
        return WindowsStorageExecutionDecision(
            False,
            "POLICY_" + policy.reason,
            False,
        )

    return WindowsStorageExecutionDecision(
        False,
        "TRUSTED_WINDOWS_STORAGE_ADAPTER_NOT_IMPLEMENTED",
        True,
    )

@dataclass(frozen=True)
class AttemptStorageTransactionDecision:
    """Assessment only; never grants credential storage execution."""

    authorized: bool
    reason: str
    candidate_valid: bool
    policy_eligible: bool


def assess_attempt_storage_transaction(
    transition: object,
    evidence: object,
    *,
    platform: str | None = None,
) -> AttemptStorageTransactionDecision:
    """Reject storage execution until a trusted Windows adapter exists.

    A candidate transition and declared security flags are not proof
    of a trusted exclusive lock, same-handle record identity, durable
    revision comparison, or atomic filesystem replacement.
    """
    from .credential_record import (
        AttemptRecordTransition,
        validate_record,
    )

    if type(transition) is not AttemptRecordTransition:
        return AttemptStorageTransactionDecision(
            False, "INVALID_TRANSITION", False, False,
        )

    candidate_valid = (
        transition.eligible is True
        and transition.reason == "CANDIDATE_ONLY_NOT_PERSISTED"
        and validate_record(transition.next_record)
    )

    if not candidate_valid:
        return AttemptStorageTransactionDecision(
            False, "INVALID_TRANSITION_CANDIDATE", False, False,
        )

    execution = assess_windows_storage_execution(
        StorageOperation.UPDATE_ATTEMPTS,
        evidence,
        platform=platform,
    )

    return AttemptStorageTransactionDecision(
        False,
        execution.reason,
        True,
        execution.policy_eligible,
    )

@dataclass(frozen=True)
class WindowsObservedStoreSecurityDecision:
    """Diagnostic observation only, never credential storage authority."""

    observed: bool
    reason: str
    storage_authorized: bool = False


def assess_windows_observed_store_security(
    *,
    location: object,
    same_handle: object,
    acl: object,
    platform: str | None = None,
) -> WindowsObservedStoreSecurityDecision:
    """Combine existing observations without elevating them to authority.

    Inputs are independently supplied diagnostic objects. Even a
    positive result cannot establish that observations concern the
    same trusted object at the time of a later filesystem operation.
    """
    from .windows_credential_store import (
        WindowsSameHandleInspection,
        WindowsAclAssessment,
    )

    location_result = assess_windows_store_location(
        location,
        platform=platform,
    )

    if not location_result.eligible:
        return WindowsObservedStoreSecurityDecision(
            False,
            "LOCATION_" + location_result.reason,
        )

    if type(same_handle) is not WindowsSameHandleInspection:
        return WindowsObservedStoreSecurityDecision(
            False,
            "INVALID_HANDLE_OBSERVATION",
        )

    if (
        same_handle.inspected is not True
        or same_handle.reason != "SAME_HANDLE_OBSERVED_NOT_AUTHORIZED"
    ):
        return WindowsObservedStoreSecurityDecision(
            False,
            "HANDLE_OBSERVATION_UNVERIFIED",
        )

    if type(acl) is not WindowsAclAssessment:
        return WindowsObservedStoreSecurityDecision(
            False,
            "INVALID_ACL_ASSESSMENT",
        )

    if acl.accepted is not True:
        return WindowsObservedStoreSecurityDecision(
            False,
            "ACL_POLICY_UNVERIFIED",
        )

    return WindowsObservedStoreSecurityDecision(
        True,
        "OBSERVATIONS_ONLY_NOT_AUTHORIZED",
    )

@dataclass(frozen=True)
class WindowsLockLifecycleObservation:
    """Caller-declared lock state, not trusted OS lock evidence."""

    acquired: bool
    held: bool
    released: bool
    same_handle: bool


@dataclass(frozen=True)
class WindowsLockLifecycleDecision:
    """Diagnostic decision only; never grants storage execution."""

    consistent: bool
    reason: str
    storage_authorized: bool = False


def assess_windows_lock_lifecycle(
    observation: object,
    *,
    platform: str | None = None,
) -> WindowsLockLifecycleDecision:
    """Assess declared lock state without acquiring or trusting a lock.

    This is a synthetic diagnostic contract. No caller-supplied state,
    including an all-true declaration, can authorize credential I/O.
    """
    import sys

    actual_platform = sys.platform if platform is None else platform

    if actual_platform != "win32":
        return WindowsLockLifecycleDecision(
            False, "WINDOWS_REQUIRED",
        )

    if type(observation) is not WindowsLockLifecycleObservation:
        return WindowsLockLifecycleDecision(
            False, "INVALID_LOCK_OBSERVATION",
        )

    fields = (
        observation.acquired,
        observation.held,
        observation.released,
        observation.same_handle,
    )

    if any(type(value) is not bool for value in fields):
        return WindowsLockLifecycleDecision(
            False, "INVALID_LOCK_FIELD",
        )

    if not observation.acquired:
        return WindowsLockLifecycleDecision(
            False, "LOCK_NOT_ACQUIRED",
        )

    if observation.released:
        return WindowsLockLifecycleDecision(
            False, "LOCK_ALREADY_RELEASED",
        )

    if not observation.held:
        return WindowsLockLifecycleDecision(
            False, "LOCK_NOT_HELD",
        )

    if not observation.same_handle:
        return WindowsLockLifecycleDecision(
            False, "LOCK_HANDLE_IDENTITY_UNVERIFIED",
        )

    return WindowsLockLifecycleDecision(
        True, "DECLARED_LOCK_STATE_ONLY_NOT_AUTHORIZED",
    )
