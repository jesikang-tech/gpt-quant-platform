from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


ENGINE = AIDecisionAdaptiveStrategy()


CASES = [
    (
        "CASE 1 HIGH / STABLE / HIGH",
        "HIGH",
        "STABLE",
        "HIGH",
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
        100,
    ),
    (
        "CASE 2 MEDIUM / STABLE / HIGH",
        "MEDIUM",
        "STABLE",
        "HIGH",
        "BALANCED",
        "MAINTAIN_BALANCE",
        90,
    ),
    (
        "CASE 3 LOW / STABLE / HIGH",
        "LOW",
        "STABLE",
        "HIGH",
        "CAUTIOUS",
        "LIMIT_EXPOSURE",
        80,
    ),
    (
        "CASE 4 HIGH / CHANGING / HIGH",
        "HIGH",
        "CHANGING",
        "HIGH",
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
        90,
    ),
    (
        "CASE 5 HIGH / STABLE / LOW",
        "HIGH",
        "STABLE",
        "LOW",
        "MONITOR",
        "MONITOR_CLOSELY",
        80,
    ),
    (
        "CASE 6 HIGH / CHANGING / LOW",
        "HIGH",
        "CHANGING",
        "LOW",
        "MONITOR",
        "MONITOR_CLOSELY",
        70,
    ),
    (
        "CASE 7 UNKNOWN / UNKNOWN / UNKNOWN",
        "UNKNOWN",
        "UNKNOWN",
        "UNKNOWN",
        "BALANCED",
        "MAINTAIN_BALANCE",
        50,
    ),
    (
        "CASE 8 LOW / CHANGING / LOW",
        "LOW",
        "CHANGING",
        "LOW",
        "CAUTIOUS",
        "LIMIT_EXPOSURE",
        50,
    ),
]


print("=" * 60)
print("PHASE 7-2-14 CONFIDENCE BOUNDARY CONTRACT")
print("=" * 60)


for (
    name,
    stability,
    grade_stability,
    consistency,
    expected_strategy,
    expected_action,
    expected_confidence,
) in CASES:

    trend = {
        "direction": "STABLE",
        "stability": stability,
        "momentum": "NEUTRAL",
        "grade_stability": grade_stability,
        "consistency": consistency,
        "latest_score": 70,
    }

    result = ENGINE.analyze(
        trend=trend,
        outcome_intelligence={
            "outcome_learning_signal": "NONE",
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        },
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
