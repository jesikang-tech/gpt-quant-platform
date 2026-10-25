"""Pure NAVER price rebuild preflight; never authorizes persistence."""

from dataclasses import dataclass

from core.naver_raw_observation import NaverRawObservation
from core.naver_http_response_validation import (
    NaverHighBelowCloseByOneRow,
    NaverZeroOhlcSpecialRow,
)


@dataclass(frozen=True)
class RebuildPreflight:
    ticker: str
    total_rows: int
    normal_rows: int
    zero_ohlc_rows: int
    high_below_close_rows: int
    price_candidates: int
    ohlcv_candidates: int
    verification_status: str = "UNVERIFIED"
    persistence_authorized: bool = False


def assess_rebuild_candidates(ticker, observations):
    """Count candidate rows without generating or writing database records."""

    if not isinstance(ticker, str) or not ticker:
        raise ValueError("Valid ticker required")

    if type(observations) not in (tuple, list):
        raise ValueError("Validated observation collection required")

    normal = 0
    zero = 0
    high_below_close = 0

    for observation in observations:
        if type(observation) not in (
            NaverRawObservation,
            NaverZeroOhlcSpecialRow,
            NaverHighBelowCloseByOneRow,
        ):
            raise ValueError("Unsupported observation type")

        if observation.ticker != ticker:
            raise ValueError("Observation ticker mismatch")

        if observation.provenance_verified is not False:
            raise ValueError("Unverified provenance required")

        if observation.adjustment != "UNKNOWN":
            raise ValueError("Unverified adjustment required")

        if observation.persistence_authorized is not False:
            raise ValueError("Persistence escalation prohibited")

        if type(observation) is NaverRawObservation:
            normal += 1
        elif type(observation) is NaverZeroOhlcSpecialRow:
            if observation.analysis_authorized is not False:
                raise ValueError("Analysis escalation prohibited")
            zero += 1
        elif type(observation) is NaverHighBelowCloseByOneRow:
            if observation.analysis_authorized is not False:
                raise ValueError("Analysis escalation prohibited")
            high_below_close += 1
        else:
            raise ValueError("Unsupported observation type")

    total = normal + zero + high_below_close

    return RebuildPreflight(
        ticker=ticker,
        total_rows=total,
        normal_rows=normal,
        zero_ohlc_rows=zero,
        high_below_close_rows=high_below_close,
        price_candidates=normal,
        ohlcv_candidates=normal,
    )