"""Pure fail-closed assessment of supplied evidence, never authorization."""

from .contracts import BASELINE_POLICY, Result, Status
from .validation import validate_input


def evaluate(value: object, policy: object = BASELINE_POLICY) -> Result:
    errors = validate_input(value, policy)
    if errors:
        return Result(Status.FAIL, errors)
    states = {item.check_id: item.status for item in value.evidence}
    failed = tuple("failed:" + key for key in policy.required_checks if states.get(key) is Status.FAIL)
    pending = tuple("unverified:" + key for key in policy.required_checks if states.get(key) in (None, Status.UNVERIFIED))
    if failed:
        return Result(Status.FAIL, failed + pending)
    if pending:
        return Result(Status.UNVERIFIED, pending)
    return Result(Status.PASS, ("supplied_evidence_passed",))
