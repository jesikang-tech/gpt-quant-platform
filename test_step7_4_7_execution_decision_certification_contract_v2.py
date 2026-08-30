from core.ai_final_execution_decision import AIFinalExecutionDecision
from core.ai_final_decision_certification import AIFinalDecisionCertification

print("=" * 60)
print("PHASE 7-4-7 EXECUTION DECISION -> CERTIFICATION CONTRACT V2")
print("=" * 60)

final_decision = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
}

execution_engine = AIFinalExecutionDecision()

execution_decision = execution_engine.analyze(
    final_decision,
    {
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_risk": "LOW",
        "orchestration_action": "PROCEED",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
        "orchestration_score": 90.0,
        "integrated_score": 90.0,
        "governance_score": 90.0,
        "lifecycle_score": 90.0,
        "operational_score": 90.0,
        "confidence_score": 90.0,
    },
    {
        "integrated_status": "INTEGRATED_HEALTHY",
        "integrated_score": 90.0,
    },
    {
        "lifecycle_status": "HEALTHY",
        "lifecycle_score": 90.0,
    },
    {
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_score": 90.0,
    },
)

print()
print("=== STEP 1 EXECUTION DECISION ===")

for key in [
    "decision",
    "action",
    "execution_decision",
    "execution_status",
    "execution_authorization",
    "reassessment_policy",
    "execution_risk",
    "execution_score",
    "execution_grade",
]:
    print(f"{key}: {execution_decision.get(key)}")

certification_engine = AIFinalDecisionCertification()

certification = certification_engine.analyze(
    final_decision,
    {
        "validation_status": "VALID",
        "validation_score": 100.0,
    },
    {
        "governance_status": "APPROVED",
        "governance_score": 98.0,
    },
    {
        "lifecycle_status": "HEALTHY",
        "lifecycle_score": 95.0,
    },
    {
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_score": 90.0,
    },
    {
        "integrated_status": "INTEGRATED_HEALTHY",
        "integrated_score": 90.0,
    },
    {
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_score": 90.0,
    },
    execution_decision,
)

print()
print("=== STEP 2 CERTIFICATION ===")

for key in [
    "decision",
    "action",
    "certification_action",
    "certification_status",
    "execution_status",
    "execution_authorization",
    "execution_readiness",
    "execution_score",
]:
    print(f"{key}: {certification.get(key)}")

checks = {
    "decision propagation":
        certification.get("decision")
        == execution_decision.get("decision"),

    "action preserved":
        certification.get("action")
        == execution_decision.get("action"),

    "execution decision ready":
        execution_decision.get("execution_status")
        == "EXECUTION_READY",

    "execution decision proceed":
        execution_decision.get("execution_decision")
        == "PROCEED",

    "execution authorization":
        execution_decision.get("execution_authorization")
        == "AUTHORIZED",

    "reassessment policy":
        execution_decision.get("reassessment_policy")
        == "NOT_REQUIRED",

    "execution risk":
        execution_decision.get("execution_risk")
        == "LOW",

    "execution score propagation":
        certification.get("execution_score")
        == execution_decision.get("execution_score"),

    "certification status":
        certification.get("certification_status")
        == "CERTIFIED",

    "certification readiness":
        certification.get("execution_readiness")
        == "READY",

    "certification action":
        certification.get("certification_action")
        == "PROCEED",
}

print()
print("=== V2 SEMANTIC CHECK ===")

all_pass = True

for name, result in checks.items():
    status = "PASS" if result else "FAIL"
    print(f"{name}: {status}")
    all_pass = all_pass and result

print()
print("OVERALL RESULT:", "PASS" if all_pass else "FAIL")
print("=" * 60)

if not all_pass:
    raise SystemExit(1)
