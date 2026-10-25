"""Isolated NAVER API entry gate.

No Flask, database, network or operational analysis imports.
"""

from core.price_provenance_gate import (
    PriceProvenanceRejected,
    assess_price_provenance,
    require_analysis_authorization,
)


def invoke_new_source_analysis(source, analysis_callback):
    """Reject new source inputs before invoking analysis."""

    if type(source) is not str or not source:
        raise PriceProvenanceRejected("INVALID_SOURCE")

    if not callable(analysis_callback):
        raise PriceProvenanceRejected("INVALID_ANALYSIS_CALLBACK")

    if source != "NAVER":
        raise PriceProvenanceRejected("UNRECOGNIZED_SOURCE")

    decision = assess_price_provenance(
        provider=source,
        adjustment="UNKNOWN",
    )

    require_analysis_authorization(decision)

    raise PriceProvenanceRejected("UNREACHABLE_AUTHORIZATION_STATE")
