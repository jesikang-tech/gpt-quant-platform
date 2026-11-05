"""Strict, side-effect-free PPM credential record contract.

This module never reads or writes credentials.
It does not grant enrollment, recovery, or execution authority.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from math import isfinite

from .auth_attempts import AttemptState, MAX_FAILURES


RECORD_VERSION = 1
MAX_RECORD_BYTES = 4096
HASH_PREFIX = "scrypt:32768:8:1$"


@dataclass(frozen=True)
class CredentialRecord:
    password_hash: str
    attempts: AttemptState
    revision: int


def _valid_hash(value: object) -> bool:
    return (
        type(value) is str
        and value.startswith(HASH_PREFIX)
        and 1 <= len(value) <= 512
        and "\n" not in value
        and "\r" not in value
    )


def _valid_attempts(value: object) -> bool:
    if type(value) is not AttemptState:
        return False

    if type(value.failures) is not int:
        return False

    if not (0 <= value.failures <= MAX_FAILURES):
        return False

    if value.locked_until is None:
        return value.failures < MAX_FAILURES

    return (
        value.failures == MAX_FAILURES
        and type(value.locked_until) in (int, float)
        and isfinite(value.locked_until)
        and value.locked_until >= 0
    )


def validate_record(value: object) -> bool:
    return (
        type(value) is CredentialRecord
        and _valid_hash(value.password_hash)
        and _valid_attempts(value.attempts)
        and type(value.revision) is int
        and value.revision >= 0
    )


def encode_record(record: CredentialRecord) -> bytes:
    """Encode a validated record as canonical UTF-8 JSON."""

    if not validate_record(record):
        raise ValueError("invalid PPM credential record")

    document = {
        "version": RECORD_VERSION,
        "password_hash": record.password_hash,
        "failures": record.attempts.failures,
        "locked_until": record.attempts.locked_until,
        "revision": record.revision,
    }

    data = json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")

    if len(data) > MAX_RECORD_BYTES:
        raise ValueError("PPM credential record exceeds size limit")

    return data


def decode_record(data: object) -> CredentialRecord:
    """Reject malformed, oversized, ambiguous, or unknown records."""

    if type(data) is not bytes or len(data) > MAX_RECORD_BYTES:
        raise ValueError("invalid PPM credential record bytes")

    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate PPM credential record key")
            result[key] = value
        return result

    try:
        document = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=unique_pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError("non-finite JSON value")
            ),
        )
    except (UnicodeDecodeError, ValueError, TypeError) as exc:
        raise ValueError("invalid PPM credential record JSON") from exc

    if type(document) is not dict:
        raise ValueError("invalid PPM credential record structure")

    expected = {
        "version",
        "password_hash",
        "failures",
        "locked_until",
        "revision",
    }

    if set(document) != expected:
        raise ValueError("unexpected PPM credential record fields")

    if type(document["version"]) is not int:
        raise ValueError("invalid PPM credential record version")

    if document["version"] != RECORD_VERSION:
        raise ValueError("unsupported PPM credential record version")

    record = CredentialRecord(
        password_hash=document["password_hash"],
        attempts=AttemptState(
            failures=document["failures"],
            locked_until=document["locked_until"],
        ),
        revision=document["revision"],
    )

    if not validate_record(record):
        raise ValueError("invalid PPM credential record content")

    return record
