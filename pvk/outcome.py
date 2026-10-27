"""Pure capture assessment. No runner, legacy log heuristic, or approval API."""

from dataclasses import dataclass, field
from enum import Enum
import json
import re

from .contracts import Approval, Result, Status
from .trust import assess_evidence_trust
from .validation import valid_artifact_id, valid_sha256


class VerificationType(Enum):
    OBSERVATION = "OBSERVATION"
    UNIT_TEST_SUMMARY = "UNIT_TEST_SUMMARY"
    STATIC_COLLECTION = "STATIC_COLLECTION"


_STATIC_FILES = frozenset({
    "pvk/contracts.py", "pvk/engine.py", "pvk/integrity.py",
    "pvk/trust.py", "pvk/validation.py", "pvk/outcome.py",
})


@dataclass(frozen=True)
class Capture:
    stdout: str | None
    stderr: str | None
    exit_code: int | None
    completed: bool | None
    exception: str | None = None


@dataclass(frozen=True)
class Expectation:
    """Independent caller expectation, never inferred from captured stdout."""

    kind: VerificationType
    run_id: str
    subject_id: str
    required_checks: tuple[str, ...] = ()


@dataclass(frozen=True)
class Assessment:
    data_result: Result
    trust_result: Result
    result: Result
    os_isolation_approval: Approval = field(default=Approval.DENIED, init=False)
    platform_test_execution_approval: Approval = field(default=Approval.DENIED, init=False)


def _expectation_valid(value):
    if type(value) is not Expectation or type(value.kind) is not VerificationType:
        return False
    if not valid_artifact_id(value.run_id) or not valid_artifact_id(value.subject_id):
        return False
    checks = value.required_checks
    if type(checks) is not tuple or any(not valid_artifact_id(item) for item in checks):
        return False
    if len(checks) != len(set(checks)):
        return False
    if value.kind is VerificationType.OBSERVATION:
        return bool(checks)
    return not checks


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate_json_key")
        value[key] = item
    return value


def _reject_constant(value):
    raise ValueError("nonfinite_json_constant")


def _observation(report, expectation):
    if set(report) != {"schema", "run_id", "subject_id", "completed", "checks"}:
        return Result(Status.FAIL, ("observation_fields_mismatch",))
    checks = report["checks"]
    if type(checks) is not list:
        return Result(Status.FAIL, ("invalid_observation_checks",))
    states = {}
    for item in checks:
        if type(item) is not dict or set(item) != {"check_id", "status"}:
            return Result(Status.FAIL, ("invalid_observation_check",))
        key = item["check_id"]
        state = item["status"]
        if not valid_artifact_id(key) or type(state) is not str or state not in {s.value for s in Status}:
            return Result(Status.FAIL, ("invalid_observation_state",))
        if key in states or key not in expectation.required_checks:
            return Result(Status.FAIL, ("duplicate_or_unexpected_check",))
        states[key] = state
    if set(states) != set(expectation.required_checks):
        return Result(Status.FAIL, ("missing_observation_check",))
    if "FAIL" in states.values():
        return Result(Status.FAIL, ("observation_failed",))
    if "UNVERIFIED" in states.values():
        return Result(Status.UNVERIFIED, ("observation_unverified",))
    return Result(Status.PASS, ("supplied_observation_data_passed",))


def _unit_summary(report, expectation):
    if set(report) != {"schema", "run_id", "subject_id", "completed", "tests_run", "failures", "errors", "skipped"}:
        return Result(Status.FAIL, ("unit_summary_fields_mismatch",))
    counts = tuple(report[key] for key in ("tests_run", "failures", "errors", "skipped"))
    if any(type(value) is not int or value < 0 for value in counts):
        return Result(Status.FAIL, ("invalid_unit_counts",))
    total, failures, errors, skipped = counts
    if total == 0 or failures + errors + skipped > total:
        return Result(Status.FAIL, ("inconsistent_unit_counts",))
    if failures or errors:
        return Result(Status.FAIL, ("unit_summary_failed",))
    if skipped:
        return Result(Status.UNVERIFIED, ("unit_summary_has_skips",))
    return Result(Status.PASS, ("supplied_unit_summary_passed",))


def _static_collection(report, expectation):
    """Validate host-check v1 as collected data only. Never produce PASS."""
    expected_strings = {
        "schema": "pvk-host-check-v1", "status": "COLLECTED",
        "execution_approval": "DENIED", "python_tests": "NOT_RUN", "sandbox": "NOT_RUN",
        "verification_status": "UNVERIFIED", "integrity_status": "UNVERIFIED",
        "hash_kind": "OBSERVED_ONLY",
        "git_listing": "NORMAL_UNTRACKED_DIRECTORIES_MAY_BE_COLLAPSED",
    }
    if set(report) != set(expected_strings) | {"completed", "git_exit_code", "git_status", "files"}:
        return Result(Status.FAIL, ("static_collection_fields_mismatch",))
    if any(type(report[key]) is not str or report[key] != value for key, value in expected_strings.items()):
        return Result(Status.FAIL, ("static_collection_state_mismatch",))
    if report["completed"] is not True:
        return Result(Status.FAIL, ("static_collection_incomplete",))
    if type(report["git_exit_code"]) is not int or report["git_exit_code"] != 0:
        return Result(Status.FAIL, ("static_collection_git_failed",))
    entries = report["git_status"]
    if type(entries) is not list or any(
        type(entry) is not str or re.fullmatch(r"[ MADRCU?!T][ MADRCU?!T] .+", entry) is None
        for entry in entries
    ):
        return Result(Status.FAIL, ("invalid_static_git_status",))
    files = report["files"]
    if type(files) is not list or len(files) != len(_STATIC_FILES):
        return Result(Status.FAIL, ("static_file_count_mismatch",))
    seen = set()
    for item in files:
        if type(item) is not dict or set(item) != {"path", "sha256"}:
            return Result(Status.FAIL, ("invalid_static_file_contract",))
        path = item["path"]
        if type(path) is not str or path not in _STATIC_FILES or path in seen:
            return Result(Status.FAIL, ("static_file_set_mismatch",))
        if not valid_sha256(item["sha256"]):
            return Result(Status.FAIL, ("invalid_static_observed_hash",))
        seen.add(path)
    if seen != _STATIC_FILES:
        return Result(Status.FAIL, ("static_file_set_mismatch",))
    return Result(Status.UNVERIFIED, (
        "static_collection_collected", "observed_hashes_not_verified",
        "platform_verification_unverified",
    ))


def _assess_data(capture, expectation):
    if type(capture) is not Capture:
        return Result(Status.FAIL, ("invalid_capture_contract",))
    if capture.exception is not None:
        return Result(Status.FAIL, ("capture_exception",))
    if type(capture.stdout) is not str or type(capture.stderr) is not str:
        return Result(Status.FAIL, ("missing_or_invalid_stream",))
    if type(capture.exit_code) is not int or type(capture.completed) is not bool:
        return Result(Status.FAIL, ("missing_or_invalid_completion",))
    if capture.exit_code != 0:
        return Result(Status.FAIL, ("nonzero_exit_code",))
    if capture.completed is not True:
        return Result(Status.FAIL, ("capture_incomplete",))
    if capture.stderr != "":
        return Result(Status.FAIL, ("stderr_not_empty",))
    if not capture.stdout or len(capture.stdout) > 65536:
        return Result(Status.FAIL, ("empty_or_oversize_stdout",))
    try:
        report = json.loads(capture.stdout, object_pairs_hook=_unique_object, parse_constant=_reject_constant)
    except (ValueError, RecursionError):
        return Result(Status.FAIL, ("invalid_report_json",))
    if type(report) is not dict:
        return Result(Status.FAIL, ("invalid_report_object",))
    # Host-check v1 has no run/subject identity fields. Do not fabricate them or
    # rewrap its data as an OBSERVATION or a test summary.
    if expectation.kind is VerificationType.STATIC_COLLECTION:
        return _static_collection(report, expectation)
    rules = {
        VerificationType.OBSERVATION: ("pvk-observation-report-v1", _observation),
        VerificationType.UNIT_TEST_SUMMARY: ("pvk-unit-summary-v1", _unit_summary),
    }
    schema, rule = rules[expectation.kind]
    if (report.get("schema") != schema or report.get("run_id") != expectation.run_id
            or report.get("subject_id") != expectation.subject_id or report.get("completed") is not True):
        return Result(Status.FAIL, ("report_identity_or_completion_mismatch",))
    return rule(report, expectation)


def assess_capture(capture: object, expectation: object, *, provenance=None, now=None) -> Assessment:
    """Assess supplied data separately from trust; no final PASS is possible yet.

    Current trust core has no issuer/signature verifier. No Result or boolean
    trust override is accepted. Caller-supplied IDs/time are not authenticated.
    """
    if not _expectation_valid(expectation):
        failure = Result(Status.FAIL, ("invalid_expectation",))
        return Assessment(failure, Result(Status.UNVERIFIED, ("trust_not_assessed",)), failure)
    data = _assess_data(capture, expectation)
    trust = (Result(Status.UNVERIFIED, ("missing_provenance",)) if provenance is None else
             assess_evidence_trust(provenance, expected_subject_id=expectation.subject_id, now=now))
    if data.status is Status.FAIL or trust.status is Status.FAIL:
        final = Result(Status.FAIL, data.reasons + trust.reasons)
    else:
        final = Result(Status.UNVERIFIED, data.reasons + trust.reasons)
    return Assessment(data, trust, final)
