from core.ai_final_decision_certification import AIFinalDecisionCertification
from core.ai_final_decision_master_control import AIFinalDecisionMasterControl

print("=" * 60)
print("PHASE 7-4-8 CERTIFICATION -> MASTER CONTROL CONTRACT")
print("=" * 60)

final_decision = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
}

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
    {
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
        "execution_readiness": "READY",
        "execution_score": 90.0,
    },
)

print()
print("=== STEP 1 CERTIFICATION ===")

for key in [
    "decision",
    "action",
    "certification_action",
    "certification_status",
    "certification_score",
    "execution_status",
    "execution_authorization",
    "execution_readiness",
    "decision_integrity",
]:
    print(f"{key}: {certification.get(key)}")


master_control_engine = AIFinalDecisionMasterControl()

master_control = master_control_engine.analyze(
    final_decision,
    certification,
    {
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
        "execution_readiness": "READY",
        "execution_score": 90.0,
    },
    {
        "governance_status": "APPROVED",
        "governance_score": 98.0,
    },
    {
        "lifecycle_status": "HEALTHY",
        "lifecycle_score": 95.0,
        "reassessment_required": False,
    },
    {
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_score": 90.0,
    },
    {
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_score": 90.0,
    },
    {
        "integrated_status": "INTEGRATED_HEALTHY",
        "integrated_score": 90.0,
    },
    {
        "validation_status": "VALID",
        "validation_score": 100.0,
    },
)

print()
print("=== STEP 2 MASTER CONTROL ===")

for key in [
    "decision",
    "action",
    "master_control_status",
    "master_control_action",
    "master_control_risk",
    "master_control_score",
    "execution_control",
    "execution_status",
    "execution_authorization",
    "execution_readiness",
    "certification_status",
    "certification_score",
    "decision_integrity",
]:
    print(f"{key}: {master_control.get(key)}")


checks = {
    "decision propagation":
        master_control.get("decision")
        == certification.get("decision"),

    "action propagation":
        master_control.get("action")
        == certification.get("action"),

    "certification status propagation":
        master_control.get("certification_status")
        == certification.get("certification_status"),

    "certification score propagation":
        master_control.get("certification_score")
        == certification.get("certification_score"),

    "execution status propagation":
        master_control.get("execution_status")
        == certification.get("execution_status"),

    "execution authorization propagation":
        master_control.get("execution_authorization")
        == certification.get("execution_authorization"),

    "execution readiness propagation":
        master_control.get("execution_readiness")
        == certification.get("execution_readiness"),

    "decision integrity propagation":
        master_control.get("decision_integrity")
        == certification.get("decision_integrity"),

    "master control status exists":
        master_control.get("master_control_status") is not None,

    "master control action exists":
        master_control.get("master_control_action") is not None,

    "execution control exists":
        master_control.get("execution_control") is not None,
}

print()
print("=== CERTIFICATION -> MASTER CONTROL CHECK ===")

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
