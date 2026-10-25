"""Offline NAVER rebuild adapter with explicit synthetic-only boundary.

No network, database, filesystem access, or persistence authorization.
"""

from dataclasses import dataclass
from decimal import Decimal

from core.naver_decimal_price_pipeline import prepare_naver_price_rows
from price_rebuild_preflight import RebuildPreflight


@dataclass(frozen=True)
class SyntheticRebuildRows:
    ticker: str
    price_row: tuple
    ohlcv_row: tuple
    verification_status: str = "SYNTHETIC_ONLY"
    persistence_authorized: bool = False


def prepare_synthetic_rebuild_rows(
    ticker,
    observation_date,
    values,
    *,
    adjustment,
    synthetic_fixture,
):
    """Prepare matching PRICE/OHLCV rows for declared synthetic data only."""

    if synthetic_fixture is not True:
        raise ValueError("Explicit synthetic fixture declaration required")

    if adjustment not in ("ADJUSTED", "UNADJUSTED"):
        raise ValueError("Explicit synthetic adjustment required")

    price_row, ohlcv_row = prepare_naver_price_rows(
        ticker,
        observation_date,
        values,
        adjustment=adjustment,
    )

    if price_row[0] != ohlcv_row[0]:
        raise ValueError("PRICE/OHLCV ticker mismatch")

    if price_row[1] != ohlcv_row[1]:
        raise ValueError("PRICE/OHLCV date mismatch")

    if type(price_row[2]) is not Decimal:
        raise ValueError("Decimal close required")

    if price_row[2] != ohlcv_row[5]:
        raise ValueError("PRICE/OHLCV close mismatch")

    return SyntheticRebuildRows(
        ticker=ticker,
        price_row=price_row,
        ohlcv_row=ohlcv_row,
    )


def reject_unverified_rebuild(preflight):
    """Never convert unverified real observations into database rows."""

    if type(preflight) is not RebuildPreflight:
        raise ValueError("RebuildPreflight required")

    if (
        preflight.verification_status != "UNVERIFIED"
        or preflight.persistence_authorized is not False
    ):
        raise ValueError("Invalid preflight authority state")

    raise ValueError(
        "UNVERIFIED_NAVER_REBUILD_DENIED: "
        "trusted provenance and adjustment basis are required"
    )