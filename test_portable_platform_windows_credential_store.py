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
