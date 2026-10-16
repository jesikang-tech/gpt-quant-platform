"""OS isolation evidence contract.

Evidence records are descriptive only.
They do not authorize test execution.
"""

from dataclasses import dataclass
from enum import Enum


class EvidenceStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNVERIFIED = "UNVERIFIED"


@dataclass(frozen=True)
class IsolationEvidence:
    sandbox_configuration: EvidenceStatus
    virtual_machine_identity: EvidenceStatus
    network_isolation: EvidenceStatus
    readonly_mapping: EvidenceStatus
    host_filesystem_isolation: EvidenceStatus
    dependency_review: EvidenceStatus


@dataclass(frozen=True)
class IsolationDecision:
    evidence_complete: bool
    execution_authorized: bool
    reason: str


def evaluate_isolation_evidence(
    evidence: IsolationEvidence,
) -> IsolationDecision:
    """Summarize evidence without granting execution authority."""

    if not isinstance(evidence, IsolationEvidence):
        return IsolationDecision(
            evidence_complete=False,
            execution_authorized=False,
            reason="Invalid evidence contract.",
        )

    statuses = (
        evidence.sandbox_configuration,
        evidence.virtual_machine_identity,
        evidence.network_isolation,
        evidence.readonly_mapping,
        evidence.host_filesystem_isolation,
        evidence.dependency_review,
    )

    complete = all(
        isinstance(status, EvidenceStatus)
        and status is EvidenceStatus.PASS
        for status in statuses
    )

    return IsolationDecision(
        evidence_complete=complete,
        execution_authorized=False,
        reason=(
            "Evidence recorded; execution authorization is not implemented."
            if complete
            else "Evidence incomplete; execution denied."
        ),
    )