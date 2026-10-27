"""Strict pure validation. External strings are never coerced into enums."""

import re

from .contracts import Evidence, Policy, RunKind, Status, VerificationInput


def validate_policy(policy: object) -> tuple[str, ...]:
    # Explicit literals avoid trusting a replaceable external policy registry.
    if type(policy) is not Policy:
        return ("invalid_policy_contract",)
    if (
        type(policy.policy_id) is not str
        or policy.policy_id != "pvk-core-v1"
        or type(policy.required_checks) is not tuple
        or any(type(item) is not str for item in policy.required_checks)
        or policy.required_checks != ("input", "integrity", "isolation")
        or policy.run_kind is not RunKind.VERIFICATION
    ):
        return ("unapproved_policy",)
    return ()


def validate_input(value: object, policy: object) -> tuple[str, ...]:
    errors = validate_policy(policy)
    if errors:
        return errors
    if type(value) is not VerificationInput:
        return ("invalid_input_contract",)
    if (
        type(value.policy_id) is not str
        or value.policy_id != policy.policy_id
        or value.run_kind is not RunKind.VERIFICATION
        or type(value.evidence) is not tuple
    ):
        return ("invalid_input_header",)
    seen = set()
    for item in value.evidence:
        if type(item) is not Evidence:
            return ("invalid_evidence_contract",)
        if type(item.check_id) is not str or type(item.status) is not Status:
            return ("invalid_evidence_fields",)
        if item.check_id not in policy.required_checks:
            return ("unknown_check",)
        if item.check_id in seen:
            return ("duplicate_check",)
        seen.add(item.check_id)
    return ()


def valid_artifact_id(value: object) -> bool:
    return type(value) is str and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}", value) is not None


def valid_sha256(value: object) -> bool:
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def valid_test_id(value: object) -> bool:
    """Canonical ASCII module.Class.test_method label; never resolved/imported."""
    return type(value) is str and len(value) <= 256 and re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*\.test_[A-Za-z0-9_]+", value,
    ) is not None
