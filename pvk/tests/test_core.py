"""Synthetic in-memory tests only. No filesystem, DB, process, or network."""

from dataclasses import FrozenInstanceError, replace
import unittest

from pvk import (
    Approval, BASELINE_POLICY, Evidence, IntegrityClaim, Policy, Result,
    Status, VerificationInput, assess_integrity, evaluate,
)


def request(*states):
    return VerificationInput("pvk-core-v1", tuple(
        Evidence(key, state) for key, state in zip(BASELINE_POLICY.required_checks, states)
    ))


class EngineTests(unittest.TestCase):
    def test_all_pass_still_denied(self):
        result = evaluate(request(Status.PASS, Status.PASS, Status.PASS))
        self.assertIs(result.status, Status.PASS)
        self.assertIs(result.execution_approval, Approval.DENIED)

    def test_fail_precedes_unverified(self):
        result = evaluate(request(Status.FAIL, Status.UNVERIFIED))
        self.assertIs(result.status, Status.FAIL)
        self.assertIn("unverified:isolation", result.reasons)

    def test_missing_and_explicit_unverified(self):
        for value in (request(), request(Status.PASS), request(Status.UNVERIFIED, Status.PASS, Status.PASS)):
            with self.subTest(value=value):
                self.assertIs(evaluate(value).status, Status.UNVERIFIED)

    def test_invalid_input_contracts(self):
        for value in (None, {}, [], "PASS", object()):
            self.assertIs(evaluate(value).status, Status.FAIL)

    def test_invalid_headers(self):
        good = request(Status.PASS)
        for value in (replace(good, policy_id="other"), replace(good, run_kind="VERIFICATION"),
                      replace(good, run_kind="OPERATIONAL"), replace(good, evidence=[])):
            self.assertIs(evaluate(value).status, Status.FAIL)

    def test_invalid_evidence(self):
        for items in ((None,), (Evidence("input", "PASS"),), (Evidence([], Status.PASS),),
                      (Evidence("unknown", Status.PASS),),
                      (Evidence("input", Status.PASS), Evidence("input", Status.FAIL))):
            self.assertIs(evaluate(VerificationInput("pvk-core-v1", items)).status, Status.FAIL)

    def test_unapproved_policies(self):
        for policy in (None, {}, Policy(policy_id="other"), Policy(required_checks=()),
                       Policy(required_checks=["input", "integrity", "isolation"]),
                       Policy(run_kind="VERIFICATION")):
            self.assertIs(evaluate(request(), policy).status, Status.FAIL)

    def test_exact_contract_types(self):
        class DerivedPolicy(Policy):
            pass
        self.assertIs(evaluate(request(), DerivedPolicy()).status, Status.FAIL)

    def test_every_state_combination_denied(self):
        for a in Status:
            for b in Status:
                for c in Status:
                    result = evaluate(request(a, b, c))
                    self.assertIs(result.execution_approval, Approval.DENIED)
                    expected = Status.FAIL if Status.FAIL in (a, b, c) else (
                        Status.UNVERIFIED if Status.UNVERIFIED in (a, b, c) else Status.PASS)
                    self.assertIs(result.status, expected)

    def test_frozen_contracts(self):
        objects = (BASELINE_POLICY, Evidence("input", Status.PASS), request(),
                   IntegrityClaim("asset", "a" * 64), Result(Status.FAIL, ("reason",)))
        for value in objects:
            name = next(iter(value.__dataclass_fields__))
            with self.assertRaises(FrozenInstanceError):
                setattr(value, name, None)

    def test_approval_not_constructor_argument(self):
        with self.assertRaises(TypeError):
            Result(Status.PASS, (), execution_approval="APPROVED")


class IntegrityTests(unittest.TestCase):
    def test_matching_digests(self):
        result = assess_integrity((IntegrityClaim("asset", "a" * 64, "a" * 64),))
        self.assertIs(result.status, Status.PASS)
        self.assertIs(result.execution_approval, Approval.DENIED)

    def test_mismatch_precedes_missing(self):
        result = assess_integrity((IntegrityClaim("a", "a" * 64, "b" * 64), IntegrityClaim("b", "a" * 64)))
        self.assertIs(result.status, Status.FAIL)
        self.assertIn("unverified:b", result.reasons)

    def test_empty_or_missing_observation(self):
        for claims in ((), (IntegrityClaim("asset", "a" * 64),)):
            self.assertIs(assess_integrity(claims).status, Status.UNVERIFIED)

    def test_invalid_manifest(self):
        for claims in (None, [], {}, (None,)):
            self.assertIs(assess_integrity(claims).status, Status.FAIL)

    def test_invalid_ids_and_digests(self):
        for identifier in ("", "../file", "C:\\file", "a/b", "a" * 129, None):
            self.assertIs(assess_integrity((IntegrityClaim(identifier, "a" * 64),)).status, Status.FAIL)
        for digest in ("", "A" * 64, "g" * 64, "a" * 63, "a" * 65, None, 123):
            self.assertIs(assess_integrity((IntegrityClaim("a", digest),)).status, Status.FAIL)
            if digest is not None:
                self.assertIs(assess_integrity((IntegrityClaim("a", "a" * 64, digest),)).status, Status.FAIL)

    def test_duplicate_artifacts(self):
        claim = IntegrityClaim("asset", "a" * 64, "a" * 64)
        self.assertIs(assess_integrity((claim, claim)).status, Status.FAIL)


if __name__ == "__main__":
    unittest.main()
