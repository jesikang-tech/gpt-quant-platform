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
