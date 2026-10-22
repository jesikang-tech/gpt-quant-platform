"""Pure precision-preserving source-price integration.

No database, network, filesystem, or operational write operations.
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from core.decimal_price_conflict import (
    PriceEvidence,
    DecimalPriceConflictRejected,
    DecimalPriceDecision,
    classify_decimal_price,
)


class DecimalSourceRejected(ValueError):
    pass


@dataclass(frozen=True)
class DecimalSourceRecord:
    ticker: str
    observation_date: str
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: Decimal
    evidence: PriceEvidence


def _decimal(value, field, *, allow_zero=False):
    if isinstance(value, bool) or isinstance(value, float):
        raise DecimalSourceRejected(f"Unsupported {field} type")

    if not isinstance(value, (str, int, Decimal)):
        raise DecimalSourceRejected(f"Invalid {field}")

    try:
        number = Decimal(value)
    except (InvalidOperation, ValueError, TypeError, OverflowError) as exc:
        raise DecimalSourceRejected(f"Invalid {field}") from exc

    if not number.is_finite():
        raise DecimalSourceRejected(f"Nonfinite {field}")

    if number < 0 or (number == 0 and not allow_zero):
        raise DecimalSourceRejected(f"Invalid {field} range")

    return number


def prepare_decimal_source_record(
    ticker,
    observation_date,
    values,
    *,
    provider,
    adjustment,
):
    from datetime import date

    if not isinstance(ticker, str) or not ticker.strip():
        raise DecimalSourceRejected("Invalid ticker")

    if not isinstance(observation_date, str):
        raise DecimalSourceRejected("Canonical date string required")

    try:
        parsed_date = date.fromisoformat(observation_date)
    except ValueError as exc:
        raise DecimalSourceRejected("Invalid date") from exc

    if parsed_date.isoformat() != observation_date:
        raise DecimalSourceRejected("Noncanonical date")

    if not isinstance(values, dict):
        raise DecimalSourceRejected("OHLCV mapping required")

    required = {"Open", "High", "Low", "Close", "Volume"}

    if set(values) != required:
        raise DecimalSourceRejected("Unexpected OHLCV fields")

    evidence = PriceEvidence(provider, adjustment)

    if (
        not isinstance(provider, str)
        or not provider
        or provider != provider.strip()
    ):
        raise DecimalSourceRejected("Invalid provider")

    if (
        not isinstance(adjustment, str)
        or adjustment not in ("ADJUSTED", "UNADJUSTED")
    ):
        raise DecimalSourceRejected("Invalid adjustment")

    opening = _decimal(values["Open"], "open")
    high = _decimal(values["High"], "high")
    low = _decimal(values["Low"], "low")
    close = _decimal(values["Close"], "close")
    volume = _decimal(values["Volume"], "volume", allow_zero=True)

    if low > high:
        raise DecimalSourceRejected("Low exceeds high")

    if not (low <= opening <= high):
        raise DecimalSourceRejected("Open outside range")

    if not (low <= close <= high):
        raise DecimalSourceRejected("Close outside range")

    return DecimalSourceRecord(
        ticker=ticker,
        observation_date=observation_date,
        open_price=opening,
        high_price=high,
        low_price=low,
        close_price=close,
        volume=volume,
        evidence=evidence,
    )


def classify_decimal_source_record(
    existing_close,
    incoming_record,
    *,
    existing_evidence,
):
    """Fail closed until trusted provenance verification exists."""

    if not isinstance(incoming_record, DecimalSourceRecord):
        raise DecimalSourceRejected("Invalid incoming record")

    raise DecimalSourceRejected(
        "Trusted provenance verification not implemented; "
        "price comparison prohibited"
    )