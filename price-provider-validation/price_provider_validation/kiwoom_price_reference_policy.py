"""Kiwoom Ver1.1 price-reference policy; no execution authority."""

from dataclasses import dataclass

from .provider_usage_policy import (
    UsagePurpose,
    assess_provider_usage,
)


@dataclass(frozen=True)
class KiwoomPriceReferenceDecision:
    provider: str = "KIWOOM"
    platform_version: str = "1.1"
    reference_policy: str = "OFFICIAL_REST_API"
    purpose: UsagePurpose = UsagePurpose.PERSONAL_OWN_ASSET
    personal_scope_reported: bool = True
    ka10086_price_basis: str = "ORIGINAL_PRICE_REPORTED"
    ka10081_price_basis: str = "API_GUIDE_REVIEW_REQUIRED"
    hts_numeric_equivalence_required: bool = False
    trading_calendar_verified: bool = False
    response_provenance_verified: bool = False
    api_execution_authorized: bool = False
    analysis_authorized: bool = False
    dashboard_authorized: bool = False
    snapshot_authorized: bool = False
    persistence_authorized: bool = False
    database_rebuild_authorized: bool = False
    broker_execution_authorized: bool = False


def assess_kiwoom_price_reference_policy():
    """Adopt a reference convention without granting operational rights."""
    usage = assess_provider_usage(
        "KIWOOM",
        UsagePurpose.PERSONAL_OWN_ASSET,
        official_reply_reviewed=True,
    )

    if (
        usage.purpose_within_reported_scope is not True
        or usage.independently_verified is not False
        or usage.api_execution_authorized is not False
        or usage.analysis_authorized is not False
        or usage.persistence_authorized is not False
        or usage.redistribution_authorized is not False
        or usage.database_rebuild_authorized is not False
    ):
        raise ValueError("KIWOOM_USAGE_POLICY_ESCALATION")

    return KiwoomPriceReferenceDecision()


def assess_kiwoom_ver11_daily_reference(
    ticker, response_row, evidence, trading_day_decision, *, api_id
):
    """Compose Ver1.1 reference policy with existing offline daily assessment.

    Caller-supplied rows only. No API, database, broker, or execution rights.
    """
    from .provider_daily_bridge import assess_provider_daily_bridge

    policy = assess_kiwoom_price_reference_policy()

    if type(api_id) is not str or api_id not in ("ka10081", "ka10086"):
        raise ValueError("UNSUPPORTED_KIWOOM_DAILY_API")

    decision = assess_provider_daily_bridge(
        "KIWOOM",
        ticker,
        response_row,
        evidence,
        trading_day_decision,
        api_id=api_id,
    )

    if (
        policy.provider != "KIWOOM"
        or policy.platform_version != "1.1"
        or policy.reference_policy != "OFFICIAL_REST_API"
        or policy.personal_scope_reported is not True
        or policy.api_execution_authorized is not False
        or policy.analysis_authorized is not False
        or policy.dashboard_authorized is not False
        or policy.snapshot_authorized is not False
        or policy.persistence_authorized is not False
        or policy.database_rebuild_authorized is not False
        or policy.broker_execution_authorized is not False
        or decision.provider != "KIWOOM"
        or decision.status != "DENIED"
        or decision.independently_verified is not False
        or decision.api_execution_authorized is not False
        or decision.analysis_authorized is not False
        or decision.dashboard_authorized is not False
        or decision.snapshot_authorized is not False
        or decision.persistence_authorized is not False
        or decision.database_rebuild_authorized is not False
        or decision.broker_execution_authorized is not False
    ):
        raise ValueError("KIWOOM_VER11_AUTHORITY_ESCALATION")

    return decision
