"""Synthetic tests for independent PPM authentication attempt policy."""

import pytest

from portable_platform_manager.auth_attempts import (
    LOCK_SECONDS,
    MAX_FAILURES,
    AttemptState,
    assess_attempt,
)


def test_first_four_failures_are_denied_without_lock():
    state = AttemptState()

    for count in range(1, MAX_FAILURES):
        result = assess_attempt(
            state,
            now=1000.0,
            password_verified=False,
        )
        assert result.accepted is False
        assert result.reason == "AUTHENTICATION_DENIED"
        assert result.state.failures == count
        assert result.state.locked_until is None
        state = result.state


def test_fifth_failure_triggers_fifteen_minute_lock():
    state = AttemptState(failures=MAX_FAILURES - 1)

    result = assess_attempt(
        state,
        now=1000.0,
        password_verified=False,
    )

    assert result.accepted is False
    assert result.reason == "LOCKED"
    assert result.state.failures == MAX_FAILURES
    assert result.state.locked_until == 1000.0 + LOCK_SECONDS


def test_correct_password_cannot_bypass_active_lock():
    state = AttemptState(
        failures=MAX_FAILURES,
        locked_until=1900.0,
    )

    result = assess_attempt(
        state,
        now=1899.0,
        password_verified=True,
    )

    assert result.accepted is False
    assert result.reason == "LOCKED"
    assert result.state == state


def test_lock_expiry_allows_new_verified_attempt():
    state = AttemptState(
        failures=MAX_FAILURES,
        locked_until=1900.0,
    )

    result = assess_attempt(
        state,
        now=1900.0,
        password_verified=True,
    )

    assert result.accepted is True
    assert result.reason == "PASSWORD_VERIFIED_ONLY"
    assert result.state == AttemptState()


def test_success_before_lock_resets_failures():
    result = assess_attempt(
        AttemptState(failures=4),
        now=1000.0,
        password_verified=True,
    )

    assert result.accepted is True
    assert result.state == AttemptState()


def test_failure_after_lock_expiry_starts_new_counter():
    state = AttemptState(
        failures=MAX_FAILURES,
        locked_until=1900.0,
    )

    result = assess_attempt(
        state,
        now=1900.0,
        password_verified=False,
    )

    assert result.accepted is False
    assert result.state == AttemptState(failures=1)


@pytest.mark.parametrize(
    "invalid_time",
    [
        None,
        -1,
        float("nan"),
        float("inf"),
        True,
        "1000",
    ],
)
def test_invalid_time_is_denied(invalid_time):
    result = assess_attempt(
        AttemptState(),
        now=invalid_time,
        password_verified=True,
    )

    assert result.accepted is False
    assert result.reason == "INVALID_STATE_OR_TIME"


@pytest.mark.parametrize(
    "invalid_state",
    [
        None,
        {},
        AttemptState(failures=-1),
        AttemptState(failures=6),
        AttemptState(failures=True),
        AttemptState(failures=5),
        AttemptState(failures=1, locked_until=1900.0),
        AttemptState(failures=5, locked_until=float("nan")),
    ],
)
def test_invalid_state_is_denied(invalid_state):
    result = assess_attempt(
        invalid_state,
        now=1000.0,
        password_verified=True,
    )

    assert result.accepted is False
    assert result.reason == "INVALID_STATE_OR_TIME"


@pytest.mark.parametrize(
    "invalid_verification",
    [
        None,
        1,
        0,
        "True",
        [],
    ],
)
def test_non_boolean_verification_result_is_denied(invalid_verification):
    result = assess_attempt(
        AttemptState(),
        now=1000.0,
        password_verified=invalid_verification,
    )

    assert result.accepted is False
    assert result.reason == "INVALID_VERIFICATION_RESULT"


def test_invalid_state_cannot_grant_authorization():
    result = assess_attempt(
        AttemptState(failures=MAX_FAILURES),
        now=1000.0,
        password_verified=True,
    )

    assert result.accepted is False
    assert result.state.failures == MAX_FAILURES


def test_state_is_immutable():
    state = AttemptState(failures=2)

    with pytest.raises(AttributeError):
        state.failures = 3
