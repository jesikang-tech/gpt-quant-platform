"""Independent PPM administrative authentication primitives.

This module performs no filesystem, database, or network access.
It does not import platform-specific authentication configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from werkzeug.security import check_password_hash, generate_password_hash


MIN_PASSPHRASE_LENGTH = 14
MAX_PASSPHRASE_LENGTH = 256

_HASH_METHOD = "scrypt:32768:8:1"


class ProtectedOperation(str, Enum):
    INSTALL = "install"
    REINSTALL = "reinstall"
    UPDATE = "update"
    UNINSTALL = "uninstall"
    RESTORE_OVERWRITE = "restore_overwrite"
    DELETE_DATA = "delete_data"


@dataclass(frozen=True)
class AuthenticationDecision:
    authorized: bool
    operation: ProtectedOperation | None
    reason: str


def validate_passphrase(passphrase: object) -> bool:
    """Validate a strong PPM passphrase without logging its value."""

    if not isinstance(passphrase, str):
        return False

    if not (
        MIN_PASSPHRASE_LENGTH
        <= len(passphrase)
        <= MAX_PASSPHRASE_LENGTH
    ):
        return False

    if any(ord(char) < 32 or ord(char) == 127 for char in passphrase):
        return False

    return True


def create_admin_hash(passphrase: str) -> str:
    """Generate a salted administrator hash for separate enrollment."""

    if not validate_passphrase(passphrase):
        raise ValueError("invalid PPM administrator passphrase")

    return generate_password_hash(passphrase, method=_HASH_METHOD)


def verify_admin_hash(stored_hash: object, passphrase: object) -> bool:
    """Fail closed for malformed credentials and invalid passwords."""

    if not isinstance(stored_hash, str):
        return False

    if not validate_passphrase(passphrase):
        return False

    if not stored_hash.startswith(_HASH_METHOD + "$"):
        return False

    try:
        return bool(check_password_hash(stored_hash, passphrase))
    except (ValueError, TypeError, OverflowError):
        return False


def assess_protected_operation(
    operation: object,
    *,
    stored_hash: object,
    passphrase: object,
) -> AuthenticationDecision:
    """Assess password proof without performing the protected action."""

    if type(operation) is not ProtectedOperation:
        return AuthenticationDecision(
            authorized=False,
            operation=None,
            reason="INVALID_OPERATION",
        )

    if not verify_admin_hash(stored_hash, passphrase):
        return AuthenticationDecision(
            authorized=False,
            operation=operation,
            reason="AUTHENTICATION_DENIED",
        )

    return AuthenticationDecision(
        authorized=True,
        operation=operation,
        reason="PASSWORD_VERIFIED_ONLY",
    )
