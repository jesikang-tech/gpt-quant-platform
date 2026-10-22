"""Read-only response projection for blocked NAVER analysis.

No price, score, portfolio, database or persistence output.
"""

from core.naver_analysis_boundary import (
    NaverAnalysisDecision,
)


class NaverAnalysisResponseRejected(ValueError):
    pass


def build_naver_analysis_response(decision):
    if type(decision) is not NaverAnalysisDecision:
        raise NaverAnalysisResponseRejected("INVALID_DECISION")

    if (
        decision.provider != "NAVER"
        or type(decision.ticker) is not str
        or not decision.ticker
        or type(decision.observation_date) is not str
        or not decision.observation_date
        or decision.status != "BLOCKED"
        or decision.reason != "UNVERIFIED_ADJUSTMENT_AND_PROVENANCE"
        or decision.analysis_authorized is not False
        or decision.dashboard_authorized is not False
        or decision.persistence_authorized is not False
    ):
        raise NaverAnalysisResponseRejected(
            "UNEXPECTED_ANALYSIS_AUTHORIZATION"
        )

    return {
        "provider": "NAVER",
        "ticker": decision.ticker,
        "observation_date": decision.observation_date,
        "status": "BLOCKED",
        "reason": "UNVERIFIED_ADJUSTMENT_AND_PROVENANCE",
        "analysis_authorized": False,
        "dashboard_authorized": False,
        "persistence_authorized": False,
    }
