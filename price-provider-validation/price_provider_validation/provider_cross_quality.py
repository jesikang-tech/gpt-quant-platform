"""Fail-closed cross-provider price-quality integration.

Reuses raw pair comparison and each provider's structural quality.
Raw equality is not numerical equivalence or independent certification.
No fallback, provider selection, I/O, or operational authority.
"""
from dataclasses import dataclass, field

from .provider_contract import ProviderObservationRejected
from .provider_pair_boundary import (
    ProviderPairDecision,
    assess_provider_pair,
)
from .provider_quality_entry import assess_provider_observation_quality


@dataclass(frozen=True)
class CrossProviderQualityDecision:
    pair_status: str
    pair_reason: str
    kis_structural_status: str | None
    kiwoom_structural_status: str | None
    status: str = field(default="DENIED", init=False)
    reason: str = field(
        default="CROSS_PROVIDER_INDEPENDENT_VERIFICATION_MISSING",
        init=False,
    )
    independently_verified: bool = field(default=False, init=False)
    numerical_equivalence_verified: bool = field(
        default=False, init=False
    )
    adjustment_policy_verified: bool = field(
        default=False, init=False
    )
    official_trading_day_verified: bool = field(
        default=False, init=False
    )
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    snapshot_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    database_rebuild_authorized: bool = field(default=False, init=False)
    broker_execution_authorized: bool = field(default=False, init=False)


def _quality_status(observation):
    if observation is None:
        return None

    decision = assess_provider_observation_quality(observation)

    if (
        decision.provider != observation.provider
        or decision.ticker != observation.ticker
        or decision.observation_date != observation.observation_date
        or decision.status != "DENIED"
        or decision.official_trading_day_verified is not False
        or decision.analysis_authorized is not False
        or decision.dashboard_authorized is not False
        or decision.snapshot_authorized is not False
        or decision.persistence_authorized is not False
    ):
        raise ProviderObservationRejected(
            "Provider quality authority escalation"
        )

    return decision.structural_status


def assess_cross_provider_quality(kis_observation, kiwoom_observation):
    """Combine existing pair and quality decisions without certification."""
    pair = assess_provider_pair(kis_observation, kiwoom_observation)

    if (
        type(pair) is not ProviderPairDecision
        or pair.status not in (
            "MISSING",
            "IDENTITY_MISMATCH",
            "PRICE_MISMATCH",
            "MATCHED_UNVERIFIED",
        )
        or pair.analysis_authorized is not False
        or pair.dashboard_authorized is not False
        or pair.snapshot_authorized is not False
        or pair.persistence_authorized is not False
    ):
        raise ProviderObservationRejected(
            "Provider pair authority escalation"
        )

    kis_status = _quality_status(kis_observation)
    kiwoom_status = _quality_status(kiwoom_observation)

    return CrossProviderQualityDecision(
        pair_status=pair.status,
        pair_reason=pair.reason,
        kis_structural_status=kis_status,
        kiwoom_structural_status=kiwoom_status,
    )
