"""Synthetic-only tests for PPM credential record serialization."""

import json

import pytest

from portable_platform_manager.auth_attempts import AttemptState
from portable_platform_manager.credential_record import (
    CredentialRecord,
    MAX_RECORD_BYTES,
    decode_record,
    encode_record,
    validate_record,
)


SYNTHETIC_HASH = "scrypt:32768:8:1$synthetic-salt$synthetic-hash"


def make_record(*, attempts=None, revision=0):
    if attempts is None:
        attempts = AttemptState()

    return CredentialRecord(
        password_hash=SYNTHETIC_HASH,
        attempts=attempts,
        revision=revision,
    )


def test_valid_record_round_trip():
    original = make_record()

    encoded = encode_record(original)
    restored = decode_record(encoded)

    assert restored == original
    assert isinstance(encoded, bytes)


def test_locked_record_round_trip():
    original = make_record(
        attempts=AttemptState(
            failures=5,
            locked_until=1900.0,
        ),
        revision=7,
    )

    assert decode_record(encode_record(original)) == original


def test_canonical_encoding_is_deterministic():
    record = make_record()

    assert encode_record(record) == encode_record(record)


def test_record_contains_no_plaintext_password_field():
    document = json.loads(encode_record(make_record()))

    assert "password" not in document
    assert "passphrase" not in document
    assert set(document) == {
        "version",
        "password_hash",
        "failures",
        "locked_until",
        "revision",
    }


@pytest.mark.parametrize(
    "invalid_attempts",
    [
        AttemptState(failures=-1),
        AttemptState(failures=6),
        AttemptState(failures=True),
        AttemptState(failures=5),
        AttemptState(failures=1, locked_until=1900.0),
        AttemptState(failures=5, locked_until=float("inf")),
        AttemptState(failures=5, locked_until=float("nan")),
    ],
)
def test_invalid_attempt_state_rejected(invalid_attempts):
    record = make_record(attempts=invalid_attempts)

    assert validate_record(record) is False

    with pytest.raises(ValueError):
        encode_record(record)


@pytest.mark.parametrize(
    "revision",
    [-1, True, 1.5, "1"],
)
def test_invalid_revision_rejected(revision):
    record = make_record(revision=revision)

    assert validate_record(record) is False

    with pytest.raises(ValueError):
        encode_record(record)


@pytest.mark.parametrize(
    "invalid_hash",
    [
        "",
        "plaintext-password",
        "pbkdf2:sha256:1000$salt$hash",
        "scrypt:32768:8:1$" + "x" * 600,
        "scrypt:32768:8:1$bad\nhash",
    ],
)
def test_invalid_hash_structure_rejected(invalid_hash):
    record = CredentialRecord(
        password_hash=invalid_hash,
        attempts=AttemptState(),
        revision=0,
    )

    assert validate_record(record) is False


@pytest.mark.parametrize(
    "invalid_document",
    [
        b"",
        b"not-json",
        b"[]",
        b"null",
        b'{"version":1,"version":1}',
        b'{"version":NaN}',
        b'{"version":Infinity}',
        b"\xff",
        b"x" * (MAX_RECORD_BYTES + 1),
    ],
)
def test_invalid_json_rejected(invalid_document):
    with pytest.raises(ValueError):
        decode_record(invalid_document)


def test_unknown_field_rejected():
    document = json.loads(encode_record(make_record()))
    document["unexpected"] = True

    with pytest.raises(ValueError):
        decode_record(json.dumps(document).encode("utf-8"))


def test_missing_field_rejected():
    document = json.loads(encode_record(make_record()))
    del document["revision"]

    with pytest.raises(ValueError):
        decode_record(json.dumps(document).encode("utf-8"))


def test_unsupported_version_rejected():
    document = json.loads(encode_record(make_record()))
    document["version"] = 2

    with pytest.raises(ValueError):
        decode_record(json.dumps(document).encode("utf-8"))


def test_boolean_version_rejected():
    document = json.loads(encode_record(make_record()))
    document["version"] = True

    with pytest.raises(ValueError):
        decode_record(json.dumps(document).encode("utf-8"))


def test_invalid_input_type_rejected():
    with pytest.raises(ValueError):
        decode_record("not bytes")


def test_record_is_immutable():
    record = make_record()

    with pytest.raises(AttributeError):
        record.revision = 1

def test_attempt_transition_increments_revision_and_preserves_hash():
    from portable_platform_manager.auth_attempts import AttemptState
    from portable_platform_manager.credential_record import (
        CredentialRecord,
        prepare_attempt_record_transition,
    )

    original = CredentialRecord(
        password_hash="scrypt:32768:8:1$synthetic-salt$synthetic-hash",
        attempts=AttemptState(failures=1),
        revision=7,
    )

    result = prepare_attempt_record_transition(
        original,
        AttemptState(failures=2),
        expected_revision=7,
    )

    assert result.eligible is True
    assert result.reason == "CANDIDATE_ONLY_NOT_PERSISTED"
    assert result.next_record.password_hash == original.password_hash
    assert result.next_record.attempts == AttemptState(failures=2)
    assert result.next_record.revision == 8
    assert original.revision == 7
    assert original.attempts == AttemptState(failures=1)


def test_attempt_transition_rejects_revision_conflict():
    from portable_platform_manager.auth_attempts import AttemptState
    from portable_platform_manager.credential_record import (
        CredentialRecord,
        prepare_attempt_record_transition,
    )

    original = CredentialRecord(
        password_hash="scrypt:32768:8:1$synthetic-salt$synthetic-hash",
        attempts=AttemptState(),
        revision=5,
    )

    result = prepare_attempt_record_transition(
        original,
        AttemptState(failures=1),
        expected_revision=4,
    )

    assert result.eligible is False
    assert result.reason == "REVISION_CONFLICT"
    assert result.next_record is None


def test_attempt_transition_rejects_invalid_current_record():
    from portable_platform_manager.auth_attempts import AttemptState
    from portable_platform_manager.credential_record import (
        CredentialRecord,
        prepare_attempt_record_transition,
    )

    invalid = CredentialRecord(
        password_hash="invalid",
        attempts=AttemptState(),
        revision=1,
    )

    result = prepare_attempt_record_transition(
        invalid,
        AttemptState(failures=1),
        expected_revision=1,
    )

    assert result.eligible is False
    assert result.reason == "INVALID_CURRENT_RECORD"
    assert result.next_record is None


def test_attempt_transition_rejects_invalid_next_state():
    from portable_platform_manager.auth_attempts import AttemptState
    from portable_platform_manager.credential_record import (
        CredentialRecord,
        prepare_attempt_record_transition,
    )

    original = CredentialRecord(
        password_hash="scrypt:32768:8:1$synthetic-salt$synthetic-hash",
        attempts=AttemptState(),
        revision=1,
    )

    for invalid in (
        None,
        False,
        AttemptState(failures=-1),
        AttemptState(failures=5),
        AttemptState(failures=5, locked_until=float("inf")),
    ):
        result = prepare_attempt_record_transition(
            original,
            invalid,
            expected_revision=1,
        )

        assert result.eligible is False
        assert result.next_record is None


def test_attempt_transition_rejects_invalid_expected_revision():
    from portable_platform_manager.auth_attempts import AttemptState
    from portable_platform_manager.credential_record import (
        CredentialRecord,
        prepare_attempt_record_transition,
    )

    original = CredentialRecord(
        password_hash="scrypt:32768:8:1$synthetic-salt$synthetic-hash",
        attempts=AttemptState(),
        revision=1,
    )

    for invalid in (None, False, -1, 1.0, "1"):
        result = prepare_attempt_record_transition(
            original,
            AttemptState(failures=1),
            expected_revision=invalid,
        )

        assert result.eligible is False
        assert result.reason == "INVALID_EXPECTED_REVISION"
        assert result.next_record is None


def test_attempt_transition_rejects_revision_limit():
    from portable_platform_manager.auth_attempts import AttemptState
    from portable_platform_manager.credential_record import (
        CredentialRecord,
        prepare_attempt_record_transition,
    )

    maximum = 2**63 - 1

    original = CredentialRecord(
        password_hash="scrypt:32768:8:1$synthetic-salt$synthetic-hash",
        attempts=AttemptState(),
        revision=maximum,
    )

    result = prepare_attempt_record_transition(
        original,
        AttemptState(failures=1),
        expected_revision=maximum,
    )

    assert result.eligible is False
    assert result.reason == "REVISION_LIMIT_REACHED"
    assert result.next_record is None


def test_attempt_transition_accepts_finite_lock_state_only():
    from portable_platform_manager.auth_attempts import AttemptState
    from portable_platform_manager.credential_record import (
        CredentialRecord,
        prepare_attempt_record_transition,
    )

    original = CredentialRecord(
        password_hash="scrypt:32768:8:1$synthetic-salt$synthetic-hash",
        attempts=AttemptState(failures=4),
        revision=10,
    )

    result = prepare_attempt_record_transition(
        original,
        AttemptState(failures=5, locked_until=1900.0),
        expected_revision=10,
    )

    assert result.eligible is True
    assert result.next_record.revision == 11
    assert result.next_record.attempts.locked_until == 1900.0
