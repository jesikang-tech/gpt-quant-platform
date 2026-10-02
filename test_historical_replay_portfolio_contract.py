from core.market_regime import analyze_market_regime


def test_market_regime_accepts_replay_scores_without_repository_read(monkeypatch):
    def reject_repository_read(*args, **kwargs):
        raise AssertionError("Historical replay must not read persisted current scores")

    monkeypatch.setattr(
        "core.market_regime.get_top_scores",
        reject_repository_read,
    )

    replay_scores = [
        {"ticker": "AAA", "final_score": 95.0},
        {"ticker": "BBB", "final_score": 92.0},
        {"ticker": "CCC", "final_score": 91.0},
    ]

    result = analyze_market_regime(scores=replay_scores)

    assert result["regime"] == "BULLISH"
    assert result["avg_score"] == 92.67
    assert result["analyzed_count"] == 3


def test_portfolio_uses_supplied_replay_regime_without_current_market_read(monkeypatch):
    from core.portfolio_advisor import generate_portfolio

    def reject_current_market_read():
        raise AssertionError("Historical replay portfolio must not read current market regime")

    monkeypatch.setattr(
        "core.portfolio_advisor.analyze_market_regime",
        reject_current_market_read,
    )

    ranking = [
        {"ticker": "AAA", "score": 95.0, "trend": 1},
        {"ticker": "BBB", "score": 92.0, "trend": 1},
        {"ticker": "CCC", "score": 91.0, "trend": 1},
    ]
    replay_regime = {
        "regime": "BULLISH",
        "confidence": 95,
        "market_strength": "Strong",
    }

    result = generate_portfolio(ranking, market_regime=replay_regime)

    assert [item["ticker"] for item in result] == ["AAA", "BBB", "CCC", "CASH"]
    assert [item["weight"] for item in result] == [50, 30, 15, 5]


def test_optimized_portfolio_uses_replay_factor_scores_without_db_read(monkeypatch):
    from core.portfolio_advisor import optimize_portfolio_weight

    def reject_score_read(*args, **kwargs):
        raise AssertionError("Historical replay portfolio must not read persisted ETF scores")

    monkeypatch.setattr(
        "core.portfolio_advisor.get_etf_score",
        reject_score_read,
    )

    ranking = [
        {
            "ticker": "AAA",
            "score": 95.0,
            "return_score": 96.0,
            "trend_score": 94.0,
            "slope_score": 93.0,
        },
        {
            "ticker": "BBB",
            "score": 92.0,
            "return_score": 93.0,
            "trend_score": 91.0,
            "slope_score": 90.0,
        },
        {
            "ticker": "CCC",
            "score": 90.0,
            "return_score": 91.0,
            "trend_score": 89.0,
            "slope_score": 88.0,
        },
    ]

    result = optimize_portfolio_weight(ranking, mode="balanced")

    assert [item["ticker"] for item in result] == ["AAA", "BBB", "CCC", "CASH"]
    assert [item["weight"] for item in result] == [40, 30, 20, 10]
    assert result[0]["return_score"] == 96.0
    assert result[0]["trend_score"] == 94.0
    assert result[0]["slope_score"] == 93.0
