"""Reusable SQLite source-protection design contract.

No sqlite3 import, file I/O, source connection, snapshot,
authorization grant, or execution capability.
"""

from dataclasses import dataclass
from enum import Enum


class SourceProtectionStatus(str, Enum):
    DENIED = "DENIED"


@dataclass(frozen=True)
class SQLiteProtectionEvidence:
    os_readonly_permissions_verified: bool = False
    sqlite_readonly_mode_verified: bool = False
    wal_consistency_verified: bool = False
    transaction_consistency_verified: bool = False
    source_side_effects_excluded: bool = False
    bounded_query_verified: bool = False
    synthetic_validation_passed: bool = False
    independent_source_approval: bool = False


@dataclass(frozen=True)
class SQLiteProtectionDecision:
    status: SourceProtectionStatus = SourceProtectionStatus.DENIED
    reason: str = "EXECUTION_NOT_AUTHORIZED"


def assess_sqlite_source_protection(
    evidence: object,
) -> SQLiteProtectionDecision:
    """Report missing prerequisites without granting access."""

    if type(evidence) is not SQLiteProtectionEvidence:
        return SQLiteProtectionDecision(
            reason="INVALID_PROTECTION_EVIDENCE"
        )

    requirements = (
        "os_readonly_permissions_verified",
        "sqlite_readonly_mode_verified",
        "wal_consistency_verified",
        "transaction_consistency_verified",
        "source_side_effects_excluded",
        "bounded_query_verified",
        "synthetic_validation_passed",
        "independent_source_approval",
    )

    for requirement in requirements:
        if getattr(evidence, requirement) is not True:
            return SQLiteProtectionDecision(
                reason=f"UNVERIFIED:{requirement}"
            )

    return SQLiteProtectionDecision(
        reason="ALL_DECLARED_PREREQUISITES_PRESENT_BUT_EXECUTION_DENIED"
    )
