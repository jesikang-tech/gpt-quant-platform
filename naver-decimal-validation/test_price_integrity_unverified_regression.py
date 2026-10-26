"""Regression: matching PRICE/OHLCV rows never grant source authority."""

import pytest

from price_integrity_decision import (
    PriceIntegrityRejected,
    assess_price_integrity,
)


def _matching_summary(verified):
    return {
        "total": 3,
        "MATCH": 3,
        "MISMATCH": 0,
        "MISSING_SOURCE": 0,
        "INVALID_PRICE": 0,
        "price_source_verified": verified,
    }


def test_matching_prices_remain_unverified():
    decision = assess_price_integrity(_matching_summary(False))

    assert decision.status == "CONSISTENT_UNVERIFIED"
    assert decision.reason == "PRICE_PAIRS_MATCH_BUT_SOURCE_UNVERIFIED"
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize("verified", [None, True, 0, "verified"])
def test_invalid_source_authority_is_rejected(verified):
    with pytest.raises(
        PriceIntegrityRejected,
        match="Source authority escalation prohibited",
    ):
        assess_price_integrity(_matching_summary(verified))
