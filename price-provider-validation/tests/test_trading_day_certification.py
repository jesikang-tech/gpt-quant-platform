"""Offline tests for the fail-closed trading-day certification boundary."""

from dataclasses import replace

import pytest

from core.trading_session_eligibility import TradingSessionDecision
from price_provider_validation.trading_day_certification import (
    TradingDayCertificationDecision,
    assess_trading_day_certification,
)


@pytest.mark.parametrize(
    ("status", "reason", "eligible"),
    [
        ("CANDIDATE", "STRUCTURALLY_VALID_UNVERIFIED", True),
        ("BLOCKED", "INVALID_OR_UNVERIFIED_OHLCV", False),
        ("NON_TRADING", "ZERO_OHLC_NON_TRADING_EVIDENCE", False),
    ],
)
def test_structural_decision_never_certifies_official_trading_day(
    status, reason, eligible
):
    structural = TradingSessionDecision(status, reason, eligible)
    decision = assess_trading_day_certification(structural)

    assert type(decision) is TradingDayCertificationDecision
    assert decision.structural_status == status
    assert decision.structural_reason == reason
    assert decision.structural_trading_day_eligible is eligible
    assert decision.official_trading_day_verified is False
    assert decision.status == "DENIED"
    assert decision.reason == "OFFICIAL_TRADING_CALENDAR_EVIDENCE_MISSING"
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "changes",
    [
        {"analysis_authorized": True},
        {"persistence_authorized": True},
        {"status": "VERIFIED"},
        {"status": "CANDIDATE", "trading_day_eligible": False},
        {"status": "BLOCKED", "trading_day_eligible": True},
        {"status": "NON_TRADING", "trading_day_eligible": True},
        {"trading_day_eligible": None},
    ],
)
def test_invalid_structural_decision_is_rejected(changes):
    structural = replace(
        TradingSessionDecision(
            "CANDIDATE", "STRUCTURALLY_VALID_UNVERIFIED", True
        ),
        **changes,
    )

    with pytest.raises(ValueError):
        assess_trading_day_certification(structural)


def test_wrong_structural_decision_type_is_rejected():
    with pytest.raises(ValueError, match="Invalid structural decision type"):
        assess_trading_day_certification(object())
