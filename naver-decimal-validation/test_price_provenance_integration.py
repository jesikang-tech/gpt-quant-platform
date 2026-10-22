"""Synthetic contract tests for price provenance at analysis boundaries."""

from pathlib import Path

import pytest

from core.price_provenance_gate import (
    PriceProvenanceRejected,
    assess_price_provenance,
    require_analysis_authorization,
)


ROOT = Path(__file__).resolve().parent
ANALYSIS = ROOT / "integration_sources" / "current_analysis.py"
API = ROOT / "integration_sources" / "api_server.py"


def test_unverified_naver_price_cannot_enter_analysis():
    decision = assess_price_provenance(
        provider="NAVER",
        adjustment="UNKNOWN",
    )
    with pytest.raises(PriceProvenanceRejected):
        require_analysis_authorization(decision)


def test_unverified_price_cannot_be_self_approved():
    decision = assess_price_provenance(
        provider="NAVER",
        adjustment="ADJUSTED",
    )
    with pytest.raises(PriceProvenanceRejected):
        require_analysis_authorization(decision)


def test_analysis_source_requires_provenance_gate():
    source = ANALYSIS.read_text(encoding="utf-8")

    assert "def get_current_analysis_data(" in source
    assert "get_etf_prices(ticker, resolved_date)" in source
    assert "require_analysis_authorization" in source


def test_price_gate_precedes_score_calculation():
    source = ANALYSIS.read_text(encoding="utf-8")

    start = source.index("def get_current_analysis_data(")
    block = source[start:]

    gate = block.index("require_analysis_authorization")
    scores = block.index("calculate_return(")

    assert gate < scores


def test_api_routes_use_common_analysis_entry():
    source = API.read_text(encoding="utf-8")

    for route in (
        '/api/historical-replay',
        '/api/ver11-analysis',
        '/api/ver11-analysis/snapshots',
    ):
        assert route in source

    assert "get_current_analysis_data(" in source
