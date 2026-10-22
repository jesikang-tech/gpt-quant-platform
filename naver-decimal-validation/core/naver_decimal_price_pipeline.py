"""Pure NAVER Decimal price preparation.

No provider calls, network, database access, or persistence authorization.
"""

from core.decimal_source_integration import prepare_decimal_source_record
from core.decimal_synthetic_bridge import prepare_decimal_price_pair


def prepare_naver_decimal_price_pair(
    ticker,
    observation_date,
    values,
    *,
    adjustment,
):
    """Validate NAVER OHLCV and return one exact Decimal price pair."""

    record = prepare_decimal_source_record(
        ticker,
        observation_date,
        values,
        provider="NAVER",
        adjustment=adjustment,
    )

    return prepare_decimal_price_pair(record)

def prepare_naver_price_rows(
    ticker,
    observation_date,
    values,
    *,
    adjustment,
):
    """Prepare PRICE and OHLCV rows from one validated observation.

    Returns pure data only. No persistence authorization is implied.
    """

    pair = prepare_naver_decimal_price_pair(
        ticker,
        observation_date,
        values,
        adjustment=adjustment,
    )

    price_row = (
        pair.ticker,
        pair.observation_date,
        pair.close_price,
    )

    ohlcv_row = (
        pair.ticker,
        pair.observation_date,
        pair.open_price,
        pair.high_price,
        pair.low_price,
        pair.close_price,
        pair.volume,
    )

    return price_row, ohlcv_row

def prepare_naver_analysis_rows(
    ticker,
    observation_date,
    values,
    *,
    adjustment,
):
    """Deny unverified integration with legacy analysis consumers."""

    raise RuntimeError(
        "UNVERIFIED_ANALYSIS_COMPATIBILITY_DENIED: "
        "legacy analysis numeric and trading-day contracts "
        "have not been verified"
    )


def parse_naver_raw_ohlcv_row(raw_row):
    """Parse one raw NAVER row without numeric float conversion.

    The caller must separately establish source provenance and adjustment.
    No provider request, database access, or persistence is performed.
    """
    from datetime import datetime

    if type(raw_row) is not str:
        raise ValueError("Raw NAVER row must be text")

    fields = raw_row.split("|")

    if len(fields) != 6:
        raise ValueError("NAVER OHLCV row requires six fields")

    date_text, opening, high, low, close, volume = fields

    if len(date_text) != 8 or not date_text.isascii() or not date_text.isdigit():
        raise ValueError("Invalid NAVER date")

    try:
        observation_date = datetime.strptime(date_text, "%Y%m%d").date()
    except ValueError as exc:
        raise ValueError("Invalid NAVER calendar date") from exc

    numeric_fields = (opening, high, low, close, volume)

    if any(
        not value
        or not value.isascii()
        or not value.isdigit()
        for value in numeric_fields
    ):
        raise ValueError("Invalid NAVER numeric text")

    return observation_date.isoformat(), {
        "Open": opening,
        "High": high,
        "Low": low,
        "Close": close,
        "Volume": volume,
    }


def prepare_naver_raw_decimal_pair(ticker, raw_row, *, adjustment):
    """Validate raw NAVER text and prepare a pure Decimal price pair.

    Adjustment is caller-declared, not independently authenticated.
    This function grants no persistence or analysis authorization.
    """
    observation_date, values = parse_naver_raw_ohlcv_row(raw_row)

    return prepare_naver_decimal_price_pair(
        ticker,
        observation_date,
        values,
        adjustment=adjustment,
    )