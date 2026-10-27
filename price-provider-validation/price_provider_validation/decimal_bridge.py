"""Fail-closed bridge to the existing Decimal OHLCV contract.

No source certification, API calls, persistence, or broker operations.
"""

from .provider_contract import (
    RawPriceObservation,
    ProviderObservationRejected,
)


def prepare_provider_decimal_record(observation):
    """Reject unverified observations before Decimal normalization."""

    if type(observation) is not RawPriceObservation:
        raise ProviderObservationRejected("Invalid observation type")

    if observation.adjustment not in ("ADJUSTED", "UNADJUSTED"):
        raise ProviderObservationRejected(
            "Verified adjustment policy required"
        )

    raise ProviderObservationRejected(
        "Independent provider provenance verification not implemented; "
        "Decimal normalization prohibited"
    )


def existing_decimal_contract():
    """Identify the existing implementation without importing or executing it."""

    return (
        "naver-decimal-validation/core/"
        "decimal_source_integration.py",
        "prepare_decimal_source_record",
    )
