"""Precision-preserving Decimal bridge contract.

No database, network, filesystem, or operational write authorization.
Unverified source records must never reach persistence.
"""

from dataclasses import dataclass
from decimal import Decimal

from core.decimal_source_integration import (
    DecimalSourceRecord,
    DecimalSourceRejected,
)


class DecimalBridgeRejected(ValueError):
    pass


@dataclass(frozen=True)
class DecimalPricePair:
    ticker: str
    observation_date: str
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: Decimal


def prepare_decimal_price_pair(record):
    """Preserve exact Decimal values without authorizing persistence."""

    if type(record) is not DecimalSourceRecord:
        raise DecimalBridgeRejected("Validated source record required")

    for field in (
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
    ):
        value = getattr(record, field)

        if type(value) is not Decimal or not value.is_finite():
            raise DecimalBridgeRejected("Invalid Decimal value")

    if not (
        record.low_price <= record.open_price <= record.high_price
        and record.low_price <= record.close_price <= record.high_price
    ):
        raise DecimalBridgeRejected("Invalid OHLC range")

    if any(
        value <= 0
        for value in (
            record.open_price,
            record.high_price,
            record.low_price,
            record.close_price,
        )
    ):
        raise DecimalBridgeRejected("Nonpositive OHLC price")

    if record.volume < 0:
        raise DecimalBridgeRejected("Negative volume")

    return DecimalPricePair(
        ticker=record.ticker,
        observation_date=record.observation_date,
        open_price=record.open_price,
        high_price=record.high_price,
        low_price=record.low_price,
        close_price=record.close_price,
        volume=record.volume,
    )


def authorize_decimal_price_persistence(pair):
    """Fail closed until trusted provenance and storage are verified."""

    if type(pair) is not DecimalPricePair:
        raise DecimalBridgeRejected("DecimalPricePair required")

    raise DecimalBridgeRejected(
        "Trusted provenance and Decimal persistence not verified; "
        "write prohibited"
    )