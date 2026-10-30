"""Synthetic-only tests for the static CI registration guard."""

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ci_test_registration_guard import RegistrationError, check_registration


def make_fixture(tmp_path, names=("test_alpha.py", "test_beta.py"), arguments=None):
    tests = tmp_path / "price-provider-validation" / "tests"
    tests.mkdir(parents=True)

    for name in names:
        (tests / name).write_text("# synthetic test file\n", encoding="utf-8")

    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)

    if arguments is None:
        arguments = [f"tests/{name}" for name in names]

    command = "python -m pytest -q " + " ".join(arguments)

    workflow = workflows / "parallel-price-provider-contract.yml"
    workflow.write_text(
        "name: Synthetic\n"
        "jobs:\n"
        "  synthetic-contract:\n"
        "    steps:\n"
        f"      - run: {command}\n"
        "  ci-registration-guard:\n"
        "    steps:\n"
        "      - run: python tools/ci_test_registration_guard.py\n",
        encoding="utf-8",
    )

    return workflow


def test_exact_registration_passes(tmp_path):
    make_fixture(tmp_path)
    assert check_registration(tmp_path) == (
        "tests/test_alpha.py",
        "tests/test_beta.py",
    )


def test_new_unregistered_test_is_rejected(tmp_path):
    make_fixture(tmp_path, arguments=["tests/test_alpha.py"])

    with pytest.raises(RegistrationError, match="Missing registrations"):
        check_registration(tmp_path)


def test_nonexistent_registered_test_is_rejected(tmp_path):
    make_fixture(
        tmp_path,
        arguments=[
            "tests/test_alpha.py",
            "tests/test_beta.py",
            "tests/test_missing.py",
        ],
    )

    with pytest.raises(RegistrationError, match="unknown registrations"):
        check_registration(tmp_path)


def test_duplicate_registration_is_rejected(tmp_path):
    make_fixture(
        tmp_path,
        arguments=[
            "tests/test_alpha.py",
            "tests/test_alpha.py",
            "tests/test_beta.py",
        ],
    )

    with pytest.raises(RegistrationError, match="Duplicate"):
        check_registration(tmp_path)


@pytest.mark.parametrize(
    "arguments",
    [
        ["tests/test_alpha.py", "--collect-only"],
        ["tests/test_alpha.py", "tests/test_beta.py;"],
        ["tests/test_alpha.py", "tests/test_beta.py::test_case"],
        ["tests/test_alpha.py", "$EXTRA_TESTS"],
    ],
)
def test_unsupported_arguments_are_rejected(tmp_path, arguments):
    make_fixture(tmp_path, arguments=arguments)

    with pytest.raises(RegistrationError):
        check_registration(tmp_path)


def test_missing_workflow_is_rejected(tmp_path):
    workflow = make_fixture(tmp_path)
    workflow.unlink()

    with pytest.raises(RegistrationError, match="missing"):
        check_registration(tmp_path)


def test_multiple_pytest_commands_are_rejected(tmp_path):
    workflow = make_fixture(tmp_path)

    text = workflow.read_text(encoding="utf-8")
    text = text.replace(
        "  ci-registration-guard:\n",
        "      - run: python -m pytest -q tests/test_alpha.py\n"
        "  ci-registration-guard:\n",
    )
    workflow.write_text(text, encoding="utf-8")

    with pytest.raises(RegistrationError, match="exactly one"):
        check_registration(tmp_path)


def test_scoped_job_ignores_other_pytest_invocations(tmp_path):
    workflow = make_fixture(tmp_path)
    text = workflow.read_text(encoding="utf-8")
    text += (
        "  unrelated-job:\n"
        "    steps:\n"
        "      - run: python -m pytest -q tests/test_unrelated.py\n"
    )
    workflow.write_text(text, encoding="utf-8")
    assert len(check_registration(tmp_path)) == 2
