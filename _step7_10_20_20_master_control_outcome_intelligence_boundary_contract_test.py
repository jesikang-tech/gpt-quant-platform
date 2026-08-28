from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def intelligence(
    master_status="MASTER_READY",
    execution_authorization="AUTHORIZED",
    certification_status="CERTIFIED",
    execution_status="EXECUTION_READY",
    outcome_evaluation=None,
):
    engine = AIDecisionOutcomeIntelligence()

    return engine.analyze(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
        },
        final_decision_master_control={
            "decision": "MAINTAIN",
            "master_control_status": master_status,
            "execution_authorization": execution_authorization,
            "execution_status": execution_status,
        },
        final_decision_certification={
            "certification_status": certification_status,
        },
        final_execution_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
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
            "reassessment_status": "NOT_REQUIRED",
            "reassessment_required": False,
        },
        intelligence_score={
            "intelligence_score": 90.0,
        },
        decision_confidence={
            "confidence_score": 90.0,
        },
        outcome_evaluation=outcome_evaluation,
    )


print("=" * 82)
print("PHASE 7-10-20-20")
print("MASTER CONTROL -> OUTCOME INTELLIGENCE")
print("PROPAGATION BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: MASTER READY -> WAITING FOR OUTCOME")
print("=" * 82)

result = intelligence()

assert_equal(
    result["master_control_status"],
    "MASTER_READY",
    "master ready -> status propagated",
)

assert_equal(
    result["learning_status"],
    "WAITING_FOR_OUTCOME",
    "master ready -> waiting for outcome",
)

assert_equal(
    result["feedback_state"],
    "COLLECTING",
    "master ready -> collecting feedback",
)

assert_equal(
    result["adaptive_learning_required"],
    False,
    "master ready -> no fabricated adaptive learning",
)


print("")
print("=" * 82)
print("CASE: MASTER REVIEW -> WAITING FOR OUTCOME")
print("=" * 82)

result = intelligence(
    master_status="MASTER_REVIEW",
)

assert_equal(
    result["master_control_status"],
    "MASTER_REVIEW",
    "master review -> status propagated",
)

assert_equal(
    result["learning_status"],
    "WAITING_FOR_OUTCOME",
    "master review -> waiting for outcome",
)

assert_equal(
    result["feedback_state"],
    "COLLECTING",
    "master review -> collecting feedback",
)


print("")
print("=" * 82)
print("CASE: MASTER BLOCKED -> BLOCKED LEARNING STATE")
print("=" * 82)

result = intelligence(
    master_status="MASTER_BLOCKED",
    execution_authorization="UNAUTHORIZED",
)

assert_equal(
    result["master_control_status"],
    "MASTER_BLOCKED",
    "master blocked -> status propagated",
)

assert_equal(
    result["learning_status"],
    "BLOCKED",
    "master blocked -> blocked learning",
)

assert_equal(
    result["feedback_state"],
    "BLOCKED",
    "master blocked -> blocked feedback",
)


print("")
print("=" * 82)
print("CASE: EVALUATED POSITIVE OUTCOME OVERRIDES MASTER BLOCK")
print("=" * 82)

result = intelligence(
    master_status="MASTER_BLOCKED",
    execution_authorization="UNAUTHORIZED",
    outcome_evaluation={
        "outcome_status": "EVALUATED",
        "outcome_score": 100.0,
        "outcome_grade": "A+",
        "learning_status": "LEARNING_AVAILABLE",
        "learning_signal": "POSITIVE",
        "learning_signal_strength": 100.0,
        "decision_effectiveness": "EFFECTIVE",
        "strategy_effectiveness": "EFFECTIVE",
        "market_response": "POSITIVE",
        "portfolio_response": "POSITIVE",
    },
)

assert_equal(
    result["outcome_status"],
    "EVALUATED",
    "evaluated outcome -> status propagated",
)

assert_equal(
    result["outcome_learning_signal"],
    "POSITIVE",
    "evaluated positive -> learning signal",
)

assert_equal(
    result["learning_status"],
    "LEARNING_AVAILABLE",
    "evaluated positive -> learning available",
)

assert_equal(
    result["feedback_state"],
    "LEARNING_AVAILABLE",
    "evaluated positive -> feedback available",
)

assert_equal(
    result["adaptive_learning_required"],
    False,
    "evaluated positive -> no adaptive learning",
)


print("")
print("=" * 82)
print("CASE: EVALUATED NEGATIVE OUTCOME OVERRIDES MASTER READY")
print("=" * 82)

result = intelligence(
    master_status="MASTER_READY",
    outcome_evaluation={
        "outcome_status": "EVALUATED",
        "outcome_score": 0.0,
        "outcome_grade": "F",
        "learning_status": "ADAPTIVE_LEARNING_REQUIRED",
        "learning_signal": "NEGATIVE",
        "learning_signal_strength": 100.0,
        "decision_effectiveness": "INEFFECTIVE",
        "strategy_effectiveness": "INEFFECTIVE",
        "market_response": "NEGATIVE",
        "portfolio_response": "NEGATIVE",
    },
)

assert_equal(
    result["outcome_status"],
    "EVALUATED",
    "evaluated negative -> status propagated",
)

assert_equal(
    result["outcome_learning_signal"],
    "NEGATIVE",
    "evaluated negative -> learning signal",
)

assert_equal(
    result["learning_status"],
    "ADAPTIVE_LEARNING_REQUIRED",
    "evaluated negative -> adaptive learning",
)

assert_equal(
    result["feedback_state"],
    "ADAPTIVE_LEARNING",
    "evaluated negative -> adaptive feedback",
)

assert_equal(
    result["adaptive_learning_required"],
    True,
    "evaluated negative -> adaptive learning required",
)


print("")
print("=" * 82)
print("CASE: MASTER CONTROL DOES NOT FABRICATE LEARNING FIELDS")
print("=" * 82)

result = intelligence(
    master_status="MASTER_REVIEW",
)

assert_equal(
    result["outcome_learning_signal"],
    "NONE",
    "master state -> no fabricated learning signal",
)

assert_equal(
    result["outcome_learning_signal_strength"],
    0.0,
    "master state -> no fabricated learning strength",
)

assert_equal(
    result["outcome_status"],
    "PENDING",
    "master state -> pending outcome",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-20 MASTER CONTROL -> OUTCOME INTELLIGENCE COMPLETE =====")
print("=" * 82)
