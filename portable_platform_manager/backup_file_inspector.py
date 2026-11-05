"""Read-only filesystem checks for explicitly selected backup files.

Does not inspect secrets, open file contents, or authorize archiving.
Caller must independently control source-root trust and file stability.
"""

from __future__ import annotations

import os
import stat
from dataclasses import dataclass
from pathlib import Path

from .backup_selection import assess_backup_path


@dataclass(frozen=True)
class BackupFileInspection:
    accepted: bool
    reason: str
    relative_path: str | None = None


def inspect_backup_file(
    source_root: object,
    relative_path: object,
) -> BackupFileInspection:
    """Inspect a regular file without following directory symlinks."""

    selection = assess_backup_path(relative_path)

    if not selection.selected or selection.relative_path is None:
        return BackupFileInspection(False, selection.reason)

    relative = selection.relative_path

    if type(source_root) not in (str, Path):
        return BackupFileInspection(False, "INVALID_SOURCE_ROOT")

    try:
        root = Path(source_root)

        if not root.is_absolute():
            return BackupFileInspection(False, "SOURCE_ROOT_NOT_ABSOLUTE")

        parts = relative.split("/")
        current = root

        root_stat = os.lstat(root)

        if not stat.S_ISDIR(root_stat.st_mode):
            return BackupFileInspection(False, "SOURCE_ROOT_NOT_DIRECTORY")

        if stat.S_ISLNK(root_stat.st_mode):
            return BackupFileInspection(False, "SOURCE_ROOT_IS_LINK")

        if getattr(root_stat, "st_file_attributes", 0) & 0x400:
            return BackupFileInspection(False, "SOURCE_ROOT_REPARSE_POINT")

        for index, part in enumerate(parts):
            current = current / part
            entry = os.lstat(current)

            if stat.S_ISLNK(entry.st_mode):
                return BackupFileInspection(False, "SYMLINK_DENIED", relative)

            if getattr(entry, "st_file_attributes", 0) & 0x400:
                return BackupFileInspection(False, "REPARSE_POINT_DENIED", relative)

            is_final = index == len(parts) - 1

            if is_final:
                if not stat.S_ISREG(entry.st_mode):
                    return BackupFileInspection(False, "NOT_REGULAR_FILE", relative)
            elif not stat.S_ISDIR(entry.st_mode):
                return BackupFileInspection(False, "PARENT_NOT_DIRECTORY", relative)

        return BackupFileInspection(True, "READ_ONLY_INSPECTION_ONLY", relative)

    except (OSError, ValueError, TypeError):
        return BackupFileInspection(False, "FILESYSTEM_INSPECTION_FAILED", relative)