"""Synthetic-only tests for isolated backup staging."""

from pathlib import Path

import pytest

from portable_platform_manager.backup_staging import stage_backup_file


def test_stages_synthetic_file_with_sha256(tmp_path: Path) -> None:
    source = tmp_path / "source"
    staging = tmp_path / "staging"
    source.mkdir()
    staging.mkdir()

    (source / "sample.txt").write_bytes(b"synthetic backup data")

    result = stage_backup_file(source, "sample.txt", staging)

    assert result.relative_path == "sample.txt"
    assert result.size == len(b"synthetic backup data")
    assert len(result.sha256) == 64
    assert (staging / "sample.txt").read_bytes() == b"synthetic backup data"


def test_denies_nonempty_staging_root(tmp_path: Path) -> None:
    source = tmp_path / "source"
    staging = tmp_path / "staging"
    source.mkdir()
    staging.mkdir()

    (source / "sample.txt").write_text("synthetic")
    (staging / "existing.txt").write_text("existing")

    with pytest.raises(ValueError, match="STAGING_ROOT_NOT_EMPTY"):
        stage_backup_file(source, "sample.txt", staging)


def test_denies_staging_inside_source(tmp_path: Path) -> None:
    source = tmp_path / "source"
    staging = source / "staging"
    source.mkdir()
    staging.mkdir()

    (source / "sample.txt").write_text("synthetic")

    with pytest.raises(ValueError, match="STAGING_INSIDE_SOURCE_DENIED"):
        stage_backup_file(source, "sample.txt", staging)


def test_denies_nested_path_until_supported(tmp_path: Path) -> None:
    source = tmp_path / "source"
    staging = tmp_path / "staging"
    (source / "docs").mkdir(parents=True)
    staging.mkdir()

    (source / "docs" / "sample.txt").write_text("synthetic")

    with pytest.raises(
        ValueError,
        match="NESTED_STAGING_REQUIRES_SAFE_DIRECTORY_CREATION",
    ):
        stage_backup_file(source, "docs/sample.txt", staging)


def test_denies_excluded_database_path(tmp_path: Path) -> None:
    source = tmp_path / "source"
    staging = tmp_path / "staging"
    source.mkdir()
    staging.mkdir()

    with pytest.raises(ValueError, match="BACKUP_FILE_INSPECTION_DENIED"):
        stage_backup_file(source, "operating.sqlite", staging)


def test_denies_missing_source_file(tmp_path: Path) -> None:
    source = tmp_path / "source"
    staging = tmp_path / "staging"
    source.mkdir()
    staging.mkdir()

    with pytest.raises(ValueError, match="BACKUP_FILE_INSPECTION_DENIED"):
        stage_backup_file(source, "missing.txt", staging)


def test_denies_source_equals_staging(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()

    (source / "sample.txt").write_text("synthetic")

    with pytest.raises(ValueError, match="STAGING_ROOT_EQUALS_SOURCE"):
        stage_backup_file(source, "sample.txt", source)


def test_denies_missing_staging_root(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()

    (source / "sample.txt").write_text("synthetic")

    with pytest.raises(FileNotFoundError):
        stage_backup_file(
            source,
            "sample.txt",
            tmp_path / "missing-staging",
        )