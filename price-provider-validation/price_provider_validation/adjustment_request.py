"""Offline adjustment-request contract; never certifies response prices.

KIS inquire_daily_itemchartprice: documented FID_ORG_ADJ_PRC values.
Kiwoom adjustment requests remain unsupported pending official verification.
No network, database, filesystem, or broker operations.
"""
from dataclasses import dataclass

from .provider_contract import ProviderObservationRejected


@dataclass(frozen=True)
class AdjustmentRequestDecision:
    provider: str
    api_id: str
    parameter: str
    requested_value: str
    declared_request_policy: str
    response_adjustment: str = "UNKNOWN"
    independently_verified: bool = False
    analysis_authorized: bool = False
    persistence_authorized: bool = False


def assess_adjustment_request(provider, api_id, parameter, value):
    """Validate a documented request selector without certifying its response."""
    if any(type(item) is not str for item in (provider, api_id, parameter, value)):
        raise ProviderObservationRejected("Invalid adjustment request type")

    if provider != "KIS" or api_id != "inquire_daily_itemchartprice":
        raise ProviderObservationRejected("Adjustment request contract unavailable")

    if parameter != "FID_ORG_ADJ_PRC":
        raise ProviderObservationRejected("Unsupported adjustment parameter")

    policies = {
        "0": "ADJUSTED",
        "1": "UNADJUSTED",
    }

    if value not in policies:
        raise ProviderObservationRejected("Unsupported adjustment request value")

    return AdjustmentRequestDecision(
        provider=provider,
        api_id=api_id,
        parameter=parameter,
        requested_value=value,
        declared_request_policy=policies[value],
    )
