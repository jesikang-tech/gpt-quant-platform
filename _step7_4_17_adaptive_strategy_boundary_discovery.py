from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy
from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence
import inspect

print("===== PHASE 7-4-17 DISCOVERY 2 RETRY =====")
print("===== OUTCOME INTELLIGENCE → ADAPTIVE STRATEGY =====")

print("")
print("===== ADAPTIVE STRATEGY SIGNATURE =====")
print(inspect.signature(AIDecisionAdaptiveStrategy.analyze))

print("")
print("===== OUTCOME INTELLIGENCE SIGNATURE =====")
print(inspect.signature(AIDecisionOutcomeIntelligence.analyze))

evaluation = {
    "evaluation_status": "WAITING_FOR_OUTCOME",
    "outcome_status": "PENDING",
    "outcome_score": 0.0,
    "outcome_grade": "N/A",
    "decision_effectiveness": "PENDING",
    "strategy_effectiveness": "PENDING",
    "market_response": "PENDING",
    "portfolio_response": "PENDING",
    "learning_status": "WAITING_FOR_OUTCOME",
    "learning_signal": "NONE",
    "learning_signal_strength": 0.0,
    "actual_outcome_available": False,
    "decision": "MAINTAIN",
    "action": "PROCEED",
    "strategy": "MAINTAIN",
    "snapshot_status": "COLLECTED",
    "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
}

final_decision = {
    "decision": "MAINTAIN",
    "action": "PROCEED",
}

master_control = {
    "master_control_status": "MASTER_READY",
    "master_control_action": "PROCEED",
    "master_control_risk": "LOW",
}

certification = {
    "certification_status": "CERTIFIED",
}

execution_decision = {
    "execution_status": "EXECUTION_READY",
    "execution_authorization": "AUTHORIZED",
}

execution_feedback = {
    "feedback_status": "STABLE",
}

execution_monitoring = {
    "monitoring_status": "STANDARD_MONITORING",
}

execution_reassessment = {
    "reassessment_status": "NOT_REQUIRED",
    "reassessment_required": False,
}

intelligence = {
    "intelligence_score": 88.0,
    "confidence_score": 90.0,
}

print("")
print("===== PENDING OUTCOME INTELLIGENCE =====")

outcome_engine = AIDecisionOutcomeIntelligence()

outcome = outcome_engine.analyze(
    final_decision=final_decision,
    final_decision_master_control=master_control,
    final_decision_certification=certification,
    final_execution_decision=execution_decision,
    final_decision_execution_feedback=execution_feedback,
    final_decision_execution_monitoring=execution_monitoring,
    final_decision_execution_reassessment=execution_reassessment,
    intelligence=intelligence,
    outcome_evaluation=evaluation,
)

print(outcome)

print("")
print("===== ADAPTIVE STRATEGY WITH PENDING OUTCOME =====")

trend = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}

strategy_engine = AIDecisionAdaptiveStrategy()

adaptive = strategy_engine.analyze(
    trend=trend,
    outcome_intelligence=outcome,
)

print(adaptive)

print("")
print("===== SEMANTIC ASSERTIONS =====")

assert outcome.get("outcome_status") == "PENDING"
print("outcome_status: PASS")

assert outcome.get("outcome_learning_status") == "WAITING_FOR_OUTCOME"
print("outcome_learning_status: PASS")

assert outcome.get("outcome_learning_signal") == "NONE"
print("outcome_learning_signal: PASS")

assert float(outcome.get("outcome_learning_signal_strength", -1)) == 0.0
print("outcome_learning_signal_strength: PASS")

assert outcome.get("adaptive_learning_required") is False
print("outcome adaptive_learning_required: PASS")

assert adaptive.get("outcome_learning_signal") == "NONE"
print("adaptive outcome_learning_signal: PASS")

assert float(adaptive.get("outcome_learning_signal_strength", -1)) == 0.0
print("adaptive outcome_learning_signal_strength: PASS")

assert adaptive.get("adaptive_learning_required") is False
print("adaptive adaptive_learning_required: PASS")

assert adaptive.get("strategy") == "MAINTAIN"
print("strategy preservation: PASS")

assert adaptive.get("action") == "MAINTAIN_ALLOCATION"
print("action preservation: PASS")

print("")
print("===== PHASE 7-4-17 DISCOVERY 2 COMPLETE =====")
