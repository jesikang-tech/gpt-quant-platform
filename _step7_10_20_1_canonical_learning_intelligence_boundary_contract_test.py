from core.ai_decision_outcome_evaluation import AIDecisionOutcomeEvaluation
from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def evaluate(score):
    engine = AIDecisionOutcomeEvaluation()

    portfolio_return = (
        float(score) - 50.0
    ) / 5.0

    return engine.evaluate(
        outcome_snapshot={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "strategy": "BALANCED",
            "snapshot_status": "COLLECTED",
            "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
        },
        actual_outcome={
            "portfolio_return": portfolio_return,
            "market_response": "EVALUATED",
            "portfolio_response": "EVALUATED",
        },
    )


def intelligence(evaluation, reassessment_required=False):
    engine = AIDecisionOutcomeIntelligence()

    return engine.analyze(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "strategy": "BALANCED",
        },
        final_decision_execution_reassessment={
            "reassessment_required": reassessment_required,
            "reassessment_status": (
                "REASSESSMENT_REQUIRED"
                if reassessment_required
                else "NOT_REQUIRED"
            ),
        },
        intelligence={},
        intelligence_score={
            "intelligence_score": 90.0
        },
        decision_confidence={
            "confidence_score": 90.0
        },
        outcome_evaluation=evaluation,
    )


print("=" * 82)
print("PHASE 7-10-20-1")
print("CANONICAL LEARNING -> OUTCOME INTELLIGENCE BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: POSITIVE OUTCOME -> CANONICAL POSITIVE -> LEARNING AVAILABLE")
print("=" * 82)

positive_evaluation = evaluate(100.0)
positive_intelligence = intelligence(
    positive_evaluation,
    reassessment_required=False,
)

assert_equal(
    positive_evaluation["learning_signal"],
    "POSITIVE",
    "POSITIVE -> canonical learning signal",
)

assert_equal(
    positive_evaluation["learning_signal_strength"],
    100.0,
    "POSITIVE -> canonical learning strength",
)

assert_equal(
    positive_intelligence["outcome_learning_signal"],
    positive_evaluation["learning_signal"],
    "POSITIVE -> intelligence signal propagation",
)

assert_equal(
    positive_intelligence["outcome_learning_signal_strength"],
    positive_evaluation["learning_signal_strength"],
    "POSITIVE -> intelligence strength propagation",
)

assert_equal(
    positive_intelligence["learning_status"],
    "LEARNING_AVAILABLE",
    "POSITIVE -> learning status",
)

assert_equal(
    positive_intelligence["feedback_state"],
    "LEARNING_AVAILABLE",
    "POSITIVE -> feedback state",
)

assert_equal(
    positive_intelligence["adaptive_learning_required"],
    False,
    "POSITIVE -> no adaptive learning requirement",
)


print("")
print("=" * 82)
print("CASE: STABLE UPPER BOUND -> CANONICAL STABLE -> LEARNING AVAILABLE")
print("=" * 82)

stable_upper_evaluation = evaluate(79.9)
stable_upper_intelligence = intelligence(
    stable_upper_evaluation,
    reassessment_required=False,
)

assert_equal(
    stable_upper_evaluation["learning_signal"],
    "STABLE",
    "79.9 -> canonical stable signal",
)

assert_equal(
    stable_upper_evaluation["learning_signal_strength"],
    59.8,
    "79.9 -> canonical stable strength",
)

assert_equal(
    stable_upper_intelligence["outcome_learning_signal"],
    "STABLE",
    "79.9 -> intelligence stable propagation",
)

assert_equal(
    stable_upper_intelligence["learning_status"],
    "LEARNING_AVAILABLE",
    "79.9 -> learning status",
)


print("")
print("=" * 82)
print("CASE: STABLE LOWER BOUND -> CANONICAL STABLE -> LEARNING AVAILABLE")
print("=" * 82)

stable_lower_evaluation = evaluate(60.0)
stable_lower_intelligence = intelligence(
    stable_lower_evaluation,
    reassessment_required=False,
)

assert_equal(
    stable_lower_evaluation["learning_signal"],
    "STABLE",
    "60.0 -> canonical stable signal",
)

assert_equal(
    stable_lower_evaluation["learning_signal_strength"],
    20.0,
    "60.0 -> canonical stable strength",
)

assert_equal(
    stable_lower_intelligence["outcome_learning_signal"],
    "STABLE",
    "60.0 -> intelligence stable propagation",
)

assert_equal(
    stable_lower_intelligence["learning_status"],
    "LEARNING_AVAILABLE",
    "60.0 -> learning status",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE OUTCOME -> CANONICAL NEGATIVE -> ADAPTIVE LEARNING")
print("=" * 82)

negative_evaluation = evaluate(0.0)
negative_intelligence = intelligence(
    negative_evaluation,
    reassessment_required=False,
)

assert_equal(
    negative_evaluation["learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> canonical learning signal",
)

assert_equal(
    negative_evaluation["learning_signal_strength"],
    100.0,
    "NEGATIVE -> canonical learning strength",
)

assert_equal(
    negative_intelligence["outcome_learning_signal"],
    negative_evaluation["learning_signal"],
    "NEGATIVE -> intelligence signal propagation",
)

assert_equal(
    negative_intelligence["outcome_learning_signal_strength"],
    negative_evaluation["learning_signal_strength"],
    "NEGATIVE -> intelligence strength propagation",
)

assert_equal(
    negative_intelligence["learning_status"],
    "ADAPTIVE_LEARNING_REQUIRED",
    "NEGATIVE -> adaptive learning status",
)

assert_equal(
    negative_intelligence["feedback_state"],
    "ADAPTIVE_LEARNING",
    "NEGATIVE -> adaptive feedback state",
)

assert_equal(
    negative_intelligence["adaptive_learning_required"],
    True,
    "NEGATIVE -> adaptive learning requirement",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-1 CANONICAL LEARNING INTELLIGENCE BOUNDARY COMPLETE =====")
print("=" * 82)
