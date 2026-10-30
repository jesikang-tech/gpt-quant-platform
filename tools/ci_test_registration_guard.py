"""Static, fail-closed test registration check for one isolated pytest workflow."""

from pathlib import Path
import re
import sys


class RegistrationError(ValueError):
    """Unsupported or inconsistent CI test registration."""


def reject_conditional_execution(text: str) -> None:
    """Reject conditional execution in the two required CI jobs."""
    required_jobs = ("synthetic-contract", "ci-registration-guard")
    lines = text.splitlines()

    job_positions = [
        (index, match.group(1))
        for index, line in enumerate(lines)
        if (match := re.fullmatch(r"  ([A-Za-z0-9_-]+):\s*", line))
    ]

    for job_name in required_jobs:
        matches = [
            index for index, name in job_positions if name == job_name
        ]

        if len(matches) != 1:
            raise RegistrationError(
                f"Required CI job missing or duplicated: {job_name}"
            )

        start = matches[0]
        end = next(
            (index for index, _ in job_positions if index > start),
            len(lines),
        )

        for line in lines[start + 1:end]:
            if re.match(r"^\s*(?:-\s*)?if\s*:", line):
                raise RegistrationError(
                    f"Conditional CI execution unsupported: {job_name}"
                )

def check_registration(root: Path) -> tuple[str, ...]:
    root = Path(root)
    tests_dir = root / "price-provider-validation" / "tests"
    workflow = root / ".github" / "workflows" / "parallel-price-provider-contract.yml"

    if not tests_dir.is_dir() or not workflow.is_file():
        raise RegistrationError("Required test directory or workflow missing")

    nested_tests = sorted(
        path.relative_to(tests_dir).as_posix()
        for path in tests_dir.rglob("test_*.py")
        if path.is_file() and path.parent != tests_dir
    )

    if nested_tests:
        raise RegistrationError(
            f"Unsupported nested test files: {nested_tests}"
        )

    actual = {
        f"tests/{path.name}"
        for path in tests_dir.glob("test_*.py")
        if path.is_file()
    }

    text = workflow.read_text(encoding="utf-8")

    marker = "  synthetic-contract:\n"
    next_job = "\n  ci-registration-guard:\n"

    if text.count(marker) != 1 or text.count(next_job) != 1:
        raise RegistrationError("Required CI job boundaries missing or duplicated")

    start = text.index(marker) + len(marker)
    end = text.index(next_job, start)

    if end <= start:
        raise RegistrationError("Invalid CI job order")

    reject_conditional_execution(text)

    scoped_text = text[start:end]

    lines = [
        line.strip()
        for line in scoped_text.splitlines()
        if re.match(r"^\s*(?:-\s*)?run:\s*python -m pytest\b", line)
    ]

    if len(lines) != 1:
        raise RegistrationError("Expected exactly one supported pytest command")

    command = lines[0]

    if any(character in command for character in ("|", ">", "<", ";", "&", "$", "`")):
        raise RegistrationError("Unsupported shell syntax")

    tokens = command.split()

    if tokens and tokens[0] == "-":
        tokens = tokens[1:]

    if tokens[:5] != ["run:", "python", "-m", "pytest", "-q"]:
        raise RegistrationError("Unsupported pytest invocation")

    arguments = tokens[5:]

    if not arguments:
        raise RegistrationError("No test files registered")

    if any(not re.fullmatch(r"tests/test_[A-Za-z0-9_]+\.py", arg) for arg in arguments):
        raise RegistrationError("Unsupported test argument")

    if len(arguments) != len(set(arguments)):
        raise RegistrationError("Duplicate test registration")

    registered = set(arguments)

    missing = sorted(actual - registered)
    unknown = sorted(registered - actual)

    if missing or unknown:
        raise RegistrationError(
            f"Missing registrations: {missing}; unknown registrations: {unknown}"
        )

    return tuple(sorted(registered))


def main() -> int:
    try:
        root = Path(__file__).resolve().parent.parent
        registered = check_registration(root)
    except (RegistrationError, OSError, UnicodeError) as exc:
        print(f"CI_TEST_REGISTRATION: FAIL: {exc}", file=sys.stderr)
        return 1

    print(f"CI_TEST_REGISTRATION: PASS ({len(registered)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
