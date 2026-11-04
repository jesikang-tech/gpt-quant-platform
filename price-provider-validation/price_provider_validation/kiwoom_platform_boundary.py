"""Offline KIWOOM platform boundary; no database, HTTP or broker access."""

from dataclasses import dataclass, field

from .provider_contract import RawPriceObservation
from .provider_evidence import (
    ProviderEvidence,
    assess_observation_evidence_binding,
)
from .trading_day_certification import TradingDayCertificationDecision
from .provider_platform_integration import assess_provider_platform_integration
from .provider_analysis_boundary import (
    ProviderAnalysisBoundaryDecision,
    assess_provider_analysis_boundary,
    invoke_provider_analysis,
)


class KiwoomPlatformBoundaryRejected(ValueError):
    pass


@dataclass(frozen=True)
class KiwoomPlatformBoundaryDecision:
    provider: str
    ticker: str
    observation_date: str
    status: str = field(default="DENIED", init=False)
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    snapshot_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)


def assess_kiwoom_platform_boundary(
    observation, evidence, trading_day_decision
):
    """Compose existing deny-only evidence and analysis contracts."""
    if type(observation) is not RawPriceObservation:
        raise KiwoomPlatformBoundaryRejected("Invalid observation type")

    if observation.provider != "KIWOOM":
        raise KiwoomPlatformBoundaryRejected("KIWOOM only")

    if type(evidence) is not ProviderEvidence:
        raise KiwoomPlatformBoundaryRejected("Invalid evidence type")

    if type(trading_day_decision) is not TradingDayCertificationDecision:
        raise KiwoomPlatformBoundaryRejected("Invalid trading-day decision")

    platform = assess_provider_platform_integration(
        observation, evidence, trading_day_decision
    )

    evidence_decision = assess_observation_evidence_binding(
        observation, evidence
    )

    analysis = assess_provider_analysis_boundary(
        observation, evidence_decision, trading_day_decision
    )

    if (
        platform.status != "DENIED"
        or platform.analysis_authorized is not False
        or platform.persistence_authorized is not False
        or analysis.status != "BLOCKED"
        or analysis.analysis_authorized is not False
        or analysis.dashboard_authorized is not False
        or analysis.snapshot_authorized is not False
        or analysis.persistence_authorized is not False
    ):
        raise KiwoomPlatformBoundaryRejected(
            "Provider authority escalation"
        )

    return KiwoomPlatformBoundaryDecision(
        provider=observation.provider,
        ticker=observation.ticker,
        observation_date=observation.observation_date,
    )


def invoke_kiwoom_platform_analysis(
    decision, analysis_callback
):
    """Never invoke analysis for an unverified KIWOOM observation."""
    if type(decision) is not KiwoomPlatformBoundaryDecision:
        raise KiwoomPlatformBoundaryRejected("Invalid boundary decision")

    if (
        decision.provider != "KIWOOM"
        or decision.status != "DENIED"
        or decision.analysis_authorized is not False
        or decision.dashboard_authorized is not False
        or decision.snapshot_authorized is not False
        or decision.persistence_authorized is not False
    ):
        raise KiwoomPlatformBoundaryRejected(
            "Boundary authority escalation"
        )

    if not callable(analysis_callback):
        raise KiwoomPlatformBoundaryRejected("Invalid analysis callback")

    analysis_decision = ProviderAnalysisBoundaryDecision(
        provider=decision.provider,
        ticker=decision.ticker,
        observation_date=decision.observation_date,
        status="BLOCKED",
        reason="UNVERIFIED_KIWOOM_PLATFORM_BOUNDARY",
    )

    return invoke_provider_analysis(
        analysis_decision, analysis_callback
    )
