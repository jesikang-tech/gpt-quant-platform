"""Real optimization and factor readback through a guarded synthetic DB."""
import pytest
from price_test_support import isolated_price_db, synthetic_portfolio_db


def test_portfolio_optimization(synthetic_portfolio_db):
    from core.portfolio_advisor import optimize_portfolio_weight
    from repository import get_etf_score

    data = synthetic_portfolio_db
    ranking = [{"ticker": ticker, "score": score} for ticker, score in data.scores.items()]
    before = len(data.db.accesses)
    portfolio = optimize_portfolio_weight(list(reversed(ranking)), "aggressive")
    assert len(data.db.accesses) == before + len(ranking)
    expected = {ticker: round(r * 0.30 + t * 0.25 + s * 0.20 + 80 * 0.15 + 90 * 0.10, 2)
                for ticker, (r, t, s) in data.factors.items()}
    assert [item["ticker"] for item in portfolio] == [
        *sorted(expected, key=expected.get, reverse=True), "CASH"]
    assert [item["weight"] for item in portfolio] == [50, 30, 15, 5]
    assert sum(item["weight"] for item in portfolio) == 100
    for item in portfolio[:-1]:
        ticker = item["ticker"]
        assert get_etf_score(ticker) == (ticker, data.scores[ticker], *data.factors[ticker])
        assert (item["return_score"], item["trend_score"], item["slope_score"]) == data.factors[ticker]
        assert item["optimization_score"] == pytest.approx(expected[ticker])
        assert item["mode"] == "aggressive"
    assert portfolio[-1]["score"] is None
