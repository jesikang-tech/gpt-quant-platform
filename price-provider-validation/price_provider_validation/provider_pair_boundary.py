"""Offline, fail-closed comparison of two untrusted provider observations.

No automatic fallback, source priority, certification, I/O, or authority grant.
Raw field equality is not independent price verification.
"""

from dataclasses import dataclass, field

from .provider_contract import (
    ProviderObservationRejected,
    RawPriceObservation,
)


@dataclass(frozen=True)
class ProviderPairDecision:
    status: str
    reason: str
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    snapshot_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)


def assess_provider_pair(kis_observation, kiwoom_observation):
    """Compare untrusted raw observations without selecting either source."""
    for observation, expected_provider in (
        (kis_observation, "KIS"),
        (kiwoom_observation, "KIWOOM"),
    ):
        if observation is None:
            continue

        if (
            type(observation) is not RawPriceObservation
            or observation.provider != expected_provider
        ):
            raise ProviderObservationRejected(
                "Invalid provider pair observation"
            )

        if observation.adjustment != "UNKNOWN":
            raise ProviderObservationRejected(
                "Unverified adjustment must remain UNKNOWN"
            )

        if (
            type(observation.raw_fields) is not tuple
            or len(observation.raw_fields) != 5
        ):
            raise ProviderObservationRejected(
                "Invalid raw provider fields"
            )

    if kis_observation is None or kiwoom_observation is None:
        return ProviderPairDecision(
            "MISSING",
            "PROVIDER_OBSERVATION_MISSING",
        )

    if (
        kis_observation.ticker != kiwoom_observation.ticker
        or kis_observation.observation_date
        != kiwoom_observation.observation_date
    ):
        return ProviderPairDecision(
            "IDENTITY_MISMATCH",
            "PROVIDER_TICKER_OR_DATE_MISMATCH",
        )

    if kis_observation.raw_fields != kiwoom_observation.raw_fields:
        return ProviderPairDecision(
            "PRICE_MISMATCH",
            "UNVERIFIED_RAW_PRICE_FIELDS_DIFFER",
        )

    return ProviderPairDecision(
        "MATCHED_UNVERIFIED",
        "RAW_FIELDS_MATCH_BUT_PROVENANCE_UNVERIFIED",
    )
