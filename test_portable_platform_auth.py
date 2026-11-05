"""Synthetic-only PPM administrator authentication tests."""

import pytest

from portable_platform_manager.auth import (
    ProtectedOperation,
    assess_protected_operation,
    create_admin_hash,
    validate_passphrase,
    verify_admin_hash,
)


SYNTHETIC_PASSPHRASE = "Synthetic-PPM-Admin-2026!"


def test_valid_synthetic_passphrase():
    assert validate_passphrase(SYNTHETIC_PASSPHRASE) is True


@pytest.mark.parametrize(
    "value",
    [
        None,
        12345678901234,
        "",
        "short",
        "1234567",
        "a" * 257,
        "valid-password\n",
        "valid-password\x00",
    ],
)
def test_invalid_passphrase_is_denied(value):
    assert validate_passphrase(value) is False


def test_salted_hash_is_not_plaintext_and_verifies():
    first = create_admin_hash(SYNTHETIC_PASSPHRASE)
    second = create_admin_hash(SYNTHETIC_PASSPHRASE)

    assert first != SYNTHETIC_PASSPHRASE
    assert first != second
    assert verify_admin_hash(first, SYNTHETIC_PASSPHRASE)
    assert verify_admin_hash(second, SYNTHETIC_PASSPHRASE)


def test_wrong_password_is_denied():
    stored = create_admin_hash(SYNTHETIC_PASSPHRASE)

    assert not verify_admin_hash(
        stored,
        "Synthetic-Wrong-Admin-2026!",
    )


@pytest.mark.parametrize(
    "stored",
    [
        None,
        "",
        "plaintext-password",
        "scrypt:32768:8:1$invalid",
        "pbkdf2:sha256:1$salt$hash",
        12345,
    ],
)
def test_malformed_or_unsupported_hash_is_denied(stored):
    assert not verify_admin_hash(
        stored,
        SYNTHETIC_PASSPHRASE,
    )


@pytest.mark.parametrize("operation", list(ProtectedOperation))
def test_protected_operations_require_valid_password(operation):
    stored = create_admin_hash(SYNTHETIC_PASSPHRASE)

    accepted = assess_protected_operation(
        operation,
        stored_hash=stored,
        passphrase=SYNTHETIC_PASSPHRASE,
    )

    denied = assess_protected_operation(
        operation,
        stored_hash=stored,
        passphrase="Synthetic-Wrong-Admin-2026!",
    )

    assert accepted.authorized is True
    assert accepted.reason == "PASSWORD_VERIFIED_ONLY"
    assert denied.authorized is False
    assert denied.reason == "AUTHENTICATION_DENIED"


@pytest.mark.parametrize(
    "operation",
    [
        None,
        "install",
        "uninstall",
        "delete_data",
        1,
        True,
    ],
)
def test_untyped_operations_are_denied(operation):
    stored = create_admin_hash(SYNTHETIC_PASSPHRASE)

    result = assess_protected_operation(
        operation,
        stored_hash=stored,
        passphrase=SYNTHETIC_PASSPHRASE,
    )

    assert result.authorized is False
    assert result.reason == "INVALID_OPERATION"


def test_missing_password_is_denied():
    stored = create_admin_hash(SYNTHETIC_PASSPHRASE)

    result = assess_protected_operation(
        ProtectedOperation.UNINSTALL,
        stored_hash=stored,
        passphrase=None,
    )

    assert result.authorized is False


def test_existing_seven_digit_web_admin_password_is_not_accepted():
    assert validate_passphrase("1234567") is False


def test_authentication_does_not_perform_install_or_delete():
    stored = create_admin_hash(SYNTHETIC_PASSPHRASE)

    result = assess_protected_operation(
        ProtectedOperation.UNINSTALL,
        stored_hash=stored,
        passphrase=SYNTHETIC_PASSPHRASE,
    )

    assert result.authorized is True
    assert result.reason == "PASSWORD_VERIFIED_ONLY"

def test_integrated_auth_success_never_authorizes_execution():
    from portable_platform_manager.auth import (
        ProtectedOperation,
        assess_protected_operation_with_attempts,
        create_admin_hash,
    )
    from portable_platform_manager.auth_attempts import AttemptState

    password = "Synthetic-PPM-Admin-2026!"
    stored_hash = create_admin_hash(password)

    result = assess_protected_operation_with_attempts(
        ProtectedOperation.INSTALL,
        stored_hash=stored_hash,
        passphrase=password,
        attempt_state=AttemptState(),
        now=1000.0,
    )

    assert result.password_accepted is True
    assert result.reason == "PASSWORD_AND_ATTEMPT_POLICY_VERIFIED_ONLY"
    assert result.next_state == AttemptState()
    assert result.execution_authorized is False


def test_integrated_auth_failure_increments_once():
    from portable_platform_manager.auth import (
        ProtectedOperation,
        assess_protected_operation_with_attempts,
        create_admin_hash,
    )
    from portable_platform_manager.auth_attempts import AttemptState

    stored_hash = create_admin_hash("Synthetic-PPM-Admin-2026!")

    result = assess_protected_operation_with_attempts(
        ProtectedOperation.UPDATE,
        stored_hash=stored_hash,
        passphrase="Wrong-Synthetic-Password!",
        attempt_state=AttemptState(failures=2),
        now=1000.0,
    )

    assert result.password_accepted is False
    assert result.reason == "AUTHENTICATION_DENIED"
    assert result.next_state == AttemptState(failures=3)
    assert result.execution_authorized is False


def test_integrated_auth_fifth_failure_locks():
    from portable_platform_manager.auth import (
        ProtectedOperation,
        assess_protected_operation_with_attempts,
        create_admin_hash,
    )
    from portable_platform_manager.auth_attempts import (
        AttemptState,
        LOCK_SECONDS,
        MAX_FAILURES,
    )

    stored_hash = create_admin_hash("Synthetic-PPM-Admin-2026!")

    result = assess_protected_operation_with_attempts(
        ProtectedOperation.DELETE_DATA,
        stored_hash=stored_hash,
        passphrase="Wrong-Synthetic-Password!",
        attempt_state=AttemptState(failures=4),
        now=1000.0,
    )

    assert result.password_accepted is False
    assert result.reason == "LOCKED"
    assert result.next_state == AttemptState(
        failures=MAX_FAILURES,
        locked_until=1000.0 + LOCK_SECONDS,
    )
    assert result.execution_authorized is False


def test_integrated_auth_active_lock_denies_correct_password():
    from portable_platform_manager.auth import (
        ProtectedOperation,
        assess_protected_operation_with_attempts,
        create_admin_hash,
    )
    from portable_platform_manager.auth_attempts import AttemptState

    password = "Synthetic-PPM-Admin-2026!"
    stored_hash = create_admin_hash(password)
    locked = AttemptState(failures=5, locked_until=1900.0)

    result = assess_protected_operation_with_attempts(
        ProtectedOperation.UNINSTALL,
        stored_hash=stored_hash,
        passphrase=password,
        attempt_state=locked,
        now=1000.0,
    )

    assert result.password_accepted is False
    assert result.reason == "LOCKED"
    assert result.next_state == locked
    assert result.execution_authorized is False


def test_integrated_auth_lock_expiry_allows_password_proof_only():
    from portable_platform_manager.auth import (
        ProtectedOperation,
        assess_protected_operation_with_attempts,
        create_admin_hash,
    )
    from portable_platform_manager.auth_attempts import AttemptState

    password = "Synthetic-PPM-Admin-2026!"
    stored_hash = create_admin_hash(password)

    result = assess_protected_operation_with_attempts(
        ProtectedOperation.RESTORE_OVERWRITE,
        stored_hash=stored_hash,
        passphrase=password,
        attempt_state=AttemptState(failures=5, locked_until=1900.0),
        now=1900.0,
    )

    assert result.password_accepted is True
    assert result.next_state == AttemptState()
    assert result.execution_authorized is False


def test_integrated_auth_invalid_state_or_time_fails_closed():
    from portable_platform_manager.auth import (
        ProtectedOperation,
        assess_protected_operation_with_attempts,
        create_admin_hash,
    )
    from portable_platform_manager.auth_attempts import AttemptState

    password = "Synthetic-PPM-Admin-2026!"
    stored_hash = create_admin_hash(password)

    for state, now in (
        (None, 1000.0),
        (AttemptState(failures=-1), 1000.0),
        (AttemptState(), -1),
        (AttemptState(), float("nan")),
        (AttemptState(), "1000"),
    ):
        result = assess_protected_operation_with_attempts(
            ProtectedOperation.INSTALL,
            stored_hash=stored_hash,
            passphrase=password,
            attempt_state=state,
            now=now,
        )

        assert result.password_accepted is False
        assert result.reason == "INVALID_STATE_OR_TIME"
        assert result.execution_authorized is False


def test_integrated_auth_invalid_operation_denied():
    from portable_platform_manager.auth import (
        assess_protected_operation_with_attempts,
    )
    from portable_platform_manager.auth_attempts import AttemptState

    result = assess_protected_operation_with_attempts(
        "install",
        stored_hash="invalid",
        passphrase="Synthetic-PPM-Admin-2026!",
        attempt_state=AttemptState(),
        now=1000.0,
    )

    assert result.password_accepted is False
    assert result.operation is None
    assert result.reason == "INVALID_OPERATION"
    assert result.execution_authorized is False
