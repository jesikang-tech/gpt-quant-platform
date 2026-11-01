"""Synthetic deny-only contract for explicit external price source requests.

No Flask app, operational database, network, or broker is invoked.
"""

import pytest

from core.naver_api_entry_gate import invoke_new_source_analysis
from core.price_provenance_gate import PriceProvenanceRejected


@pytest.mark.parametrize(
    "source",
    [
        "KIS",
        "KIWOOM",
        "NAVER",
        "kis",
        "kiwoom",
        "naver",
        " KIS",
        "KIWOOM ",
        "",
        None,
        123,
        True,
        [],
        {},
    ],
)
def test_explicit_unverified_source_denied_before_analysis(source):
    calls = []

    def forbidden_analysis():
        calls.append("EXECUTED")
        raise AssertionError("Analysis callback must never execute")

    with pytest.raises(PriceProvenanceRejected):
        invoke_new_source_analysis(source, forbidden_analysis)

    assert calls == []


@pytest.mark.parametrize("source", ["KIS", "KIWOOM", "NAVER"])
def test_source_denial_does_not_invoke_callback(source):
    def forbidden_analysis():
        raise AssertionError("Unexpected analysis execution")

    with pytest.raises(PriceProvenanceRejected):
        invoke_new_source_analysis(source, forbidden_analysis)


def test_invalid_callback_rejected_without_execution():
    with pytest.raises(
        PriceProvenanceRejected,
        match="INVALID_ANALYSIS_CALLBACK",
    ):
        invoke_new_source_analysis("KIS", object())


def test_source_denial_is_repeatable():
    calls = []

    for source in ("KIS", "KIWOOM", "NAVER"):
        with pytest.raises(PriceProvenanceRejected):
            invoke_new_source_analysis(
                source,
                lambda: calls.append("EXECUTED"),
            )

    assert calls == []
