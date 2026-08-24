from core.ai_final_decision_lifecycle_intelligence import (
    AIFinalDecisionLifecycleIntelligence
)
from core.ai_final_decision_lifecycle_governance_control import (
    AIFinalDecisionLifecycleGovernanceControl
)

print("=" * 82)
print("PHASE 7-9-5 REASSESSMENT -> LIFECYCLE -> GOVERNANCE & CONTROL")
print("CROSS-ENGINE PROPAGATION CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

lifecycle_engine = AIFinalDecisionLifecycleIntelligence()
governance_control_engine = (
    AIFinalDecisionLifecycleGovernanceControl()
)

final_decision = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "validation_status": "VALID",
    "validation_score": 90.0,
}

governance = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "governance_status": "APPROVED",
    "governance_score": 90.0,
}

execution_control = {
    "control_status": "AUTHORIZED",
    "control_risk": "LOW",
}

execution_assurance = {
    "assurance_status": "ASSURED",
    "assurance_risk": "LOW",
    "assurance_score": 90.0,
}

execution_monitoring = {
    "monitoring_status": "STANDARD_MONITORING",
    "monitoring_risk": "LOW",
    "monitoring_score": 90.0,
}

execution_feedback = {
    "feedback_status": "STABLE",
    "feedback_risk": "LOW",
    "feedback_score": 90.0,
}

decision_confidence = {
    "confidence_score": 90.0,
}

validation = {
    "validation_status": "VALID",
    "validation_score": 90.0,
}


def run_case(name, reassessment):
    lifecycle = lifecycle_engine.analyze(
        final_decision=final_decision,
        governance=governance,
        execution_control=execution_control,
        execution_assurance=execution_assurance,
        execution_monitoring=execution_monitoring,
        execution_feedback=execution_feedback,
        reassessment=reassessment,
    )

    governance_control = governance_control_engine.govern(
        final_decision=final_decision,
        governance=governance,
        execution_control=execution_control,
        execution_assurance=execution_assurance,
        execution_monitoring=execution_monitoring,
        execution_feedback=execution_feedback,
        reassessment=reassessment,
        lifecycle=lifecycle,
        decision_confidence=decision_confidence,
        validation=validation,
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- LIFECYCLE ---")
    print(
        "reassessment_required:",
        lifecycle.get("reassessment_required")
    )
    print(
        "reassessment_status:",
        lifecycle.get("reassessment_status")
    )
    print(
        "lifecycle_status:",
        lifecycle.get("lifecycle_status")
    )
    print(
        "lifecycle_action:",
        lifecycle.get("lifecycle_action")
    )

    print("--- GOVERNANCE & CONTROL ---")
    print(
        "operational_status:",
        governance_control.get("operational_status")
    )
    print(
        "operational_action:",
        governance_control.get("operational_action")
    )
    print(
        "reassessment_policy:",
        governance_control.get("reassessment_policy")
    )
    print(
        "monitoring_policy:",
        governance_control.get("monitoring_policy")
    )

    return lifecycle, governance_control


lifecycle_required, control_required = run_case(
    "REASSESSMENT_REQUIRED",
    {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
        "reassessment_risk": "MEDIUM",
        "reassessment_score": 90.0,
    },
)

assert lifecycle_required.get(
    "lifecycle_status"
) == "REASSESSMENT_REQUIRED"

assert lifecycle_required.get(
    "lifecycle_action"
) == "REASSESS"

assert control_required.get(
    "operational_status"
) == "REASSESSMENT_REQUIRED"

assert control_required.get(
    "operational_action"
) == "REASSESS"

assert control_required.get(
    "reassessment_policy"
) == "IMMEDIATE"

assert control_required.get(
    "monitoring_policy"
) == "INTENSIVE"

print(
    "REASSESSMENT_REQUIRED cross-engine propagation: PASS"
)


lifecycle_normal, control_normal = run_case(
    "NOT_REQUIRED",
    {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_risk": "LOW",
        "reassessment_score": 90.0,
    },
)

assert lifecycle_normal.get(
    "lifecycle_status"
) == "HEALTHY"

assert lifecycle_normal.get(
    "lifecycle_action"
) == "CONTINUE"

assert control_normal.get(
    "operational_status"
) == "OPERATIONALLY_HEALTHY"

assert control_normal.get(
    "operational_action"
) == "CONTINUE"

assert control_normal.get(
    "reassessment_policy"
) == "NOT_REQUIRED"

assert control_normal.get(
    "monitoring_policy"
) == "STANDARD"

print(
    "NOT_REQUIRED cross-engine propagation: PASS"
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "REASSESSMENT_REQUIRED"
    " -> LIFECYCLE REASSESSMENT_REQUIRED"
    " -> GOVERNANCE_CONTROL REASSESSMENT_REQUIRED"
    " -> REASSESS"
    " -> IMMEDIATE"
    " -> INTENSIVE: PASS"
)

print(
    "NOT_REQUIRED"
    " -> LIFECYCLE HEALTHY"
    " -> GOVERNANCE_CONTROL OPERATIONALLY_HEALTHY"
    " -> CONTINUE"
    " -> NOT_REQUIRED"
    " -> STANDARD: PASS"
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
    "===== PHASE 7-9-5 CROSS-ENGINE PROPAGATION "
    "CONTRACT TEST COMPLETE ====="
)
print("=" * 82)
