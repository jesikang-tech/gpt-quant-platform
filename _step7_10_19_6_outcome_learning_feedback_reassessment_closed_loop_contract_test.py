"""
PHASE 7-10-19-6
OUTCOME LEARNING
->
ADAPTIVE STRATEGY
->
EXECUTION FEEDBACK
->
REASSESSMENT

CLOSED-LOOP BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_decision_outcome_evaluation import (
    AIDecisionOutcomeEvaluation,
)
from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence,
)
from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)
from core.ai_final_decision_execution_feedback import (
    AIFinalDecisionExecutionFeedback,
)
from core.ai_final_decision_reassessment import (
    AIFinalDecisionReassessment,
)


evaluation_engine = AIDecisionOutcomeEvaluation()
outcome_intelligence_engine = AIDecisionOutcomeIntelligence()
adaptive_strategy_engine = AIDecisionAdaptiveStrategy()
feedback_engine = AIFinalDecisionExecutionFeedback()
reassessment_engine = AIFinalDecisionReassessment()


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def evaluate_outcome(portfolio_return):
    return evaluation_engine.evaluate(
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


def build_outcome_intelligence(evaluation):
    return outcome_intelligence_engine.analyze(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
        },
        final_decision_master_control={
            "decision": "MAINTAIN",
            "master_control_action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "master_control_status": "MASTER_READY",
        },
        final_decision_certification={
            "certification_status": "CERTIFIED",
        },
        final_execution_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
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
        intelligence={
            "intelligence_score": 90.0,
        },
        intelligence_score={
            "intelligence_score": 90.0,
        },
        decision_confidence={
            "confidence_score": 90.0,
        },
        outcome_evaluation=evaluation,
    )


def build_adaptive_strategy(outcome_intelligence):
    return adaptive_strategy_engine.analyze(
        trend={
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 75,
        },
        outcome_intelligence=outcome_intelligence,
    )


def build_feedback(
    monitoring_status="STANDARD_MONITORING",
    monitoring_risk="LOW",
    monitoring_score=95.0,
    assurance_status="ASSURED",
    assurance_risk="LOW",
    assurance_score=95.0,
    control_status="AUTHORIZED",
    control_risk="LOW",
    governance_status="APPROVED",
    governance_score=95.0,
    validation_status="VALID",
    validation_score=95.0,
):
    return feedback_engine.feedback(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "validation_status": validation_status,
            "validation_score": validation_score,
        },
        governance={
            "governance_status": governance_status,
            "governance_score": governance_score,
        },
        execution_control={
            "control_status": control_status,
            "control_risk": control_risk,
        },
        execution_assurance={
            "assurance_status": assurance_status,
            "assurance_risk": assurance_risk,
            "assurance_score": assurance_score,
            "validation_status": validation_status,
            "validation_score": validation_score,
        },
        execution_monitoring={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "monitoring_status": monitoring_status,
            "monitoring_action": "CONTINUE",
            "monitoring_risk": monitoring_risk,
            "monitoring_score": monitoring_score,
            "assurance_status": assurance_status,
            "assurance_risk": assurance_risk,
            "assurance_score": assurance_score,
            "control_status": control_status,
            "control_risk": control_risk,
            "governance_status": governance_status,
            "governance_score": governance_score,
            "validation_status": validation_status,
            "validation_score": validation_score,
        },
    )


def build_reassessment(feedback):
    return reassessment_engine.reassess(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "validation_status": feedback["validation_status"],
            "validation_score": feedback["validation_score"],
        },
        governance={
            "governance_status": feedback["governance_status"],
            "governance_score": feedback["governance_score"],
        },
        execution_control={
            "control_status": feedback["control_status"],
            "control_risk": feedback["control_risk"],
        },
        execution_assurance={
            "assurance_status": feedback["assurance_status"],
            "assurance_risk": feedback["assurance_risk"],
            "assurance_score": feedback["assurance_score"],
            "validation_status": feedback["validation_status"],
            "validation_score": feedback["validation_score"],
        },
        execution_feedback=feedback,
        execution_monitoring={
            "monitoring_status": feedback["monitoring_status"],
            "monitoring_risk": feedback["monitoring_risk"],
            "monitoring_score": feedback["monitoring_score"],
        },
    )


print("=" * 82)
print("PHASE 7-10-19-6")
print("OUTCOME LEARNING")
print("-> ADAPTIVE STRATEGY")
print("-> EXECUTION FEEDBACK")
print("-> REASSESSMENT")
print("CLOSED-LOOP BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: POSITIVE OUTCOME -> GROWTH -> STABLE FEEDBACK")
print("=" * 82)

positive_evaluation = evaluate_outcome(10.0)
positive_intelligence = build_outcome_intelligence(
    positive_evaluation
)
positive_adaptive = build_adaptive_strategy(
    positive_intelligence
)
positive_feedback = build_feedback()
positive_reassessment = build_reassessment(
    positive_feedback
)

print("evaluation:", positive_evaluation)
print("outcome_intelligence:", positive_intelligence)
print("adaptive_strategy:", positive_adaptive)
print("feedback:", positive_feedback)
print("reassessment:", positive_reassessment)

assert_equal(
    positive_evaluation["learning_signal"],
    "POSITIVE",
    "POSITIVE -> evaluation signal",
)

assert_equal(
    positive_intelligence["learning_status"],
    "LEARNING_AVAILABLE",
    "POSITIVE -> learning available",
)

assert_equal(
    positive_intelligence["adaptive_learning_required"],
    False,
    "POSITIVE -> no adaptive learning requirement",
)

assert_equal(
    positive_adaptive["strategy"],
    "GROWTH",
    "POSITIVE -> GROWTH",
)

assert_equal(
    positive_adaptive["action"],
    "INCREASE_RISK",
    "POSITIVE -> INCREASE_RISK",
)

assert_equal(
    positive_feedback["feedback_status"],
    "STABLE",
    "POSITIVE -> stable feedback",
)

assert_equal(
    positive_feedback["feedback_action"],
    "CONTINUE",
    "POSITIVE -> feedback continue",
)

assert_equal(
    positive_feedback["reassessment_required"],
    False,
    "POSITIVE -> feedback no reassessment",
)

assert_equal(
    positive_reassessment["reassessment_required"],
    False,
    "POSITIVE -> reassessment not required",
)

assert_equal(
    positive_reassessment["reassessment_status"],
    "NOT_REQUIRED",
    "POSITIVE -> NOT_REQUIRED",
)

assert_equal(
    positive_reassessment["reassessment_action"],
    "CONTINUE",
    "POSITIVE -> reassessment continue",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE OUTCOME -> DEFENSIVE -> ATTENTION -> REASSESS")
print("=" * 82)

negative_evaluation = evaluate_outcome(-10.0)
negative_intelligence = build_outcome_intelligence(
    negative_evaluation
)
negative_adaptive = build_adaptive_strategy(
    negative_intelligence
)
negative_feedback = build_feedback(
    monitoring_status="STANDARD_MONITORING",
    monitoring_risk="HIGH",
    monitoring_score=85.0,
)
negative_reassessment = build_reassessment(
    negative_feedback
)

print("evaluation:", negative_evaluation)
print("outcome_intelligence:", negative_intelligence)
print("adaptive_strategy:", negative_adaptive)
print("feedback:", negative_feedback)
print("reassessment:", negative_reassessment)

assert_equal(
    negative_evaluation["learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> evaluation signal",
)

assert_equal(
    negative_intelligence["learning_status"],
    "ADAPTIVE_LEARNING_REQUIRED",
    "NEGATIVE -> adaptive learning required",
)

assert_equal(
    negative_intelligence["adaptive_learning_required"],
    True,
    "NEGATIVE -> adaptive requirement",
)

assert_equal(
    negative_adaptive["strategy"],
    "DEFENSIVE",
    "NEGATIVE -> DEFENSIVE",
)

assert_equal(
    negative_adaptive["action"],
    "REDUCE_RISK",
    "NEGATIVE -> REDUCE_RISK",
)

assert_equal(
    negative_feedback["feedback_status"],
    "REQUIRES_ATTENTION",
    "NEGATIVE -> attention feedback",
)

assert_equal(
    negative_feedback["feedback_action"],
    "ENHANCED_REVIEW",
    "NEGATIVE -> enhanced review",
)

assert_equal(
    negative_feedback["feedback_risk"],
    "HIGH",
    "NEGATIVE -> high feedback risk",
)

assert_equal(
    negative_feedback["reassessment_required"],
    True,
    "NEGATIVE -> feedback reassessment required",
)

assert_equal(
    negative_reassessment["reassessment_required"],
    True,
    "NEGATIVE -> reassessment required",
)

assert_equal(
    negative_reassessment["reassessment_status"],
    "REASSESSMENT_REQUIRED",
    "NEGATIVE -> REASSESSMENT_REQUIRED",
)

assert_equal(
    negative_reassessment["reassessment_action"],
    "REASSESS",
    "NEGATIVE -> REASSESS",
)

assert_equal(
    negative_reassessment["reassessment_risk"],
    "HIGH",
    "NEGATIVE -> HIGH reassessment risk",
)


print("")
print("=" * 82)
print("CASE: CRITICAL FEEDBACK -> HALT -> CRITICAL REASSESSMENT")
print("=" * 82)

critical_feedback = build_feedback(
    monitoring_status="CRITICAL_MONITORING",
    monitoring_risk="CRITICAL",
    monitoring_score=50.0,
    assurance_status="ASSURED",
    assurance_risk="CRITICAL",
    assurance_score=70.0,
    control_status="AUTHORIZED",
    control_risk="CRITICAL",
    governance_status="APPROVED",
    governance_score=90.0,
    validation_status="VALID",
    validation_score=90.0,
)

critical_reassessment = build_reassessment(
    critical_feedback
)

print("feedback:", critical_feedback)
print("reassessment:", critical_reassessment)

assert_equal(
    critical_feedback["feedback_status"],
    "CRITICAL",
    "CRITICAL -> feedback status",
)

assert_equal(
    critical_feedback["feedback_action"],
    "HALT",
    "CRITICAL -> HALT",
)

assert_equal(
    critical_feedback["feedback_risk"],
    "CRITICAL",
    "CRITICAL -> feedback risk",
)

assert_equal(
    critical_feedback["reassessment_required"],
    True,
    "CRITICAL -> feedback reassessment required",
)

assert_equal(
    critical_reassessment["reassessment_required"],
    True,
    "CRITICAL -> reassessment required",
)

assert_equal(
    critical_reassessment["reassessment_status"],
    "CRITICAL_REASSESSMENT",
    "CRITICAL -> CRITICAL_REASSESSMENT",
)

assert_equal(
    critical_reassessment["reassessment_action"],
    "HALT_AND_REASSESS",
    "CRITICAL -> HALT_AND_REASSESS",
)

assert_equal(
    critical_reassessment["reassessment_risk"],
    "CRITICAL",
    "CRITICAL -> CRITICAL risk",
)


print("")
print("=" * 82)
print("SAFETY")
print("=" * 82)
print("Memory-only execution: PASS")
print("No production DB access.")
print("No API runtime call.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")
print("Actual Outcome data exists only in memory test dictionaries.")

print("")
print("=" * 82)
print("===== PHASE 7-10-19-6 CLOSED-LOOP BOUNDARY COMPLETE =====")
print("=" * 82)
