"""
GPT Quant Platform

AI Portfolio Decision Engine

Step5-3-52
"""


def generate_ai_decision(
        market_regime,
        market_strategy,
        portfolio_health,
        top_etf
):
    """
    Generate Final AI Portfolio Decision

    Args:

        market_regime:
            {
                "regime": "NEUTRAL",
                "confidence": 82,
                "market_strength": "Strong"
            }

        market_strategy:
            {
                "strategy": "Balanced Strategy",
                "recommendation": "HOLD",
                "portfolio_mode": "balanced"
            }

        portfolio_health:
            {
                "health_score": 89.7,
                "risk_level": "Balanced",
                "confidence": "MEDIUM"
            }

        top_etf:
            {
                "ticker": "365040",
                "score": 93
            }


    Returns:

        {
            "decision": "...",
            "action": "...",
            "confidence": 0,
            "reason": "...",
            "summary": "..."
        }

    """


    if not market_regime:
        return {
            "decision": "UNKNOWN",
            "action": "No Action",
            "confidence": 0,
            "market_view": "UNKNOWN",
            "recommended_mode": "balanced",
            "risk_control": "Unknown",
            "next_action": "Wait for market data",
            "reason": "Market data unavailable",
            "summary": "Unable to generate AI decision"
        }


    regime = market_regime.get(
        "regime",
        "NEUTRAL"
    )


    market_confidence = market_regime.get(
        "confidence",
        0
    )


    strategy = market_strategy.get(
        "strategy",
        "Balanced Strategy"
    )


    recommendation = market_strategy.get(
        "recommendation",
        "HOLD"
    )


    health_score = portfolio_health.get(
        "health_score",
        0
    )


    risk_level = portfolio_health.get(
        "risk_level",
        "Unknown"
    )


    ticker = top_etf.get(
        "ticker",
        "-"
    )


    score = top_etf.get(
        "score",
        0
    )



    # -----------------------------
    # Bullish Decision
    # -----------------------------

    if (
        regime == "BULLISH"
        and
        recommendation == "BUY"
        and
        health_score >= 80
    ):

        return {

            "decision":
                "ACCUMULATE",

            "action":
                "Increase Equity Allocation",

            "confidence":
                market_confidence,

            "market_view":
                regime,

            "recommended_mode":
                "aggressive",

            "risk_control":
                "Monitor volatility while increasing exposure",

            "next_action":
                "Increase high score ETF allocation",

            "reason":
                f"Market momentum is positive. "
                f"Portfolio health is strong. "
                f"Top ETF {ticker} score {score}",

            "summary":
                "Growth allocation is recommended"

        }



    # -----------------------------
    # Bearish Decision
    # -----------------------------

    elif (
        regime == "BEARISH"
        or
        risk_level == "High Risk"
    ):

        return {

            "decision":
                "DEFENSIVE",

            "action":
                "Increase Cash Weight",

            "confidence":
                market_confidence,

            "market_view":
                regime,

            "recommended_mode":
                "conservative",

            "risk_control":
                "Reduce equity exposure",

            "next_action":
                "Increase defensive allocation",

            "reason":
                "Market weakness or portfolio risk detected",

            "summary":
                "Risk control strategy recommended"

        }



    # -----------------------------
    # Neutral Decision
    # -----------------------------

    else:

        return {

            "decision":
                "MAINTAIN",

            "action":
                "Hold Balanced Allocation",

            "confidence":
                market_confidence,

            "market_view":
                regime,

            "recommended_mode":
                "balanced",

            "risk_control":
                "Maintain current portfolio risk",

            "next_action":
                "Monitor market momentum",

            "reason":
                f"Market regime {regime}. "
                f"Strategy {strategy}. "
                f"Portfolio risk {risk_level}",

            "summary":
                "Current portfolio allocation should be maintained"

        }



def calculate_decision_score(
        market_regime,
        portfolio_health,
        top_etf
):
    """
    Calculate AI Decision Score

    Score components:

    Market Confidence : 40
    Portfolio Health  : 40
    ETF Score         : 20

    Total : 100
    """


    market_confidence = market_regime.get(
        "confidence",
        0
    )


    health_score = portfolio_health.get(
        "health_score",
        0
    )


    etf_score = top_etf.get(
        "score",
        0
    )


    decision_score = (

        market_confidence * 0.4

        +

        health_score * 0.4

        +

        etf_score * 0.2

    )


    return round(
        decision_score,
        1
    )



def get_decision_grade(score):


    if score >= 90:

        return "A+"


    elif score >= 80:

        return "A"


    elif score >= 70:

        return "B"


    else:

        return "C"