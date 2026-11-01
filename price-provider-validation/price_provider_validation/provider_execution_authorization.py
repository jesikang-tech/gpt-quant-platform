"""Fail-closed provider execution authorization integration.

Combines existing certification and licensing decisions.
Never executes external callbacks or grants operational authority.
"""
from dataclasses import dataclass, field

from .provider_contract import SUPPORTED_PROVIDERS
from .provider_certification_acceptance import ProviderCertificationAcceptance
from .provider_license_purpose import ProviderLicenseDecision


class ProviderExecutionRejected(ValueError):
    pass


@dataclass(frozen=True)
class ProviderExecutionDecision:
    provider: str
    certification_status: str
    license_status: str
    status: str = field(default="DENIED", init=False)
    reason: str = field(
        default="INDEPENDENT_EXECUTION_AUTHORIZATION_MISSING",
        init=False,
    )
    independently_verified: bool = field(default=False, init=False)
    api_execution_authorized: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    snapshot_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    redistribution_authorized: bool = field(default=False, init=False)
    database_rebuild_authorized: bool = field(default=False, init=False)
    live_api_execution_authorized: bool = field(default=False, init=False)
    broker_execution_authorized: bool = field(default=False, init=False)


def assess_provider_execution_authorization(certification, license_decision):
    """Reject forged or unverified decisions; never authorize execution."""
    if type(certification) is not ProviderCertificationAcceptance:
        raise ProviderExecutionRejected("Invalid certification decision type")

    if type(license_decision) is not ProviderLicenseDecision:
        raise ProviderExecutionRejected("Invalid license decision type")

    if (
        type(certification.provider) is not str
        or certification.provider not in SUPPORTED_PROVIDERS
        or license_decision.provider != certification.provider
    ):
        raise ProviderExecutionRejected("Provider identity mismatch")

    if (
        certification.status != "DENIED"
        or certification.independently_verified is not False
        or certification.analysis_authorized is not False
        or certification.dashboard_authorized is not False
        or certification.snapshot_authorized is not False
        or certification.persistence_authorized is not False
        or certification.database_rebuild_authorized is not False
        or certification.live_api_execution_authorized is not False
        or certification.broker_execution_authorized is not False
    ):
        raise ProviderExecutionRejected("Certification authority escalation")

    if (
        license_decision.status != "DENIED"
        or license_decision.independently_verified is not False
        or license_decision.license_verified is not False
        or license_decision.api_execution_authorized is not False
        or license_decision.analysis_authorized is not False
        or license_decision.dashboard_authorized is not False
        or license_decision.snapshot_authorized is not False
        or license_decision.persistence_authorized is not False
        or license_decision.redistribution_authorized is not False
        or license_decision.commercial_use_authorized is not False
        or license_decision.database_rebuild_authorized is not False
        or license_decision.broker_execution_authorized is not False
    ):
        raise ProviderExecutionRejected("License authority escalation")

    return ProviderExecutionDecision(
        provider=certification.provider,
        certification_status=certification.status,
        license_status=license_decision.status,
    )


def invoke_provider_execution(decision, execution_callback):
    """Always deny execution before invoking any callback."""
    if type(decision) is not ProviderExecutionDecision:
        raise ProviderExecutionRejected("Invalid execution decision type")

    if (
        type(decision.provider) is not str
        or decision.provider not in SUPPORTED_PROVIDERS
        or decision.status != "DENIED"
        or decision.certification_status != "DENIED"
        or decision.license_status != "DENIED"
        or decision.independently_verified is not False
        or decision.api_execution_authorized is not False
        or decision.analysis_authorized is not False
        or decision.dashboard_authorized is not False
        or decision.snapshot_authorized is not False
        or decision.persistence_authorized is not False
        or decision.redistribution_authorized is not False
        or decision.database_rebuild_authorized is not False
        or decision.live_api_execution_authorized is not False
        or decision.broker_execution_authorized is not False
    ):
        raise ProviderExecutionRejected("Execution authority escalation")

    if not callable(execution_callback):
        raise ProviderExecutionRejected("Invalid execution callback")

    raise ProviderExecutionRejected(
        "Provider execution is not independently authorized"
    )
