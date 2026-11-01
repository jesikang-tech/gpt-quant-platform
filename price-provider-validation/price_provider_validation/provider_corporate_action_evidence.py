"""Offline corporate-action evidence consistency, never certification.

Caller-supplied declarations cannot establish independent authenticity,
adjustment factors, or actual response-price adjustment.
No I/O, broker, network, database, or operational authority.
"""
from dataclasses import dataclass, field
from datetime import date

from .provider_contract import SUPPORTED_PROVIDERS
from .provider_evidence import (
    ProviderEvidence,
    ProviderEvidenceRejected,
    assess_provider_evidence,
)


class CorporateActionEvidenceRejected(ValueError):
    pass


_ACTIONS = frozenset((
    "SPLIT",
    "REVERSE_SPLIT",
    "CASH_DIVIDEND",
    "STOCK_DIVIDEND",
))


@dataclass(frozen=True)
class CorporateActionDeclaration:
    provider: str
    ticker: str
    observation_date: str
    action_date: str
    action_type: str
    source_reference: str


@dataclass(frozen=True)
class CorporateActionAssessment:
    provider: str
    ticker: str
    action_type: str
    reason: str = field(
        default="CORPORATE_ACTION_NOT_INDEPENDENTLY_VERIFIED",
        init=False,
    )
    status: str = field(default="DENIED", init=False)
    corporate_action_verified: bool = field(default=False, init=False)
    independently_verified: bool = field(default=False, init=False)
    response_adjustment: str = field(default="UNKNOWN", init=False)
    adjustment_factor_verified: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    database_rebuild_authorized: bool = field(default=False, init=False)
    broker_execution_authorized: bool = field(default=False, init=False)


def assess_corporate_action_declaration(evidence, declaration):
    """Validate identity and date syntax, never verify a corporate action."""
    if type(evidence) is not ProviderEvidence:
        raise CorporateActionEvidenceRejected("Invalid evidence type")

    if type(declaration) is not CorporateActionDeclaration:
        raise CorporateActionEvidenceRejected("Invalid declaration type")

    try:
        decision = assess_provider_evidence(evidence)
    except ProviderEvidenceRejected as exc:
        raise CorporateActionEvidenceRejected("Invalid provider evidence") from exc

    if (
        decision.status != "DENIED"
        or decision.independently_verified is not False
        or decision.analysis_authorized is not False
        or decision.persistence_authorized is not False
    ):
        raise CorporateActionEvidenceRejected("Evidence authority escalation")

    if (
        type(declaration.provider) is not str
        or declaration.provider not in SUPPORTED_PROVIDERS
        or declaration.provider != evidence.provider
    ):
        raise CorporateActionEvidenceRejected("Provider mismatch")

    if type(declaration.ticker) is not str or declaration.ticker != evidence.ticker:
        raise CorporateActionEvidenceRejected("Ticker mismatch")

    if (
        type(declaration.observation_date) is not str
        or declaration.observation_date != evidence.observation_date
    ):
        raise CorporateActionEvidenceRejected("Observation date mismatch")

    if (
        type(declaration.action_type) is not str
        or declaration.action_type not in _ACTIONS
    ):
        raise CorporateActionEvidenceRejected("Unsupported corporate action")

    if type(declaration.action_date) is not str:
        raise CorporateActionEvidenceRejected("Invalid action date")

    try:
        parsed = date.fromisoformat(declaration.action_date)
    except ValueError as exc:
        raise CorporateActionEvidenceRejected("Invalid action date") from exc

    if parsed.isoformat() != declaration.action_date:
        raise CorporateActionEvidenceRejected("Noncanonical action date")

    if (
        type(declaration.source_reference) is not str
        or not declaration.source_reference
        or declaration.source_reference != declaration.source_reference.strip()
    ):
        raise CorporateActionEvidenceRejected("Invalid source reference")

    return CorporateActionAssessment(
        provider=declaration.provider,
        ticker=declaration.ticker,
        action_type=declaration.action_type,
    )
