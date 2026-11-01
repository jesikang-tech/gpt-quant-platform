"""Fail-closed Kiwoom adjustment request and raw-response binding.

Request selection is not response adjustment certification.
No broker calls, network, database, persistence, or analysis execution.
"""
from dataclasses import dataclass, field

from .adjustment_request import assess_adjustment_request
from .kiwoom_raw_json_binding import bind_kiwoom_raw_json_observation
from .provider_contract import ProviderObservationRejected


@dataclass(frozen=True)
class KiwoomAdjustmentBindingDecision:
    api_id: str
    ticker: str
    observation_date: str
    requested_policy: str
    response_adjustment: str = field(default="UNKNOWN", init=False)
    status: str = field(default="DENIED", init=False)
    independently_verified: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    database_rebuild_authorized: bool = field(default=False, init=False)


def assess_kiwoom_adjustment_raw_binding(
    api_id,
    ticker,
    parameter,
    value,
    raw_response,
    evidence,
    *,
    requested_base_date,
    observation_date,
):
    """Bind a documented request policy to unverified raw JSON evidence."""
    request = assess_adjustment_request(
        "KIWOOM", api_id, parameter, value
    )

    observation, evidence_decision = bind_kiwoom_raw_json_observation(
        api_id,
        ticker,
        raw_response,
        evidence,
        requested_base_date=requested_base_date,
        observation_date=observation_date,
    )

    if (
        request.response_adjustment != "UNKNOWN"
        or request.independently_verified is not False
        or request.analysis_authorized is not False
        or request.persistence_authorized is not False
        or observation.adjustment != "UNKNOWN"
        or evidence_decision.status != "DENIED"
        or evidence_decision.independently_verified is not False
        or evidence_decision.analysis_authorized is not False
        or evidence_decision.persistence_authorized is not False
    ):
        raise ProviderObservationRejected(
            "Adjustment or evidence authority escalation"
        )

    return KiwoomAdjustmentBindingDecision(
        api_id=api_id,
        ticker=observation.ticker,
        observation_date=observation.observation_date,
        requested_policy=request.declared_request_policy,
    )
