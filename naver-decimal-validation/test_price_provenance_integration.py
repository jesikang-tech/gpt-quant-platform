"""Behavioral provenance contracts at the isolated NAVER analysis boundary.

The legacy ETF reader has no established connection to this boundary.
Do not import the application or require a blanket gate on its DB prices.
"""

from pathlib import Path

import pytest

from core import naver_decimal_price_pipeline, price_provenance_gate
from core.price_provenance_gate import (
    PriceProvenanceRejected,
    assess_price_provenance,
    require_analysis_authorization,
)


ROOT = Path(__file__).resolve().parent
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


@pytest.mark.parametrize("adjustment", ["UNKNOWN", "ADJUSTED", "UNADJUSTED"])
def test_naver_analysis_entry_executes_provenance_gate(monkeypatch, adjustment):
    events = []

    def assess(**claims):
        decision = assess_price_provenance(**claims)
        events.append(("assess", claims, decision))
        return decision

    def require(decision):
        events.append(("require", decision))
        return require_analysis_authorization(decision)

    # Observe the real gate, without replacing its denial with a stub.
    monkeypatch.setattr(price_provenance_gate, "assess_price_provenance", assess)
    monkeypatch.setattr(price_provenance_gate, "require_analysis_authorization", require)

    with pytest.raises(RuntimeError, match="UNVERIFIED_ANALYSIS_COMPATIBILITY_DENIED") as error:
        naver_decimal_price_pipeline.prepare_naver_analysis_rows(
            "069500", "2026-09-16",
            {"Open": "9680", "High": "9715", "Low": "9621",
             "Close": "9676", "Volume": "252142"},
            adjustment=adjustment,
        )

    assert [event[0] for event in events] == ["assess", "require"]
    assert events[0][1] == {"provider": "NAVER", "adjustment": adjustment}
    assert events[1][1] is events[0][2]
    assert events[0][2].analysis_authorized is False
    assert isinstance(error.value.__cause__, PriceProvenanceRejected)


@pytest.mark.parametrize("adjustment", ["UNKNOWN", "ADJUSTED", "UNADJUSTED"])
def test_naver_gate_rejects_before_numeric_preparation(monkeypatch, adjustment):
    events = []
    rejections = []

    def require(decision):
        events.append("gate")
        try:
            return require_analysis_authorization(decision)
        except PriceProvenanceRejected as exc:
            rejections.append(exc)
            events.append("rejected")
            raise

    def numeric_preparation(*args, **kwargs):
        events.append("numeric_preparation")
        pytest.fail("Unverified NAVER prices reached numeric preparation")

    monkeypatch.setattr(price_provenance_gate, "require_analysis_authorization", require)
    for name in (
        "prepare_decimal_source_record",
        "prepare_decimal_price_pair",
        "prepare_naver_decimal_price_pair",
        "prepare_naver_price_rows",
    ):
        monkeypatch.setattr(naver_decimal_price_pipeline, name, numeric_preparation)

    with pytest.raises(RuntimeError, match="UNVERIFIED_ANALYSIS_COMPATIBILITY_DENIED") as error:
        naver_decimal_price_pipeline.prepare_naver_analysis_rows(
            "069500", "2026-09-16",
            {"Open": "9680", "High": "9715", "Low": "9621",
             "Close": "9676", "Volume": "252142"},
            adjustment=adjustment,
        )

    assert events == ["gate", "rejected"]
    assert len(rejections) == 1
    assert error.value.__cause__ is rejections[0]


def test_api_routes_use_common_analysis_entry():
    source = API.read_text(encoding="utf-8")

    for route in (
        '/api/historical-replay',
        '/api/ver11-analysis',
        '/api/ver11-analysis/snapshots',
    ):
        assert route in source

    assert "get_current_analysis_data(" in source
