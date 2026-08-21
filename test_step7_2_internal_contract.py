from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


ENGINE = AIDecisionAdaptiveStrategy()


REQUIRED_FIELDS = {
    "strategy": str,
    "action": str,
    "confidence": int,
    "score": int,
    "direction": str,
    "stability": str,
    "momentum": str,
    "grade_stability": str,
    "consistency": str,
    "outcome_learning_signal": str,
    "outcome_learning_signal_strength": float,
    "adaptive_learning_required": bool,
    "summary": str,
}


ACTION_MAP = {
    "GROWTH": "INCREASE_RISK",
    "DEFENSIVE": "REDUCE_RISK",
    "MAINTAIN": "MAINTAIN_ALLOCATION",
    "CAUTIOUS": "LIMIT_EXPOSURE",
    "MONITOR": "MONITOR_CLOSELY",
    "BALANCED": "MAINTAIN_BALANCE",
}


CASES = [
    (
        "CASE 1 BASE GROWTH",
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
        92,
    ),
    (
        "CASE 2 BASE MAINTAIN",
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
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        },
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
        100,
        85,
    ),
    (
        "CASE 3 NEGATIVE OVERRIDE",
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
        92,
    ),
    (
        "CASE 4 POSITIVE STRONG",
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
        85,
    ),
    (
        "CASE 5 UNKNOWN DEFAULT",
        {},
        {},
        "BALANCED",
        "MAINTAIN_BALANCE",
        50,
        0,
    ),
]


print("=" * 60)
print("PHASE 7-2-16 ADAPTIVE STRATEGY INTERNAL CONTRACT")
print("=" * 60)


for (
    name,
    trend,
    outcome,
    expected_strategy,
    expected_action,
    expected_confidence,
    expected_score,
) in CASES:

    result = ENGINE.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    # Required fields
    assert set(REQUIRED_FIELDS).issubset(result)

    # Field types
    for field, expected_type in REQUIRED_FIELDS.items():
        assert type(result[field]) is expected_type

    # Strategy / action
    assert result["strategy"] == expected_strategy
    assert result["action"] == expected_action
    assert ACTION_MAP[result["strategy"]] == result["action"]

    # Confidence / score
    assert 0 <= result["confidence"] <= 100
    assert result["confidence"] == expected_confidence
    assert result["score"] == expected_score

    # Learning state
    signal = result["outcome_learning_signal"]
    strength = result["outcome_learning_signal_strength"]
    adaptive = result["adaptive_learning_required"]

    assert signal in {"NONE", "POSITIVE", "NEGATIVE"}
    assert 0.0 <= strength <= 1.0

    if signal == "NONE":
        assert strength == 0.0
        assert adaptive is False

    if signal == "NEGATIVE" and adaptive:
        assert result["strategy"] == "DEFENSIVE"
        assert result["action"] == "REDUCE_RISK"

    # Summary semantic consistency
    summary = result["summary"]

    assert (
        f"Adaptive strategy is {result['strategy']}."
        in summary
    )

    assert (
        f"Recommended action is {result['action']}."
        in summary
    )

    print(
        f"{name}: PASS | "
        f"{result['strategy']} -> "
        f"{result['action']} | "
        f"confidence={result['confidence']} | "
        f"fields=13 | types=PASS"
    )


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
