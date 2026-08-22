from core.ai_decision_outcome_evaluation import AIDecisionOutcomeEvaluation

print("===== PENDING SNAPSHOT → EVALUATION SEMANTIC DISCOVERY =====")

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

print("")
print("===== INPUT SNAPSHOT =====")
print(snapshot)

engine = AIDecisionOutcomeEvaluation()

result = engine.evaluate(
    outcome_snapshot=snapshot,
    actual_outcome={}
)

print("")
print("===== EVALUATION RESULT =====")
print(result)

print("")
print("===== SEMANTIC ASSERTIONS =====")

assert result.get("snapshot_status") == "COLLECTED"
print("snapshot_status: PASS")

assert result.get("snapshot_purpose") == "FUTURE_OUTCOME_EVALUATION"
print("snapshot_purpose: PASS")

assert result.get("outcome_status") == "PENDING"
print("outcome_status: PASS")

assert result.get("actual_outcome_available") is False
print("actual_outcome_available: PASS")

print("")
print("===== PHASE 7-4-15 DISCOVERY 2 COMPLETE =====")
