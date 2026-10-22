"""Reusable evidence acquisition contract.

Pure declarations only. No I/O, database access, execution or authorization.
"""

from dataclasses import dataclass, field
from enum import Enum


class EvidenceDesignStatus(Enum):
    PROPOSED = "PROPOSED"
    DESIGN_APPROVED = "DESIGN_APPROVED"


@dataclass(frozen=True)
class EvidenceScope:
    platform_id: str
    purpose: str
    subject_id: str
    observation_date: str
    design_status: EvidenceDesignStatus


@dataclass(frozen=True)
class EvidenceAcquisitionDecision:
    scope: EvidenceScope
    reason: str = "EXECUTION_NOT_AUTHORIZED"
    source_access_authorized: bool = field(default=False, init=False)
    execution_authorized: bool = field(default=False, init=False)
    modification_authorized: bool = field(default=False, init=False)
    provenance_verified: bool = field(default=False, init=False)


def prepare_evidence_acquisition(scope: object) -> EvidenceAcquisitionDecision:
    """Record a well-formed scope without granting operational access."""

    if type(scope) is not EvidenceScope:
        raise ValueError("EXACT_EVIDENCE_SCOPE_REQUIRED")

    if type(scope.design_status) is not EvidenceDesignStatus:
        raise ValueError("INVALID_DESIGN_STATUS")

    for value in (
        scope.platform_id,
        scope.purpose,
        scope.subject_id,
        scope.observation_date,
    ):
        if type(value) is not str or not value.strip():
            raise ValueError("INVALID_EVIDENCE_SCOPE_FIELD")

    return EvidenceAcquisitionDecision(scope)