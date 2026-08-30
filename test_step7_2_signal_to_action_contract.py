from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


ENGINE = AIDecisionAdaptiveStrategy()


BASE_TREND = {
    "direction": "SIDEWAYS",
    "stability": "MEDIUM",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "MEDIUM",
    "latest_score": 85,
}


print("=" * 60)
print("PHASE 7-2-8 SIGNAL-TO-ACTION CONTRACT")
print("=" * 60)


def run_case(
    name,
    outcome_intelligence,
    expected_strategy,
    expected_action,
    expected_signal,
    expected_strength,
    expected_adaptive,
):
    result = ENGINE.analyze(
        trend=BASE_TREND,
        outcome_intelligence=outcome_intelligence,
    )

    assert result["strategy"] == expected_strategy
    assert result["action"] == expected_action

    assert (
        result["outcome_learning_signal"]
        == expected_signal
    )

    assert (
        result["outcome_learning_signal_strength"]
        == expected_strength
    )

    assert (
        result["adaptive_learning_required"]
        is expected_adaptive
    )

    print(
        f"{name}: PASS | "
        f"{result['outcome_learning_signal']} | "
        f"strength={result['outcome_learning_signal_strength']} | "
        f"adaptive={result['adaptive_learning_required']} | "
        f"{result['strategy']} -> {result['action']}"
    )


print("")
print("=== END-TO-END OUTCOME LEARNING FLOW ===")


run_case(
    "CASE 1 NEGATIVE",
    {
        "outcome_learning_signal": "NEGATIVE",
        "outcome_learning_signal_strength": 1.0,
        "adaptive_learning_required": True,
    },
    "DEFENSIVE",
    "REDUCE_RISK",
    "NEGATIVE",
    1.0,
    True,
)


run_case(
    "CASE 2 POSITIVE",
    {
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 0.7,
        "adaptive_learning_required": False,
    },
    "GROWTH",
    "INCREASE_RISK",
    "POSITIVE",
    0.7,
    False,
)


run_case(
    "CASE 3 NONE",
    {
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": False,
    },
    "BALANCED",
    "MAINTAIN_BALANCE",
    "NONE",
    0.0,
    False,
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
