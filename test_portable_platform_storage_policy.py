"""Synthetic-only tests for PPM storage precondition policy."""

from dataclasses import replace

import pytest

from portable_platform_manager.storage_policy import (
    StorageEvidence,
    StorageOperation,
    assess_storage_preconditions,
)


def evidence(**overrides):
    values = dict(
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
    )
    values.update(overrides)
    return StorageEvidence(**values)


@pytest.mark.parametrize(
    "operation",
    [
        StorageOperation.UPDATE_ATTEMPTS,
        StorageOperation.REPLACE_CREDENTIAL,
        StorageOperation.ENROLL,
    ],
)
def test_missing_evidence_denied(operation):
    result = assess_storage_preconditions(operation, None)

    assert result.eligible is False
    assert result.reason == "INVALID_EVIDENCE"


@pytest.mark.parametrize(
    "field",
    [
        "outside_package",
        "outside_install_tree",
        "trusted_parent",
        "protected_acl",
        "exclusive_lock",
        "atomic_replace_supported",
    ],
)
def test_missing_common_boundary_denied(field):
    result = assess_storage_preconditions(
        StorageOperation.UPDATE_ATTEMPTS,
        replace(evidence(), **{field: False}),
    )

    assert result.eligible is False
    assert result.reason == "STORAGE_BOUNDARY_UNVERIFIED"


def test_update_attempts_declared_eligible():
    result = assess_storage_preconditions(
        StorageOperation.UPDATE_ATTEMPTS,
        evidence(),
    )

    assert result.eligible is True
    assert result.reason == "PRECONDITIONS_DECLARED_ONLY"


def test_initial_enrollment_declared_eligible():
    result = assess_storage_preconditions(
        StorageOperation.ENROLL,
        evidence(
            current_record_valid=False,
            enrollment_authorized=True,
        ),
    )

    assert result.eligible is True
    assert result.reason == "PRECONDITIONS_DECLARED_ONLY"


def test_enrollment_without_authority_denied():
    result = assess_storage_preconditions(
        StorageOperation.ENROLL,
        evidence(current_record_valid=False),
    )

    assert result.eligible is False
    assert result.reason == "ENROLLMENT_AUTHORITY_MISSING"


def test_enrollment_with_existing_record_denied():
    result = assess_storage_preconditions(
        StorageOperation.ENROLL,
        evidence(enrollment_authorized=True),
    )

    assert result.eligible is False
    assert result.reason == "EXISTING_CREDENTIAL_PRESENT"


def test_update_with_invalid_current_record_denied():
    result = assess_storage_preconditions(
        StorageOperation.UPDATE_ATTEMPTS,
        evidence(current_record_valid=False),
    )

    assert result.eligible is False
    assert result.reason == "CURRENT_RECORD_INVALID"


def test_update_with_revision_conflict_denied():
    result = assess_storage_preconditions(
        StorageOperation.UPDATE_ATTEMPTS,
        evidence(revision_matches=False),
    )

    assert result.eligible is False
    assert result.reason == "REVISION_CONFLICT"


def test_replacement_without_authority_denied():
    result = assess_storage_preconditions(
        StorageOperation.REPLACE_CREDENTIAL,
        evidence(),
    )

    assert result.eligible is False
    assert result.reason == "REPLACEMENT_AUTHORITY_MISSING"


def test_replacement_with_authority_declared_eligible():
    result = assess_storage_preconditions(
        StorageOperation.REPLACE_CREDENTIAL,
        evidence(replacement_authorized=True),
    )

    assert result.eligible is True
    assert result.reason == "PRECONDITIONS_DECLARED_ONLY"


@pytest.mark.parametrize(
    "invalid_operation",
    [
        None,
        "update_attempts",
        1,
        True,
    ],
)
def test_invalid_operation_denied(invalid_operation):
    result = assess_storage_preconditions(
        invalid_operation,
        evidence(),
    )

    assert result.eligible is False
    assert result.reason == "INVALID_OPERATION"


@pytest.mark.parametrize(
    "invalid_value",
    [
        None,
        1,
        "true",
    ],
)
def test_nonboolean_evidence_denied(invalid_value):
    result = assess_storage_preconditions(
        StorageOperation.UPDATE_ATTEMPTS,
        replace(evidence(), protected_acl=invalid_value),
    )

    assert result.eligible is False
    assert result.reason == "INVALID_EVIDENCE_FIELD"


def test_evidence_is_immutable():
    item = evidence()

    with pytest.raises(AttributeError):
        item.protected_acl = False


def test_decision_does_not_authorize_file_writes():
    result = assess_storage_preconditions(
        StorageOperation.UPDATE_ATTEMPTS,
        evidence(),
    )

    assert result.eligible is True
    assert result.reason == "PRECONDITIONS_DECLARED_ONLY"
    assert not hasattr(result, "write_authorized")
    assert not hasattr(result, "execution_authorized")
