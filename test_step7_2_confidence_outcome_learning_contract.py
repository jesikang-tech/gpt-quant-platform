from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


ENGINE = AIDecisionAdaptiveStrategy()


CASES = [
    (
        "CASE 1 GROWTH + NONE",
        {
            "direction": "UP",
            "stability": "HIGH",
            "momentum": "POSITIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 92,
        },
        {
            "outcome_learning_signal": "NONE",
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        },
        "GROWTH",
        "INCREASE_RISK",
        100,
    ),
    (
        "CASE 2 GROWTH + NEGATIVE ADAPTIVE",
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
        100,
    ),
    (
        "CASE 3 MAINTAIN + POSITIVE",
        {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        },
        {
            "outcome_learning_signal": "POSITIVE",
            "outcome_learning_signal_strength": 1.0,
            "adaptive_learning_required": False,
        },
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
        100,
    ),
    (
        "CASE 4 MAINTAIN + NEGATIVE ADAPTIVE",
        {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
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
        "CASE 5 DEFENSIVE + POSITIVE",
        {
            "direction": "DOWN",
            "stability": "HIGH",
            "momentum": "NEGATIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 55,
        },
        {
            "outcome_learning_signal": "POSITIVE",
            "outcome_learning_signal_strength": 1.0,
            "adaptive_learning_required": False,
        },
        "DEFENSIVE",
        "REDUCE_RISK",
        100,
    ),
]


print("=" * 60)
print("PHASE 7-2-13 CONFIDENCE / OUTCOME LEARNING CONTRACT")
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
