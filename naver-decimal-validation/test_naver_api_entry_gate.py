"""Executable tests for the isolated NAVER API entry gate."""

import pytest

from core.naver_api_entry_gate import invoke_new_source_analysis
from core.price_provenance_gate import PriceProvenanceRejected


def test_naver_request_rejected_before_analysis():
    calls = []

    def analysis():
        calls.append("EXECUTED")
        return {"success": True}

    with pytest.raises(PriceProvenanceRejected):
        invoke_new_source_analysis("NAVER", analysis)

    assert calls == []


@pytest.mark.parametrize("source", [None, "", "OTHER", "LEGACY", 123])
def test_invalid_source_rejected_without_analysis(source):
    calls = []

    def analysis():
        calls.append("EXECUTED")

    with pytest.raises(PriceProvenanceRejected):
        invoke_new_source_analysis(source, analysis)

    assert calls == []


def test_invalid_callback_rejected():
    with pytest.raises(
        PriceProvenanceRejected,
        match="INVALID_ANALYSIS_CALLBACK",
    ):
        invoke_new_source_analysis("NAVER", None)
