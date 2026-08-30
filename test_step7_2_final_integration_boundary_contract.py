from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy

print("=" * 60)
print("PHASE 7-2-20 FINAL INTEGRATION BOUNDARY CONTRACT")
print("=" * 60)

engine = AIDecisionAdaptiveStrategy()

trend = {
    "direction": "UP",
    "stability": "HIGH",
    "momentum": "POSITIVE",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 92,
}

outcome = {
    "outcome_learning_signal": "NEGATIVE",
    "outcome_learning_signal_strength": 1.0,
    "adaptive_learning_required": True,
}

result = engine.analyze(trend, outcome)

required = {
    "strategy": "DEFENSIVE",
    "action": "REDUCE_RISK",
    "confidence": 100,
    "score": 92,
    "direction": "UP",
    "stability": "HIGH",
    "momentum": "POSITIVE",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "outcome_learning_signal": "NEGATIVE",
    "outcome_learning_signal_strength": 1.0,
    "adaptive_learning_required": True,
}

expected_summary = (
    "Adaptive strategy is DEFENSIVE. "
    "Recommended action is REDUCE_RISK. "
    "AI decision direction is UP, momentum is POSITIVE, "
    "and stability is high."
)

assert len(result) == 13

for key, expected in required.items():
    assert result[key] == expected, (
        f"{key}: expected {expected!r}, got {result[key]!r}"
    )

assert result["summary"] == expected_summary

print(
    "FINAL INTEGRATION: PASS | "
    f"{result['strategy']} -> {result['action']} | "
    f"confidence={result['confidence']} | "
    f"signal={result['outcome_learning_signal']} | "
    f"adaptive={result['adaptive_learning_required']}"
)

print("OUTPUT FIELD COUNT: PASS | 13")
print("SUMMARY CONSISTENCY: PASS")
print()
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
