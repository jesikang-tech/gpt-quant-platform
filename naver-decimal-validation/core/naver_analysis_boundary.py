"""Fail-closed boundary for unverified NAVER observations.

Pure in-memory contract. No operational analysis or persistence.
"""

from dataclasses import dataclass

from core.naver_raw_observation import NaverRawObservation


@dataclass(frozen=True)
class NaverAnalysisDecision:
    provider: str
    ticker: str
    observation_date: str
    status: str
    reason: str
    analysis_authorized: bool
    dashboard_authorized: bool
    persistence_authorized: bool


def assess_naver_analysis_observation(observation):
    if type(observation) is not NaverRawObservation:
        raise ValueError("INVALID_NAVER_OBSERVATION")

    if (
        observation.provider != "NAVER"
        or observation.adjustment != "UNKNOWN"
        or observation.provenance_verified is not False
        or observation.persistence_authorized is not False
    ):
        raise ValueError("UNEXPECTED_NAVER_TRUST_STATE")

    return NaverAnalysisDecision(
        provider="NAVER",
        ticker=observation.ticker,
        observation_date=observation.observation_date,
        status="BLOCKED",
        reason="UNVERIFIED_ADJUSTMENT_AND_PROVENANCE",
        analysis_authorized=False,
        dashboard_authorized=False,
        persistence_authorized=False,
    )