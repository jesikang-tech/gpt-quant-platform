"""Synthetic tests for trading-session classification.

No operational database, provider, or persistence access.
"""

from dataclasses import FrozenInstanceError

import pytest

from core.trading_session_eligibility import assess_trading_session


def test_normal_pair_is_candidate_without_authorization():
    decision = assess_trading_session(
        "105.375",
        ("100.125", "110.500", "90.000", "105.375", "1000"),
    )

    assert decision.status == "CANDIDATE"
    assert decision.trading_day_eligible is True
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


def test_zero_ohlc_is_not_a_trading_day():
    decision = assess_trading_session(
        "53000", ("0", "0", "0", "53000", "0")
    )

    assert decision.status == "NON_TRADING"
    assert decision.reason == "ZERO_OHLC_NON_TRADING_EVIDENCE"
    assert decision.trading_day_eligible is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


def test_price_ohlcv_close_mismatch_is_blocked():
    decision = assess_trading_session(
        "105", ("100", "110", "90", "106", "1000")
    )

    assert decision.status == "BLOCKED"
    assert decision.reason == "PRICE_OHLCV_CLOSE_MISMATCH"
    assert decision.trading_day_eligible is False


@pytest.mark.parametrize(
    "ohlcv",
    [
        ("100", "110", "90", "105", "0"),
        ("100", "104", "90", "105", "1000"),
        ("100", "110", "106", "105", "1000"),
        ("0", "110", "90", "105", "1000"),
        ("100", "110", "90", "105", "-1"),
    ],
)
def test_invalid_or_unverified_ohlcv_is_blocked(ohlcv):
    decision = assess_trading_session("105", ohlcv)

    assert decision.status == "BLOCKED"
    assert decision.trading_day_eligible is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "ohlcv",
    [
        None,
        (),
        ("100", "110", "90", "105"),
        ("100", "110", "90", "105", None),
    ],
)
def test_missing_ohlcv_is_rejected(ohlcv):
    with pytest.raises(ValueError):
        assess_trading_session("105", ohlcv)


def test_nonfinite_close_is_rejected():
    with pytest.raises(ValueError):
        assess_trading_session(
            "NaN", ("100", "110", "90", "105", "1000")
        )


def test_decision_is_immutable():
    decision = assess_trading_session(
        "105", ("100", "110", "90", "105", "1000")
    )

    with pytest.raises(FrozenInstanceError):
        decision.analysis_authorized = True
