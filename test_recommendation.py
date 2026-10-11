"""Recommendations computed from synthetic scores and rank histories."""
import pytest
from price_test_support import isolated_price_db, synthetic_ranking_db


@pytest.mark.parametrize("ticker,recommendation,confidence", [
    ("111111", "HOLD", "MEDIUM"), ("222222", "HOLD", "MEDIUM"),
    ("333333", "WATCH", "MEDIUM"), ("missing", "AVOID", "LOW")])
def test_recommendation(synthetic_ranking_db, ticker, recommendation, confidence):
    from ranking_analyzer import generate_ai_recommendation
    result = generate_ai_recommendation(ticker)
    assert result["recommendation"] == recommendation
    assert result["confidence"] == confidence
    assert isinstance(result["reasons"], list)
    if ticker == "222222":
        assert result["reasons"]  # stable rank history contributes an explanation
