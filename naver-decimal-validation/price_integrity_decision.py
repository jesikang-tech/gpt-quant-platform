"""Pure PRICE/OHLCV integrity decision; never authorizes operations."""

from dataclasses import dataclass


class PriceIntegrityRejected(ValueError):
    """Invalid or unsupported price-quality summary."""


@dataclass(frozen=True)
class PriceIntegrityDecision:
    status: str
    reason: str
    total: int
    matched: int
    analysis_authorized: bool = False
    persistence_authorized: bool = False


def assess_price_integrity(summary):
    """Assess an existing read-only quality summary without DB access."""

    if type(summary) is not dict:
        raise PriceIntegrityRejected("Quality summary mapping required")

    required = (
        "total",
        "MATCH",
        "MISMATCH",
        "MISSING_SOURCE",
        "INVALID_PRICE",
        "price_source_verified",
    )

    if any(key not in summary for key in required):
        raise PriceIntegrityRejected("Incomplete quality summary")

    counts = tuple(summary[key] for key in required[:5])

    if any(type(value) is not int or value < 0 for value in counts):
        raise PriceIntegrityRejected("Invalid quality counts")

    total, matched, mismatched, missing, invalid = counts

    if total != matched + mismatched + missing + invalid:
        raise PriceIntegrityRejected("Inconsistent quality totals")

    if summary["price_source_verified"] is not False:
        raise PriceIntegrityRejected("Source authority escalation prohibited")

    if "weekend_rows" in summary:
        weekends = summary["weekend_rows"]
        if type(weekends) is not int or not 0 <= weekends <= total:
            raise PriceIntegrityRejected("Invalid weekend count")

    if total == 0:
        return PriceIntegrityDecision(
            status="BLOCKED",
            reason="EMPTY_DATASET",
            total=total,
            matched=matched,
        )

    if mismatched or missing or invalid:
        return PriceIntegrityDecision(
            status="BLOCKED",
            reason="PRICE_OHLCV_INCONSISTENT",
            total=total,
            matched=matched,
        )

    return PriceIntegrityDecision(
        status="CONSISTENT_UNVERIFIED",
        reason="PRICE_PAIRS_MATCH_BUT_SOURCE_UNVERIFIED",
        total=total,
        matched=matched,
    )
