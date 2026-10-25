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


def require_persistence_authorization(decision):
    """Reject persistence until independently verified trust exists."""
    if type(decision) is not PriceProvenanceDecision:
        raise PriceProvenanceRejected("Invalid provenance decision")

    raise PriceProvenanceRejected(
        "Price provenance is unverified; persistence is prohibited"
    )


def invoke_naver_persistence(persist_callback):
    """Deny new NAVER persistence before invoking any write callback."""
    if not callable(persist_callback):
        raise PriceProvenanceRejected("Invalid persistence callback")

    decision = assess_price_provenance(
        provider="NAVER",
        adjustment="UNKNOWN",
    )
    require_persistence_authorization(decision)

    return persist_callback()
