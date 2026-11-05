"""Synthetic-only tests for read-only backup filesystem inspection."""

from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from portable_platform_manager.backup_file_inspector import (
    inspect_backup_file,
)


def test_regular_file_is_declaratively_accepted(tmp_path: Path) -> None:
    folder = tmp_path / "src"
    folder.mkdir()
    (folder / "module.py").write_text("x = 1", encoding="utf-8")

    result = inspect_backup_file(tmp_path, "src/module.py")

    assert result.accepted
    assert result.reason == "READ_ONLY_INSPECTION_ONLY"
    assert result.relative_path == "src/module.py"


@pytest.mark.parametrize(
    "path",
    [
        ".env",
        "secrets/token.txt",
        "data/prices.db",
        "../outside.py",
        "/absolute.py",
        "",
        None,
    ],
)
def test_unsafe_paths_are_denied(tmp_path: Path, path: object) -> None:
    result = inspect_backup_file(tmp_path, path)
    assert not result.accepted


def test_missing_file_is_denied(tmp_path: Path) -> None:
    result = inspect_backup_file(tmp_path, "missing.py")
    assert not result.accepted
    assert result.reason == "FILESYSTEM_INSPECTION_FAILED"


def test_directory_is_denied(tmp_path: Path) -> None:
    (tmp_path / "folder").mkdir()
    result = inspect_backup_file(tmp_path, "folder")
    assert not result.accepted
    assert result.reason == "NOT_REGULAR_FILE"


def test_relative_source_root_is_denied() -> None:
    result = inspect_backup_file("relative", "module.py")
    assert not result.accepted
    assert result.reason == "SOURCE_ROOT_NOT_ABSOLUTE"


def test_invalid_source_root_is_denied() -> None:
    result = inspect_backup_file(object(), "module.py")
    assert not result.accepted
    assert result.reason == "INVALID_SOURCE_ROOT"


def test_symlink_file_is_denied(tmp_path: Path) -> None:
    target = tmp_path / "target.py"
    target.write_text("x = 1", encoding="utf-8")
    link = tmp_path / "link.py"

    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("Symlink creation unavailable")

    result = inspect_backup_file(tmp_path, "link.py")
    assert not result.accepted
    assert result.reason == "SYMLINK_DENIED"


def test_symlink_directory_is_denied(tmp_path: Path) -> None:
    real = tmp_path / "real"
    real.mkdir()
    (real / "module.py").write_text("x = 1", encoding="utf-8")

    link = tmp_path / "linked"

    try:
        link.symlink_to(real, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Directory symlink creation unavailable")

    result = inspect_backup_file(tmp_path, "linked/module.py")
    assert not result.accepted
    assert result.reason == "SYMLINK_DENIED"


def test_reparse_point_attribute_is_denied(tmp_path: Path) -> None:
    target = tmp_path / "module.py"
    target.write_text("x = 1", encoding="utf-8")

    real_lstat = os.lstat

    def fake_lstat(path: object):
        result = real_lstat(path)

        if Path(path) == target:
            return SimpleNamespace(
                st_mode=result.st_mode,
                st_file_attributes=0x400,
            )

        return result

    with patch(
        "portable_platform_manager.backup_file_inspector.os.lstat",
        side_effect=fake_lstat,
    ):
        decision = inspect_backup_file(tmp_path, "module.py")

    assert not decision.accepted
    assert decision.reason == "REPARSE_POINT_DENIED"


def test_source_root_symlink_is_denied(tmp_path: Path) -> None:
    real = tmp_path / "real"
    real.mkdir()
    (real / "module.py").write_text("x = 1", encoding="utf-8")

    link = tmp_path / "root_link"

    try:
        link.symlink_to(real, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Directory symlink creation unavailable")

    decision = inspect_backup_file(link, "module.py")

    assert not decision.accepted
    assert decision.reason in (
        "SOURCE_ROOT_IS_LINK",
        "SOURCE_ROOT_NOT_DIRECTORY",
    )


def test_inspector_has_no_execution_authority(tmp_path: Path) -> None:
    file = tmp_path / "module.py"
    file.write_text("x = 1", encoding="utf-8")

    decision = inspect_backup_file(tmp_path, "module.py")

    assert decision.accepted
    assert decision.reason == "READ_ONLY_INSPECTION_ONLY"
    assert not hasattr(decision, "execute")
    assert not hasattr(decision, "archive")