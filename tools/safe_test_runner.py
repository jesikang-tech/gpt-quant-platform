"""Fail-closed preflight for a future isolated test runner.

This module never executes pytest or imports test modules.
Allowlist membership does not authorize test execution.
"""

from enum import Enum
from pathlib import Path
import sys


ALLOWED_TEST_FILES = frozenset({
    "test_price_test_import_safety.py",
})


class OSIsolationStatus(Enum):
    NOT_IMPLEMENTED = "NOT IMPLEMENTED"
    UNCONFIRMED = "UNCONFIRMED"


def check_os_isolation() -> OSIsolationStatus:
    """Report unavailable verification without probing OS or data resources.

    No trusted procedure exists to prove OS-level access denial. Environment
    variables, file presence, identity and privilege are not isolation evidence.
    A VERIFIED status is deliberately not provided.
    """
    return OSIsolationStatus.NOT_IMPLEMENTED


def os_isolation_approved(status: object) -> bool:
    """Deny every status, including unknown or externally supplied values.

    This preflight cannot approve isolation or authorize execution.
    """
    return False


def validate_candidate(candidate: str) -> tuple[bool, str]:
    if not candidate:
        return False, "No test candidate supplied."

    if (
        "/" in candidate
        or "\\" in candidate
        or ":" in candidate
        or candidate in (".", "..")
    ):
        return False, "Paths are not accepted; use an exact filename."

    if candidate not in ALLOWED_TEST_FILES:
        return False, "Candidate is not on the allowlist."

    return True, "Candidate filename is on the allowlist."


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent

    print("===== SAFE TEST RUNNER: PREFLIGHT ONLY =====")
    print(f"Project root: {project_root}")
    print("Test execution: DISABLED")
    isolation_status = check_os_isolation()
    isolation_approved = os_isolation_approved(isolation_status)
    print(f"OS isolation verification: {isolation_status.value}")
    print(f"OS isolation approval: {'APPROVED' if isolation_approved else 'DENIED'}")
    print("Database access: NOT PERFORMED")

    if len(sys.argv) != 2:
        print("Allowlist verification: DENIED")
        print("Reason: Supply exactly one candidate filename.")
    else:
        allowed, reason = validate_candidate(sys.argv[1])
        print(f"Allowlist verification: {'MATCH' if allowed else 'DENIED'}")
        print(f"Reason: {reason}")

    print("Result: DENIED")
    print("Reason: Test execution is disabled until OS isolation is verified.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
