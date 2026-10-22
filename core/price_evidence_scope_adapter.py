"""Price-specific scope adapter for the reusable PVK evidence contract.

Pure in-memory transformation only. No database or filesystem access.
"""

from datetime import date
from enum import Enum

from pvk.evidence_acquisition_contract import (
    EvidenceDesignStatus,
    EvidenceScope,
    prepare_evidence_acquisition,
)


class PriceEvidenceScopeKind(Enum):
    TICKER_ON_DATE = "TICKER_ON_DATE"
    TRADING_DATE = "TRADING_DATE"


def prepare_price_evidence_scope(
    kind: PriceEvidenceScopeKind,
    *,
    ticker: str | None = None,
    trading_date: str | None = None,
):
    """Prepare a denied acquisition decision for an explicit investigation."""

    if type(kind) is not PriceEvidenceScopeKind:
        raise ValueError("INVALID_PRICE_SCOPE_KIND")

    if type(trading_date) is not str:
        raise ValueError("EXPLICIT_TRADING_DATE_REQUIRED")

    try:
        parsed_date = date.fromisoformat(trading_date)
    except ValueError as error:
        raise ValueError("INVALID_TRADING_DATE") from error

    if parsed_date.isoformat() != trading_date:
        raise ValueError("NON_CANONICAL_TRADING_DATE")

    if kind is PriceEvidenceScopeKind.TICKER_ON_DATE:
        if type(ticker) is not str or not ticker.isascii():
            raise ValueError("EXPLICIT_TICKER_REQUIRED")
        if not ticker.isalnum() or len(ticker) > 12:
            raise ValueError("INVALID_TICKER")
        subject = ticker
    else:
        if ticker is not None:
            raise ValueError("DATE_SCOPE_MUST_NOT_SPECIFY_TICKER")
        subject = "ALL_TICKERS_ON_DATE"

    scope = EvidenceScope(
        platform_id="GPT_QUANT_PLATFORM_1",
        purpose="PRICE_OHLCV_DISCREPANCY_INVESTIGATION",
        subject_id=subject,
        observation_date=trading_date,
        design_status=EvidenceDesignStatus.PROPOSED,
    )

    return prepare_evidence_acquisition(scope)

def prepare_price_readonly_evidence(
    kind: PriceEvidenceScopeKind,
    *,
    ticker: str | None = None,
    trading_date: str | None = None,
):
    """Compose price scope validation with the denied PVK read-only boundary."""

    from pvk.readonly_evidence_boundary import (
        ReadOnlyEvidenceRequest,
        assess_readonly_evidence_request,
    )

    existing_decision = prepare_price_evidence_scope(
        kind,
        ticker=ticker,
        trading_date=trading_date,
    )

    if (
        existing_decision.source_access_authorized
        or existing_decision.execution_authorized
        or existing_decision.modification_authorized
    ):
        raise RuntimeError("UNEXPECTED_PRICE_EVIDENCE_AUTHORIZATION")

    scope_id = (
        f"{kind.value}:{ticker}:{trading_date}"
        if kind is PriceEvidenceScopeKind.TICKER_ON_DATE
        else f"{kind.value}:{trading_date}"
    )

    request = ReadOnlyEvidenceRequest(
        purpose="PRICE_OHLCV_DISCREPANCY_INVESTIGATION",
        scope_id=scope_id,
    )

    return assess_readonly_evidence_request(request)
