"""Fail-closed preflight for a future isolated test runner.

This module does not execute pytest, import test modules, or access databases.
Passing a preflight never authorizes test execution.
"""

from pathlib import Path
import sys


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent

    print("===== SAFE TEST RUNNER: PREFLIGHT ONLY =====")
    print(f"Project root: {project_root}")
    print("Test execution: DISABLED")
    print("OS isolation verification: NOT IMPLEMENTED")
    print("Allowlist verification: NOT IMPLEMENTED")
    print("Database access: NOT PERFORMED")
    print("Result: DENIED")
    print("Reason: Isolation and authorization checks are incomplete.")

    return 2


if __name__ == "__main__":
    sys.exit(main())
