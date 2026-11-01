"""Provider usage-purpose assessment; never grants execution authority."""

from dataclasses import dataclass
from enum import Enum


class UsagePurpose(str, Enum):
    PERSONAL_OWN_ASSET = "PERSONAL_OWN_ASSET"
    THIRD_PARTY_DISTRIBUTION = "THIRD_PARTY_DISTRIBUTION"
    COMMERCIAL_SERVICE = "COMMERCIAL_SERVICE"


@dataclass(frozen=True)
class UsageAssessment:
    provider: str
    purpose: UsagePurpose
    purpose_within_reported_scope: bool
    independently_verified: bool = False
    api_execution_authorized: bool = False
    analysis_authorized: bool = False
    persistence_authorized: bool = False
    redistribution_authorized: bool = False
    database_rebuild_authorized: bool = False


def assess_provider_usage(
    provider: str,
    purpose: UsagePurpose,
    *,
    official_reply_reviewed: bool = False,
) -> UsageAssessment:
    """Classify documented purpose scope without certifying rights or data."""
    if type(provider) is not str or provider != "KIWOOM":
        raise ValueError("Provider requires independent policy review")
    if type(purpose) is not UsagePurpose:
        raise TypeError("purpose must be UsagePurpose")
    if type(official_reply_reviewed) is not bool:
        raise TypeError("official_reply_reviewed must be exactly bool")

    within_scope = (
        official_reply_reviewed
        and purpose is UsagePurpose.PERSONAL_OWN_ASSET
    )
    return UsageAssessment(
        provider=provider,
        purpose=purpose,
        purpose_within_reported_scope=within_scope,
    )
