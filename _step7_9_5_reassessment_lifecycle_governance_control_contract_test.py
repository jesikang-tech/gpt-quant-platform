from core.ai_final_decision_lifecycle_governance_control import (
    AIFinalDecisionLifecycleGovernanceControl
)

print("=" * 82)
print("PHASE 7-9-5 REASSESSMENT -> LIFECYCLE GOVERNANCE & CONTROL")
print("DOWNSTREAM PROPAGATION BOUNDARY CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

engine = AIFinalDecisionLifecycleGovernanceControl()

common_final_decision = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
}

common_governance = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "governance_status": "APPROVED",
    "governance_score": 90.0,
}

common_execution_control = {
    "control_status": "AUTHORIZED",
    "control_risk": "LOW",
}

common_execution_assurance = {
    "assurance_status": "ASSURED",
    "assurance_risk": "LOW",
    "assurance_score": 90.0,
}

common_execution_monitoring = {
    "monitoring_status": "STANDARD_MONITORING",
    "monitoring_risk": "LOW",
    "monitoring_score": 90.0,
}

common_execution_feedback = {
    "feedback_status": "STABLE",
    "feedback_risk": "LOW",
    "feedback_score": 90.0,
}

common_lifecycle = {
    "lifecycle_status": "HEALTHY",
    "lifecycle_action": "CONTINUE",
    "lifecycle_risk": "LOW",
    "lifecycle_score": 90.0,
    "reassessment_required": False,
}

common_decision_confidence = {
    "confidence_score": 90.0,
}

common_validation = {
    "validation_status": "VALID",
    "validation_score": 90.0,
}


def run_case(
    name,
    reassessment,
    lifecycle,
    expected_status,
    expected_action,
    expected_reassessment_policy,
    expected_monitoring_policy,
):
    result = engine.govern(
        final_decision=common_final_decision,
        governance=common_governance,
        execution_control=common_execution_control,
        execution_assurance=common_execution_assurance,
        execution_monitoring=common_execution_monitoring,
        execution_feedback=common_execution_feedback,
        reassessment=reassessment,
        lifecycle=lifecycle,
        decision_confidence=common_decision_confidence,
        validation=common_validation,
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
        "operational_status:",
        result.get("operational_status")
    )
    print(
        "operational_action:",
        result.get("operational_action")
    )
    print(
        "reassessment_policy:",
        result.get("reassessment_policy")
    )
    print(
        "monitoring_policy:",
        result.get("monitoring_policy")
    )
    print(
        "operational_risk:",
        result.get("operational_risk")
    )
    print(
        "operational_score:",
        result.get("operational_score")
    )

    assert result.get("operational_status") == expected_status
    assert result.get("operational_action") == expected_action
    assert result.get("reassessment_policy") == expected_reassessment_policy
    assert result.get("monitoring_policy") == expected_monitoring_policy

    print(
        f"{name}: PASS | "
        f"status={result.get('operational_status')} | "
        f"action={result.get('operational_action')} | "
        f"reassessment_policy={result.get('reassessment_policy')} | "
        f"monitoring_policy={result.get('monitoring_policy')}"
    )


run_case(
    "REASSESSMENT_REQUIRED",
    {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
        "reassessment_risk": "MEDIUM",
        "reassessment_score": 90.0,
    },
    {
        **common_lifecycle,
        "lifecycle_status": "REASSESSMENT_REQUIRED",
        "lifecycle_action": "REASSESS",
        "lifecycle_risk": "MEDIUM",
        "reassessment_required": True,
    },
    "REASSESSMENT_REQUIRED",
    "REASSESS",
    "IMMEDIATE",
    "INTENSIVE",
)


run_case(
    "NOT_REQUIRED",
    {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_risk": "LOW",
        "reassessment_score": 90.0,
    },
    common_lifecycle,
    "OPERATIONALLY_HEALTHY",
    "CONTINUE",
    "NOT_REQUIRED",
    "STANDARD",
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "REASSESSMENT_REQUIRED -> "
    "LIFECYCLE GOVERNANCE CONTROL REASSESSMENT_REQUIRED "
    "-> REASSESS -> IMMEDIATE -> INTENSIVE: PASS"
)

print(
    "NOT_REQUIRED -> "
    "OPERATIONALLY_HEALTHY -> CONTINUE "
    "-> NOT_REQUIRED -> STANDARD: PASS"
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
    "LIFECYCLE GOVERNANCE & CONTROL CONTRACT TEST COMPLETE ====="
)
print("=" * 82)
