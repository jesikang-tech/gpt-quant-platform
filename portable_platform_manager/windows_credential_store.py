"""Windows-only PPM credential store foundation.

This module validates declared storage locations only.
It does not create directories, read credentials, modify ACLs,
or authorize credential writes.

Lexical path checks are not sufficient against junctions,
symlinks, reparse points, or concurrent filesystem changes.
Those require trusted handle-based verification before IO.
"""

from __future__ import annotations

import ntpath
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class WindowsStoreLocation:
    package_root: str
    install_root: str
    credential_root: str


@dataclass(frozen=True)
class LocationDecision:
    eligible: bool
    reason: str


def _canonical_declared_path(value: object) -> str | None:
    if type(value) is not str or not value:
        return None

    if "\x00" in value or any(ord(char) < 32 for char in value):
        return None

    if "/" in value:
        return None

    if not ntpath.isabs(value):
        return None

    drive, tail = ntpath.splitdrive(value)

    if len(drive) != 2 or drive[1] != ":":
        return None

    if not drive[0].isalpha():
        return None

    if not tail.startswith("\\"):
        return None

    normalized = ntpath.normpath(value)

    if normalized != value:
        return None

    parts = tail.split("\\")

    reserved = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{index}" for index in range(1, 10)),
        *(f"LPT{index}" for index in range(1, 10)),
        *(f"COM{char}" for char in "\u00b9\u00b2\u00b3"),
        *(f"LPT{char}" for char in "\u00b9\u00b2\u00b3"),
    }

    for part in parts[1:]:
        if not part:
            return None

        if part in (".", ".."):
            return None

        if part.endswith((" ", ".")):
            return None

        if any(char in part for char in '<>:"|?*'):
            return None

        if any(ord(char) < 32 for char in part):
            return None

        device_name = part.split(".", 1)[0].upper()

        if device_name in reserved:
            return None

    return ntpath.normcase(normalized)


def _overlaps(left: str, right: str) -> bool:
    return (
        left == right
        or left.startswith(right.rstrip("\\") + "\\")
        or right.startswith(left.rstrip("\\") + "\\")
    )


def assess_windows_store_location(
    location: object,
    *,
    platform: str | None = None,
) -> LocationDecision:
    """Check lexical separation; never grant filesystem authority."""

    actual_platform = sys.platform if platform is None else platform

    if actual_platform != "win32":
        return LocationDecision(False, "WINDOWS_REQUIRED")

    if type(location) is not WindowsStoreLocation:
        return LocationDecision(False, "INVALID_LOCATION")

    package = _canonical_declared_path(location.package_root)
    install = _canonical_declared_path(location.install_root)
    credential = _canonical_declared_path(location.credential_root)

    if package is None or install is None or credential is None:
        return LocationDecision(False, "INVALID_PATH")

    if _overlaps(credential, package):
        return LocationDecision(False, "PACKAGE_CREDENTIAL_OVERLAP")

    if _overlaps(credential, install):
        return LocationDecision(False, "INSTALL_CREDENTIAL_OVERLAP")

    return LocationDecision(True, "LEXICAL_SEPARATION_ONLY")
