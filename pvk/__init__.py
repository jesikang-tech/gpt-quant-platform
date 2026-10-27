"""Platform Verification Kit: assessment only, no runner or approval API."""

from .contracts import (
    Approval, BASELINE_POLICY, Evidence, IntegrityClaim, Policy, Result,
    RunKind, Status, VerificationInput, ManifestRequirements, EvidenceProvenance,
)
from .engine import evaluate
from .integrity import assess_integrity, assess_manifest
from .trust import assess_evidence_trust
from .validation import validate_input, validate_policy

__all__ = [
    "Approval", "BASELINE_POLICY", "Evidence", "IntegrityClaim", "Policy",
    "Result", "RunKind", "Status", "VerificationInput", "evaluate",
    "assess_integrity", "validate_input", "validate_policy",
    "ManifestRequirements", "EvidenceProvenance", "assess_manifest",
    "assess_evidence_trust",
]
