from core.market_regime import analyze_market_regime
from core.market_strategy import generate_market_strategy
from core.portfolio_advisor import optimize_portfolio_weight


def build_point_in_time_explanation(data):
    market_regime = data.get("market_regime", {})
    market_strategy = data.get("market_strategy", {})
    portfolio = data.get("portfolio", [])

    allocations = []
    cash_weight = 0

    for item in portfolio:
        ticker = item.get("ticker")
        weight = item.get("weight", 0)

        if ticker == "CASH":
            cash_weight += weight
            continue

        allocations.append(
            {
                "ticker": ticker,
                "weight": weight,
                "score": item.get("score"),
                "return_score": item.get("return_score"),
                "trend_score": item.get("trend_score"),
                "slope_score": item.get("slope_score"),
                "optimization_score": item.get("optimization_score"),
                "factor_analysis": item.get("factor_analysis"),
            }
        )

    regime = market_regime.get("regime", "UNKNOWN")
    confidence = market_regime.get("confidence", 0)
    avg_score = market_regime.get("avg_score")
    market_strength = market_regime.get("market_strength", "Unknown")

    if regime == "BULLISH":
        market_reason = (
            f"Point-in-Time average score {avg_score} "
            f"supports a bullish market regime with "
            f"{confidence}% confidence."
        )
    elif regime == "BEARISH":
        market_reason = (
            f"Point-in-Time average score {avg_score} "
            f"supports a bearish market regime with "
            f"{confidence}% confidence."
        )
    else:
        market_reason = (
            f"Point-in-Time average score {avg_score} "
            f"supports a neutral market regime with "
            f"{confidence}% confidence."
        )

    return {
        "analysis_date": data.get("analysis_date"),
        "period": data.get("period"),
        "market_regime": {
            "regime": regime,
            "confidence": confidence,
            "avg_score": avg_score,
            "market_strength": market_strength,
            "breadth": market_regime.get("breadth"),
            "momentum": market_regime.get("momentum"),
            "risk": market_regime.get("risk"),
            "reason": market_reason,
        },
        "market_strategy": {
            "strategy": market_strategy.get("strategy"),
            "portfolio_mode": market_strategy.get("portfolio_mode"),
            "cash_target": market_strategy.get("cash_target"),
            "recommendation": market_strategy.get("recommendation"),
            "rebalance_action": market_strategy.get("rebalance_action"),
            "confidence": market_strategy.get("confidence"),
            "market_strength": market_strategy.get("market_strength"),
            "reason": market_strategy.get("message"),
        },
        "portfolio": {
            "cash_weight": cash_weight,
            "allocations": allocations,
            "reason": (
                f"Portfolio allocation follows the Point-in-Time "
                f"{market_strategy.get('portfolio_mode', 'balanced')} "
                f"strategy under the {regime} market regime."
            ),
        },
    }


def attach_point_in_time_portfolio(data):
    scores = data.get(
        "market_regime_scores",
        data.get("current_score_top", []),
    )

    market_regime = analyze_market_regime(scores=scores)
    market_strategy = generate_market_strategy(market_regime)

    ranking = [
        {
            "ticker": item.get("ticker"),
            "score": item.get("final_score", 0),
            "return_score": item.get("return_score"),
            "trend_score": item.get("trend_score"),
            "slope_score": item.get("slope_score"),
        }
        for item in scores
    ]

    portfolio = optimize_portfolio_weight(
        ranking,
        mode=market_strategy.get("portfolio_mode", "balanced"),
    )

    data["market_regime"] = market_regime
    data["market_strategy"] = market_strategy
    data["portfolio"] = portfolio
    data["point_in_time_explanation"] = build_point_in_time_explanation(data)

    return data
