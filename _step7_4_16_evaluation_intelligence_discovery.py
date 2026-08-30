from core.ai_decision_outcome_evaluation import AIDecisionOutcomeEvaluation
from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence

print("===== PHASE 7-4-16 EVALUATION → INTELLIGENCE DISCOVERY 2 =====")

snapshot = {
    "snapshot_status": "COLLECTED",
    "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
    "outcome_status": "PENDING",
    "decision": "MAINTAIN",
    "action": "PROCEED",
    "strategy": "MAINTAIN",
    "market_view": "NEUTRAL",
    "risk_level": "LOW",
}

evaluation_engine = AIDecisionOutcomeEvaluation()

evaluation = evaluation_engine.evaluate(
    outcome_snapshot=snapshot,
    actual_outcome={}
)

print("")
print("===== OUTCOME EVALUATION =====")
print(evaluation)

intelligence_engine = AIDecisionOutcomeIntelligence()

intelligence = intelligence_engine.analyze(
    final_decision={
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "EXECUTION_READY",
    },
    final_decision_master_control={
        "master_control_status": "MASTER_READY",
        "execution_authorization": "AUTHORIZED",
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
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_required": False,
    },
    intelligence={
        "intelligence_score": 88.0,
    },
    intelligence_score={
        "intelligence_score": 88.0,
    },
    decision_confidence={
        "confidence_score": 90.0,
    },
    outcome_evaluation=evaluation,
)

print("")
print("===== OUTCOME INTELLIGENCE =====")
print(intelligence)

print("")
print("===== SEMANTIC BOUNDARY =====")

assert evaluation["evaluation_status"] == "WAITING_FOR_OUTCOME"
assert evaluation["outcome_status"] == "PENDING"
assert evaluation["learning_status"] == "WAITING_FOR_OUTCOME"
assert evaluation["learning_signal"] == "NONE"
assert evaluation["learning_signal_strength"] == 0.0
assert evaluation["actual_outcome_available"] is False

assert intelligence["outcome_status"] == "PENDING"
assert intelligence["outcome_learning_status"] == "WAITING_FOR_OUTCOME"
assert intelligence["outcome_learning_signal"] == "NONE"
assert intelligence["outcome_learning_signal_strength"] == 0.0
assert intelligence["learning_status"] == "WAITING_FOR_OUTCOME"
assert intelligence["feedback_state"] == "COLLECTING"
assert intelligence["adaptive_learning_required"] is False

print("evaluation boundary: PASS")
print("outcome_status propagation: PASS")
print("learning_status propagation: PASS")
print("learning_signal propagation: PASS")
print("learning_signal_strength propagation: PASS")
print("feedback_state: PASS")
print("adaptive_learning_required: PASS")

print("")
print("===== PHASE 7-4-16 DISCOVERY 2 COMPLETE =====")
