from core.ai_decision_outcome_collector import (
    AIDecisionOutcomeDataCollector
)


engine = AIDecisionOutcomeDataCollector()


print("=" * 60)
print(
    "Step6-10-G Outcome Collector Semantic Regression Test"
)
print("=" * 60)


# CASE 1 - COMPLETE INPUT
result = engine.collect(
    final_decision={
        "decision": "MAINTAIN",
        "action": "MAINTAIN_ALLOCATION",
        "strategy": "BALANCED",
        "market_view": "NEUTRAL",
        "risk_level": "MEDIUM",
        "validation_score": 95.0,
    },
    final_decision_certification={
        "certification_score": 99.0,
        "certification_status": "CERTIFIED",
        "certification_risk": "LOW",
    },
    final_execution_decision={
        "execution_score": 98.0,
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
    },
    final_decision_governance={
        "governance_score": 97.0,
        "governance_status": "MASTER_READY",
    },
    final_decision_lifecycle={
        "lifecycle_score": 96.0,
    },
    final_decision_operational_intelligence={
        "operational_score": 94.0,
    },
    final_decision_orchestration={
        "orchestration_score": 93.0,
    },
    final_decision_integrated_intelligence={
        "integrated_score": 92.0,
    },
    final_decision_execution_monitoring={
        "monitoring_status": "MONITORING",
    },
    final_decision_execution_feedback={
        "feedback_status": "HEALTHY",
    },
    final_decision_execution_reassessment={
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
    },
    intelligence={
        "market_view": "NEUTRAL",
    },
    intelligence_score={
        "intelligence_score": 91.0,
    },
    decision_confidence={
        "confidence_score": 90.0,
    },
)

assert result["snapshot_status"] == "COLLECTED"
assert result["outcome_status"] == "PENDING"
assert result["snapshot_purpose"] == "FUTURE_OUTCOME_EVALUATION"
assert result["decision"] == "MAINTAIN"
assert result["action"] == "MAINTAIN_ALLOCATION"
assert result["strategy"] == "BALANCED"
assert result["market_view"] == "NEUTRAL"
assert result["risk_level"] == "MEDIUM"
assert result["confidence_score"] == 90.0
assert result["intelligence_score"] == 91.0
assert result["validation_score"] == 95.0
assert result["certification_score"] == 99.0
assert result["execution_score"] == 98.0
assert result["governance_score"] == 97.0
assert result["lifecycle_score"] == 96.0
assert result["operational_score"] == 94.0
assert result["orchestration_score"] == 93.0
assert result["integrated_score"] == 92.0
assert result["execution_status"] == "EXECUTION_READY"
assert result["execution_authorization"] == "AUTHORIZED"
assert result["certification_status"] == "CERTIFIED"
assert result["governance_status"] == "MASTER_READY"
assert result["monitoring_status"] == "MONITORING"
assert result["feedback_status"] == "HEALTHY"
assert result["reassessment_required"] is False
assert result["reassessment_status"] == "NOT_REQUIRED"

print("CASE 1 COMPLETE INPUT: PASS")


# CASE 2 - EMPTY INPUT
result = engine.collect()

assert result["snapshot_status"] == "COLLECTED"
assert result["outcome_status"] == "PENDING"
assert result["snapshot_purpose"] == "FUTURE_OUTCOME_EVALUATION"
assert result["decision"] == "UNKNOWN"
assert result["action"] == "REVIEW"
assert result["strategy"] == "UNKNOWN"
assert result["market_view"] == "UNKNOWN"
assert result["risk_level"] == "UNKNOWN"
assert result["execution_status"] == "UNKNOWN"
assert result["execution_authorization"] == "UNKNOWN"
assert result["certification_status"] == "UNKNOWN"
assert result["governance_status"] == "UNKNOWN"
assert result["monitoring_status"] == "UNKNOWN"
assert result["feedback_status"] == "UNKNOWN"
assert result["reassessment_status"] == "UNKNOWN"
assert result["reassessment_required"] is False

print("CASE 2 EMPTY INPUT: PASS")


# CASE 3 - REASSESSMENT INPUT
result = engine.collect(
    final_decision={
        "decision": "REVIEW",
        "action": "REASSESS",
        "strategy": "DEFENSIVE",
    },
    final_decision_execution_reassessment={
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
    },
)

assert result["snapshot_status"] == "COLLECTED"
assert result["outcome_status"] == "PENDING"
assert result["decision"] == "REVIEW"
assert result["action"] == "REASSESS"
assert result["strategy"] == "DEFENSIVE"
assert result["reassessment_required"] is True
assert result["reassessment_status"] == "REASSESSMENT_REQUIRED"

print("CASE 3 REASSESSMENT INPUT: PASS")


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
