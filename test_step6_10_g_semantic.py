from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy


engine = AIDecisionAdaptiveStrategy()


CASES = [
    {
        "name": "CASE 1 NEGATIVE",
        "trend": {
            "direction": "DOWN",
            "stability": "HIGH",
            "momentum": "NEGATIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 70,
        },
        "outcome": {
            "outcome_status": "EVALUATED",
            "outcome_learning_signal": "NEGATIVE",
            "outcome_learning_signal_strength": 100.0,
            "adaptive_learning_required": True,
        },
        "expected_strategy": "DEFENSIVE",
        "expected_action": "REDUCE_RISK",
        "expected_signal": "NEGATIVE",
        "expected_learning_required": True,
    },
    {
        "name": "CASE 2 POSITIVE",
        "trend": {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        },
        "outcome": {
            "outcome_status": "EVALUATED",
            "outcome_learning_signal": "POSITIVE",
            "outcome_learning_signal_strength": 100.0,
            "adaptive_learning_required": False,
        },
        "expected_strategy": "MAINTAIN",
        "expected_action": "MAINTAIN_ALLOCATION",
        "expected_signal": "POSITIVE",
        "expected_learning_required": False,
    },
    {
        "name": "CASE 3 PENDING",
        "trend": {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        },
        "outcome": {
            "outcome_status": "PENDING",
            "outcome_learning_signal": "NONE",
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        },
        "expected_strategy": "MAINTAIN",
        "expected_action": "MAINTAIN_ALLOCATION",
        "expected_signal": "NONE",
        "expected_learning_required": False,
    },
]


all_pass = True

print("=" * 60)
print("Step6-10-G Adaptive Strategy Semantic Regression Test")
print("=" * 60)

for case in CASES:
    result = engine.analyze(
        case["trend"],
        outcome_intelligence=case["outcome"],
    )

    strategy_pass = (
        result["strategy"] == case["expected_strategy"]
    )

    action_pass = (
        result["action"] == case["expected_action"]
    )

    signal_pass = (
        result["outcome_learning_signal"]
        == case["expected_signal"]
    )

    learning_pass = (
        result["adaptive_learning_required"]
        == case["expected_learning_required"]
    )

    case_pass = (
        strategy_pass
        and action_pass
        and signal_pass
        and learning_pass
    )

    all_pass = all_pass and case_pass

    print("")
    print(case["name"])
    print("-" * 40)
    print("Expected strategy :", case["expected_strategy"])
    print("Actual strategy   :", result["strategy"])
    print("Expected action   :", case["expected_action"])
    print("Actual action     :", result["action"])
    print("Learning signal   :", result["outcome_learning_signal"])
    print(
        "Adaptive required:",
        result["adaptive_learning_required"],
    )
    print("RESULT            :", "PASS" if case_pass else "FAIL")


print("")
print("=" * 60)
print("OVERALL RESULT:", "PASS" if all_pass else "FAIL")
print("=" * 60)

if not all_pass:
    raise AssertionError(
        "Step6-10-G semantic contract regression failed."
    )
