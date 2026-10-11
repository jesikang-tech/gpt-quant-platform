"""Market regimes from controlled scores and guarded database fallback."""
import pytest
from price_test_support import isolated_price_db


@pytest.mark.parametrize("scores,regime", [([95, 93, 92], "BULLISH"),
    ([85, 82, 80], "NEUTRAL"), ([70, 60, 50], "BEARISH")])
def test_market_regime_db_and_explicit_scores(isolated_price_db, scores, regime):
    from core.market_regime import analyze_market_regime
    conn = isolated_price_db.connect()
    try:
        with conn:
            conn.executemany("INSERT INTO etf_scores(ticker, final_score) VALUES (?, ?)",
                             [(str(index), score) for index, score in enumerate(scores)])
    finally:
        conn.close()
    explicit = [{"ticker": str(index), "final_score": score} for index, score in enumerate(scores)]
    result = analyze_market_regime()
    assert result == analyze_market_regime(explicit)
    assert result["regime"] == regime
    assert result["avg_score"] == round(sum(scores) / len(scores), 2)
    assert result["analyzed_count"] == len(scores)


def test_market_regime_empty(isolated_price_db):
    from core.market_regime import analyze_market_regime
    assert analyze_market_regime()["regime"] == "UNKNOWN"
