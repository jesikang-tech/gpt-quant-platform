"""Synthetic tests for the pure backup plan declaration contract."""

import pytest

from portable_platform_manager.backup_plan import assess_backup_plan


def test_valid_declaration_only():
    result = assess_backup_plan(
        ("src/main.py", "docs/readme.md"),
        content_verified=True,
        filesystem_verified=True,
    )
    assert result.accepted is True
    assert result.reason == "DECLARATION_ONLY"
    assert result.selected_paths == (
        "src/main.py",
        "docs/readme.md",
    )


@pytest.mark.parametrize(
    "paths",
    [
        None,
        [],
        (),
        "src/main.py",
        ["src/main.py"],
        ("../outside.py",),
        ("/absolute.py",),
    ],
)
def test_invalid_allowlist_denied(paths):
    assert not assess_backup_plan(paths).accepted


@pytest.mark.parametrize(
    "path",
    [
        ".env",
        "config/.env.production",
        "secrets/token.txt",
        "credentials/account.json",
        "data/production.sqlite",
        "data/production.db",
        "private/key.pem",
        "src/__pycache__/cache.pyc",
    ],
)
def test_sensitive_paths_denied(path):
    result = assess_backup_plan(
        (path,),
        content_verified=True,
        filesystem_verified=True,
    )
    assert result.accepted is False


def test_duplicate_paths_denied():
    result = assess_backup_plan(
        ("src/Main.py", "src/main.py"),
        content_verified=True,
        filesystem_verified=True,
    )
    assert result.reason == "DUPLICATE_BACKUP_PATH"


def test_unverified_content_denied():
    result = assess_backup_plan(
        ("src/main.py",),
        filesystem_verified=True,
    )
    assert result.reason == "CONTENT_VERIFICATION_REQUIRED"


def test_unverified_filesystem_denied():
    result = assess_backup_plan(
        ("src/main.py",),
        content_verified=True,
    )
    assert result.reason == "FILESYSTEM_VERIFICATION_REQUIRED"


@pytest.mark.parametrize(
    "flag",
    [None, 0, 1, "true", [], {}],
)
def test_invalid_verification_flags_denied(flag):
    result = assess_backup_plan(
        ("src/main.py",),
        content_verified=flag,
        filesystem_verified=True,
    )
    assert not result.accepted

    result = assess_backup_plan(
        ("src/main.py",),
        content_verified=True,
        filesystem_verified=flag,
    )
    assert not result.accepted


def test_unsafe_archive_format_denied():
    result = assess_backup_plan(
        ("src/main.py",),
        archive_format="tar",
        content_verified=True,
        filesystem_verified=True,
    )
    assert result.reason == "UNSUPPORTED_ARCHIVE_FORMAT"


def test_zip_filename_encryption_denied():
    result = assess_backup_plan(
        ("src/main.py",),
        archive_format="zip",
        filename_encryption=True,
        content_verified=True,
        filesystem_verified=True,
    )
    assert result.reason == "ZIP_FILENAME_ENCRYPTION_UNSUPPORTED"


@pytest.mark.parametrize(
    "execution_requested",
    [True, 1, "yes"],
)
def test_execution_requests_denied(execution_requested):
    result = assess_backup_plan(
        ("src/main.py",),
        execution_requested=execution_requested,
        content_verified=True,
        filesystem_verified=True,
    )
    assert result.accepted is False


def test_no_verification_claim_is_inferred():
    result = assess_backup_plan(("src/main.py",))
    assert result.accepted is False
    assert result.reason == "CONTENT_VERIFICATION_REQUIRED"