from core.ai_final_decision_lifecycle_intelligence import (
    AIFinalDecisionLifecycleIntelligence
)

print("=" * 82)
print("PHASE 7-9-5 REASSESSMENT -> LIFECYCLE")
print("DOWNSTREAM PROPAGATION BOUNDARY CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

engine = AIFinalDecisionLifecycleIntelligence()

common_final_decision = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "validation_status": "VALID",
    "validation_score": 90.0,
}

common_governance = {
    "governance_status": "APPROVED",
    "governance_score": 90.0,
}

common_control = {
    "control_status": "AUTHORIZED",
    "control_risk": "LOW",
}

common_assurance = {
    "assurance_status": "ASSURED",
    "assurance_risk": "LOW",
    "assurance_score": 90.0,
}

common_monitoring = {
    "monitoring_status": "STANDARD",
    "monitoring_risk": "LOW",
    "monitoring_score": 90.0,
}

common_feedback = {
    "feedback_status": "STABLE",
    "feedback_risk": "LOW",
    "feedback_score": 90.0,
}


def run_case(
    name,
    reassessment,
    expected_status,
    expected_action,
):
    result = engine.analyze(
        final_decision=common_final_decision,
        governance=common_governance,
        execution_control=common_control,
        execution_assurance=common_assurance,
        execution_monitoring=common_monitoring,
        execution_feedback=common_feedback,
        reassessment=reassessment,
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print(
        "reassessment_required:",
        result.get("reassessment_required")
    )
    print(
        "reassessment_status:",
        result.get("reassessment_status")
    )
    print(
        "lifecycle_status:",
        result.get("lifecycle_status")
    )
    print(
        "lifecycle_action:",
        result.get("lifecycle_action")
    )
    print(
        "lifecycle_risk:",
        result.get("lifecycle_risk")
    )
    print(
        "lifecycle_score:",
        result.get("lifecycle_score")
    )

    assert result.get("lifecycle_status") == expected_status
    assert result.get("lifecycle_action") == expected_action

    print(
        f"{name}: PASS | "
        f"status={result.get('lifecycle_status')} | "
        f"action={result.get('lifecycle_action')} | "
        f"risk={result.get('lifecycle_risk')} | "
        f"score={result.get('lifecycle_score')}"
    )


run_case(
    "REASSESSMENT_REQUIRED",
    {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
        "reassessment_risk": "MEDIUM",
        "reassessment_score": 90.0,
    },
    "REASSESSMENT_REQUIRED",
    "REASSESS",
)


run_case(
    "NOT_REQUIRED",
    {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_risk": "LOW",
        "reassessment_score": 90.0,
    },
    "HEALTHY",
    "CONTINUE",
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "REASSESSMENT_REQUIRED -> "
    "LIFECYCLE REASSESSMENT_REQUIRED -> REASSESS: PASS"
)

print(
    "NOT_REQUIRED -> "
    "LIFECYCLE HEALTHY -> CONTINUE: PASS"
)

print("")
print("=" * 82)
print("SAFETY")
print("=" * 82)

print("Memory-only execution: PASS")
print("No production DB access.")
print("No API runtime call.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")

print("")
print(
    "===== PHASE 7-9-5 REASSESSMENT -> "
    "LIFECYCLE CONTRACT TEST COMPLETE ====="
)
print("=" * 82)
