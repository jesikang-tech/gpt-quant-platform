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


def test_historical_replay_analysis_builds_point_in_time_portfolio(monkeypatch):
    import current_analysis
    from core.market_regime import analyze_market_regime
    from core.market_strategy import generate_market_strategy
    from core.portfolio_advisor import optimize_portfolio_weight

    replay_analysis = {
        "success": True,
        "analysis_date": "2026-06-12",
        "period": "3m",
        "current_score_top": [
            {
                "ticker": "AAA",
                "name": "AAA",
                "return_score": 96.0,
                "trend_score": 94.0,
                "slope_score": 93.0,
                "final_score": 94.8,
                "uptrend_ratio": 80.0,
            },
            {
                "ticker": "BBB",
                "name": "BBB",
                "return_score": 93.0,
                "trend_score": 91.0,
                "slope_score": 90.0,
                "final_score": 91.8,
                "uptrend_ratio": 75.0,
            },
            {
                "ticker": "CCC",
                "name": "CCC",
                "return_score": 91.0,
                "trend_score": 89.0,
                "slope_score": 88.0,
                "final_score": 89.8,
                "uptrend_ratio": 70.0,
            },
        ],
    }

    def fake_replay_analysis(*args, **kwargs):
        return replay_analysis

    monkeypatch.setattr(
        current_analysis,
        "get_current_analysis_data",
        fake_replay_analysis,
    )

    scores = replay_analysis["current_score_top"]
    regime = analyze_market_regime(scores=scores)
    strategy = generate_market_strategy(regime)

    ranking = [
        {
            "ticker": item["ticker"],
            "score": item["final_score"],
            "return_score": item["return_score"],
            "trend_score": item["trend_score"],
            "slope_score": item["slope_score"],
        }
        for item in scores
    ]

    portfolio = optimize_portfolio_weight(
        ranking,
        mode=strategy["portfolio_mode"],
    )

    assert regime["regime"] == "BULLISH"
    assert strategy["portfolio_mode"] == "aggressive"
    assert [item["ticker"] for item in portfolio] == [
        "AAA",
        "BBB",
        "CCC",
        "CASH",
    ]
    assert [item["weight"] for item in portfolio] == [50, 30, 15, 5]
    assert portfolio[0]["return_score"] == 96.0
    assert portfolio[0]["trend_score"] == 94.0
    assert portfolio[0]["slope_score"] == 93.0


def test_historical_replay_api_exposes_point_in_time_portfolio(monkeypatch):
    import api_server

    replay_scores = [
        {
            "ticker": "AAA",
            "name": "AAA",
            "return_score": 96.0,
            "trend_score": 94.0,
            "slope_score": 93.0,
            "final_score": 94.8,
            "uptrend_ratio": 80.0,
            "selection_pass": True,
            "price": 150.0,
            "future_performance": None,
            "future_performance_days": 0,
            "reality_test": {},
        },
        {
            "ticker": "BBB",
            "name": "BBB",
            "return_score": 93.0,
            "trend_score": 91.0,
            "slope_score": 90.0,
            "final_score": 91.8,
            "uptrend_ratio": 75.0,
            "selection_pass": True,
            "price": 140.0,
            "future_performance": None,
            "future_performance_days": 0,
            "reality_test": {},
        },
        {
            "ticker": "CCC",
            "name": "CCC",
            "return_score": 91.0,
            "trend_score": 89.0,
            "slope_score": 88.0,
            "final_score": 89.8,
            "uptrend_ratio": 70.0,
            "selection_pass": True,
            "price": 130.0,
            "future_performance": None,
            "future_performance_days": 0,
            "reality_test": {},
        },
    ]

    monkeypatch.setattr(
        "api_server.get_current_analysis_data",
        lambda **kwargs: {
            "success": True,
            "analysis_date": "2026-06-12",
            "market_data_date": "2026-06-12",
            "period": "3m",
            "lookback_trading_days": 60,
            "return_threshold": 15,
            "uptrend_threshold": 60,
            "total_etf": 3,
            "enough_data": 3,
            "selection": {
                "return_threshold": 15,
                "uptrend_threshold": 60,
                "count": 3,
                "top": replay_scores,
            },
            "current_score_top": replay_scores,
            "db_write": False,
        },
    )

    from testing_helpers import authenticated_client

    client = authenticated_client(api_server.app)
    response = client.get(
        "/api/historical-replay?date=2026-06-12&period=3m"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["analysis_date"] == "2026-06-12"
    assert data["period"] == "3m"
    assert data["db_write"] is False
    assert "market_regime" in data
    assert "market_strategy" in data
    assert "portfolio" in data

    assert data["market_regime"]["regime"] == "BULLISH"
    assert data["market_strategy"]["portfolio_mode"] == "aggressive"
    assert [item["ticker"] for item in data["portfolio"]] == [
        "AAA",
        "BBB",
        "CCC",
        "CASH",
    ]
    assert [item["weight"] for item in data["portfolio"]] == [
        50,
        30,
        15,
        5,
    ]
