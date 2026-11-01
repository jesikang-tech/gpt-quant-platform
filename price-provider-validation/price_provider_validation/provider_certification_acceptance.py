"""Offline certification acceptance requirements; no operational authority.

This is a deny-only assessment of caller-supplied requirement flags.
Flags are declarations, not independently verified certification evidence.
No I/O, provider calls, database access, or execution permissions.
"""
from dataclasses import dataclass, field

from .provider_contract import SUPPORTED_PROVIDERS


class ProviderCertificationRejected(ValueError):
    pass


@dataclass(frozen=True)
class ProviderCertificationRequirements:
    provider: str
    source_evidence_present: bool
    raw_binding_present: bool
    adjustment_evidence_present: bool
    calendar_evidence_present: bool
    quality_evidence_present: bool
    licensing_evidence_present: bool


@dataclass(frozen=True)
class ProviderCertificationAcceptance:
    provider: str
    missing_requirements: tuple[str, ...]
    reason: str = field(default="INDEPENDENT_CERTIFICATION_NOT_ESTABLISHED", init=False)
    status: str = field(default="DENIED", init=False)
    independently_verified: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    snapshot_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    database_rebuild_authorized: bool = field(default=False, init=False)
    live_api_execution_authorized: bool = field(default=False, init=False)
    broker_execution_authorized: bool = field(default=False, init=False)


_REQUIREMENT_FIELDS = (
    "source_evidence_present",
    "raw_binding_present",
    "adjustment_evidence_present",
    "calendar_evidence_present",
    "quality_evidence_present",
    "licensing_evidence_present",
)


def assess_provider_certification_requirements(requirements):
    """Report declared missing requirements, never certify or authorize."""
    if type(requirements) is not ProviderCertificationRequirements:
        raise ProviderCertificationRejected("Invalid requirements type")
    if (
        type(requirements.provider) is not str
        or requirements.provider not in SUPPORTED_PROVIDERS
    ):
        raise ProviderCertificationRejected("Unsupported provider")

    missing = []
    for name in _REQUIREMENT_FIELDS:
        value = getattr(requirements, name)
        if type(value) is not bool:
            raise ProviderCertificationRejected("Invalid requirement flag: " + name)
        if value is False:
            missing.append(name)

    return ProviderCertificationAcceptance(
        provider=requirements.provider,
        missing_requirements=tuple(missing),
    )
