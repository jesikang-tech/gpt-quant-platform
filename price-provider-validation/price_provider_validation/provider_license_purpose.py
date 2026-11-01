"""Fail-closed KIS/KIWOOM licensing and usage-purpose assessment.

Caller declarations are not independently verified contractual rights.
No provider API, filesystem, database, broker, or execution operations.
"""
from dataclasses import dataclass, field

from .provider_contract import SUPPORTED_PROVIDERS
from .provider_usage_policy import (
    UsagePurpose,
    assess_provider_usage,
)


class ProviderLicenseRejected(ValueError):
    pass


@dataclass(frozen=True)
class ProviderLicenseRequirements:
    provider: str
    purpose: UsagePurpose
    official_terms_present: bool
    license_document_present: bool
    provider_identity_bound: bool
    purpose_scope_documented: bool
    redistribution_scope_documented: bool
    commercial_scope_documented: bool
    official_reply_reviewed: bool = False


@dataclass(frozen=True)
class ProviderLicenseDecision:
    provider: str
    purpose: UsagePurpose
    missing_requirements: tuple[str, ...]
    reported_personal_scope: bool
    status: str = field(default="DENIED", init=False)
    reason: str = field(
        default="CONTRACTUAL_USAGE_RIGHTS_NOT_INDEPENDENTLY_VERIFIED",
        init=False,
    )
    independently_verified: bool = field(default=False, init=False)
    license_verified: bool = field(default=False, init=False)
    api_execution_authorized: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    snapshot_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    redistribution_authorized: bool = field(default=False, init=False)
    commercial_use_authorized: bool = field(default=False, init=False)
    database_rebuild_authorized: bool = field(default=False, init=False)
    broker_execution_authorized: bool = field(default=False, init=False)


_EVIDENCE_FIELDS = (
    "official_terms_present",
    "license_document_present",
    "provider_identity_bound",
    "purpose_scope_documented",
    "redistribution_scope_documented",
    "commercial_scope_documented",
)


def assess_provider_license_purpose(requirements):
    """Report declared gaps without granting contractual or operational rights."""
    if type(requirements) is not ProviderLicenseRequirements:
        raise ProviderLicenseRejected("Invalid license requirements type")

    if (
        type(requirements.provider) is not str
        or requirements.provider not in SUPPORTED_PROVIDERS
    ):
        raise ProviderLicenseRejected("Unsupported provider")

    if type(requirements.purpose) is not UsagePurpose:
        raise ProviderLicenseRejected("Invalid usage purpose")

    for name in (*_EVIDENCE_FIELDS, "official_reply_reviewed"):
        if type(getattr(requirements, name)) is not bool:
            raise ProviderLicenseRejected(
                "Invalid license declaration: " + name
            )

    missing = tuple(
        name for name in _EVIDENCE_FIELDS
        if getattr(requirements, name) is False
    )

    reported_personal_scope = False

    if requirements.provider == "KIWOOM":
        usage = assess_provider_usage(
            "KIWOOM",
            requirements.purpose,
            official_reply_reviewed=requirements.official_reply_reviewed,
        )

        if (
            usage.provider != requirements.provider
            or usage.purpose is not requirements.purpose
            or usage.independently_verified is not False
            or usage.api_execution_authorized is not False
            or usage.analysis_authorized is not False
            or usage.persistence_authorized is not False
            or usage.redistribution_authorized is not False
            or usage.database_rebuild_authorized is not False
        ):
            raise ProviderLicenseRejected(
                "Usage policy authority escalation"
            )

        reported_personal_scope = usage.purpose_within_reported_scope

    return ProviderLicenseDecision(
        provider=requirements.provider,
        purpose=requirements.purpose,
        missing_requirements=missing,
        reported_personal_scope=reported_personal_scope,
    )
