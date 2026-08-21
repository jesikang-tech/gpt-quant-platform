from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy


ENGINE = AIDecisionAdaptiveStrategy()


CASES = [
    (
        "CASE 1 NORMAL",
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
        100,
        92,
    ),
    (
        "CASE 2 EMPTY",
        {},
        {},
        "BALANCED",
        "MAINTAIN_BALANCE",
        50,
        0,
    ),
    (
        "CASE 3 PARTIAL",
        {
            "direction": "UP",
        },
        {},
        "BALANCED",
        "MAINTAIN_BALANCE",
        50,
        0,
    ),
    (
        "CASE 4 OUTCOME DEFAULT",
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
        },
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
        100,
        85,
    ),
    (
        "CASE 5 NEGATIVE ADAPTIVE",
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
]


EXPECTED_FIELDS = {
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


def check_case(
    name,
    trend,
    outcome,
    expected_strategy,
    expected_action,
    expected_confidence,
    expected_score,
):
    result = ENGINE.analyze(
        trend,
        outcome_intelligence=outcome,
    )

    assert result["strategy"] == expected_strategy
    assert result["action"] == expected_action
    assert result["confidence"] == expected_confidence
    assert result["score"] == expected_score

    assert set(result.keys()) == set(EXPECTED_FIELDS.keys())

    for field, expected_type in EXPECTED_FIELDS.items():
        assert isinstance(result[field], expected_type), (
            f"{name}: {field} type mismatch: "
            f"{type(result[field]).__name__}"
        )

    assert 0 <= result["confidence"] <= 100
    assert isinstance(result["summary"], str)
    assert result["summary"]

    print(
        f"{name}: PASS | "
        f"{result['strategy']} -> {result['action']} | "
        f"confidence={result['confidence']} | "
        f"score={result['score']} | "
        f"fields={len(result)} | types=PASS"
    )


print("=" * 60)
print("PHASE 7-2-17 INPUT TYPE / VALUE BOUNDARY CONTRACT")
print("=" * 60)

for case in CASES:
    check_case(*case)

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
