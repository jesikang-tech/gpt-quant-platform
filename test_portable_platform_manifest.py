"""Synthetic-only tests for portable platform manifest validation."""

import copy

import pytest

from portable_platform_manager.manifest import validate_manifest


def valid_manifest():
    return {
        "platform_id": "synthetic-platform",
        "platform_version": "1.2.3",
        "package_format_version": 1,
        "supported_operating_systems": ["windows"],
        "runtime_requirements": {},
        "install_directory_policy": "DENIED",
        "data_directory_policy": "DENIED",
        "log_directory_policy": "DENIED",
        "permitted_entrypoints": ["app/start.py"],
        "execution_authority_policy": "DENIED",
        "backup_policy": "DENIED",
        "uninstall_policy": "DENIED",
    }


def test_valid_synthetic_manifest():
    result = validate_manifest(valid_manifest())

    assert result.platform_id == "synthetic-platform"
    assert result.platform_version == "1.2.3"
    assert result.permitted_entrypoints == ("app/start.py",)


@pytest.mark.parametrize(
    "field,value",
    [
        ("platform_id", ""),
        ("platform_id", "../unsafe"),
        ("platform_id", "UPPERCASE"),
        ("platform_version", "latest"),
        ("platform_version", "1.0"),
        ("package_format_version", True),
        ("package_format_version", 2),
        ("supported_operating_systems", ["linux"]),
        ("runtime_requirements", {"python": "3.14"}),
        ("install_directory_policy", "ALLOW"),
        ("data_directory_policy", "ALLOW"),
        ("log_directory_policy", "ALLOW"),
        ("execution_authority_policy", "ALLOW"),
        ("backup_policy", "ALLOW"),
        ("uninstall_policy", "ALLOW"),
    ],
)
def test_invalid_manifest_values_are_denied(field, value):
    manifest = valid_manifest()
    manifest[field] = value

    with pytest.raises(ValueError):
        validate_manifest(manifest)


@pytest.mark.parametrize(
    "entrypoint",
    [
        "../outside.py",
        "/absolute.py",
        "C:/windows/system32/cmd.exe",
        "app\\start.py",
        "app/../start.py",
        "app//start.py",
        "./start.py",
        "app/\x00start.py",
    ],
)
def test_unsafe_entrypoints_are_denied(entrypoint):
    manifest = valid_manifest()
    manifest["permitted_entrypoints"] = [entrypoint]

    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_missing_field_is_denied():
    manifest = valid_manifest()
    del manifest["backup_policy"]

    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_unknown_field_is_denied():
    manifest = valid_manifest()
    manifest["unexpected"] = True

    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_duplicate_entrypoints_are_denied():
    manifest = valid_manifest()
    manifest["permitted_entrypoints"] = ["app/start.py", "app/start.py"]

    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_too_many_entrypoints_are_denied():
    manifest = valid_manifest()
    manifest["permitted_entrypoints"] = [
        f"app/entry_{index}.py" for index in range(33)
    ]

    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_input_manifest_is_not_modified():
    manifest = valid_manifest()
    original = copy.deepcopy(manifest)

    validate_manifest(manifest)

    assert manifest == original


@pytest.mark.parametrize(
    "entrypoint",
    [
        "CON",
        "NUL.txt",
        "app/PRN",
        "app/AUX.log",
        "app/COM1.py",
        "app/LPT1.txt",
        "app/start.py.",
        "app/start.py ",
        "app/start.py:stream",
    ],
)
def test_windows_reserved_or_ambiguous_entrypoints_are_denied(entrypoint):
    manifest = valid_manifest()
    manifest["permitted_entrypoints"] = [entrypoint]

    with pytest.raises(ValueError):
        validate_manifest(manifest)


def test_case_insensitive_entrypoint_collision():
    manifest = valid_manifest()
    manifest["permitted_entrypoints"] = [
        "App/Start.py",
        "app/start.py",
    ]

    with pytest.raises(ValueError):
        validate_manifest(manifest)