"""Fail-closed trading-day certification boundary.

Structural OHLCV eligibility is not official exchange-calendar evidence.
This module does not fetch calendars or certify external data.
"""

from dataclasses import dataclass

from core.trading_session_eligibility import TradingSessionDecision


@dataclass(frozen=True)
class TradingDayCertificationDecision:
    structural_status: str
    structural_reason: str
    structural_trading_day_eligible: bool
    official_trading_day_verified: bool = False
    status: str = "DENIED"
    reason: str = "OFFICIAL_TRADING_CALENDAR_EVIDENCE_MISSING"
    analysis_authorized: bool = False
    persistence_authorized: bool = False


def assess_trading_day_certification(structural_decision):
    """Preserve structural classification without certifying a trading day."""
    if type(structural_decision) is not TradingSessionDecision:
        raise ValueError("Invalid structural decision type")

    if (
        structural_decision.analysis_authorized is not False
        or structural_decision.persistence_authorized is not False
    ):
        raise ValueError("Structural decision authority escalation")

    if structural_decision.status not in (
        "CANDIDATE", "BLOCKED", "NON_TRADING"
    ):
        raise ValueError("Unknown structural status")

    if type(structural_decision.trading_day_eligible) is not bool:
        raise ValueError("Invalid structural eligibility")

    if (
        structural_decision.status == "CANDIDATE"
        and structural_decision.trading_day_eligible is not True
    ):
        raise ValueError("Inconsistent candidate eligibility")

    if (
        structural_decision.status != "CANDIDATE"
        and structural_decision.trading_day_eligible is not False
    ):
        raise ValueError("Inconsistent blocked eligibility")

    return TradingDayCertificationDecision(
        structural_status=structural_decision.status,
        structural_reason=structural_decision.reason,
        structural_trading_day_eligible=structural_decision.trading_day_eligible,
    )
