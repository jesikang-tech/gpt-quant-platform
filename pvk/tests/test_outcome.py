"""Synthetic outcome tests. Written only, not executed during implementation."""

from dataclasses import FrozenInstanceError, replace
import json
import unittest

from pvk.contracts import Approval, EvidenceProvenance, Result, Status
from pvk.outcome import Assessment, Capture, Expectation, VerificationType, assess_capture


def observation(**updates):
    report = {"schema": "pvk-observation-report-v1", "run_id": "run_1",
              "subject_id": "platform_1", "completed": True,
              "checks": [{"check_id": "probe", "status": "PASS"}]}
    report.update(updates)
    return Capture(json.dumps(report), "", 0, True)


def unit_summary(**updates):
    report = {"schema": "pvk-unit-summary-v1", "run_id": "run_1",
              "subject_id": "platform_1", "completed": True,
              "tests_run": 3, "failures": 0, "errors": 0, "skipped": 0}
    report.update(updates)
    return Capture(json.dumps(report), "", 0, True)


class OutcomeTests(unittest.TestCase):
    def setUp(self):
        self.expected = Expectation(VerificationType.OBSERVATION, "run_1", "platform_1", ("probe",))
        self.unit_expected = Expectation(VerificationType.UNIT_TEST_SUMMARY, "run_1", "platform_1")

    def check(self, capture, data_status, final_status=None, expectation=None, **kwargs):
        assessment = assess_capture(capture, self.expected if expectation is None else expectation, **kwargs)
        self.assertIs(assessment.data_result.status, data_status)
        self.assertIs(assessment.result.status, final_status or (
            Status.FAIL if data_status is Status.FAIL else Status.UNVERIFIED))
        for result in (assessment.data_result, assessment.trust_result, assessment.result):
            self.assertIs(result.execution_approval, Approval.DENIED)
        self.assertIs(assessment.os_isolation_approval, Approval.DENIED)
        self.assertIs(assessment.platform_test_execution_approval, Approval.DENIED)
        return assessment

    def test_observation_pass_is_data_only(self):
        result = self.check(observation(), Status.PASS)
        self.assertIs(result.trust_result.status, Status.UNVERIFIED)

    def test_unit_summary_uses_separate_rules(self):
        self.check(unit_summary(), Status.PASS, expectation=self.unit_expected)
        self.check(unit_summary(), Status.FAIL)
        self.check(observation(), Status.FAIL, expectation=self.unit_expected)

    def test_raw_pass_and_legacy_lines_not_accepted(self):
        for text in ("PASS", "OK", "PASS\n" * 9, '"PASS"', "[]", "null"):
            self.check(Capture(text, "", 0, True), Status.FAIL)

    def test_missing_or_invalid_capture(self):
        for value in (None, {}, Result(Status.PASS, ()), replace(observation(), stdout=None),
                      replace(observation(), stderr=None), replace(observation(), exit_code=None),
                      replace(observation(), completed=None), replace(observation(), exit_code=False),
                      replace(observation(), completed=1)):
            self.check(value, Status.FAIL)

    def test_failure_signals_override_pass_output(self):
        for value in (replace(observation(), exit_code=1), replace(observation(), exit_code=-1),
                      replace(observation(), stderr="PASS"), replace(observation(), stderr=" "),
                      replace(observation(), completed=False), replace(observation(), exception="error"),
                      replace(observation(), exception="")):
            self.check(value, Status.FAIL)

    def test_identity_completion_and_unknown_fields(self):
        for updates in ({"run_id": "other"}, {"subject_id": "other"}, {"completed": False},
                        {"completed": 1}, {"schema": "unknown"}, {"approval": "APPROVED"}):
            self.check(observation(**updates), Status.FAIL)

    def test_missing_duplicate_and_unknown_checks(self):
        for checks in ([], [{"check_id": "other", "status": "PASS"}],
                       [{"check_id": "probe", "status": "PASS"}] * 2,
                       [{"check_id": "probe", "status": "UNKNOWN"}],
                       [{"check_id": "probe", "status": True}],
                       [{"check_id": "probe", "status": "PASS", "extra": 1}], None):
            self.check(observation(checks=checks), Status.FAIL)

    def test_observation_fail_precedes_unverified(self):
        expected = replace(self.expected, required_checks=("probe", "second"))
        self.check(observation(checks=[{"check_id": "probe", "status": "UNVERIFIED"},
                                       {"check_id": "second", "status": "FAIL"}]),
                   Status.FAIL, expectation=expected)
        self.check(observation(checks=[{"check_id": "probe", "status": "UNVERIFIED"}]), Status.UNVERIFIED)

    def test_invalid_json_duplicate_keys_and_extra_output(self):
        good = observation().stdout
        for text in ("", "{" , good + good, "log\n" + good, good[:-1] + ',"completed":true}',
                     good.replace('"status": "PASS"', '"status":"PASS","status":"FAIL"'),
                     good.replace('"PASS"', "NaN"), "x" * 65537):
            self.check(Capture(text, "", 0, True), Status.FAIL)

    def test_unit_failures_errors_skips_and_zero_tests(self):
        for updates, status in (({"failures": 1}, Status.FAIL), ({"errors": 1}, Status.FAIL),
                                ({"failures": 1, "skipped": 1}, Status.FAIL),
                                ({"skipped": 1}, Status.UNVERIFIED), ({"tests_run": 0}, Status.FAIL)):
            self.check(unit_summary(**updates), status, expectation=self.unit_expected)

    def test_invalid_or_inconsistent_unit_counts(self):
        for updates in ({"tests_run": True}, {"failures": -1}, {"errors": "0"},
                        {"skipped": 0.0}, {"tests_run": 1, "skipped": 2}, {"extra": "PASS"}):
            self.check(unit_summary(**updates), Status.FAIL, expectation=self.unit_expected)

    def test_invalid_expectation_contracts(self):
        for expected in ({}, replace(self.expected, kind="OBSERVATION"),
                         replace(self.expected, run_id="../run"), replace(self.expected, required_checks=()),
                         replace(self.expected, required_checks=["probe"]),
                         replace(self.expected, required_checks=("probe", "probe")),
                         replace(self.unit_expected, required_checks=("probe",))):
            assessment = assess_capture(observation(), expected)
            self.assertIs(assessment.result.status, Status.FAIL)
            self.assertIs(assessment.result.execution_approval, Approval.DENIED)
            self.assertIs(assessment.os_isolation_approval, Approval.DENIED)
            self.assertIs(assessment.platform_test_execution_approval, Approval.DENIED)

    def test_self_declared_provenance_does_not_promote(self):
        provenance = EvidenceProvenance("trusted_issuer", "platform_1", 100, 200)
        self.check(observation(), Status.PASS, provenance=provenance, now=150)
        self.check(observation(), Status.PASS, Status.FAIL, provenance=provenance, now=200)
        self.check(observation(), Status.PASS, Status.FAIL, provenance=provenance)
        self.check(observation(), Status.PASS, Status.FAIL,
                   provenance=replace(provenance, subject_id="other"), now=150)

    def test_forged_result_not_accepted_as_capture_or_trust(self):
        forged = Result(Status.PASS, ())
        self.check(forged, Status.FAIL)
        self.check(observation(), Status.PASS, Status.FAIL, provenance=forged, now=150)

    def test_new_contracts_are_frozen(self):
        assessment = assess_capture(observation(), self.expected)
        for value, name in ((self.expected, "run_id"), (observation(), "completed"),
                            (assessment, "os_isolation_approval")):
            with self.assertRaises(FrozenInstanceError):
                setattr(value, name, None)
        with self.assertRaises(TypeError):
            Assessment(assessment.data_result, assessment.trust_result, assessment.result,
                       os_isolation_approval="APPROVED")

    def test_subclasses_rejected(self):
        class DerivedCapture(Capture):
            pass

        class DerivedExpectation(Expectation):
            pass

        self.check(DerivedCapture(observation().stdout, "", 0, True), Status.FAIL)
        result = assess_capture(observation(), DerivedExpectation(
            VerificationType.OBSERVATION, "run_1", "platform_1", ("probe",)))
        self.assertIs(result.result.status, Status.FAIL)
        self.assertIs(result.os_isolation_approval, Approval.DENIED)
        self.assertIs(result.platform_test_execution_approval, Approval.DENIED)


def static_report():
    return {
        "schema": "pvk-host-check-v1", "status": "COLLECTED", "completed": True,
        "git_exit_code": 0, "git_status": [],
        "git_listing": "NORMAL_UNTRACKED_DIRECTORIES_MAY_BE_COLLAPSED",
        "hash_kind": "OBSERVED_ONLY", "integrity_status": "UNVERIFIED",
        "verification_status": "UNVERIFIED", "execution_approval": "DENIED",
        "python_tests": "NOT_RUN", "sandbox": "NOT_RUN",
        "files": [{"path": path, "sha256": "a" * 64} for path in (
            "pvk/contracts.py", "pvk/engine.py", "pvk/integrity.py",
            "pvk/trust.py", "pvk/validation.py", "pvk/outcome.py",
        )],
    }


class StaticCollectionTests(unittest.TestCase):
    def setUp(self):
        self.expected = Expectation(VerificationType.STATIC_COLLECTION, "local_run", "platform_1")

    def check(self, report, expected_status=Status.FAIL, **capture_changes):
        capture = replace(Capture(json.dumps(report), "", 0, True), **capture_changes)
        result = assess_capture(capture, self.expected)
        self.assertIs(result.data_result.status, expected_status)
        self.assertIs(result.result.status, expected_status)
        for item in (result.data_result, result.trust_result, result.result):
            self.assertIs(item.execution_approval, Approval.DENIED)
        self.assertIs(result.os_isolation_approval, Approval.DENIED)
        self.assertIs(result.platform_test_execution_approval, Approval.DENIED)
        return result

    def test_collection_never_becomes_pass(self):
        result = self.check(static_report(), Status.UNVERIFIED)
        self.assertIn("static_collection_collected", result.data_result.reasons)
        self.assertIn("observed_hashes_not_verified", result.result.reasons)

    def test_every_required_field_missing_is_rejected(self):
        for key in static_report():
            report = static_report()
            del report[key]
            with self.subTest(missing=key):
                self.check(report)

    def test_unexpected_fields_and_failure_report_rejected(self):
        for extra in ({"error": "collection error"}, {"run_id": "forged"},
                      {"subject_id": "forged"}, {"tests_run": 10}, {"extra": None}):
            self.check(dict(static_report(), **extra))
        self.check(dict(static_report(), status="FAIL", completed=False, error="missing file"))

    def test_all_state_fields_strict(self):
        fields = ("schema", "status", "hash_kind", "integrity_status", "verification_status",
                  "execution_approval", "python_tests", "sandbox", "git_listing")
        for key in fields:
            for value in (None, True, 0, [], {}, "PASS", "", static_report()[key].swapcase()):
                with self.subTest(field=key, value=value):
                    self.check(dict(static_report(), **{key: value}))

    def test_completion_and_git_exit_types(self):
        for value in (False, None, 1, "true", [], {}):
            self.check(dict(static_report(), completed=value))
        for value in (False, True, None, 0.0, "0", 1, -1, [], {}):
            self.check(dict(static_report(), git_exit_code=value))

    def test_transport_failure_overrides_collected_json(self):
        for changes in ({"exit_code": 1}, {"exit_code": -1}, {"exit_code": False},
                        {"exit_code": None}, {"completed": False}, {"completed": None},
                        {"stderr": "error"}, {"stderr": None}, {"exception": "failure"},
                        {"stdout": None}):
            self.check(static_report(), **changes)

    def test_file_list_must_be_exact_and_unique(self):
        files = static_report()["files"]
        for value in (None, {}, "files", [], files[:-1], files + [files[0]],
                      files[:-1] + [files[0]], files[:-1] + [{"path": "pvk/other.py", "sha256": "a" * 64}]):
            self.check(dict(static_report(), files=value))
        self.check(dict(static_report(), files=list(reversed(files))), Status.UNVERIFIED)

    def test_file_record_and_path_types(self):
        for item in (None, [], "file", {}, {"path": "pvk/contracts.py"},
                     {"path": "pvk/contracts.py", "sha256": "a" * 64, "extra": 1},
                     {"path": [], "sha256": "a" * 64},
                     {"path": "pvk/../pvk/contracts.py", "sha256": "a" * 64},
                     {"path": "PVK/contracts.py", "sha256": "a" * 64}):
            report = static_report()
            report["files"][0] = item
            self.check(report)

    def test_sha256_strict_format(self):
        for digest in (None, 0, True, [], {}, "A" * 64, "a" * 63, "a" * 65, "g" * 64, "a" * 64 + "\n"):
            report = static_report()
            report["files"][0]["sha256"] = digest
            self.check(report)

    def test_git_entries_are_informational_and_typed(self):
        self.check(dict(static_report(), git_status=["?? new_directory/", " M pvk/outcome.py"]), Status.UNVERIFIED)
        for entries in (None, {}, "?? directory/", [None], [True], ["fatal: error"], ["?? a\nPASS"]):
            self.check(dict(static_report(), git_status=entries))

    def test_duplicate_top_and_nested_json_fields(self):
        text = json.dumps(static_report())
        for forged in (text[:-1] + ',"status":"COLLECTED"}',
                       text.replace('"sha256": "', '"sha256":"forged","sha256": "', 1)):
            self.check(static_report(), stdout=forged)

    def test_raw_pass_and_nonfinite_or_trailing_output(self):
        text = json.dumps(static_report())
        for forged in ("PASS", "PASS\n" * 9, text + text, "log\n" + text,
                       text.replace('"git_exit_code": 0', '"git_exit_code": NaN')):
            self.check(static_report(), stdout=forged)

    def test_collection_cannot_impersonate_existing_types(self):
        capture = Capture(json.dumps(static_report()), "", 0, True)
        for expected in (Expectation(VerificationType.OBSERVATION, "local_run", "platform_1", ("probe",)),
                         Expectation(VerificationType.UNIT_TEST_SUMMARY, "local_run", "platform_1")):
            result = assess_capture(capture, expected)
            self.assertIs(result.data_result.status, Status.FAIL)
            self.assertIs(result.result.execution_approval, Approval.DENIED)
        for capture in (observation(), unit_summary()):
            result = assess_capture(capture, self.expected)
            self.assertIs(result.result.status, Status.FAIL)
            self.assertIs(result.platform_test_execution_approval, Approval.DENIED)

    def test_no_checks_override_or_provenance_promotion(self):
        capture = Capture(json.dumps(static_report()), "", 0, True)
        result = assess_capture(capture, replace(self.expected, required_checks=("probe",)))
        self.assertIs(result.result.status, Status.FAIL)
        provenance = EvidenceProvenance("trusted_issuer", "platform_1", 100, 200)
        for now, status in ((150, Status.UNVERIFIED), (200, Status.FAIL)):
            result = assess_capture(capture, self.expected, provenance=provenance, now=now)
            self.assertIs(result.data_result.status, Status.UNVERIFIED)
            self.assertIs(result.result.status, status)
            self.assertIs(result.result.execution_approval, Approval.DENIED)
            self.assertIs(result.os_isolation_approval, Approval.DENIED)
