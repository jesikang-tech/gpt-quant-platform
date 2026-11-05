"""Synthetic tests for the reusable PPM backup path policy."""

from dataclasses import FrozenInstanceError

import pytest

from portable_platform_manager.backup_selection import (
    BackupSelectionDecision,
    assess_backup_path,
)


@pytest.mark.parametrize(
    "path",
    [
        "app/main.py",
        "docs/README.md",
        "tests/test_strategy.py",
        "config/example.json",
    ],
)
def test_ordinary_project_paths_are_lexically_selected(path):
    result = assess_backup_path(path)
    assert result == BackupSelectionDecision(
        True, "LEXICALLY_SELECTED_ONLY", path
    )


@pytest.mark.parametrize(
    "path",
    [
        ".git/config",
        ".venv/Scripts/python.exe",
        "venv/Lib/site.py",
        "__pycache__/module.pyc",
        "node_modules/package/index.js",
        "secrets/token.txt",
        "credentials/account.json",
        "private/key.txt",
        "app/.env",
        "app/.env.production",
        "data/production.sqlite",
        "data/production.sqlite3",
        "data/production.db",
        "data/production.db-wal",
        "data/production.db-shm",
        "certificates/server.pem",
        "certificates/server.key",
        "certificates/client.pfx",
        "certificates/client.p12",
        "keys/id_rsa",
        "keys/id_ed25519",
        "config/credentials.json",
        "config/secrets.json",
    ],
)
def test_sensitive_or_generated_paths_are_excluded(path):
    result = assess_backup_path(path)
    assert result.selected is False
    assert result.reason.startswith(("EXCLUDED_", "ENVIRONMENT_"))


@pytest.mark.parametrize(
    "path",
    [
        "../outside.txt",
        "app/../outside.txt",
        "/absolute/file.txt",
        "C:/Windows/system.ini",
        "app\\main.py",
        "app//main.py",
        "app/./main.py",
        "app/NUL.txt",
        "app/CON",
        "app/trailing.",
        "app/trailing ",
        "app/file?.txt",
        "",
        None,
        123,
    ],
)
def test_unsafe_paths_fail_closed(path):
    result = assess_backup_path(path)
    assert result.selected is False
    assert result.reason == "UNSAFE_RELATIVE_PATH"


def test_additional_excluded_component_is_reusable():
    result = assess_backup_path(
        "custom_runtime/state.json",
        additional_excluded_components=("custom_runtime",),
    )
    assert result.selected is False
    assert result.reason == "EXCLUDED_COMPONENT"


@pytest.mark.parametrize(
    "policy",
    [
        ["custom_runtime"],
        ("../outside",),
        ("a/b",),
        ("",),
        (123,),
    ],
)
def test_invalid_exclusion_policy_is_denied(policy):
    result = assess_backup_path(
        "app/main.py",
        additional_excluded_components=policy,
    )
    assert result.selected is False
    assert result.reason == "INVALID_EXCLUSION_POLICY"


def test_selection_decision_is_immutable():
    result = assess_backup_path("app/main.py")
    with pytest.raises(FrozenInstanceError):
        result.selected = False


def test_selection_has_no_filesystem_authority():
    result = assess_backup_path("app/main.py")
    assert result.reason == "LEXICALLY_SELECTED_ONLY"
    assert result.selected is True
    assert not hasattr(result, "filesystem_verified")
    assert not hasattr(result, "archive_authorized")
