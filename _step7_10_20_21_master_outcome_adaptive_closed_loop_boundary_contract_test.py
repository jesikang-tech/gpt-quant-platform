from core.ai_decision_outcome_evaluation import AIDecisionOutcomeEvaluation
from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence
from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def evaluate(portfolio_return):
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
            "portfolio_return": portfolio_return,
            "market_response": "EVALUATED",
            "portfolio_response": "EVALUATED",
        },
    )


def intelligence(
    evaluation,
    master_control_status="MASTER_READY",
    execution_status="EXECUTION_READY",
    execution_authorization="AUTHORIZED",
):
    engine = AIDecisionOutcomeIntelligence()

    return engine.analyze(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "strategy": "BALANCED",
        },
        final_decision_master_control={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "master_control_status": master_control_status,
            "execution_status": execution_status,
            "execution_authorization": execution_authorization,
        },
        final_decision_certification={
            "certification_status": "CERTIFIED",
        },
        final_execution_decision={
            "execution_status": execution_status,
            "execution_authorization": execution_authorization,
        },
        final_decision_execution_feedback={
            "feedback_status": "STABLE",
        },
        final_decision_execution_monitoring={
            "monitoring_status": "STANDARD_MONITORING",
        },
        final_decision_execution_reassessment={
            "reassessment_required": False,
            "reassessment_status": "NOT_REQUIRED",
        },
        intelligence_score={
            "intelligence_score": 90.0,
        },
        decision_confidence={
            "confidence_score": 90.0,
        },
        outcome_evaluation=evaluation,
    )


def adaptive(outcome_intelligence, trend):
    engine = AIDecisionAdaptiveStrategy()
    return engine.analyze(
        trend,
        outcome_intelligence,
    )


print("=" * 82)
print("PHASE 7-10-20-21")
print("MASTER CONTROL -> OUTCOME INTELLIGENCE -> ADAPTIVE STRATEGY")
print("CLOSED PROPAGATION BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


stable_trend = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}

balanced_trend = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "MEDIUM",
    "latest_score": 85,
}


print("")
print("=" * 82)
print("CASE: MASTER READY + NO OUTCOME -> WAITING / NO ADAPTIVE LEARNING")
print("=" * 82)

pending = intelligence(
    {
        "outcome_status": "PENDING",
        "learning_signal": "NONE",
        "learning_signal_strength": 0.0,
    }
)

assert_equal(
    pending["master_control_status"],
    "MASTER_READY",
    "master ready -> intelligence master status",
)

assert_equal(
    pending["learning_status"],
    "WAITING_FOR_OUTCOME",
    "master ready -> waiting for outcome",
)

assert_equal(
    pending["feedback_state"],
    "COLLECTING",
    "master ready -> collecting feedback",
)

assert_equal(
    pending["adaptive_learning_required"],
    False,
    "master ready -> no adaptive learning",
)

pending_strategy = adaptive(
    pending,
    stable_trend,
)

assert_equal(
    pending_strategy["strategy"],
    "MAINTAIN",
    "pending -> base strategy preserved",
)


print("")
print("=" * 82)
print("CASE: EVALUATED POSITIVE -> LEARNING AVAILABLE -> ADAPTIVE STRATEGY")
print("=" * 82)

positive_evaluation = evaluate(50.0)
positive = intelligence(
    positive_evaluation,
)

assert_equal(
    positive["outcome_status"],
    "EVALUATED",
    "positive -> evaluated status",
)

assert_equal(
    positive["outcome_learning_signal"],
    "POSITIVE",
    "positive -> intelligence signal",
)

assert_equal(
    positive["learning_status"],
    "LEARNING_AVAILABLE",
    "positive -> learning available",
)

assert_equal(
    positive["adaptive_learning_required"],
    False,
    "positive -> no adaptive learning",
)

positive_strategy = adaptive(
    positive,
    balanced_trend,
)

assert_equal(
    positive_strategy["strategy"],
    "GROWTH",
    "positive -> adaptive growth",
)

assert_equal(
    positive_strategy["action"],
    "INCREASE_RISK",
    "positive -> increase risk",
)


print("")
print("=" * 82)
print("CASE: EVALUATED NEGATIVE -> ADAPTIVE LEARNING -> DEFENSIVE")
print("=" * 82)

negative_evaluation = evaluate(-50.0)
negative = intelligence(
    negative_evaluation,
)

assert_equal(
    negative["outcome_status"],
    "EVALUATED",
    "negative -> evaluated status",
)

assert_equal(
    negative["outcome_learning_signal"],
    "NEGATIVE",
    "negative -> intelligence signal",
)

assert_equal(
    negative["learning_status"],
    "ADAPTIVE_LEARNING_REQUIRED",
    "negative -> adaptive learning status",
)

assert_equal(
    negative["feedback_state"],
    "ADAPTIVE_LEARNING",
    "negative -> adaptive feedback",
)

assert_equal(
    negative["adaptive_learning_required"],
    True,
    "negative -> adaptive learning required",
)

negative_strategy = adaptive(
    negative,
    stable_trend,
)

assert_equal(
    negative_strategy["strategy"],
    "DEFENSIVE",
    "negative -> adaptive defensive",
)

assert_equal(
    negative_strategy["action"],
    "REDUCE_RISK",
    "negative -> reduce risk",
)


print("")
print("=" * 82)
print("CASE: MASTER BLOCKED + EVALUATED POSITIVE -> OUTCOME OVERRIDES CONTROL STATE")
print("=" * 82)

blocked_positive = intelligence(
    positive_evaluation,
    master_control_status="MASTER_BLOCKED",
    execution_status="EXECUTION_BLOCKED",
    execution_authorization="UNAUTHORIZED",
)

assert_equal(
    blocked_positive["master_control_status"],
    "MASTER_BLOCKED",
    "blocked master -> status preserved",
)

assert_equal(
    blocked_positive["outcome_status"],
    "EVALUATED",
    "blocked master + outcome -> evaluated preserved",
)

assert_equal(
    blocked_positive["outcome_learning_signal"],
    "POSITIVE",
    "blocked master + outcome -> positive signal",
)

assert_equal(
    blocked_positive["learning_status"],
    "LEARNING_AVAILABLE",
    "evaluated positive -> learning available",
)

blocked_positive_strategy = adaptive(
    blocked_positive,
    balanced_trend,
)

assert_equal(
    blocked_positive_strategy["strategy"],
    "GROWTH",
    "evaluated positive -> adaptive growth despite prior block",
)


print("")
print("=" * 82)
print("CASE: MASTER CONTROL DOES NOT FABRICATE LEARNING")
print("=" * 82)

master_only = intelligence(
    {
        "outcome_status": "PENDING",
    }
)

assert_equal(
    master_only["outcome_learning_signal"],
    "NONE",
    "master control -> no fabricated signal",
)

assert_equal(
    master_only["outcome_learning_signal_strength"],
    0.0,
    "master control -> no fabricated strength",
)

assert_equal(
    master_only["adaptive_learning_required"],
    False,
    "master control -> no fabricated adaptive requirement",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-21 MASTER -> OUTCOME -> ADAPTIVE COMPLETE =====")
print("=" * 82)
