"""Pure, platform-independent backup path selection.

No filesystem, archive, database, network, or broker access.
A selected path is not proof that its content is safe to archive.
"""

from __future__ import annotations

from dataclasses import dataclass

from .manifest import _safe_relative_path


_EXCLUDED_COMPONENTS = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "node_modules",
        ".env",
        "secrets",
        "credentials",
        "private",
    }
)

_EXCLUDED_FILENAMES = frozenset(
    {
        ".env",
        ".env.local",
        ".env.production",
        "id_rsa",
        "id_ed25519",
        "credentials.json",
        "secrets.json",
    }
)

_EXCLUDED_SUFFIXES = (
    ".sqlite",
    ".sqlite3",
    ".db",
    ".db-wal",
    ".db-shm",
    ".pem",
    ".key",
    ".pfx",
    ".p12",
    ".pyc",
)


@dataclass(frozen=True)
class BackupSelectionDecision:
    selected: bool
    reason: str
    relative_path: str | None = None


def assess_backup_path(
    relative_path: object,
    *,
    additional_excluded_components: tuple[str, ...] = (),
) -> BackupSelectionDecision:
    """Select a declared relative path using conservative defaults.

    This is a lexical policy only. It does not inspect file contents,
    symlinks, reparse points, ACLs, or the filesystem.
    """
    try:
        path = _safe_relative_path(relative_path)
    except (TypeError, ValueError):
        return BackupSelectionDecision(False, "UNSAFE_RELATIVE_PATH")

    if type(additional_excluded_components) is not tuple:
        return BackupSelectionDecision(False, "INVALID_EXCLUSION_POLICY")

    if any(
        type(item) is not str
        or not item
        or "/" in item
        or "\\" in item
        for item in additional_excluded_components
    ):
        return BackupSelectionDecision(False, "INVALID_EXCLUSION_POLICY")

    excluded = _EXCLUDED_COMPONENTS | frozenset(
        item.casefold() for item in additional_excluded_components
    )

    components = tuple(item.casefold() for item in path.split("/"))
    filename = components[-1]

    if any(component in excluded for component in components):
        return BackupSelectionDecision(False, "EXCLUDED_COMPONENT", path)

    if filename in _EXCLUDED_FILENAMES:
        return BackupSelectionDecision(False, "EXCLUDED_FILENAME", path)

    if filename.endswith(_EXCLUDED_SUFFIXES):
        return BackupSelectionDecision(False, "EXCLUDED_SUFFIX", path)

    if filename.startswith(".env."):
        return BackupSelectionDecision(False, "ENVIRONMENT_FILE", path)

    return BackupSelectionDecision(True, "LEXICALLY_SELECTED_ONLY", path)
