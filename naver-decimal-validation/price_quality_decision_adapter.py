"""Adapt existing price-quality summaries to a fail-closed decision.

This module never opens a database or authorizes analysis or persistence.
"""

from price_integrity_decision import (
    PriceIntegrityRejected,
    assess_price_integrity,
)


def assess_overall_quality_summary(summary):
    """Assess an already-computed overall PRICE/OHLCV quality summary."""
    if type(summary) is not dict:
        raise PriceIntegrityRejected("Overall quality summary required")
    if "weekend_rows" not in summary:
        raise PriceIntegrityRejected("Overall weekend count required")
    return assess_price_integrity(summary)


def assess_daily_quality_summary(summary):
    """Assess an already-computed date-specific quality summary."""
    if type(summary) is not dict:
        raise PriceIntegrityRejected("Daily quality summary required")
    day = summary.get("date")
    if type(day) is not str or not day:
        raise PriceIntegrityRejected("Daily quality date required")
    return assess_price_integrity(summary)
