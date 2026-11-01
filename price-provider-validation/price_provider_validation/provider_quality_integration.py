"""Fail-closed integration of provider price quality and trading-day contracts.

Reuses existing structural classification and trading-day certification.
No external verification, analysis, persistence, database, or broker access.
"""

from dataclasses import dataclass

from .price_quality_adapter import (
    ProviderPriceQualityInput,
    assess_provider_price_quality,
)
from .trading_day_certification import (
    assess_trading_day_certification,
)


@dataclass(frozen=True)
class ProviderQualityIntegrationDecision:
    provider: str
    ticker: str
    observation_date: str
    structural_status: str
    structural_reason: str
    structural_trading_day_eligible: bool
    official_trading_day_verified: bool = False
    status: str = "DENIED"
    reason: str = "OFFICIAL_TRADING_CALENDAR_EVIDENCE_MISSING"
    analysis_authorized: bool = False
    dashboard_authorized: bool = False
    snapshot_authorized: bool = False
    persistence_authorized: bool = False


def assess_provider_quality_integration(quality_input):
    """Combine structural quality and fail-closed trading-day decisions."""

    from .provider_contract import ProviderObservationRejected

    if type(quality_input) is not ProviderPriceQualityInput:
        raise ProviderObservationRejected("Invalid quality input type")

    if quality_input.adjustment != "UNKNOWN":
        raise ProviderObservationRejected(
            "Unverified adjustment must remain UNKNOWN"
        )

    if (
        quality_input.analysis_authorized is not False
        or quality_input.persistence_authorized is not False
    ):
        raise ProviderObservationRejected(
            "Quality input authority escalation"
        )

    structural = assess_provider_price_quality(quality_input)
    certification = assess_trading_day_certification(structural)

    if (
        certification.status != "DENIED"
        or certification.official_trading_day_verified is not False
        or certification.analysis_authorized is not False
        or certification.persistence_authorized is not False
    ):
        raise ProviderObservationRejected(
            "Trading-day certification authority escalation"
        )

    return ProviderQualityIntegrationDecision(
        provider=quality_input.provider,
        ticker=quality_input.ticker,
        observation_date=quality_input.observation_date,
        structural_status=certification.structural_status,
        structural_reason=certification.structural_reason,
        structural_trading_day_eligible=(
            certification.structural_trading_day_eligible
        ),
    )
