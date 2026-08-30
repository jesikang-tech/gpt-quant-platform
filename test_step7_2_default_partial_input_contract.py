from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


ENGINE = AIDecisionAdaptiveStrategy()


print("=" * 60)
print("PHASE 7-2-9 DEFAULT / PARTIAL INPUT CONTRACT")
print("=" * 60)


CASES = [
    (
        "CASE 1 EMPTY TREND",
        {},
        None,
        {
            "strategy": "BALANCED",
            "action": "MAINTAIN_BALANCE",
            "confidence": 50,
            "score": 0,
            "direction": "STABLE",
            "stability": "UNKNOWN",
            "momentum": "NEUTRAL",
            "grade_stability": "UNKNOWN",
            "consistency": "UNKNOWN",
            "outcome_learning_signal": "NONE",
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        },
    ),
    (
        "CASE 2 EMPTY TREND + EMPTY OUTCOME",
        {},
        {},
        {
            "strategy": "BALANCED",
            "action": "MAINTAIN_BALANCE",
            "confidence": 50,
            "score": 0,
            "direction": "STABLE",
            "stability": "UNKNOWN",
            "momentum": "NEUTRAL",
            "grade_stability": "UNKNOWN",
            "consistency": "UNKNOWN",
            "outcome_learning_signal": "NONE",
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        },
    ),
    (
        "CASE 3 PARTIAL TREND",
        {
            "direction": "UP",
        },
        None,
        {
            "strategy": "BALANCED",
            "action": "MAINTAIN_BALANCE",
            "confidence": 50,
            "score": 0,
            "direction": "UP",
            "stability": "UNKNOWN",
            "momentum": "NEUTRAL",
            "grade_stability": "UNKNOWN",
            "consistency": "UNKNOWN",
            "outcome_learning_signal": "NONE",
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        },
    ),
    (
        "CASE 4 PARTIAL OUTCOME",
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
        },
        {
            "strategy": "MAINTAIN",
            "action": "MAINTAIN_ALLOCATION",
            "confidence": 100,
            "score": 85,
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "outcome_learning_signal": "NEGATIVE",
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        },
    ),
]


for name, trend, outcome, expected in CASES:
    result = ENGINE.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    for key, value in expected.items():
        assert result[key] == value, (
            f"{name}: {key}: "
            f"expected={value!r}, "
            f"actual={result[key]!r}"
        )

    print(
        f"{name}: PASS | "
        f"{result['strategy']} -> {result['action']} | "
        f"signal={result['outcome_learning_signal']} | "
        f"strength={result['outcome_learning_signal_strength']} | "
        f"adaptive={result['adaptive_learning_required']}"
    )


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
