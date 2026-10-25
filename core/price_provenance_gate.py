"""Fail-closed price provenance gate for isolated synthetic validation."""

from dataclasses import dataclass


class PriceProvenanceRejected(ValueError):
    """Price input lacks independently established provenance."""


@dataclass(frozen=True)
class PriceProvenanceDecision:
    status: str = "BLOCKED"
    reason: str = "PRICE_PROVENANCE_NOT_ESTABLISHED"
    analysis_authorized: bool = False
    portfolio_authorized: bool = False
    dashboard_authorized: bool = False
    snapshot_authorized: bool = False
    persistence_authorized: bool = False


def assess_price_provenance(*, provider=None, adjustment=None):
    """Return a blocked decision; caller assertions cannot grant trust."""
    if provider is not None and type(provider) is not str:
        raise PriceProvenanceRejected("Invalid provider")
    if adjustment is not None and type(adjustment) is not str:
        raise PriceProvenanceRejected("Invalid adjustment")

    return PriceProvenanceDecision()


def require_analysis_authorization(decision):
    """Reject all unverified evidence, including forged approval fields."""
    if type(decision) is not PriceProvenanceDecision:
        raise PriceProvenanceRejected("Invalid provenance decision")

    raise PriceProvenanceRejected(
        "Price provenance is unverified; analysis is prohibited"
    )
