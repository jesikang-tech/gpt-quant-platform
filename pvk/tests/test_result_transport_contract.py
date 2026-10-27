"""Fail-closed tests for memory-only result transport declarations."""

import hashlib
import unittest
from dataclasses import replace

from pvk.contracts import Approval, Status
from pvk.result_transport_contract import (
    MAX_RESULT_BYTES,
    ResultEnvelope,
    ResultStream,
    TransportIdentity,
    validate_result_envelope,
)


class ResultTransportContractTests(unittest.TestCase):
    def setUp(self):
        self.identity = TransportIdentity(
            "request-1", "baseline-1", "runner-1",
            "runtime-1", "config-1",
        )

    def stream(self, name, content):
        return ResultStream(
            name, len(content), hashlib.sha256(content).hexdigest(), content
        )

    def envelope(self, stdout=b"OK", stderr=b""):
        return ResultEnvelope(
            self.identity,
            (self.stream("stdout", stdout), self.stream("stderr", stderr)),
        )

    def assess(self, envelope, expected=None):
        return validate_result_envelope(
            envelope,
            expected_identity=self.identity if expected is None else expected,
        )

    def assert_denied(self, assessment):
        self.assertEqual(assessment.execution_approval, Approval.DENIED)
        self.assertEqual(assessment.platform_execution, Approval.DENIED)
        self.assertEqual(assessment.os_isolation_approval, Approval.DENIED)
        self.assertEqual(assessment.os_boundary, Status.UNVERIFIED)
        self.assertFalse(assessment.provenance_verified)
        self.assertEqual(assessment.operating_db_access, "PROHIBITED")

    def test_matching_declarations_remain_unverified(self):
        result = self.assess(self.envelope())
        self.assertEqual(result.result.status, Status.UNVERIFIED)
        self.assert_denied(result)

    def test_empty_streams_are_permitted_but_unverified(self):
        result = self.assess(self.envelope(b"", b""))
        self.assertEqual(result.result.status, Status.UNVERIFIED)
        self.assert_denied(result)

    def test_expected_identity_mismatch_fails(self):
        wrong = replace(self.identity, request_id="request-2")
        result = self.assess(self.envelope(), wrong)
        self.assertEqual(result.result.status, Status.FAIL)
        self.assert_denied(result)

    def test_forged_stream_hash_fails(self):
        envelope = self.envelope()
        forged = replace(
            envelope.streams[0], declared_sha256="0" * 64
        )
        result = self.assess(
            replace(envelope, streams=(forged, envelope.streams[1]))
        )
        self.assertEqual(result.result.status, Status.FAIL)
        self.assert_denied(result)

    def test_duplicate_stdout_streams_fail(self):
        envelope = self.envelope()
        result = self.assess(
            replace(envelope, streams=(envelope.streams[0], envelope.streams[0]))
        )
        self.assertEqual(result.result.status, Status.FAIL)
        self.assert_denied(result)

    def test_missing_stream_fails(self):
        envelope = self.envelope()
        result = self.assess(
            replace(envelope, streams=(envelope.streams[0],))
        )
        self.assertEqual(result.result.status, Status.FAIL)
        self.assert_denied(result)

    def test_aggregate_size_limit_fails(self):
        result = self.assess(
            self.envelope(b"A" * MAX_RESULT_BYTES, b"B")
        )
        self.assertEqual(result.result.status, Status.FAIL)
        self.assert_denied(result)

    def test_declared_size_mismatch_fails(self):
        envelope = self.envelope()
        wrong = replace(envelope.streams[0], size_bytes=100)
        result = self.assess(
            replace(envelope, streams=(wrong, envelope.streams[1]))
        )
        self.assertEqual(result.result.status, Status.FAIL)
        self.assert_denied(result)

    def test_non_bytes_content_fails(self):
        envelope = self.envelope()
        wrong = replace(envelope.streams[0], content="OK")
        result = self.assess(
            replace(envelope, streams=(wrong, envelope.streams[1]))
        )
        self.assertEqual(result.result.status, Status.FAIL)
        self.assert_denied(result)

    def test_invalid_envelope_type_fails(self):
        result = self.assess({"identity": self.identity})
        self.assertEqual(result.result.status, Status.FAIL)
        self.assert_denied(result)


if __name__ == "__main__":
    unittest.main()
