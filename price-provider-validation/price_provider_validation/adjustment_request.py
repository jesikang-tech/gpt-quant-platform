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

    contracts = {
        ("KIS", "inquire_daily_itemchartprice"): (
            "FID_ORG_ADJ_PRC",
            {"0": "ADJUSTED", "1": "UNADJUSTED"},
        ),
        ("KIWOOM", "ka10081"): (
            "upd_stkpc_tp",
            {"0": "UNADJUSTED", "1": "ADJUSTED"},
        ),
    }

    contract = contracts.get((provider, api_id))

    if contract is None:
        raise ProviderObservationRejected("Adjustment request contract unavailable")

    expected_parameter, policies = contract

    if parameter != expected_parameter:
        raise ProviderObservationRejected("Unsupported adjustment parameter")

    if value not in policies:
        raise ProviderObservationRejected("Unsupported adjustment request value")

    return AdjustmentRequestDecision(
        provider=provider,
        api_id=api_id,
        parameter=parameter,
        requested_value=value,
        declared_request_policy=policies[value],
    )
