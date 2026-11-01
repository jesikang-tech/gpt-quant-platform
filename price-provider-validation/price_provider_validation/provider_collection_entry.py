"""Fail-closed external price collection entry.

No broker, network, database, filesystem or market-data execution.
The supplied collection callback is never invoked.
"""

from .provider_contract import ProviderObservationRejected
from .provider_usage_policy import UsageAssessment, UsagePurpose


def invoke_provider_collection(usage_decision, collect_callback):
    """Reject unverified external collection before invoking a callback."""
    if type(usage_decision) is not UsageAssessment:
        raise ProviderObservationRejected("Invalid usage decision type")

    if (
        usage_decision.provider != "KIWOOM"
        or type(usage_decision.purpose) is not UsagePurpose
        or type(usage_decision.purpose_within_reported_scope) is not bool
        or usage_decision.independently_verified is not False
        or usage_decision.api_execution_authorized is not False
        or usage_decision.analysis_authorized is not False
        or usage_decision.persistence_authorized is not False
        or usage_decision.redistribution_authorized is not False
        or usage_decision.database_rebuild_authorized is not False
    ):
        raise ProviderObservationRejected("Collection authority escalation")

    if not callable(collect_callback):
        raise ProviderObservationRejected("Invalid collection callback")

    raise ProviderObservationRejected(
        "Provider API execution is unverified; collection is prohibited"
    )
