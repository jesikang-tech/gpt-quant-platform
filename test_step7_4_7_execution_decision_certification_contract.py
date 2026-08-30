from core.ai_final_execution_decision import AIFinalExecutionDecision
from core.ai_final_decision_certification import AIFinalDecisionCertification

print("=" * 60)
print("PHASE 7-4-7 EXECUTION DECISION -> CERTIFICATION CONTRACT")
print("=" * 60)

final_decision = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
}

execution_engine = AIFinalExecutionDecision()

execution_decision = execution_engine.analyze(
    final_decision,
    {
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
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
    "execution_status",
    "execution_authorization",
    "execution_readiness",
    "execution_score",
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
        certification.get("decision") == execution_decision.get("decision"),

    "action preserved":
        certification.get("action") == execution_decision.get("action"),

    "execution status propagation":
        certification.get("execution_status")
        == execution_decision.get("execution_status"),

    "execution authorization propagation":
        certification.get("execution_authorization")
        == execution_decision.get("execution_authorization"),

    "execution readiness propagation":
        certification.get("execution_readiness")
        == execution_decision.get("execution_readiness"),

    "execution score propagation":
        certification.get("execution_score")
        == execution_decision.get("execution_score"),

    "certification action exists":
        certification.get("certification_action") is not None,

    "certification status exists":
        certification.get("certification_status") is not None,
}

print()
print("=== EXECUTION DECISION -> CERTIFICATION CHECK ===")

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
