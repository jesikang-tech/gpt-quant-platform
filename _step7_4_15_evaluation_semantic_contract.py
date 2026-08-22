from core.ai_decision_outcome_evaluation import AIDecisionOutcomeEvaluation

print("===== PHASE 7-4-15 EVALUATION SEMANTIC CONTRACT =====")

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

engine = AIDecisionOutcomeEvaluation()

result = engine.evaluate(
    outcome_snapshot=snapshot,
    actual_outcome={}
)

print("")
print("===== PENDING EVALUATION RESULT =====")
print(result)

print("")
print("===== CONTRACT ASSERTIONS =====")

assert result["evaluation_status"] == "WAITING_FOR_OUTCOME"
print("evaluation_status: PASS")

assert result["outcome_status"] == "PENDING"
print("outcome_status: PASS")

assert result["outcome_score"] == 0.0
print("outcome_score: PASS")

assert result["outcome_grade"] == "N/A"
print("outcome_grade: PASS")

assert result["decision_effectiveness"] == "PENDING"
assert result["strategy_effectiveness"] == "PENDING"
assert result["market_response"] == "PENDING"
assert result["portfolio_response"] == "PENDING"
print("effectiveness / response states: PASS")

assert result["learning_status"] == "WAITING_FOR_OUTCOME"
print("learning_status: PASS")

assert result["learning_signal"] == "NONE"
print("learning_signal: PASS")

assert result["learning_signal_strength"] == 0.0
print("learning_signal_strength: PASS")

assert result["actual_outcome_available"] is False
print("actual_outcome_available: PASS")

assert result["snapshot_status"] == "COLLECTED"
assert result["snapshot_purpose"] == "FUTURE_OUTCOME_EVALUATION"
print("snapshot boundary: PASS")

print("")
print("===== PHASE 7-4-15 SEMANTIC CONTRACT PASS =====")
