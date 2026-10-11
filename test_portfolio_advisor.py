"""Portfolio allocation and health with synthetic market scores."""
from price_test_support import isolated_price_db, synthetic_ranking_db


def test_portfolio_and_health(synthetic_ranking_db):
    from core.market_regime import analyze_market_regime
    from core.market_strategy import generate_market_strategy
    from core.portfolio_advisor import generate_portfolio, analyze_portfolio_health
    ranking = [{"ticker": ticker, "score": scores[-1], "trend": 1}
               for ticker, scores in synthetic_ranking_db.scores.items()]
    regime = analyze_market_regime()
    assert generate_market_strategy(regime)["market"] == regime["regime"]
    portfolio = generate_portfolio(list(reversed(ranking)))
    assert portfolio == generate_portfolio(ranking, regime)
    assert [item["ticker"] for item in portfolio] == ["111111", "222222", "333333", "CASH"]
    assert sum(item["weight"] for item in portfolio) == 100
    aggressive = {"regime": "BULLISH", "confidence": 90, "market_strength": "Strong"}
    assert generate_market_strategy(aggressive)["portfolio_mode"] == "aggressive"
    aggressive_portfolio = generate_portfolio(ranking, aggressive)
    assert [item["weight"] for item in aggressive_portfolio] == [50, 30, 15, 5]
    health = analyze_portfolio_health(portfolio)
    assert health["allocation"] == {item["ticker"]: item["weight"] for item in portfolio[:-1]}
    assert health["cash_weight"] == portfolio[-1]["weight"]
    assert 0 <= health["health_score"] <= 100
    assert health["rebalance"]


def test_portfolio_empty(isolated_price_db):
    from core.portfolio_advisor import generate_portfolio, analyze_portfolio_health
    assert generate_portfolio([]) == []
    assert analyze_portfolio_health([])["health_score"] == 0
