"""Price-pair validation contract.

No database connections, writes, provider calls or operational authorization.
"""

from dataclasses import dataclass
from datetime import date
from math import isfinite


class PricePairRejected(ValueError):
    pass


@dataclass(frozen=True)
class PricePair:
    ticker: str
    observation_date: str
    close_price: float
    open_price: float | None
    high_price: float | None
    low_price: float | None
    volume: float | None


def _number(value, *, required=False):
    if value is None and not required:
        return None

    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not isfinite(value)
    ):
        raise PricePairRejected("Invalid numeric field")

    result = float(value)

    if required and result <= 0:
        raise PricePairRejected("Close price must be positive")

    return result


def prepare_price_pair(
    ticker,
    observation_date,
    close_price,
    open_price=None,
    high_price=None,
    low_price=None,
    volume=None,
):
    if not isinstance(ticker, str) or not ticker.strip():
        raise PricePairRejected("Invalid ticker")

    if not isinstance(observation_date, str):
        raise PricePairRejected("Invalid observation date")

    try:
        parsed_date = date.fromisoformat(observation_date)
    except ValueError as exc:
        raise PricePairRejected("Invalid observation date") from exc

    if parsed_date.isoformat() != observation_date:
        raise PricePairRejected("Noncanonical observation date")

    close_price = _number(close_price, required=True)
    open_price = _number(open_price)
    high_price = _number(high_price)
    low_price = _number(low_price)
    volume = _number(volume)

    for value in (open_price, high_price, low_price):
        if value is not None and value <= 0:
            raise PricePairRejected("OHLC prices must be positive")

    if volume is not None and volume < 0:
        raise PricePairRejected("Volume must be nonnegative")

    if (
        low_price is not None
        and high_price is not None
        and low_price > high_price
    ):
        raise PricePairRejected("Low price exceeds high price")

    return PricePair(
        ticker=ticker.strip(),
        observation_date=observation_date,
        close_price=close_price,
        open_price=open_price,
        high_price=high_price,
        low_price=low_price,
        volume=volume,
    )