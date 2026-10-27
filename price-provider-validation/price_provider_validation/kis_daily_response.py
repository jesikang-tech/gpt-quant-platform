"""Offline KIS daily-response field adapter.

Field names are based on the official KIS
inquire_daily_itemchartprice example.

No API execution, adjustment certification,
provenance verification, or analysis authorization.
"""

from datetime import date

from .kis_adapter import prepare_kis_observation
from .provider_contract import ProviderObservationRejected


_KIS_DAILY_FIELDS = (
    "stck_oprc",
    "stck_hgpr",
    "stck_lwpr",
    "stck_clpr",
    "acml_vol",
)

_KIS_DATE_FIELD = "stck_bsop_date"


def prepare_kis_daily_observation(ticker, response_row):
    """Preserve one documented output2 row as unverified raw data."""

    if type(response_row) is not dict:
        raise ProviderObservationRejected("Invalid KIS response row")

    required = (_KIS_DATE_FIELD,) + _KIS_DAILY_FIELDS

    if any(field not in response_row for field in required):
        raise ProviderObservationRejected("Missing KIS response field")

    raw_date = response_row[_KIS_DATE_FIELD]

    if (
        type(raw_date) is not str
        or len(raw_date) != 8
        or not raw_date.isascii()
        or not raw_date.isdecimal()
    ):
        raise ProviderObservationRejected("Invalid KIS date")

    try:
        parsed = date.fromisoformat(raw_date)
    except ValueError as exc:
        raise ProviderObservationRejected("Invalid KIS date") from exc

    if parsed.strftime("%Y%m%d") != raw_date:
        raise ProviderObservationRejected("Noncanonical KIS date")

    values = tuple(response_row[field] for field in _KIS_DAILY_FIELDS)

    if any(type(value) is not str or not value for value in values):
        raise ProviderObservationRejected("Invalid KIS price field")

    return prepare_kis_observation(
        ticker,
        parsed.isoformat(),
        values,
    )


def kis_daily_array_field():
    """Return the documented KIS daily response array name."""

    return "output2"
