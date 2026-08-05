from repository import get_top_scores


def analyze_market_regime():

    rankings = get_top_scores(limit=30)

    if not rankings:
        return {
            "regime": "UNKNOWN",
            "confidence": 0,
            "breadth": "Unknown",
            "momentum": "Neutral",
            "risk": "High",
            "strategy": "No Data"
        }

    scores = [item[1] for item in rankings]

    avg_score = sum(scores) / len(scores)

    max_score = max(scores)
    min_score = min(scores)

    score_spread = round(
        max_score - min_score,
        2
    )

    high_score_count = sum(
        1 for s in scores
        if s >= 90
    )

    high_score_ratio = round(
        high_score_count / len(scores) * 100,
        1
    )

    strong_score_count = sum(
        1 for s in scores
        if s >= 85
    )

    if strong_score_count >= len(scores) * 0.7:
        market_strength = "Strong"

    elif strong_score_count >= len(scores) * 0.4:
        market_strength = "Moderate"

    else:
        market_strength = "Weak"

    if avg_score >= 90:
        regime = "BULLISH"
        confidence = 95
        breadth = "Strong"
        momentum = "Positive"
        risk = "Low"
        strategy = "Risk-On Portfolio"

    elif avg_score >= 80:
        regime = "NEUTRAL"
        confidence = 82
        breadth = "Balanced"
        momentum = "Stable"
        risk = "Medium"
        strategy = "Balanced Portfolio"

    else:
        regime = "BEARISH"
        confidence = 75
        breadth = "Weak"
        momentum = "Negative"
        risk = "High"
        strategy = "Defensive Portfolio"


    return {
        "regime": regime,
        "confidence": confidence,
        "breadth": breadth,
        "momentum": momentum,
        "risk": risk,
        "strategy": strategy,

        "avg_score": round(avg_score, 2),

        "max_score": round(max_score, 2),
        "min_score": round(min_score, 2),

        "score_spread": score_spread,

        "high_score_ratio": high_score_ratio,

        "market_strength": market_strength,

        "analyzed_count": len(rankings)
    }