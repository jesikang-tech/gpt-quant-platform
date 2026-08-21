from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy

engine = AIDecisionAdaptiveStrategy()

cases = [
    (
        "CASE 1 NONE / BALANCED",
        {
            "direction": "SIDEWAYS",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 70,
        },
        {
            "outcome_learning_signal": "NONE",
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        },
        "BALANCED",
        "MAINTAIN_BALANCE",
        80,
        "NONE",
        0.0,
        False,
    ),
    (
        "CASE 2 POSITIVE / BALANCED",
        {
            "direction": "SIDEWAYS",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 70,
        },
        {
            "outcome_learning_signal": "POSITIVE",
            "outcome_learning_signal_strength": 0.7,
            "adaptive_learning_required": False,
        },
        "GROWTH",
        "INCREASE_RISK",
        80,
        "POSITIVE",
        0.7,
        False,
    ),
    (
        "CASE 3 NEGATIVE / ADAPTIVE",
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
        "NEGATIVE",
        1.0,
        True,
    ),
    (
        "CASE 4 NEGATIVE / NO ADAPTIVE",
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
        100,
        "NEGATIVE",
        1.0,
        False,
    ),
    (
        "CASE 5 POSITIVE / MAINTAIN",
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
        "POSITIVE",
        1.0,
        False,
    ),
]

print("=" * 60)
print("PHASE 7-2-19 OUTCOME LEARNING FULL FLOW CONTRACT")
print("=" * 60)

for (
    name,
    trend,
    outcome,
    expected_strategy,
    expected_action,
    expected_confidence,
    expected_signal,
    expected_strength,
    expected_adaptive,
) in cases:

    result = engine.analyze(
        trend,
        outcome_intelligence=outcome,
    )

    summary = result["summary"]

    assert result["strategy"] == expected_strategy
    assert result["action"] == expected_action
    assert result["confidence"] == expected_confidence
    assert result["outcome_learning_signal"] == expected_signal
    assert result["outcome_learning_signal_strength"] == expected_strength
    assert result["adaptive_learning_required"] is expected_adaptive

    assert expected_strategy in summary
    assert expected_action in summary

    print(
        f"{name}: PASS | "
        f"{result['strategy']} -> {result['action']} | "
        f"confidence={result['confidence']} | "
        f"signal={result['outcome_learning_signal']} | "
        f"adaptive={result['adaptive_learning_required']} | "
        f"summary=CONSISTENT"
    )

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
