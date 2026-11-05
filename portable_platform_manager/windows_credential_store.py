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

    if tail == "\\":
        return ntpath.normcase(normalized)

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


@dataclass(frozen=True)
class WindowsDirectoryInspection:
    """Read-only OS inspection result; not a storage authorization."""

    accepted: bool
    reason: str
    path: str | None = None


def inspect_windows_directory(
    path: object,
    *,
    platform: str | None = None,
) -> WindowsDirectoryInspection:
    """Inspect a Windows directory without modifying filesystem state.

    This first-stage implementation rejects non-Windows systems,
    malformed paths, missing directories, and reparse-point paths.

    It does not establish handle-based identity, ownership, ACL
    safety, exclusive locking, or atomic-write guarantees.
    """

    import os
    import stat

    actual_platform = sys.platform if platform is None else platform

    if actual_platform != "win32":
        return WindowsDirectoryInspection(False, "WINDOWS_REQUIRED")

    canonical = _canonical_declared_path(path)

    if canonical is None:
        return WindowsDirectoryInspection(False, "INVALID_PATH")

    try:
        current = ntpath.splitdrive(canonical)[0] + "\\"

        for component in canonical[len(current):].split("\\"):
            if not component:
                continue

            current = ntpath.join(current, component)
            info = os.lstat(current)

            if info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                return WindowsDirectoryInspection(
                    False,
                    "REPARSE_POINT_DENIED",
                )

            if not stat.S_ISDIR(info.st_mode):
                return WindowsDirectoryInspection(
                    False,
                    "NOT_A_DIRECTORY",
                )

    except (OSError, AttributeError, ValueError):
        return WindowsDirectoryInspection(
            False,
            "DIRECTORY_INSPECTION_FAILED",
        )

    return WindowsDirectoryInspection(
        True,
        "READ_ONLY_PATH_INSPECTED_NOT_AUTHORIZED",
        canonical,
    )


@dataclass(frozen=True)
class WindowsHandleInspection:
    """Read-only handle diagnostic, never credential storage authority."""

    accepted: bool
    reason: str
    final_path: str | None = None


def inspect_windows_directory_handle(
    path: object,
    *,
    platform: str | None = None,
) -> WindowsHandleInspection:
    """Inspect a directory handle without granting storage authority.

    Path components are inspected sequentially. This does not prove
    ancestor safety, owner/ACL safety, locking, or atomic writes.
    The platform override is for synthetic tests, not authorization.
    """

    if sys.platform != "win32":
        return WindowsHandleInspection(False, "WINDOWS_REQUIRED")

    if platform is not None and platform != "win32":
        return WindowsHandleInspection(False, "WINDOWS_REQUIRED")

    canonical = _canonical_declared_path(path)

    if canonical is None:
        return WindowsHandleInspection(False, "INVALID_PATH")

    import ctypes
    from ctypes import wintypes

    FILE_READ_ATTRIBUTES = 0x0080
    FILE_SHARE_READ = 0x00000001
    OPEN_EXISTING = 3
    FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
    FILE_ATTRIBUTE_DIRECTORY = 0x00000010
    FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
    FILE_NAME_NORMALIZED = 0

    class BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("dwFileAttributes", wintypes.DWORD),
            ("ftCreationTime", wintypes.FILETIME),
            ("ftLastAccessTime", wintypes.FILETIME),
            ("ftLastWriteTime", wintypes.FILETIME),
            ("dwVolumeSerialNumber", wintypes.DWORD),
            ("nFileSizeHigh", wintypes.DWORD),
            ("nFileSizeLow", wintypes.DWORD),
            ("nNumberOfLinks", wintypes.DWORD),
            ("nFileIndexHigh", wintypes.DWORD),
            ("nFileIndexLow", wintypes.DWORD),
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    create_file = kernel32.CreateFileW
    create_file.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ]
    create_file.restype = wintypes.HANDLE

    get_info = kernel32.GetFileInformationByHandle
    get_info.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(BY_HANDLE_FILE_INFORMATION),
    ]
    get_info.restype = wintypes.BOOL

    get_final_path = kernel32.GetFinalPathNameByHandleW
    get_final_path.argtypes = [
        wintypes.HANDLE,
        wintypes.LPWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
    ]
    get_final_path.restype = wintypes.DWORD

    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL

    invalid_handle = ctypes.c_void_p(-1).value

    drive, tail = ntpath.splitdrive(canonical)
    current = drive + "\\"
    components = [part for part in tail.split("\\") if part]
    paths = [current]

    for component in components:
        current = ntpath.join(current, component)
        paths.append(current)

    for inspected_path in paths:
        handle = create_file(
            inspected_path,
            FILE_READ_ATTRIBUTES,
            FILE_SHARE_READ,
            None,
            OPEN_EXISTING,
            FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT,
            None,
        )

        if handle in (None, invalid_handle):
            return WindowsHandleInspection(False, "HANDLE_OPEN_FAILED")

        try:
            info = BY_HANDLE_FILE_INFORMATION()

            if not get_info(handle, ctypes.byref(info)):
                return WindowsHandleInspection(False, "HANDLE_INFO_FAILED")

            if info.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT:
                return WindowsHandleInspection(
                    False,
                    "REPARSE_POINT_DENIED",
                )

            if not info.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY:
                return WindowsHandleInspection(
                    False,
                    "NOT_A_DIRECTORY",
                )

            required = get_final_path(
                handle,
                None,
                0,
                FILE_NAME_NORMALIZED,
            )

            if required == 0 or required > 32768:
                return WindowsHandleInspection(
                    False,
                    "FINAL_PATH_FAILED",
                )

            buffer = ctypes.create_unicode_buffer(required + 1)

            written = get_final_path(
                handle,
                buffer,
                len(buffer),
                FILE_NAME_NORMALIZED,
            )

            if written == 0 or written >= len(buffer):
                return WindowsHandleInspection(
                    False,
                    "FINAL_PATH_FAILED",
                )

            final_path = buffer.value

            if not final_path.startswith("\\\\?\\"):
                return WindowsHandleInspection(
                    False,
                    "UNEXPECTED_FINAL_PATH",
                )

            normalized_final = _canonical_declared_path(
                final_path[4:]
            )

            if normalized_final != ntpath.normcase(inspected_path):
                return WindowsHandleInspection(
                    False,
                    "HANDLE_PATH_MISMATCH",
                )

        finally:
            close_handle(handle)

    return WindowsHandleInspection(
        True,
        "ANCESTOR_HANDLES_INSPECTED_NOT_AUTHORIZED",
        canonical,
    )
@dataclass(frozen=True)
class WindowsAclEntry:
    """Synthetic ACE declaration; not verified Windows OS evidence."""

    sid: str
    access_type: str
    rights: int
    inherited: bool


@dataclass(frozen=True)
class WindowsAclAssessment:
    """Policy result only; never grants credential storage authority."""

    accepted: bool
    reason: str


def _valid_synthetic_sid(value: object) -> bool:
    """Validate canonical numeric SID syntax without resolving identity."""
    if type(value) is not str:
        return False

    parts = value.split("-")

    if len(parts) < 4 or parts[0] != "S" or parts[1] != "1":
        return False

    if len(parts) > 18:
        return False

    for part in parts[2:]:
        if not part or not part.isascii() or not part.isdecimal():
            return False
        if len(part) > 1 and part.startswith("0"):
            return False

    authority = int(parts[2])
    if authority > 0xFFFFFFFFFFFF:
        return False

    return all(int(part) <= 0xFFFFFFFF for part in parts[3:])


_SYNTHETIC_ALLOWED_RIGHTS = (
    0x001F01FF  # FileSystemRights.FullControl mask
    | 0x10000000  # GENERIC_ALL
    | 0x80000000  # GENERIC_READ
    | 0x40000000  # GENERIC_WRITE
    | 0x20000000  # GENERIC_EXECUTE
)

_SYNTHETIC_DANGEROUS_RIGHTS = (
    0x00000002  # FILE_WRITE_DATA
    | 0x00000004  # FILE_APPEND_DATA
    | 0x00000010  # FILE_WRITE_EA
    | 0x00000040  # FILE_DELETE_CHILD
    | 0x00000100  # FILE_WRITE_ATTRIBUTES
    | 0x00010000  # DELETE
    | 0x00040000  # WRITE_DAC
    | 0x00080000  # WRITE_OWNER
    | 0x10000000  # GENERIC_ALL
    | 0x40000000  # GENERIC_WRITE
    | 0x20000000  # GENERIC_EXECUTE_DENIED_FOR_UNTRUSTED
)


def assess_synthetic_windows_acl(
    *,
    owner_sid: object,
    expected_owner_sid: object,
    protected_dacl: object,
    entries: object,
    trusted_sids: object,
) -> WindowsAclAssessment:
    """Fail-closed evaluation of synthetic ACL declarations.

    This is not a Windows access-check algorithm, effective-rights
    calculation, OS security descriptor inspection, or authorization.
    """

    if (
        not _valid_synthetic_sid(owner_sid)
        or not _valid_synthetic_sid(expected_owner_sid)
        or owner_sid != expected_owner_sid
    ):
        return WindowsAclAssessment(False, "OWNER_UNVERIFIED")

    if protected_dacl is not True:
        return WindowsAclAssessment(False, "DACL_NOT_PROTECTED")

    if (
        type(trusted_sids) not in (tuple, frozenset)
        or not trusted_sids
        or any(
            not _valid_synthetic_sid(sid)
            for sid in trusted_sids
        )
        or owner_sid not in trusted_sids
    ):
        return WindowsAclAssessment(False, "INVALID_TRUSTED_SIDS")

    if type(entries) not in (tuple, list) or not entries:
        return WindowsAclAssessment(False, "INVALID_ACL_ENTRIES")

    for entry in entries:
        if type(entry) is not WindowsAclEntry:
            return WindowsAclAssessment(False, "INVALID_ACL_ENTRY")

        if (
            not _valid_synthetic_sid(entry.sid)
            or entry.access_type not in ("ALLOW", "DENY")
            or type(entry.rights) is not int
            or entry.rights < 0
            or entry.rights > 0xFFFFFFFF
            or (entry.rights & ~_SYNTHETIC_ALLOWED_RIGHTS) != 0
            or type(entry.inherited) is not bool
        ):
            return WindowsAclAssessment(False, "INVALID_ACL_ENTRY")

        if entry.inherited:
            return WindowsAclAssessment(False, "INHERITED_ACE_UNVERIFIED")

        if entry.sid not in trusted_sids:
            if entry.access_type == "ALLOW" and (
                entry.rights & _SYNTHETIC_DANGEROUS_RIGHTS
            ):
                return WindowsAclAssessment(
                    False,
                    "UNTRUSTED_WRITE_RIGHTS",
                )

    return WindowsAclAssessment(
        True,
        "SYNTHETIC_POLICY_ONLY_NOT_AUTHORIZED",
    )
@dataclass(frozen=True)
class WindowsSecurityDescriptorInspection:
    """Read-only observation; never a credential storage authorization."""

    inspected: bool
    reason: str
    owner_sid: str | None = None
    dacl_present: bool = False
    dacl_null: bool = True


def _denied_windows_security_descriptor(
    reason: str,
) -> WindowsSecurityDescriptorInspection:
    """Fail closed without claiming actual Windows ACL verification."""
    return WindowsSecurityDescriptorInspection(
        inspected=False,
        reason=reason,
        owner_sid=None,
        dacl_present=False,
        dacl_null=True,
    )

def _inspect_security_descriptor_from_handle(
    handle: object,
) -> WindowsSecurityDescriptorInspection:
    """Observe owner and DACL from an already-open Windows handle.

    This is not an ACL effectiveness assessment or storage authorization.
    The caller owns and must close the handle.
    """
    if sys.platform != "win32":
        return _denied_windows_security_descriptor("WINDOWS_REQUIRED")

    import ctypes
    from ctypes import wintypes

    if type(handle) is not int or handle in (0, -1):
        return _denied_windows_security_descriptor("INVALID_HANDLE")

    if handle < 0 or handle > ctypes.c_void_p(-1).value:
        return _denied_windows_security_descriptor("INVALID_HANDLE")

    if handle == ctypes.c_void_p(-1).value:
        return _denied_windows_security_descriptor("INVALID_HANDLE")

    OWNER_SECURITY_INFORMATION = 0x00000001
    DACL_SECURITY_INFORMATION = 0x00000004
    SE_FILE_OBJECT = 1

    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    get_security_info = advapi32.GetSecurityInfo
    get_security_info.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_void_p),
    ]
    get_security_info.restype = wintypes.DWORD

    convert_sid = advapi32.ConvertSidToStringSidW
    convert_sid.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_void_p),
    ]
    convert_sid.restype = wintypes.BOOL

    local_free = kernel32.LocalFree
    local_free.argtypes = [ctypes.c_void_p]
    local_free.restype = ctypes.c_void_p

    owner = ctypes.c_void_p()
    dacl = ctypes.c_void_p()
    descriptor = ctypes.c_void_p()
    sid_string = ctypes.c_void_p()

    try:
        status = get_security_info(
            handle,
            SE_FILE_OBJECT,
            OWNER_SECURITY_INFORMATION | DACL_SECURITY_INFORMATION,
            ctypes.byref(owner),
            None,
            ctypes.byref(dacl),
            None,
            ctypes.byref(descriptor),
        )

        if status != 0:
            return _denied_windows_security_descriptor(
                "SECURITY_INFO_FAILED"
            )

        if not descriptor.value or not owner.value:
            return _denied_windows_security_descriptor(
                "OWNER_OR_DESCRIPTOR_MISSING"
            )

        if not dacl.value:
            return _denied_windows_security_descriptor(
                "NULL_OR_MISSING_DACL"
            )

        if not convert_sid(owner, ctypes.byref(sid_string)):
            return _denied_windows_security_descriptor(
                "OWNER_SID_CONVERSION_FAILED"
            )

        if not sid_string.value:
            return _denied_windows_security_descriptor(
                "OWNER_SID_MISSING"
            )

        owner_sid = ctypes.wstring_at(sid_string.value)

        if not _valid_synthetic_sid(owner_sid):
            return _denied_windows_security_descriptor(
                "OWNER_SID_INVALID"
            )

        return WindowsSecurityDescriptorInspection(
            inspected=True,
            reason="HANDLE_SECURITY_OBSERVED_NOT_AUTHORIZED",
            owner_sid=owner_sid,
            dacl_present=True,
            dacl_null=False,
        )
    finally:
        if sid_string.value:
            local_free(sid_string)
        if descriptor.value:
            local_free(descriptor)
