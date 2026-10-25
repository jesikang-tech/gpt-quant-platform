"""Pure trading-session eligibility contract for synthetic price pairs.

This module does not authenticate data provenance, authorize analysis,
access a database, or authorize persistence.
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class TradingSessionDecision:
    status: str
    reason: str
    trading_day_eligible: bool
    analysis_authorized: bool = False
    persistence_authorized: bool = False


def _decimal(value):
    if value is None or isinstance(value, bool):
        raise ValueError("Missing or invalid numeric field")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("Invalid numeric field") from exc
    if not result.is_finite():
        raise ValueError("Nonfinite numeric field")
    return result


def assess_trading_session(price_close, ohlcv):
    """Classify a synthetic pair without granting operational authority.

    ohlcv must contain (open, high, low, close, volume).
    """
    if type(ohlcv) not in (tuple, list) or len(ohlcv) != 5:
        raise ValueError("Five OHLCV fields required")

    close = _decimal(price_close)
    opening, high, low, ohlcv_close, volume = (
        _decimal(value) for value in ohlcv
    )

    if close <= 0 or ohlcv_close <= 0:
        raise ValueError("Positive close required")

    if close != ohlcv_close:
        return TradingSessionDecision(
            "BLOCKED", "PRICE_OHLCV_CLOSE_MISMATCH", False
        )

    if (
        opening == 0
        and high == 0
        and low == 0
        and volume == 0
    ):
        return TradingSessionDecision(
            "NON_TRADING", "ZERO_OHLC_NON_TRADING_EVIDENCE", False
        )

    if (
        min(opening, high, low) <= 0
        or volume <= 0
        or high < max(opening, close)
        or low > min(opening, close)
    ):
        return TradingSessionDecision(
            "BLOCKED", "INVALID_OR_UNVERIFIED_OHLCV", False
        )

    return TradingSessionDecision(
        "CANDIDATE", "STRUCTURALLY_VALID_UNVERIFIED", True
    )
