"""Memory-only transfer declarations; not a transport, parser or authenticator.

The caller supplies an independent expected identity and exactly two byte
streams. SHA-256 binds declarations to those bytes only, not to a trusted
baseline or real guest. IDs do not attest runner/runtime/config contents.
Replay, freshness, completeness and actual exit status are not established.
Public frozen reports are not credentials or a malicious-Python boundary.
"""

from dataclasses import dataclass, field
from hashlib import sha256

from .contracts import Approval, Result, Status
from .validation import valid_artifact_id, valid_sha256


MAX_RESULT_BYTES = 65536  # Aggregate stdout + stderr bytes, not UTF-16 characters.


@dataclass(frozen=True)
class TransportIdentity:
    request_id: str
    baseline_id: str
    runner_id: str
    runtime_id: str
    sandbox_config_id: str


@dataclass(frozen=True)
class ResultStream:
    stream_id: str
    size_bytes: int
    declared_sha256: str
    content: bytes


@dataclass(frozen=True)
class ResultEnvelope:
    identity: TransportIdentity
    streams: tuple[ResultStream, ...]


@dataclass(frozen=True)
class TransportAssessment:
    result: Result
    execution_approval: Approval = field(default=Approval.DENIED, init=False)
    os_isolation_approval: Approval = field(default=Approval.DENIED, init=False)
    os_boundary: Status = field(default=Status.UNVERIFIED, init=False)
    provenance_verified: bool = field(default=False, init=False)
    platform_execution: Approval = field(default=Approval.DENIED, init=False)
    operating_db_access: str = field(default="PROHIBITED", init=False)


def _identity_valid(value):
    return type(value) is TransportIdentity and all(valid_artifact_id(item) for item in (
        value.request_id, value.baseline_id, value.runner_id,
        value.runtime_id, value.sandbox_config_id,
    ))


def _fail(reason):
    return TransportAssessment(Result(Status.FAIL, (reason,)))


def validate_result_envelope(envelope: object, *, expected_identity: object) -> TransportAssessment:
    """Validate exact types, independent ID equality and byte declarations.

    Streams are a tuple so duplicates cannot disappear in a dictionary. Empty
    streams are allowed (notably stderr); this does not establish completion
    or a valid observation. No decoding, JSON conversion or outcome promotion
    occurs. No caller-provided trust/approval flag or size-limit override exists.
    """
    if type(envelope) is not ResultEnvelope:
        return _fail("invalid_envelope_contract")
    if not _identity_valid(expected_identity) or not _identity_valid(envelope.identity):
        return _fail("invalid_transport_identity")
    if envelope.identity != expected_identity:
        return _fail("transport_identity_mismatch")
    streams = envelope.streams
    if type(streams) is not tuple or len(streams) != 2:
        return _fail("invalid_stream_tuple")
    seen = set()
    total = 0
    for stream in streams:
        if type(stream) is not ResultStream:
            return _fail("invalid_stream_contract")
        if type(stream.stream_id) is not str or stream.stream_id not in ("stdout", "stderr"):
            return _fail("invalid_stream_id")
        if stream.stream_id in seen:
            return _fail("duplicate_stream_id")
        seen.add(stream.stream_id)
        if type(stream.size_bytes) is not int or not 0 <= stream.size_bytes <= MAX_RESULT_BYTES:
            return _fail("invalid_declared_size")
        if type(stream.content) is not bytes:
            return _fail("invalid_content_type")
        if len(stream.content) != stream.size_bytes:
            return _fail("stream_size_mismatch")
        total += stream.size_bytes
        if total > MAX_RESULT_BYTES:
            return _fail("aggregate_size_limit")
        if not valid_sha256(stream.declared_sha256):
            return _fail("invalid_sha256_declaration")
        if sha256(stream.content).hexdigest() != stream.declared_sha256:
            return _fail("stream_hash_mismatch")
    if seen != {"stdout", "stderr"}:
        return _fail("stream_set_mismatch")
    return TransportAssessment(Result(Status.UNVERIFIED, (
        "memory_declarations_match_only", "provenance_and_freshness_unverified",
        "completion_and_exit_status_unverified", "os_isolation_unverified",
    )))
