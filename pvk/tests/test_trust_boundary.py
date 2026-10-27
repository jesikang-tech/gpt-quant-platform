"""Additional synthetic tests, authored only; no external resources."""

from dataclasses import FrozenInstanceError, replace
import unittest

from pvk import (
    Approval, EvidenceProvenance, IntegrityClaim, ManifestRequirements, Result,
    Status, assess_evidence_trust, assess_integrity, assess_manifest,
)


def claim(identifier="asset"):
    return IntegrityClaim(identifier, "a" * 64, "a" * 64)


class BoundaryAssertions(unittest.TestCase):
    def check_result(self, result, status, reason=None):
        self.assertIs(result.status, status)
        self.assertIs(result.execution_approval, Approval.DENIED)
        if reason is not None:
            self.assertIn(reason, result.reasons)


class ManifestTests(BoundaryAssertions):
    def test_exact_manifest(self):
        self.check_result(assess_manifest((claim(),), ManifestRequirements(("asset",))), Status.PASS)

    def test_missing_required_artifact(self):
        self.check_result(assess_manifest((), ManifestRequirements(("asset",))),
                          Status.FAIL, "missing_artifact:asset")

    def test_unexpected_artifact(self):
        self.check_result(assess_manifest((claim(), claim("extra")), ManifestRequirements(("asset",))),
                          Status.FAIL, "unexpected_artifact:extra")

    def test_duplicate_artifact(self):
        self.check_result(assess_manifest((claim(), claim()), ManifestRequirements(("asset",))),
                          Status.FAIL, "duplicate_artifact:asset")

    def test_membership_errors_are_distinct(self):
        result = assess_manifest((claim("extra"), claim("extra")), ManifestRequirements(("asset",)))
        self.check_result(result, Status.FAIL)
        for reason in ("missing_artifact:asset", "unexpected_artifact:extra", "duplicate_artifact:extra"):
            self.assertIn(reason, result.reasons)

    def test_invalid_required_lists(self):
        for required in ((), [], ["asset"], "asset", None, (None,), ([],), ("../asset",), ("",)):
            with self.subTest(required=required):
                self.check_result(assess_manifest((claim(),), ManifestRequirements(required)), Status.FAIL)

    def test_duplicate_required_ids(self):
        self.check_result(assess_manifest((claim(),), ManifestRequirements(("asset", "asset"))),
                          Status.FAIL, "duplicate_required_artifact")

    def test_invalid_contracts(self):
        for requirements in (None, {}, ("asset",)):
            self.check_result(assess_manifest((claim(),), requirements), Status.FAIL)
        for claims in (None, [], (None,), (IntegrityClaim([], "a" * 64),)):
            self.check_result(assess_manifest(claims, ManifestRequirements(("asset",))), Status.FAIL)

    def test_digest_validation_is_retained(self):
        requirements = ManifestRequirements(("asset",))
        for item, status in ((replace(claim(), observed_sha256=None), Status.UNVERIFIED),
                             (replace(claim(), observed_sha256="b" * 64), Status.FAIL),
                             (replace(claim(), expected_sha256="invalid"), Status.FAIL),
                             (replace(claim(), observed_sha256="invalid"), Status.FAIL)):
            self.check_result(assess_manifest((item,), requirements), status)

    def test_legacy_empty_manifest_unchanged(self):
        self.check_result(assess_integrity(()), Status.UNVERIFIED, "empty_manifest")
        self.check_result(assess_integrity((claim(),)), Status.PASS)

    def test_membership_order_independent(self):
        self.check_result(assess_manifest((claim("b"), claim("a")),
                                        ManifestRequirements(("a", "b"))), Status.PASS)


class ProvenanceTests(BoundaryAssertions):
    def assess(self, provenance=None, **kwargs):
        return assess_evidence_trust(
            provenance if provenance is not None else EvidenceProvenance("issuer", "asset", 100, 200),
            expected_subject_id=kwargs.get("subject", "asset"), now=kwargs.get("now", 150),
        )

    def test_self_declared_source_never_trusted(self):
        for source in ("issuer", "trusted_issuer", "forged_admin"):
            self.check_result(self.assess(EvidenceProvenance(source, "asset", 100, 200)),
                              Status.UNVERIFIED, "issuer_and_signature_unverified")

    def test_self_declared_time_never_trusted(self):
        self.check_result(self.assess(), Status.UNVERIFIED, "declared_time_unverified")

    def test_expiry_boundary_and_expired(self):
        for now in (200, 201):
            self.check_result(self.assess(now=now), Status.FAIL, "evidence_expired")

    def test_issue_boundary_is_unverified(self):
        self.check_result(self.assess(now=100), Status.UNVERIFIED)

    def test_future_evidence(self):
        self.check_result(self.assess(now=99), Status.FAIL, "evidence_from_future")

    def test_invalid_validity_window(self):
        for expiry in (99, 100):
            self.check_result(self.assess(EvidenceProvenance("issuer", "asset", 100, expiry)),
                              Status.FAIL, "invalid_validity_window")

    def test_wrong_subject(self):
        self.check_result(self.assess(subject="other"), Status.FAIL, "evidence_subject_mismatch")

    def test_invalid_or_unavailable_time(self):
        for value in (None, True, "150", 150.0, -1):
            self.check_result(self.assess(now=value), Status.FAIL)
            self.check_result(self.assess(EvidenceProvenance("issuer", "asset", value, 200)), Status.FAIL)
            self.check_result(self.assess(EvidenceProvenance("issuer", "asset", 100, value)), Status.FAIL)

    def test_invalid_provenance_contract_or_identity(self):
        for value in (None, {}, "trusted", Result(Status.PASS, ())):
            self.check_result(assess_evidence_trust(value, expected_subject_id="asset", now=150), Status.FAIL)
        for value in (None, "", "../asset", []):
            self.check_result(self.assess(subject=value), Status.FAIL)
            self.check_result(self.assess(EvidenceProvenance(value, "asset", 100, 200)), Status.FAIL)
            self.check_result(self.assess(EvidenceProvenance("issuer", value, 100, 200)), Status.FAIL)

    def test_direct_pass_result_has_no_authority(self):
        result = Result(Status.PASS, ("self_declared",))
        self.check_result(result, Status.PASS)
        self.check_result(assess_evidence_trust(result, expected_subject_id="asset", now=150), Status.FAIL)

    def test_new_contracts_frozen(self):
        for value, field in ((ManifestRequirements(("asset",)), "artifact_ids"),
                             (EvidenceProvenance("issuer", "asset", 100, 200), "source_id")):
            with self.assertRaises(FrozenInstanceError):
                setattr(value, field, None)

    def test_subclasses_rejected(self):
        class DerivedRequirements(ManifestRequirements):
            pass

        class DerivedProvenance(EvidenceProvenance):
            pass

        self.check_result(assess_manifest((claim(),), DerivedRequirements(("asset",))), Status.FAIL)
        self.check_result(self.assess(DerivedProvenance("issuer", "asset", 100, 200)), Status.FAIL)
