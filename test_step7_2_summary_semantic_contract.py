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
        {},
        "GROWTH",
        "INCREASE_RISK",
        "UP",
        "POSITIVE",
        "high",
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
        {},
        "DEFENSIVE",
        "REDUCE_RISK",
        "DOWN",
        "NEGATIVE",
        "high",
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
        {},
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
        "STABLE",
        "NEUTRAL",
        "high",
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
        {},
        "CAUTIOUS",
        "LIMIT_EXPOSURE",
        "UP",
        "POSITIVE",
        "low",
    ),
    (
        "CASE 5 MONITOR",
        {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "CHANGING",
            "consistency": "LOW",
            "latest_score": 65,
        },
        {},
        "MONITOR",
        "MONITOR_CLOSELY",
        "STABLE",
        "NEUTRAL",
        "high",
    ),
    (
        "CASE 6 BALANCED",
        {
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 70,
        },
        {},
        "BALANCED",
        "MAINTAIN_BALANCE",
        "STABLE",
        "NEUTRAL",
        "medium",
    ),
    (
        "CASE 7 NEGATIVE ADAPTIVE OVERRIDE",
        {
            "direction": "UP",
            "stability": "HIGH",
            "momentum": "POSITIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 92,
        },
        {
            "outcome_learning_signal": "NEGATIVE",
            "outcome_learning_signal_strength": 1.0,
            "adaptive_learning_required": True,
        },
        "DEFENSIVE",
        "REDUCE_RISK",
        "UP",
        "POSITIVE",
        "high",
    ),
]


print("=" * 60)
print("PHASE 7-2-15 SUMMARY SEMANTIC CONTRACT")
print("=" * 60)


for (
    name,
    trend,
    outcome,
    expected_strategy,
    expected_action,
    expected_direction,
    expected_momentum,
    expected_stability,
) in CASES:

    result = ENGINE.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    summary = result["summary"]

    assert result["strategy"] == expected_strategy
    assert result["action"] == expected_action

    assert (
        f"Adaptive strategy is {expected_strategy}."
        in summary
    )

    assert (
        f"Recommended action is {expected_action}."
        in summary
    )

    assert (
        f"AI decision direction is {expected_direction},"
        in summary
    )

    assert (
        f"momentum is {expected_momentum},"
        in summary
    )

    assert (
        f"stability is {expected_stability}."
        in summary
    )

    print(
        f"{name}: PASS | "
        f"{result['strategy']} -> "
        f"{result['action']} | "
        f"summary=CONSISTENT"
    )


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
