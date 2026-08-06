"""
GPT Quant Platform
AI Market Strategy Engine

Step5-3-45
"""


def generate_market_strategy(market_regime):
    """
    Generate AI Market Strategy

    Args:
        market_regime:
            {
                "regime": "NEUTRAL",
                "confidence": 82,
                "market_strength": "Strong"
            }

    Returns:
        strategy dictionary
    """


    if not market_regime:

        return {
            "market": "UNKNOWN",
            "strategy": "No Strategy",
            "portfolio_mode": "balanced",
            "cash_target": 10,

            "market_strength": "Unknown",
            "confidence": 0,
            "recommendation": "HOLD",
            "rebalance_action": "No Action",

            "message": "Market data unavailable"
        }



    regime = market_regime.get(
        "regime",
        "NEUTRAL"
    )


    confidence = market_regime.get(
        "confidence",
        0
    )


    strength = market_regime.get(
        "market_strength",
        "Unknown"
    )



    if regime == "BULLISH":

        strategy = {
            "market": regime,
            "strategy": "Aggressive Growth",
            "portfolio_mode": "aggressive",
            "cash_target": 5,

            "market_strength": strength,
            "confidence": confidence,
            "recommendation": "BUY",
            "rebalance_action": "Increase Equity",

            "message":
                f"Strong momentum detected. "
                f"Growth allocation recommended. "
                f"Confidence {confidence}%"
        }



    elif regime == "BEARISH":

        strategy = {
            "market": regime,
            "strategy": "Defensive Strategy",
            "portfolio_mode": "conservative",
            "cash_target": 30,

            "market_strength": strength,
            "confidence": confidence,
            "recommendation": "REDUCE",
            "rebalance_action": "Increase Cash",

            "message":
                f"Risk control recommended. "
                f"Market weakness detected. "
                f"Confidence {confidence}%"
        }



    else:

        strategy = {
            "market": regime,
            "strategy": "Balanced Strategy",
            "portfolio_mode": "balanced",
            "cash_target": 10,

            "market_strength": strength,
            "confidence": confidence,
            "recommendation": "HOLD",
            "rebalance_action": "No Action",

            "message":
                f"Market balance maintained. "
                f"Strength {strength}. "
                f"Confidence {confidence}%"                
        }



    return strategy