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

def test_staged_hash_matches_independent_digest(tmp_path: Path) -> None:
    import hashlib

    source = tmp_path / "source"
    staging = tmp_path / "staging"
    source.mkdir()
    staging.mkdir()

    payload = b"synthetic integrity payload"
    (source / "sample.txt").write_bytes(payload)

    result = stage_backup_file(source, "sample.txt", staging)

    expected_hash = hashlib.sha256(payload).hexdigest()

    assert result.sha256 == expected_hash
    assert hashlib.sha256(
        (staging / "sample.txt").read_bytes()
    ).hexdigest() == expected_hash


def test_detects_source_change_during_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import os

    from portable_platform_manager import backup_staging

    source = tmp_path / "source"
    staging = tmp_path / "staging"
    source.mkdir()
    staging.mkdir()

    file = source / "sample.txt"
    file.write_bytes(b"original")

    original_open = backup_staging.os.open

    def changed_open(path, flags):
        file.write_bytes(b"changed content")
        return original_open(path, flags)

    monkeypatch.setattr(backup_staging.os, "open", changed_open)

    with pytest.raises(ValueError, match="SOURCE_CHANGED_DURING_OPEN"):
        stage_backup_file(source, "sample.txt", staging)

    assert list(staging.iterdir()) == []


def test_detects_staging_hash_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from portable_platform_manager import backup_staging

    source = tmp_path / "source"
    staging = tmp_path / "staging"
    source.mkdir()
    staging.mkdir()

    (source / "sample.txt").write_bytes(b"synthetic")

    original_sha256 = backup_staging.hashlib.sha256
    calls = 0

    def controlled_sha256(*args, **kwargs):
        nonlocal calls
        calls += 1

        if calls == 2:
            class IncorrectDigest:
                def update(self, data):
                    pass

                def hexdigest(self):
                    return "0" * 64

            return IncorrectDigest()

        return original_sha256(*args, **kwargs)

    monkeypatch.setattr(
        backup_staging.hashlib,
        "sha256",
        controlled_sha256,
    )

    with pytest.raises(ValueError, match="STAGING_OUTPUT_HASH_MISMATCH"):
        stage_backup_file(source, "sample.txt", staging)

    assert not (staging / "sample.txt").exists()

def test_windows_staging_denied_until_verified(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from portable_platform_manager import backup_staging

    source = tmp_path / "source"
    staging = tmp_path / "staging"
    source.mkdir()
    staging.mkdir()
    (source / "sample.txt").write_bytes(b"synthetic")

    monkeypatch.setattr(backup_staging.os, "name", "nt")

    with pytest.raises(
        ValueError,
        match="WINDOWS_SAFE_SOURCE_READER_PENDING_VERIFICATION",
    ):
        stage_backup_file(source, "sample.txt", staging)

    assert list(staging.iterdir()) == []