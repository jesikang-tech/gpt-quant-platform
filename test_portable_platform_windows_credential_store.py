"""Synthetic-only tests for Windows PPM credential location validation."""

from dataclasses import replace

import pytest

from portable_platform_manager.windows_credential_store import (
    WindowsStoreLocation,
    assess_windows_store_location,
)


def location(**overrides):
    values = dict(
        package_root=r"C:\PPM\Packages\Platform5",
        install_root=r"D:\Platforms\Platform5",
        credential_root=r"C:\ProgramData\PPM\Credentials",
    )
    values.update(overrides)
    return WindowsStoreLocation(**values)


def assess(item, platform="win32"):
    return assess_windows_store_location(item, platform=platform)


def test_separate_windows_locations_declared_eligible():
    result = assess(location())

    assert result.eligible is True
    assert result.reason == "LEXICAL_SEPARATION_ONLY"


@pytest.mark.parametrize("platform", ["linux", "darwin", "", "WIN32"])
def test_nonwindows_platform_denied(platform):
    result = assess(location(), platform=platform)

    assert result.eligible is False
    assert result.reason == "WINDOWS_REQUIRED"


@pytest.mark.parametrize(
    "invalid",
    [None, {}, "C:\\PPM", True, 1],
)
def test_invalid_location_object_denied(invalid):
    result = assess(invalid)

    assert result.eligible is False
    assert result.reason == "INVALID_LOCATION"


@pytest.mark.parametrize(
    "invalid_path",
    [
        "",
        "relative\\credentials",
        "C:relative\\credentials",
        "\\rooted\\credentials",
        "C:/ProgramData/PPM",
        "C:\\ProgramData\\..\\Secrets",
        "C:\\ProgramData\\.\\Secrets",
        "C:\\ProgramData\\Secrets\\",
        "C:\\ProgramData\\Secret ",
        "C:\\ProgramData\\Secret.",
        "C:\\ProgramData\\Secrets:stream",
        "C:\\ProgramData\\Secrets\x00hidden",
        "C:\\ProgramData\\Secrets\nhidden",
        "\\\\server\\share\\secrets",
    ],
)
def test_invalid_credential_path_denied(invalid_path):
    result = assess(location(credential_root=invalid_path))

    assert result.eligible is False
    assert result.reason == "INVALID_PATH"


@pytest.mark.parametrize(
    "invalid",
    [None, 1, True, [], {}],
)
def test_nonstring_credential_path_denied(invalid):
    result = assess(location(credential_root=invalid))

    assert result.eligible is False
    assert result.reason == "INVALID_PATH"


@pytest.mark.parametrize(
    "field",
    ["package_root", "install_root"],
)
def test_equal_credential_root_denied(field):
    source = location()
    result = assess(
        replace(source, credential_root=getattr(source, field))
    )

    assert result.eligible is False
    assert result.reason in (
        "PACKAGE_CREDENTIAL_OVERLAP",
        "INSTALL_CREDENTIAL_OVERLAP",
    )


def test_credential_root_inside_package_denied():
    result = assess(
        location(
            credential_root=r"C:\PPM\Packages\Platform5\Secrets",
        )
    )

    assert result.eligible is False
    assert result.reason == "PACKAGE_CREDENTIAL_OVERLAP"


def test_package_inside_credential_root_denied():
    result = assess(
        location(
            credential_root=r"C:\PPM",
        )
    )

    assert result.eligible is False
    assert result.reason == "PACKAGE_CREDENTIAL_OVERLAP"


def test_credential_root_inside_install_denied():
    result = assess(
        location(
            credential_root=r"D:\Platforms\Platform5\Secrets",
        )
    )

    assert result.eligible is False
    assert result.reason == "INSTALL_CREDENTIAL_OVERLAP"


def test_install_inside_credential_root_denied():
    result = assess(
        location(
            credential_root=r"D:\Platforms",
        )
    )

    assert result.eligible is False
    assert result.reason == "INSTALL_CREDENTIAL_OVERLAP"


def test_windows_case_insensitive_overlap_denied():
    result = assess(
        location(
            credential_root=r"c:\ppm\packages\platform5\secrets",
        )
    )

    assert result.eligible is False
    assert result.reason == "PACKAGE_CREDENTIAL_OVERLAP"


def test_sibling_path_is_not_false_overlap():
    result = assess(
        location(
            credential_root=r"C:\PPM\Packages\Platform5-Other",
        )
    )

    assert result.eligible is True
    assert result.reason == "LEXICAL_SEPARATION_ONLY"


@pytest.mark.parametrize(
    "field",
    ["package_root", "install_root"],
)
def test_invalid_other_root_denied(field):
    result = assess(
        location(**{field: "..\\invalid"})
    )

    assert result.eligible is False
    assert result.reason == "INVALID_PATH"


def test_location_is_immutable():
    item = location()

    with pytest.raises(AttributeError):
        item.credential_root = r"C:\Other"


def test_declared_location_does_not_grant_write_authority():
    result = assess(location())

    assert result.eligible is True
    assert result.reason == "LEXICAL_SEPARATION_ONLY"
    assert not hasattr(result, "write_authorized")
    assert not hasattr(result, "acl_verified")


@pytest.mark.parametrize(
    "invalid_path",
    [
        r"C:\ProgramData\PPM\CON",
        r"C:\ProgramData\PPM\nul.txt",
        r"C:\ProgramData\PPM\COM1",
        r"C:\ProgramData\PPM\LPT9.log",
        r"C:\ProgramData\PPM\AUX",
        r"C:\ProgramData\PPM\bad<name",
        r"C:\ProgramData\PPM\bad>name",
        r"C:\ProgramData\PPM\bad|name",
        r"C:\ProgramData\PPM\bad?name",
        r"C:\ProgramData\PPM\bad*name",
        "C:\\ProgramData\\PPM\\COM\u00b9",
        "C:\\ProgramData\\PPM\\LPT\u00b2",
        r"C:\ProgramData\\PPM",
    ],
)
def test_windows_special_paths_denied(invalid_path):
    result = assess(location(credential_root=invalid_path))

    assert result.eligible is False
    assert result.reason == "INVALID_PATH"


def test_directory_inspection_nonwindows_denied():
    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory,
    )

    result = inspect_windows_directory(
        r"C:\ProgramData\PPM\Credentials",
        platform="linux",
    )

    assert result.accepted is False
    assert result.reason == "WINDOWS_REQUIRED"


def test_directory_inspection_invalid_path_denied():
    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory,
    )

    result = inspect_windows_directory(
        r"C:\ProgramData\..\Credentials",
        platform="win32",
    )

    assert result.accepted is False
    assert result.reason == "INVALID_PATH"


def test_directory_inspection_normal_path(monkeypatch):
    import os
    import stat
    from types import SimpleNamespace

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory,
    )

    visited = []

    def fake_lstat(path):
        visited.append(path)
        return SimpleNamespace(
            st_mode=stat.S_IFDIR | 0o700,
            st_file_attributes=0,
        )

    monkeypatch.setattr(os, "lstat", fake_lstat)

    result = inspect_windows_directory(
        r"C:\ProgramData\PPM\Credentials",
        platform="win32",
    )

    assert result.accepted is True
    assert result.reason == "READ_ONLY_PATH_INSPECTED_NOT_AUTHORIZED"
    assert len(visited) == 3


def test_directory_inspection_reparse_point_denied(monkeypatch):
    import os
    import stat
    from types import SimpleNamespace

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory,
    )

    def fake_lstat(path):
        attributes = (
            stat.FILE_ATTRIBUTE_REPARSE_POINT
            if path.lower().endswith("ppm")
            else 0
        )

        return SimpleNamespace(
            st_mode=stat.S_IFDIR | 0o700,
            st_file_attributes=attributes,
        )

    monkeypatch.setattr(os, "lstat", fake_lstat)

    result = inspect_windows_directory(
        r"C:\ProgramData\PPM\Credentials",
        platform="win32",
    )

    assert result.accepted is False
    assert result.reason == "REPARSE_POINT_DENIED"


def test_directory_inspection_regular_file_denied(monkeypatch):
    import os
    import stat
    from types import SimpleNamespace

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory,
    )

    def fake_lstat(path):
        return SimpleNamespace(
            st_mode=stat.S_IFREG | 0o600,
            st_file_attributes=0,
        )

    monkeypatch.setattr(os, "lstat", fake_lstat)

    result = inspect_windows_directory(
        r"C:\ProgramData\PPM\Credentials",
        platform="win32",
    )

    assert result.accepted is False
    assert result.reason == "NOT_A_DIRECTORY"


def test_directory_inspection_missing_path_denied(monkeypatch):
    import os

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory,
    )

    def fake_lstat(path):
        raise FileNotFoundError("synthetic missing directory")

    monkeypatch.setattr(os, "lstat", fake_lstat)

    result = inspect_windows_directory(
        r"C:\ProgramData\PPM\Credentials",
        platform="win32",
    )

    assert result.accepted is False
    assert result.reason == "DIRECTORY_INSPECTION_FAILED"


def test_directory_inspection_missing_windows_attributes_denied(monkeypatch):
    import os
    import stat
    from types import SimpleNamespace

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory,
    )

    def fake_lstat(path):
        return SimpleNamespace(st_mode=stat.S_IFDIR | 0o700)

    monkeypatch.setattr(os, "lstat", fake_lstat)

    result = inspect_windows_directory(
        r"C:\ProgramData\PPM\Credentials",
        platform="win32",
    )

    assert result.accepted is False
    assert result.reason == "DIRECTORY_INSPECTION_FAILED"


def test_windows_handle_inspection_invalid_path():
    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory_handle,
    )

    result = inspect_windows_directory_handle(
        r"C:\ProgramData\..\PPM",
    )

    assert result.accepted is False
    assert result.reason in ("INVALID_PATH", "WINDOWS_REQUIRED")


def test_windows_handle_inspection_existing_directory(tmp_path):
    import sys
    import pytest

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory_handle,
    )

    if sys.platform != "win32":
        pytest.skip("Windows handle test")

    directory = tmp_path / "credential-test"
    directory.mkdir()

    result = inspect_windows_directory_handle(str(directory))

    assert result.accepted is True
    assert result.reason == "ANCESTOR_HANDLES_INSPECTED_NOT_AUTHORIZED"
    assert result.final_path is not None


def test_windows_handle_inspection_regular_file_denied(tmp_path):
    import sys
    import pytest

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory_handle,
    )

    if sys.platform != "win32":
        pytest.skip("Windows handle test")

    regular_file = tmp_path / "not-a-directory.txt"
    regular_file.write_text("synthetic test only", encoding="utf-8")

    result = inspect_windows_directory_handle(str(regular_file))

    assert result.accepted is False
    assert result.reason == "NOT_A_DIRECTORY"


def test_windows_handle_inspection_missing_directory_denied(tmp_path):
    import sys
    import pytest

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory_handle,
    )

    if sys.platform != "win32":
        pytest.skip("Windows handle test")

    missing = tmp_path / "missing-directory"

    result = inspect_windows_directory_handle(str(missing))

    assert result.accepted is False
    assert result.reason == "HANDLE_OPEN_FAILED"


def test_windows_handle_inspection_ancestor_symlink_denied(tmp_path):
    import os
    import sys
    import pytest

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory_handle,
    )

    if sys.platform != "win32":
        pytest.skip("Windows handle test")

    actual_parent = tmp_path / "actual-parent"
    actual_parent.mkdir()

    credential_dir = actual_parent / "credentials"
    credential_dir.mkdir()

    linked_parent = tmp_path / "linked-parent"

    try:
        os.symlink(
            actual_parent,
            linked_parent,
            target_is_directory=True,
        )
    except (OSError, NotImplementedError):
        pytest.skip("Windows symlink privilege unavailable")

    result = inspect_windows_directory_handle(
        str(linked_parent / "credentials")
    )

    assert result.accepted is False
    assert result.reason in (
        "REPARSE_POINT_DENIED",
        "HANDLE_PATH_MISMATCH",
        "HANDLE_OPEN_FAILED",
    )


def test_windows_handle_inspection_result_never_grants_storage_authority(
    tmp_path,
):
    import sys
    import pytest

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory_handle,
    )

    if sys.platform != "win32":
        pytest.skip("Windows handle test")

    directory = tmp_path / "read-only-inspection"
    directory.mkdir()

    result = inspect_windows_directory_handle(str(directory))

    assert result.accepted is True
    assert result.reason == "ANCESTOR_HANDLES_INSPECTED_NOT_AUTHORIZED"
    assert not hasattr(result, "write_authorized")
    assert not hasattr(result, "acl_verified")
    assert not hasattr(result, "lock_verified")


def test_windows_drive_root_canonicalization():
    from portable_platform_manager.windows_credential_store import (
        _canonical_declared_path,
    )

    assert _canonical_declared_path("C:\\") == "c:\\"
    assert _canonical_declared_path("D:\\") == "d:\\"
    assert _canonical_declared_path("C:") is None
    assert _canonical_declared_path("C:\\\\") is None
    assert _canonical_declared_path("C:\\..") is None


def test_windows_drive_root_remains_separate_from_credential_location():
    from portable_platform_manager.windows_credential_store import (
        assess_windows_store_location,
    )

    result = assess_windows_store_location(
        location(credential_root="C:\\"),
        platform="win32",
    )

    assert result.eligible is False
    assert result.reason == "PACKAGE_CREDENTIAL_OVERLAP"
def test_synthetic_windows_acl_rejects_untrusted_write():
    from portable_platform_manager.windows_credential_store import (
        WindowsAclEntry,
        assess_synthetic_windows_acl,
    )

    result = assess_synthetic_windows_acl(
        owner_sid="S-1-5-18",
        expected_owner_sid="S-1-5-18",
        protected_dacl=True,
        trusted_sids=("S-1-5-18", "S-1-5-32-544"),
        entries=(
            WindowsAclEntry(
                "S-1-5-32-545", "ALLOW", 0x00000002, False
            ),
        ),
    )

    assert result.accepted is False
    assert result.reason == "UNTRUSTED_WRITE_RIGHTS"


def test_synthetic_windows_acl_rejects_unprotected_dacl():
    from portable_platform_manager.windows_credential_store import (
        WindowsAclEntry,
        assess_synthetic_windows_acl,
    )

    result = assess_synthetic_windows_acl(
        owner_sid="S-1-5-18",
        expected_owner_sid="S-1-5-18",
        protected_dacl=False,
        trusted_sids=("S-1-5-18",),
        entries=(WindowsAclEntry("S-1-5-18", "ALLOW", 1, False),),
    )

    assert result.accepted is False
    assert result.reason == "DACL_NOT_PROTECTED"


def test_synthetic_windows_acl_rejects_wrong_owner():
    from portable_platform_manager.windows_credential_store import (
        WindowsAclEntry,
        assess_synthetic_windows_acl,
    )

    result = assess_synthetic_windows_acl(
        owner_sid="S-1-5-32-545",
        expected_owner_sid="S-1-5-18",
        protected_dacl=True,
        trusted_sids=("S-1-5-18",),
        entries=(WindowsAclEntry("S-1-5-18", "ALLOW", 1, False),),
    )

    assert result.accepted is False
    assert result.reason == "OWNER_UNVERIFIED"


def test_synthetic_windows_acl_accepts_policy_without_authority():
    from portable_platform_manager.windows_credential_store import (
        WindowsAclEntry,
        assess_synthetic_windows_acl,
    )

    result = assess_synthetic_windows_acl(
        owner_sid="S-1-5-18",
        expected_owner_sid="S-1-5-18",
        protected_dacl=True,
        trusted_sids=("S-1-5-18", "S-1-5-32-544"),
        entries=(
            WindowsAclEntry("S-1-5-18", "ALLOW", 0x001F01FF, False),
            WindowsAclEntry("S-1-5-32-545", "ALLOW", 0x00000001, False),
        ),
    )

    assert result.accepted is True
    assert result.reason == "SYNTHETIC_POLICY_ONLY_NOT_AUTHORIZED"
    assert not hasattr(result, "write_authorized")
    assert not hasattr(result, "acl_verified")


def test_synthetic_windows_acl_rejects_inherited_ace():
    from portable_platform_manager.windows_credential_store import (
        WindowsAclEntry,
        assess_synthetic_windows_acl,
    )

    result = assess_synthetic_windows_acl(
        owner_sid="S-1-5-18",
        expected_owner_sid="S-1-5-18",
        protected_dacl=True,
        trusted_sids=("S-1-5-18",),
        entries=(WindowsAclEntry("S-1-5-18", "ALLOW", 1, True),),
    )

    assert result.accepted is False
    assert result.reason == "INHERITED_ACE_UNVERIFIED"
@pytest.mark.parametrize(
    "owner_sid,rights",
    [
        ("S-1-5-018", 1),
        ("S-1-5-4294967296", 1),
        ("S-1-5-18-extra", 1),
        ("S-1-5-18", 0x00000200),
        ("S-1-5-18", 0x02000000),
    ],
)
def test_synthetic_windows_acl_rejects_invalid_sid_and_rights(
    owner_sid,
    rights,
):
    from portable_platform_manager.windows_credential_store import (
        WindowsAclEntry,
        assess_synthetic_windows_acl,
    )

    result = assess_synthetic_windows_acl(
        owner_sid=owner_sid,
        expected_owner_sid=owner_sid,
        protected_dacl=True,
        trusted_sids=("S-1-5-18",),
        entries=(
            WindowsAclEntry(
                "S-1-5-18",
                "ALLOW",
                rights,
                False,
            ),
        ),
    )

    assert result.accepted is False
@pytest.mark.parametrize(
    "rights",
    [
        0x10000000,  # GENERIC_ALL
        0x40000000,  # GENERIC_WRITE
        0x20000000,  # GENERIC_EXECUTE
        0x02000000,  # MAXIMUM_ALLOWED: unknown rights denied
    ],
)
def test_synthetic_windows_acl_rejects_untrusted_generic_rights(rights):
    from portable_platform_manager.windows_credential_store import (
        WindowsAclEntry,
        assess_synthetic_windows_acl,
    )

    result = assess_synthetic_windows_acl(
        owner_sid="S-1-5-18",
        expected_owner_sid="S-1-5-18",
        protected_dacl=True,
        trusted_sids=("S-1-5-18",),
        entries=(
            WindowsAclEntry(
                "S-1-5-32-545",
                "ALLOW",
                rights,
                False,
            ),
        ),
    )

    assert result.accepted is False
def test_windows_security_descriptor_result_denies_authority():
    from portable_platform_manager.windows_credential_store import (
        WindowsSecurityDescriptorInspection,
    )

    result = WindowsSecurityDescriptorInspection(
        inspected=True,
        reason="OBSERVATION_ONLY_NOT_AUTHORIZED",
        owner_sid="S-1-5-18",
        dacl_present=True,
        dacl_null=False,
    )

    assert result.inspected is True
    assert not hasattr(result, "storage_authorized")


def test_windows_security_descriptor_failure_is_closed():
    from portable_platform_manager.windows_credential_store import (
        _denied_windows_security_descriptor,
    )

    result = _denied_windows_security_descriptor("SECURITY_INFO_FAILED")

    assert result.inspected is False
    assert result.owner_sid is None
    assert result.dacl_present is False
    assert result.dacl_null is True
    assert not hasattr(result, "storage_authorized")
    assert result.reason == "SECURITY_INFO_FAILED"

def test_security_descriptor_handle_rejects_invalid_handle():
    import sys
    import pytest

    from portable_platform_manager.windows_credential_store import (
        _inspect_security_descriptor_from_handle,
    )

    if sys.platform != "win32":
        pytest.skip("Windows handle test")

    import ctypes

    invalid_values = (
        None,
        0,
        -1,
        ctypes.c_void_p(-1).value,
        "not-a-handle",
        True,
    )

    for invalid in invalid_values:
        result = _inspect_security_descriptor_from_handle(invalid)
        assert result.inspected is False
        assert result.reason == "INVALID_HANDLE"
        assert not hasattr(result, "storage_authorized")


def test_security_descriptor_handle_requires_windows():
    import sys

    from portable_platform_manager.windows_credential_store import (
        _inspect_security_descriptor_from_handle,
    )

    if sys.platform == "win32":
        return

    result = _inspect_security_descriptor_from_handle(1)

    assert result.inspected is False
    assert result.reason == "WINDOWS_REQUIRED"

def test_windows_security_descriptor_real_directory_handle(tmp_path):
    """Observe security metadata on a CI temporary directory only."""
    import ctypes
    import sys
    import pytest
    from ctypes import wintypes

    from portable_platform_manager.windows_credential_store import (
        _inspect_security_descriptor_from_handle,
    )

    if sys.platform != "win32":
        pytest.skip("Windows-only security descriptor test")

    directory = tmp_path / "security-observation"
    directory.mkdir()

    READ_CONTROL = 0x00020000
    FILE_READ_ATTRIBUTES = 0x00000080
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    FILE_SHARE_DELETE = 0x00000004
    OPEN_EXISTING = 3
    FILE_FLAG_BACKUP_SEMANTICS = 0x02000000

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

    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL

    handle = create_file(
        str(directory),
        READ_CONTROL | FILE_READ_ATTRIBUTES,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS,
        None,
    )

    invalid = ctypes.c_void_p(-1).value

    assert handle not in (None, invalid), (
        "Temporary directory handle could not be opened"
    )

    try:
        result = _inspect_security_descriptor_from_handle(handle)
    finally:
        assert close_handle(handle) != 0

    assert result.inspected is True
    assert result.reason == "HANDLE_SECURITY_OBSERVED_NOT_AUTHORIZED"
    assert isinstance(result.owner_sid, str)
    assert result.owner_sid.startswith("S-1-")
    assert result.dacl_present is True
    assert result.dacl_null is False
    assert not hasattr(result, "storage_authorized")
    assert not hasattr(result, "acl_verified")

def test_windows_optional_security_observation_success(tmp_path):
    """Verify opt-in observation and default compatibility on Windows CI."""
    import sys
    import pytest

    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory_handle,
    )

    if sys.platform != "win32":
        pytest.skip("Windows-only integration test")

    directory = tmp_path / "optional-security-observation"
    directory.mkdir()

    default_result = inspect_windows_directory_handle(str(directory))
    explicit_false = inspect_windows_directory_handle(
        str(directory),
        inspect_security=False,
    )
    observed = inspect_windows_directory_handle(
        str(directory),
        inspect_security=True,
    )

    assert default_result.accepted is True
    assert explicit_false == default_result
    assert observed.accepted is True
    assert observed.reason == "ANCESTOR_HANDLES_INSPECTED_NOT_AUTHORIZED"
    assert observed.final_path == default_result.final_path
    assert not hasattr(observed, "storage_authorized")
    assert not hasattr(observed, "acl_verified")


def test_windows_optional_security_observation_invalid_option():
    from portable_platform_manager.windows_credential_store import (
        inspect_windows_directory_handle,
    )

    for invalid in (None, 0, 1, "true", [], {}):
        result = inspect_windows_directory_handle(
            r"C:\PPM\credentials",
            inspect_security=invalid,
        )

        assert result.accepted is False
        assert result.reason == "INVALID_SECURITY_OPTION"


def test_windows_optional_security_observation_failure_denied(
    tmp_path,
    monkeypatch,
):
    """Simulate descriptor observation failure without changing OS ACLs."""
    import sys
    import pytest

    import portable_platform_manager.windows_credential_store as store

    if sys.platform != "win32":
        pytest.skip("Windows-only integration test")

    directory = tmp_path / "security-observation-denied"
    directory.mkdir()

    observed_handles = []

    def denied_observation(handle):
        observed_handles.append(handle)
        return store._denied_windows_security_descriptor(
            "SYNTHETIC_SECURITY_FAILURE"
        )

    monkeypatch.setattr(
        store,
        "_inspect_security_descriptor_from_handle",
        denied_observation,
    )

    result = store.inspect_windows_directory_handle(
        str(directory),
        inspect_security=True,
    )

    assert result.accepted is False
    assert result.reason == "SECURITY_DESCRIPTOR_OBSERVATION_FAILED"
    assert len(observed_handles) >= 1
    assert not hasattr(result, "storage_authorized")
