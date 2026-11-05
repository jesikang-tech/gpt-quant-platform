"""Pure backup plan assessment; never authorizes archive execution."""

from __future__ import annotations

from dataclasses import dataclass

from .archive_contract import assess_archive_contract
from .backup_selection import assess_backup_path


@dataclass(frozen=True)
class BackupPlanDecision:
    accepted: bool
    reason: str
    selected_paths: tuple[str, ...] = ()


def assess_backup_plan(
    paths: object,
    *,
    archive_format: object = "7z",
    filename_encryption: object = True,
    content_verified: object = False,
    filesystem_verified: object = False,
    execution_requested: object = False,
) -> BackupPlanDecision:
    """Assess an explicit allowlist without touching the filesystem."""

    if type(paths) is not tuple or not paths:
        return BackupPlanDecision(False, "INVALID_EXPLICIT_ALLOWLIST")

    if type(execution_requested) is not bool:
        return BackupPlanDecision(False, "INVALID_EXECUTION_REQUEST")

    if execution_requested:
        return BackupPlanDecision(False, "EXECUTION_NOT_AUTHORIZED")

    archive = assess_archive_contract(
        archive_format,
        filename_encryption=filename_encryption,
        execution_requested=False,
    )

    if not archive.accepted:
        return BackupPlanDecision(False, archive.reason)

    selected: list[str] = []
    seen: set[str] = set()

    for path in paths:
        decision = assess_backup_path(path)

        if not decision.selected or decision.relative_path is None:
            return BackupPlanDecision(False, decision.reason)

        normalized = decision.relative_path
        key = normalized.casefold()

        if key in seen:
            return BackupPlanDecision(False, "DUPLICATE_BACKUP_PATH")

        seen.add(key)
        selected.append(normalized)

    if type(content_verified) is not bool or not content_verified:
        return BackupPlanDecision(False, "CONTENT_VERIFICATION_REQUIRED")

    if type(filesystem_verified) is not bool or not filesystem_verified:
        return BackupPlanDecision(False, "FILESYSTEM_VERIFICATION_REQUIRED")

    return BackupPlanDecision(
        True,
        "DECLARATION_ONLY",
        tuple(selected),
    )