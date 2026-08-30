from core.ai_decision_outcome_evaluation import AIDecisionOutcomeEvaluation
from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def trend():
    return {
        "direction": "STABLE",
        "stability": "MEDIUM",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "MEDIUM",
        "latest_score": 85,
    }


def evaluate(score):
    engine = AIDecisionOutcomeEvaluation()

    return engine.evaluate(
        outcome_snapshot={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "strategy": "BALANCED",
            "snapshot_status": "COLLECTED",
            "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
        },
        actual_outcome={
            "portfolio_return": score,
            "market_response": "EVALUATED",
            "portfolio_response": "EVALUATED",
        },
    )


def adapt(evaluation):
    engine = AIDecisionAdaptiveStrategy()

    return engine.analyze(
        trend(),
        {
            "outcome_learning_signal":
                evaluation["learning_signal"],
            "outcome_learning_signal_strength":
                evaluation["learning_signal_strength"],
            "adaptive_learning_required":
                evaluation["learning_signal"] == "NEGATIVE",
        },
    )


print("=" * 82)
print("PHASE 7-10-20-2")
print("CANONICAL LEARNING -> ADAPTIVE STRATEGY BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

print("")
print("=" * 82)
print("CASE: POSITIVE CANONICAL LEARNING -> GROWTH")
print("=" * 82)

positive = evaluate(10.0)
positive_strategy = adapt(positive)

assert_equal(
    positive["learning_signal"],
    "POSITIVE",
    "POSITIVE -> canonical signal",
)

assert_equal(
    positive_strategy["strategy"],
    "GROWTH",
    "POSITIVE -> GROWTH",
)

assert_equal(
    positive_strategy["action"],
    "INCREASE_RISK",
    "POSITIVE -> INCREASE_RISK",
)


print("")
print("=" * 82)
print("CASE: STABLE CANONICAL LEARNING -> EXISTING STRATEGY")
print("=" * 82)

stable = evaluate(2.0)
stable_strategy = adapt(stable)

assert_equal(
    stable["learning_signal"],
    "STABLE",
    "STABLE -> canonical signal",
)

assert_equal(
    stable_strategy["strategy"],
    "BALANCED",
    "STABLE -> BALANCED",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE CANONICAL LEARNING -> DEFENSIVE")
print("=" * 82)

negative = evaluate(-10.0)
negative_strategy = adapt(negative)

assert_equal(
    negative["learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> canonical signal",
)

assert_equal(
    negative_strategy["strategy"],
    "DEFENSIVE",
    "NEGATIVE -> DEFENSIVE",
)

assert_equal(
    negative_strategy["action"],
    "REDUCE_RISK",
    "NEGATIVE -> REDUCE_RISK",
)

assert_equal(
    negative_strategy["adaptive_learning_required"],
    True,
    "NEGATIVE -> adaptive learning required",
)


print("")
print("=" * 82)
print("CASE: NONE SIGNAL -> EXISTING STRATEGY")
print("=" * 82)

none_engine = AIDecisionAdaptiveStrategy()

none_strategy = none_engine.analyze(
    trend(),
    {
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": False,
    },
)

assert_equal(
    none_strategy["strategy"],
    "BALANCED",
    "NONE -> BALANCED",
)

assert_equal(
    none_strategy["action"],
    "MAINTAIN_BALANCE",
    "NONE -> MAINTAIN_ALLOCATION",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-2 CANONICAL LEARNING ADAPTIVE STRATEGY BOUNDARY COMPLETE =====")
print("=" * 82)
