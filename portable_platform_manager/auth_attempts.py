"""Pure, fail-closed PPM authentication attempt policy.

No clock, filesystem, database, network, or broker access.
The caller must persist state safely and serialize updates.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


MAX_FAILURES = 5
LOCK_SECONDS = 15 * 60


@dataclass(frozen=True)
class AttemptState:
    failures: int = 0
    locked_until: float | None = None


@dataclass(frozen=True)
class AttemptDecision:
    accepted: bool
    reason: str
    state: AttemptState


def _valid_time(now: object) -> bool:
    return (
        type(now) in (int, float)
        and isfinite(now)
        and now >= 0
    )


def _valid_state(state: object) -> bool:
    if type(state) is not AttemptState:
        return False

    if type(state.failures) is not int:
        return False

    if not (0 <= state.failures <= MAX_FAILURES):
        return False

    if state.locked_until is None:
        return state.failures < MAX_FAILURES

    return (
        state.failures == MAX_FAILURES
        and _valid_time(state.locked_until)
    )


def assess_attempt(
    state: object,
    *,
    now: object,
    password_verified: object,
) -> AttemptDecision:
    """Return the next state; never perform the protected operation."""

    if not _valid_state(state) or not _valid_time(now):
        return AttemptDecision(
            accepted=False,
            reason="INVALID_STATE_OR_TIME",
            state=AttemptState(
                failures=MAX_FAILURES,
                locked_until=float("inf"),
            ),
        )

    if type(password_verified) is not bool:
        return AttemptDecision(
            accepted=False,
            reason="INVALID_VERIFICATION_RESULT",
            state=state,
        )

    if state.locked_until is not None:
        if now < state.locked_until:
            return AttemptDecision(
                accepted=False,
                reason="LOCKED",
                state=state,
            )

        state = AttemptState()

    if password_verified:
        return AttemptDecision(
            accepted=True,
            reason="PASSWORD_VERIFIED_ONLY",
            state=AttemptState(),
        )

    failures = state.failures + 1

    if failures >= MAX_FAILURES:
        return AttemptDecision(
            accepted=False,
            reason="LOCKED",
            state=AttemptState(
                failures=MAX_FAILURES,
                locked_until=now + LOCK_SECONDS,
            ),
        )

    return AttemptDecision(
        accepted=False,
        reason="AUTHENTICATION_DENIED",
        state=AttemptState(failures=failures),
    )
