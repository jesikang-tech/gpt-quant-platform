"""Synthetic tests for the Windows PPM storage boundary."""

from dataclasses import replace

import pytest

from portable_platform_manager.storage_policy import (
    StorageEvidence,
    StorageOperation,
)
from portable_platform_manager.windows_credential_store import (
    WindowsStoreLocation,
)
from portable_platform_manager.windows_storage_boundary import (
    WindowsSecurityEvidence,
    assess_windows_storage_boundary,
)


def location():
    return WindowsStoreLocation(
        package_root=r"C:\PPM\Packages\Platform5",
        install_root=r"D:\Platforms\Platform5",
        credential_root=r"C:\ProgramData\PPM\Credentials",
    )


def storage(**overrides):
    values = dict(
        outside_package=True,
        outside_install_tree=True,
        trusted_parent=True,
        protected_acl=True,
        exclusive_lock=True,
        atomic_replace_supported=True,
        current_record_valid=True,
        revision_matches=True,
        enrollment_authorized=True,
        replacement_authorized=True,
    )
    values.update(overrides)
    return StorageEvidence(**values)


def evidence(**overrides):
    values = dict(
        location=location(),
        storage=storage(),
        handle_path_verified=True,
        no_reparse_points=True,
        owner_verified=True,
        acl_verified=True,
        lock_verified=True,
        atomic_write_verified=True,
    )
    values.update(overrides)
    return WindowsSecurityEvidence(**values)


def assess(operation, item, platform="win32"):
    return assess_windows_storage_boundary(
        operation,
        item,
        platform=platform,
    )


def test_declared_preconditions_do_not_grant_file_authority():
    result = assess(StorageOperation.UPDATE_ATTEMPTS, evidence())

    assert result.eligible is True
    assert result.reason == "DECLARED_PRECONDITIONS_ONLY"
    assert not hasattr(result, "write_authorized")


@pytest.mark.parametrize(
    "field",
    [
        "handle_path_verified",
        "no_reparse_points",
        "owner_verified",
        "acl_verified",
        "lock_verified",
        "atomic_write_verified",
    ],
)
def test_missing_windows_security_condition_denied(field):
    item = replace(evidence(), **{field: False})

    result = assess(StorageOperation.UPDATE_ATTEMPTS, item)

    assert result.eligible is False
    assert result.reason == "WINDOWS_SECURITY_UNVERIFIED"


@pytest.mark.parametrize(
    "field",
    [
        "handle_path_verified",
        "no_reparse_points",
        "owner_verified",
        "acl_verified",
        "lock_verified",
        "atomic_write_verified",
    ],
)
@pytest.mark.parametrize("invalid", [None, 1, "true"])
def test_nonboolean_security_condition_denied(field, invalid):
    item = replace(evidence(), **{field: invalid})

    result = assess(StorageOperation.UPDATE_ATTEMPTS, item)

    assert result.eligible is False
    assert result.reason == "INVALID_SECURITY_FLAGS"


@pytest.mark.parametrize(
    "invalid",
    [None, {}, "trusted", True],
)
def test_invalid_evidence_object_denied(invalid):
    result = assess(StorageOperation.UPDATE_ATTEMPTS, invalid)

    assert result.eligible is False
    assert result.reason == "INVALID_WINDOWS_EVIDENCE"


def test_nonwindows_platform_denied():
    result = assess(
        StorageOperation.UPDATE_ATTEMPTS,
        evidence(),
        platform="linux",
    )

    assert result.eligible is False
    assert result.reason == "LOCATION_WINDOWS_REQUIRED"


def test_overlapping_credential_location_denied():
    item = replace(
        evidence(),
        location=replace(
            location(),
            credential_root=r"C:\PPM\Packages\Platform5\Secrets",
        ),
    )

    result = assess(StorageOperation.UPDATE_ATTEMPTS, item)

    assert result.eligible is False
    assert result.reason == "LOCATION_PACKAGE_CREDENTIAL_OVERLAP"


@pytest.mark.parametrize(
    "field",
    [
        "outside_package",
        "outside_install_tree",
        "trusted_parent",
        "protected_acl",
        "exclusive_lock",
        "atomic_replace_supported",
        "current_record_valid",
        "revision_matches",
    ],
)
def test_storage_policy_failure_propagates_denial(field):
    item = replace(
        evidence(),
        storage=storage(**{field: False}),
    )

    result = assess(StorageOperation.UPDATE_ATTEMPTS, item)

    assert result.eligible is False
    assert result.reason.startswith("STORAGE_")


def test_enrollment_without_authority_denied():
    item = replace(
        evidence(),
        storage=storage(enrollment_authorized=False),
    )

    result = assess(StorageOperation.ENROLL, item)

    assert result.eligible is False
    assert result.reason.startswith("STORAGE_")


def test_credential_replacement_without_authority_denied():
    item = replace(
        evidence(),
        storage=storage(replacement_authorized=False),
    )

    result = assess(StorageOperation.REPLACE_CREDENTIAL, item)

    assert result.eligible is False
    assert result.reason.startswith("STORAGE_")


def test_invalid_operation_denied():
    result = assess("UPDATE_ATTEMPTS", evidence())

    assert result.eligible is False
    assert result.reason.startswith("STORAGE_")


def test_security_evidence_is_immutable():
    item = evidence()

    with pytest.raises(AttributeError):
        item.acl_verified = False


def test_storage_evidence_is_not_os_verification():
    item = evidence()
    result = assess(StorageOperation.UPDATE_ATTEMPTS, item)

    assert item.acl_verified is True
    assert result.reason == "DECLARED_PRECONDITIONS_ONLY"
    assert not hasattr(result, "os_verified")

def test_storage_execution_denies_all_declared_authority():
    """Even a policy-eligible declaration cannot authorize writes."""
    from portable_platform_manager.storage_policy import (
        StorageEvidence,
        StorageOperation,
    )
    from portable_platform_manager.windows_credential_store import (
        WindowsStoreLocation,
    )
    from portable_platform_manager.windows_storage_boundary import (
        WindowsSecurityEvidence,
        assess_windows_storage_boundary,
        assess_windows_storage_execution,
    )

    location = WindowsStoreLocation(
        package_root="C:\\ppm-package",
        install_root="C:\\ppm-install",
        credential_root="C:\\ppm-private",
    )

    storage = StorageEvidence(
        outside_package=True,
        outside_install_tree=True,
        trusted_parent=True,
        protected_acl=True,
        exclusive_lock=True,
        atomic_replace_supported=True,
        current_record_valid=False,
        revision_matches=True,
        enrollment_authorized=True,
        replacement_authorized=True,
    )

    evidence = WindowsSecurityEvidence(
        location=location,
        storage=storage,
        handle_path_verified=True,
        no_reparse_points=True,
        owner_verified=True,
        acl_verified=True,
        lock_verified=True,
        atomic_write_verified=True,
    )

    policy = assess_windows_storage_boundary(
        StorageOperation.ENROLL,
        evidence,
        platform="win32",
    )
    assert policy.eligible is True
    assert policy.reason == "DECLARED_PRECONDITIONS_ONLY"

    execution = assess_windows_storage_execution(
        StorageOperation.ENROLL,
        evidence,
        platform="win32",
    )
    assert execution.authorized is False
    assert execution.policy_eligible is True
    assert execution.reason == (
        "TRUSTED_WINDOWS_STORAGE_ADAPTER_NOT_IMPLEMENTED"
    )


def test_storage_execution_rejects_invalid_evidence():
    """Invalid evidence cannot authorize credential operations."""
    from portable_platform_manager.storage_policy import StorageOperation
    from portable_platform_manager.windows_storage_boundary import (
        assess_windows_storage_execution,
    )

    for evidence in (None, False, True, {}, [], "verified"):
        decision = assess_windows_storage_execution(
            StorageOperation.ENROLL,
            evidence,
            platform="win32",
        )
        assert decision.authorized is False
        assert decision.policy_eligible is False
        assert decision.reason.startswith("POLICY_")


def test_storage_execution_denies_invalid_operation():
    """An invalid operation cannot gain execution authority."""
    from portable_platform_manager.windows_storage_boundary import (
        assess_windows_storage_execution,
    )

    decision = assess_windows_storage_execution(
        "enroll",
        None,
        platform="win32",
    )

    assert decision.authorized is False
    assert decision.policy_eligible is False

def _synthetic_attempt_transition():
    from portable_platform_manager.auth_attempts import AttemptState
    from portable_platform_manager.credential_record import (
        CredentialRecord,
        prepare_attempt_record_transition,
    )

    current = CredentialRecord(
        password_hash="scrypt:32768:8:1$synthetic-salt$synthetic-hash",
        attempts=AttemptState(),
        revision=3,
    )

    return prepare_attempt_record_transition(
        current,
        AttemptState(failures=1),
        expected_revision=3,
    )


def test_attempt_transaction_valid_candidate_still_denied():
    from portable_platform_manager.windows_storage_boundary import (
        assess_attempt_storage_transaction,
    )

    result = assess_attempt_storage_transaction(
        _synthetic_attempt_transition(),
        None,
        platform="win32",
    )

    assert result.authorized is False
    assert result.candidate_valid is True
    assert result.policy_eligible is False


def test_attempt_transaction_invalid_transition_denied():
    from portable_platform_manager.windows_storage_boundary import (
        assess_attempt_storage_transaction,
    )

    for invalid in (None, False, {}, "candidate"):
        result = assess_attempt_storage_transaction(
            invalid,
            None,
            platform="win32",
        )

        assert result.authorized is False
        assert result.reason == "INVALID_TRANSITION"
        assert result.candidate_valid is False
        assert result.policy_eligible is False


def test_attempt_transaction_forged_candidate_denied():
    from portable_platform_manager.credential_record import (
        AttemptRecordTransition,
    )
    from portable_platform_manager.windows_storage_boundary import (
        assess_attempt_storage_transaction,
    )

    valid = _synthetic_attempt_transition()

    forged = (
        AttemptRecordTransition(
            True,
            "FORGED_AUTHORITY",
            valid.next_record,
        ),
        AttemptRecordTransition(
            False,
            "CANDIDATE_ONLY_NOT_PERSISTED",
            valid.next_record,
        ),
        AttemptRecordTransition(
            True,
            "CANDIDATE_ONLY_NOT_PERSISTED",
            None,
        ),
    )

    for candidate in forged:
        result = assess_attempt_storage_transaction(
            candidate,
            None,
            platform="win32",
        )

        assert result.authorized is False
        assert result.reason == "INVALID_TRANSITION_CANDIDATE"
        assert result.candidate_valid is False
        assert result.policy_eligible is False


def test_attempt_transaction_declared_evidence_cannot_authorize():
    from portable_platform_manager.storage_policy import StorageEvidence
    from portable_platform_manager.windows_credential_store import (
        WindowsStoreLocation,
    )
    from portable_platform_manager.windows_storage_boundary import (
        WindowsSecurityEvidence,
        assess_attempt_storage_transaction,
    )

    evidence = WindowsSecurityEvidence(
        location=WindowsStoreLocation(
            package_root=r"C:\PPM-Package",
            install_root=r"C:\PPM-Install",
            credential_root=r"C:\PPM-Credentials",
        ),
        storage=StorageEvidence(
            outside_package=True,
            outside_install_tree=True,
            trusted_parent=True,
            protected_acl=True,
            exclusive_lock=True,
            atomic_replace_supported=True,
            current_record_valid=True,
            revision_matches=True,
            enrollment_authorized=False,
            replacement_authorized=False,
        ),
        handle_path_verified=True,
        no_reparse_points=True,
        owner_verified=True,
        acl_verified=True,
        lock_verified=True,
        atomic_write_verified=True,
    )

    result = assess_attempt_storage_transaction(
        _synthetic_attempt_transition(),
        evidence,
        platform="win32",
    )

    assert result.authorized is False
    assert result.candidate_valid is True
    assert result.reason != ""
    if result.policy_eligible:
        assert result.reason == (
            "TRUSTED_WINDOWS_STORAGE_ADAPTER_NOT_IMPLEMENTED"
        )


def test_attempt_transaction_rejects_missing_security_evidence():
    from portable_platform_manager.windows_storage_boundary import (
        assess_attempt_storage_transaction,
    )

    result = assess_attempt_storage_transaction(
        _synthetic_attempt_transition(),
        None,
        platform="win32",
    )

    assert result.authorized is False
    assert result.policy_eligible is False
    assert result.reason == "POLICY_INVALID_WINDOWS_EVIDENCE"

def _p2_observation_inputs():
    from portable_platform_manager.windows_credential_store import (
        WindowsStoreLocation,
        WindowsSameHandleInspection,
        WindowsAclAssessment,
    )

    return (
        WindowsStoreLocation(
            package_root=r"C:\PPM\package",
            install_root=r"C:\PPM\installed",
            credential_root=r"C:\PPM\credentials",
        ),
        WindowsSameHandleInspection(
            True,
            "SAME_HANDLE_OBSERVED_NOT_AUTHORIZED",
        ),
        WindowsAclAssessment(
            True,
            "SYNTHETIC_ACL_POLICY_ONLY",
        ),
    )


def test_observed_store_security_valid_observations_not_authorized():
    from portable_platform_manager.windows_storage_boundary import (
        assess_windows_observed_store_security,
    )

    location, handle, acl = _p2_observation_inputs()
    result = assess_windows_observed_store_security(
        location=location,
        same_handle=handle,
        acl=acl,
        platform="win32",
    )

    assert result.observed is True
    assert result.reason == "OBSERVATIONS_ONLY_NOT_AUTHORIZED"
    assert result.storage_authorized is False


def test_observed_store_security_invalid_handle_denied():
    from portable_platform_manager.windows_storage_boundary import (
        assess_windows_observed_store_security,
    )

    location, _, acl = _p2_observation_inputs()
    result = assess_windows_observed_store_security(
        location=location,
        same_handle=object(),
        acl=acl,
        platform="win32",
    )

    assert result.observed is False
    assert result.reason == "INVALID_HANDLE_OBSERVATION"
    assert result.storage_authorized is False


def test_observed_store_security_unverified_handle_denied():
    from portable_platform_manager.windows_storage_boundary import (
        assess_windows_observed_store_security,
    )
    from portable_platform_manager.windows_credential_store import (
        WindowsSameHandleInspection,
    )

    location, _, acl = _p2_observation_inputs()
    result = assess_windows_observed_store_security(
        location=location,
        same_handle=WindowsSameHandleInspection(
            False,
            "HANDLE_OPEN_FAILED",
        ),
        acl=acl,
        platform="win32",
    )

    assert result.observed is False
    assert result.reason == "HANDLE_OBSERVATION_UNVERIFIED"
    assert result.storage_authorized is False


def test_observed_store_security_invalid_acl_denied():
    from portable_platform_manager.windows_storage_boundary import (
        assess_windows_observed_store_security,
    )

    location, handle, _ = _p2_observation_inputs()
    result = assess_windows_observed_store_security(
        location=location,
        same_handle=handle,
        acl=object(),
        platform="win32",
    )

    assert result.observed is False
    assert result.reason == "INVALID_ACL_ASSESSMENT"
    assert result.storage_authorized is False


def test_observed_store_security_unverified_acl_denied():
    from portable_platform_manager.windows_storage_boundary import (
        assess_windows_observed_store_security,
    )
    from portable_platform_manager.windows_credential_store import (
        WindowsAclAssessment,
    )

    location, handle, _ = _p2_observation_inputs()
    result = assess_windows_observed_store_security(
        location=location,
        same_handle=handle,
        acl=WindowsAclAssessment(
            False,
            "ACL_POLICY_UNVERIFIED",
        ),
        platform="win32",
    )

    assert result.observed is False
    assert result.reason == "ACL_POLICY_UNVERIFIED"
    assert result.storage_authorized is False


def test_observed_store_security_non_windows_denied():
    from portable_platform_manager.windows_storage_boundary import (
        assess_windows_observed_store_security,
    )

    location, handle, acl = _p2_observation_inputs()
    result = assess_windows_observed_store_security(
        location=location,
        same_handle=handle,
        acl=acl,
        platform="linux",
    )

    assert result.observed is False
    assert result.reason == "LOCATION_WINDOWS_REQUIRED"
    assert result.storage_authorized is False


def test_observed_store_security_overlapping_location_denied():
    from portable_platform_manager.windows_storage_boundary import (
        assess_windows_observed_store_security,
    )
    from portable_platform_manager.windows_credential_store import (
        WindowsStoreLocation,
    )

    _, handle, acl = _p2_observation_inputs()
    location = WindowsStoreLocation(
        package_root=r"C:\PPM\package",
        install_root=r"C:\PPM\installed",
        credential_root=r"C:\PPM\package\credentials",
    )

    result = assess_windows_observed_store_security(
        location=location,
        same_handle=handle,
        acl=acl,
        platform="win32",
    )

    assert result.observed is False
    assert result.reason == "LOCATION_PACKAGE_CREDENTIAL_OVERLAP"
    assert result.storage_authorized is False
