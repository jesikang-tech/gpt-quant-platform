from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy


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
        100,
        92,
        "NONE",
        0.0,
        False,
    ),
    (
        "CASE 2 MAINTAIN",
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
        100,
        85,
        "NONE",
        0.0,
        False,
    ),
    (
        "CASE 3 DEFENSIVE OVERRIDE",
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
        "NEGATIVE",
        1.0,
        True,
    ),
    (
        "CASE 4 EMPTY DEFAULT",
        {},
        {},
        "BALANCED",
        "MAINTAIN_BALANCE",
        50,
        0,
        "NONE",
        0.0,
        False,
    ),
    (
        "CASE 5 PARTIAL INPUT",
        {"direction": "UP"},
        {},
        "BALANCED",
        "MAINTAIN_BALANCE",
        50,
        0,
        "NONE",
        0.0,
        False,
    ),
]


def check_case(
    name,
    trend,
    outcome,
    expected_strategy,
    expected_action,
    expected_confidence,
    expected_score,
    expected_signal,
    expected_strength,
    expected_adaptive,
):
    result = ENGINE.analyze(
        trend,
        outcome_intelligence=outcome,
    )

    assert result["strategy"] == expected_strategy
    assert result["action"] == expected_action
    assert result["confidence"] == expected_confidence
    assert result["score"] == expected_score
    assert result["outcome_learning_signal"] == expected_signal
    assert result["outcome_learning_signal_strength"] == expected_strength
    assert result["adaptive_learning_required"] is expected_adaptive

    assert 0 <= result["confidence"] <= 100

    assert (
        result["strategy"],
        result["action"],
    ) in {
        ("GROWTH", "INCREASE_RISK"),
        ("DEFENSIVE", "REDUCE_RISK"),
        ("MAINTAIN", "MAINTAIN_ALLOCATION"),
        ("CAUTIOUS", "LIMIT_EXPOSURE"),
        ("MONITOR", "MONITOR_CLOSELY"),
        ("BALANCED", "MAINTAIN_BALANCE"),
    }

    assert result["summary"].startswith(
        f"Adaptive strategy is {result['strategy']}."
    )

    assert (
        f"Recommended action is {result['action']}."
        in result["summary"]
    )

    print(
        f"{name}: PASS | "
        f"{result['strategy']} -> {result['action']} | "
        f"confidence={result['confidence']} | "
        f"score={result['score']} | "
        f"signal={result['outcome_learning_signal']} | "
        f"adaptive={result['adaptive_learning_required']}"
    )


print("=" * 60)
print("PHASE 7-2-18 CANONICAL LIFECYCLE REGRESSION CONTRACT")
print("=" * 60)

for case in CASES:
    check_case(*case)

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
