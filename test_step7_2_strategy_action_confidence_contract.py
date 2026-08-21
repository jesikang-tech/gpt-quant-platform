from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


ENGINE = AIDecisionAdaptiveStrategy()


CASES = [
    (
        "CASE 1 GROWTH",
        {
            "direction": "UP",
            "stability": "HIGH",
            "momentum": "POSITIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 92,
        },
        None,
        "GROWTH",
        "INCREASE_RISK",
        100,
    ),
    (
        "CASE 2 DEFENSIVE",
        {
            "direction": "DOWN",
            "stability": "HIGH",
            "momentum": "NEGATIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 55,
        },
        {
            "outcome_learning_signal": "NEGATIVE",
            "outcome_learning_signal_strength": 1.0,
            "adaptive_learning_required": True,
        },
        "DEFENSIVE",
        "REDUCE_RISK",
        100,
    ),
    (
        "CASE 3 MAINTAIN",
        {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        },
        None,
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
        100,
    ),
    (
        "CASE 4 CAUTIOUS",
        {
            "direction": "UP",
            "stability": "LOW",
            "momentum": "POSITIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 70,
        },
        None,
        "CAUTIOUS",
        "LIMIT_EXPOSURE",
        80,
    ),
    (
        "CASE 5 MONITOR",
        {
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "CHANGING",
            "consistency": "LOW",
            "latest_score": 65,
        },
        None,
        "MONITOR",
        "MONITOR_CLOSELY",
        60,
    ),
]


print("=" * 60)
print("PHASE 7-2-10 STRATEGY / ACTION / CONFIDENCE CONTRACT")
print("=" * 60)

for (
    name,
    trend,
    outcome,
    expected_strategy,
    expected_action,
    expected_confidence,
) in CASES:

    result = ENGINE.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    assert result["strategy"] == expected_strategy
    assert result["action"] == expected_action
    assert result["confidence"] == expected_confidence

    print(
        f"{name}: PASS | "
        f"{result['strategy']} -> "
        f"{result['action']} | "
        f"confidence={result['confidence']}"
    )


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
