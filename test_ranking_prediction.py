"""Prediction branches driven by synthetic rank histories."""
import pytest
from price_test_support import isolated_price_db, synthetic_ranking_db


@pytest.mark.parametrize("ticker,prediction,confidence", [
    ("111111", "UNCERTAIN", 50), ("222222", "MAINTAIN", 85),
    ("333333", "DOWNRISK", 80), ("444444", "UNCERTAIN", 50),
])
def test_ranking_prediction(synthetic_ranking_db, ticker, prediction, confidence):
    from ranking_analyzer import generate_ranking_prediction
    result = generate_ranking_prediction(ticker)
    assert result["ticker"] == ticker
    assert result["prediction"] == prediction
    assert result["confidence"] == confidence
    assert result["message"]
