"""Offline Kiwoom instrument-scope assessment.

An instrument label is not evidence of official API support.
No network, broker, database, or execution authority.
"""
from dataclasses import dataclass
from enum import Enum

from .provider_contract import ProviderObservationRejected


class InstrumentKind(str, Enum):
    STOCK = "STOCK"
    ETF = "ETF"
    ETN = "ETN"


@dataclass(frozen=True)
class InstrumentScopeAssessment:
    provider: str
    api_id: str
    ticker: str
    instrument_kind: InstrumentKind
    support_status: str = "UNVERIFIED"
    api_execution_authorized: bool = False
    analysis_authorized: bool = False
    persistence_authorized: bool = False
    database_rebuild_authorized: bool = False


def assess_kiwoom_instrument_scope(api_id, ticker, instrument_kind):
    """Classify a declared instrument without certifying API support."""
    if type(api_id) is not str or api_id not in (
        "ka10081", "ka10086"
    ):
        raise ProviderObservationRejected("Unsupported Kiwoom API")

    if (
        type(ticker) is not str
        or not ticker
        or ticker != ticker.strip()
    ):
        raise ProviderObservationRejected("Invalid ticker")

    if type(instrument_kind) is not InstrumentKind:
        raise ProviderObservationRejected("Invalid instrument kind")

    return InstrumentScopeAssessment(
        provider="KIWOOM",
        api_id=api_id,
        ticker=ticker,
        instrument_kind=instrument_kind,
    )
