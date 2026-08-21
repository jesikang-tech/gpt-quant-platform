from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


ENGINE = AIDecisionAdaptiveStrategy()


CASES = [
    (
        "CASE 1 GROWTH + NEGATIVE ADAPTIVE",
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
    ),
    (
        "CASE 2 DEFENSIVE + POSITIVE STRONG",
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
    ),
    (
        "CASE 3 MAINTAIN + NEGATIVE WITHOUT ADAPTIVE",
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
            "adaptive_learning_required": False,
        },
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
    ),
    (
        "CASE 4 MAINTAIN + POSITIVE STRONG",
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
    ),
    (
        "CASE 5 NONE + ADAPTIVE TRUE",
        {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        },
        {
            "outcome_learning_signal": "NONE",
            "outcome_learning_signal_strength": 1.0,
            "adaptive_learning_required": True,
        },
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
    ),
    (
        "CASE 6 NEGATIVE + ADAPTIVE TRUE + GROWTH TREND",
        {
            "direction": "UP",
            "stability": "HIGH",
            "momentum": "POSITIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 95,
        },
        {
            "outcome_learning_signal": "NEGATIVE",
            "outcome_learning_signal_strength": 0.7,
            "adaptive_learning_required": True,
        },
        "DEFENSIVE",
        "REDUCE_RISK",
    ),
]


print("=" * 60)
print("PHASE 7-2-12 CONFLICTING SIGNAL PRIORITY CONTRACT")
print("=" * 60)

for (
    name,
    trend,
    outcome,
    expected_strategy,
    expected_action,
) in CASES:

    result = ENGINE.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    assert result["strategy"] == expected_strategy
    assert result["action"] == expected_action

    print(
        f"{name}: PASS | "
        f"{result['strategy']} -> "
        f"{result['action']} | "
        f"signal={result['outcome_learning_signal']} | "
        f"adaptive={result['adaptive_learning_required']}"
    )


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
