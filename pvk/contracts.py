"""Immutable, in-memory PVK v1 contracts; no execution capabilities."""

from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    """Supplied-data assessment only; PASS is neither verification nor permission."""

    PASS = "PASS"
    FAIL = "FAIL"
    UNVERIFIED = "UNVERIFIED"


class Approval(Enum):
    DENIED = "DENIED"


class RunKind(Enum):
    VERIFICATION = "VERIFICATION"


@dataclass(frozen=True)
class Policy:
    policy_id: str = "pvk-core-v1"
    required_checks: tuple[str, ...] = ("input", "integrity", "isolation")
    run_kind: RunKind = RunKind.VERIFICATION


@dataclass(frozen=True)
class Evidence:
    check_id: str
    status: Status


@dataclass(frozen=True)
class VerificationInput:
    policy_id: str
    evidence: tuple[Evidence, ...]
    run_kind: RunKind = RunKind.VERIFICATION


@dataclass(frozen=True)
class IntegrityClaim:
    """Logical artifact ID and externally supplied SHA-256 digests, not paths."""

    artifact_id: str
    expected_sha256: str
    observed_sha256: str | None = None


@dataclass(frozen=True)
class Result:
    """Publicly constructible report, never a trusted authorization token."""

    status: Status
    reasons: tuple[str, ...]
    execution_approval: Approval = field(default=Approval.DENIED, init=False)


@dataclass(frozen=True)
class ManifestRequirements:
    """Explicit logical ID set, encoded as a tuple so duplicates can be rejected."""

    artifact_ids: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceProvenance:
    """Untrusted declarations; UTC Unix seconds, expiry is exclusive."""

    source_id: str
    subject_id: str
    issued_at: int
    expires_at: int


BASELINE_POLICY = Policy()
