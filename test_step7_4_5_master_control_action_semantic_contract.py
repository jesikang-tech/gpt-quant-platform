from core.ai_final_decision_master_control import AIFinalDecisionMasterControl

print("=" * 60)
print("PHASE 7-4-5 MASTER CONTROL ACTION SEMANTIC CONTRACT")
print("=" * 60)

engine = AIFinalDecisionMasterControl()

base_final = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
}

base_execution = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "execution_status": "EXECUTION_READY",
    "execution_authorization": "AUTHORIZED",
}

base_governance = {
    "governance_status": "APPROVED",
    "governance_score": 98.7,
}

base_lifecycle = {
    "lifecycle_status": "HEALTHY",
    "lifecycle_score": 95.0,
    "reassessment_required": False,
}

base_operational = {
    "operational_status": "OPERATIONALLY_HEALTHY",
    "operational_score": 95.0,
}

base_orchestration = {
    "orchestration_status": "ORCHESTRATION_READY",
    "orchestration_score": 95.0,
}

base_integrated = {
    "integrated_status": "INTEGRATED_HEALTHY",
    "integrated_score": 95.0,
}

base_validation = {
    "validation_status": "VALID",
    "validation_score": 100.0,
}

print()
print("=== CASE A: CERTIFICATION REVIEW ===")

review_certification = {
    "decision": "ACCUMULATE",
    "certification_action": "PROCEED",
    "certification_status": "CERTIFICATION_REVIEW",
    "certification_risk": "MEDIUM",
    "execution_status": "EXECUTION_READY",
    "execution_authorization": "AUTHORIZED",
    "execution_readiness": "READY",
    "decision_integrity": "INTACT",
    "certification_score": 81.2,
}

review = engine.analyze(
    base_final,
    review_certification,
    base_execution,
    base_governance,
    base_lifecycle,
    base_operational,
    base_orchestration,
    base_integrated,
    base_validation,
)

print("action:", review["action"])
print("master_control_status:", review["master_control_status"])
print("master_control_action:", review["master_control_action"])
print("execution_control:", review["execution_control"])

review_checks = {
    "upstream action preserved": review["action"] == "PROCEED",
    "master review": review["master_control_status"] == "MASTER_REVIEW",
    "master action review": review["master_control_action"] == "REVIEW",
    "execution hold": review["execution_control"] == "HOLD",
}

for name, result in review_checks.items():
    print(f"{name}: {'PASS' if result else 'FAIL'}")

print()
print("=== CASE B: MASTER READY ===")

ready_certification = {
    "decision": "ACCUMULATE",
    "certification_action": "PROCEED",
    "certification_status": "CERTIFIED",
    "certification_risk": "LOW",
    "execution_status": "EXECUTION_READY",
    "execution_authorization": "AUTHORIZED",
    "execution_readiness": "READY",
    "decision_integrity": "INTACT",
    "certification_score": 98.0,
}

ready = engine.analyze(
    base_final,
    ready_certification,
    base_execution,
    base_governance,
    base_lifecycle,
    base_operational,
    base_orchestration,
    base_integrated,
    base_validation,
)

print("action:", ready["action"])
print("master_control_status:", ready["master_control_status"])
print("master_control_action:", ready["master_control_action"])
print("execution_control:", ready["execution_control"])

ready_checks = {
    "upstream action preserved": ready["action"] == "PROCEED",
    "master ready": ready["master_control_status"] == "MASTER_READY",
    "master action proceed": ready["master_control_action"] == "PROCEED",
    "execution execute": ready["execution_control"] == "EXECUTE",
}

for name, result in ready_checks.items():
    print(f"{name}: {'PASS' if result else 'FAIL'}")

all_checks = list(review_checks.values()) + list(ready_checks.values())

print()
print("OVERALL RESULT:", "PASS" if all(all_checks) else "FAIL")
print("=" * 60)
