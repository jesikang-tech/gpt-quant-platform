"""Offline Kiwoom daily-response field adapter.

Official documented field names only. This is not provenance
verification, adjustment certification, or API execution.
"""
from datetime import date

from .provider_contract import ProviderObservationRejected
from .kiwoom_adapter import prepare_kiwoom_observation


_DAILY_FIELDS = {
    "ka10081": (
        "stk_dt_pole_chart_qry",
        "dt",
        ("open_pric", "high_pric", "low_pric", "cur_prc", "trde_qty"),
    ),
    "ka10086": (
        "daly_stkpc",
        "date",
        ("open_pric", "high_pric", "low_pric", "close_pric", "trde_qty"),
    ),
}


def prepare_kiwoom_daily_observation(api_id, ticker, response_row):
    """Map one untrusted response row into an UNKNOWN-adjustment observation."""
    if type(api_id) is not str or api_id not in _DAILY_FIELDS:
        raise ProviderObservationRejected("Unsupported Kiwoom daily API")

    if type(response_row) is not dict:
        raise ProviderObservationRejected("Invalid response row")

    _, date_field, price_fields = _DAILY_FIELDS[api_id]

    required = (date_field,) + price_fields

    if any(field not in response_row for field in required):
        raise ProviderObservationRejected("Missing Kiwoom response field")

    raw_date = response_row[date_field]

    if type(raw_date) is not str or len(raw_date) != 8 or not raw_date.isascii():
        raise ProviderObservationRejected("Invalid Kiwoom date")

    if not raw_date.isdecimal():
        raise ProviderObservationRejected("Invalid Kiwoom date")

    try:
        parsed = date.fromisoformat(raw_date)
    except ValueError as exc:
        raise ProviderObservationRejected("Invalid Kiwoom date") from exc

    if parsed.strftime("%Y%m%d") != raw_date:
        raise ProviderObservationRejected("Noncanonical Kiwoom date")

    values = tuple(response_row[field] for field in price_fields)

    if any(type(value) is not str or not value for value in values):
        raise ProviderObservationRejected("Invalid Kiwoom price field")

    return prepare_kiwoom_observation(
        ticker,
        parsed.isoformat(),
        values,
    )


def kiwoom_daily_array_field(api_id):
    """Return the documented array field without accessing an API."""
    if type(api_id) is not str or api_id not in _DAILY_FIELDS:
        raise ProviderObservationRejected("Unsupported Kiwoom daily API")
    return _DAILY_FIELDS[api_id][0]
