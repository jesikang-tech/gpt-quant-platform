from core.ai_decision_outcome_evaluation import AIDecisionOutcomeEvaluation
from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence

print("===== PHASE 7-4-16 EVALUATION → INTELLIGENCE SEMANTIC CONTRACT =====")

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

evaluation = AIDecisionOutcomeEvaluation().evaluate(
    outcome_snapshot=snapshot,
    actual_outcome={}
)

intelligence = AIDecisionOutcomeIntelligence().analyze(
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
print("===== EVALUATION =====")
print(evaluation)

print("")
print("===== OUTCOME INTELLIGENCE =====")
print(intelligence)

print("")
print("===== CONTRACT ASSERTIONS =====")

assert evaluation["evaluation_status"] == "WAITING_FOR_OUTCOME"
assert evaluation["outcome_status"] == "PENDING"
assert evaluation["outcome_score"] == 0.0
assert evaluation["learning_status"] == "WAITING_FOR_OUTCOME"
assert evaluation["learning_signal"] == "NONE"
assert evaluation["learning_signal_strength"] == 0.0
assert evaluation["actual_outcome_available"] is False

assert intelligence["outcome_status"] == evaluation["outcome_status"]
assert intelligence["outcome_score"] == evaluation["outcome_score"]
assert intelligence["outcome_learning_status"] == evaluation["learning_status"]
assert intelligence["outcome_learning_signal"] == evaluation["learning_signal"]
assert intelligence["outcome_learning_signal_strength"] == evaluation["learning_signal_strength"]

assert intelligence["decision_effectiveness"] == "PENDING"
assert intelligence["strategy_effectiveness"] == "PENDING"
assert intelligence["market_response"] == "PENDING"
assert intelligence["portfolio_response"] == "PENDING"

assert intelligence["learning_status"] == "WAITING_FOR_OUTCOME"
assert intelligence["feedback_state"] == "COLLECTING"
assert intelligence["adaptive_learning_required"] is False

print("evaluation → outcome_status: PASS")
print("evaluation → outcome_score: PASS")
print("evaluation → learning_status: PASS")
print("evaluation → learning_signal: PASS")
print("evaluation → learning_signal_strength: PASS")
print("evaluation → effectiveness states: PASS")
print("evaluation → feedback_state: PASS")
print("adaptive learning boundary: PASS")

print("")
print("===== PHASE 7-4-16 SEMANTIC CONTRACT PASS =====")
