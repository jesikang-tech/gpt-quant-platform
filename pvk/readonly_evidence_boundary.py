"""Reusable, fail-closed evidence acquisition design boundary.

Pure contract only. No SQLite imports, filesystem operations,
database access, snapshot creation, subprocesses, or authorization.
"""

from dataclasses import dataclass, field
from enum import Enum


class EvidenceAccessMode(str, Enum):
    READ_ONLY = "READ_ONLY"


class EvidenceBoundaryStatus(str, Enum):
    DENIED = "DENIED"


@dataclass(frozen=True)
class ReadOnlyEvidenceRequest:
    purpose: str
    scope_id: str
    access_mode: EvidenceAccessMode = EvidenceAccessMode.READ_ONLY


@dataclass(frozen=True)
class ReadOnlyEvidenceDecision:
    status: EvidenceBoundaryStatus
    reason: str
    source_access_authorized: bool = field(default=False, init=False)
    execution_authorized: bool = field(default=False, init=False)
    source_modification_authorized: bool = field(default=False, init=False)
    snapshot_authorized: bool = field(default=False, init=False)


def assess_readonly_evidence_request(
    request: object,
) -> ReadOnlyEvidenceDecision:
    """Assess request shape; never grant operational access."""

    if type(request) is not ReadOnlyEvidenceRequest:
        return ReadOnlyEvidenceDecision(
            EvidenceBoundaryStatus.DENIED,
            "INVALID_REQUEST_TYPE",
        )

    if (
        type(request.purpose) is not str
        or not request.purpose.strip()
        or type(request.scope_id) is not str
        or not request.scope_id.strip()
    ):
        return ReadOnlyEvidenceDecision(
            EvidenceBoundaryStatus.DENIED,
            "INVALID_REQUEST_SCOPE",
        )

    if request.access_mode is not EvidenceAccessMode.READ_ONLY:
        return ReadOnlyEvidenceDecision(
            EvidenceBoundaryStatus.DENIED,
            "UNSUPPORTED_ACCESS_MODE",
        )

    return ReadOnlyEvidenceDecision(
        EvidenceBoundaryStatus.DENIED,
        "EXECUTION_AND_SOURCE_ACCESS_NOT_APPROVED",
    )
