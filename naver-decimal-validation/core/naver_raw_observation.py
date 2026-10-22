"""Pure NAVER raw observation boundary.

Preserves raw OHLCV text and refuses to infer adjustment status.
No network, database, filesystem access or persistence authority.
"""

from dataclasses import dataclass

from core.naver_decimal_price_pipeline import parse_naver_raw_ohlcv_row


class NaverRawObservationRejected(ValueError):
    pass


@dataclass(frozen=True)
class NaverRawObservation:
    ticker: str
    observation_date: str
    raw_row: str
    values: tuple
    provider: str = "NAVER"
    adjustment: str = "UNKNOWN"
    provenance_verified: bool = False
    persistence_authorized: bool = False


def prepare_naver_raw_observation(ticker, raw_row):
    """Preserve one NAVER raw observation without inventing provenance."""

    if (
        type(ticker) is not str
        or not ticker
        or ticker != ticker.strip()
    ):
        raise NaverRawObservationRejected("Invalid ticker")

    observation_date, values = parse_naver_raw_ohlcv_row(raw_row)

    return NaverRawObservation(
        ticker=ticker,
        observation_date=observation_date,
        raw_row=raw_row,
        values=tuple(
            values[field]
            for field in ("Open", "High", "Low", "Close", "Volume")
        ),
    )


def authorize_naver_raw_observation(observation):
    """Deny promotion of unverified raw data into persistence."""

    if type(observation) is not NaverRawObservation:
        raise NaverRawObservationRejected("Invalid observation")

    raise NaverRawObservationRejected(
        "NAVER adjustment and provenance are unverified; "
        "operational persistence prohibited"
    )
