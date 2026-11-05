"""Declarative encrypted archive contract.

No archive creation, filesystem writes, subprocess execution, or secrets.
An accepted declaration does not authorize archive execution.
"""

from __future__ import annotations

from dataclasses import dataclass


SUPPORTED_FORMATS = frozenset({"zip", "7z"})


@dataclass(frozen=True)
class ArchiveContractDecision:
    accepted: bool
    reason: str
    archive_format: str | None = None
    filename_encryption: bool = False


def assess_archive_contract(
    archive_format: object,
    *,
    encryption: object = "AES256",
    filename_encryption: object = False,
    password_delivery: object = "INTERACTIVE_EXTERNAL_TOOL",
    execution_requested: object = False,
) -> ArchiveContractDecision:
    """Validate declared archive properties without executing anything."""

    if type(archive_format) is not str or archive_format not in SUPPORTED_FORMATS:
        return ArchiveContractDecision(False, "UNSUPPORTED_ARCHIVE_FORMAT")

    if encryption != "AES256" or type(encryption) is not str:
        return ArchiveContractDecision(False, "ENCRYPTION_NOT_ACCEPTED")

    if type(filename_encryption) is not bool:
        return ArchiveContractDecision(False, "INVALID_FILENAME_ENCRYPTION")

    if filename_encryption and archive_format != "7z":
        return ArchiveContractDecision(False, "ZIP_FILENAME_ENCRYPTION_UNSUPPORTED")

    if (
        type(password_delivery) is not str
        or password_delivery != "INTERACTIVE_EXTERNAL_TOOL"
    ):
        return ArchiveContractDecision(False, "UNSAFE_PASSWORD_DELIVERY")

    if type(execution_requested) is not bool:
        return ArchiveContractDecision(False, "INVALID_EXECUTION_REQUEST")

    if execution_requested:
        return ArchiveContractDecision(False, "EXECUTION_NOT_AUTHORIZED")

    return ArchiveContractDecision(
        True,
        "DECLARATION_ONLY",
        archive_format,
        filename_encryption,
    )
