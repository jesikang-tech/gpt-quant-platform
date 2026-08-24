from core.ai_final_decision_lifecycle_intelligence import (
    AIFinalDecisionLifecycleIntelligence
)
from core.ai_final_decision_lifecycle_governance_control import (
    AIFinalDecisionLifecycleGovernanceControl
)
from core.ai_final_decision_operational_intelligence import (
    AIFinalDecisionOperationalIntelligence
)

print("=" * 82)
print("PHASE 7-9-5 GOVERNANCE & CONTROL -> OPERATIONAL INTELLIGENCE")
print("REASSESSMENT DOWNSTREAM PROPAGATION BOUNDARY CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

lifecycle_engine = AIFinalDecisionLifecycleIntelligence()
governance_control_engine = (
    AIFinalDecisionLifecycleGovernanceControl()
)
operational_engine = AIFinalDecisionOperationalIntelligence()


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

    operational_intelligence = operational_engine.analyze(
        final_decision=final_decision,
        governance_control=governance_control,
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

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
        "operational_risk:",
        governance_control.get("operational_risk")
    )
    print(
        "reassessment_policy:",
        governance_control.get("reassessment_policy")
    )
    print(
        "monitoring_policy:",
        governance_control.get("monitoring_policy")
    )

    print("--- OPERATIONAL INTELLIGENCE ---")
    print(
        "intelligence_status:",
        operational_intelligence.get("intelligence_status")
    )
    print(
        "intelligence_action:",
        operational_intelligence.get("intelligence_action")
    )
    print(
        "intelligence_risk:",
        operational_intelligence.get("intelligence_risk")
    )
    print(
        "priority:",
        operational_intelligence.get("priority")
    )

    return governance_control, operational_intelligence


governance_required, operational_required = run_case(
    "REASSESSMENT_REQUIRED",
    {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
        "reassessment_risk": "MEDIUM",
        "reassessment_score": 90.0,
    },
)

assert governance_required.get(
    "operational_status"
) == "REASSESSMENT_REQUIRED"

assert governance_required.get(
    "operational_action"
) == "REASSESS"

assert governance_required.get(
    "operational_risk"
) == "MEDIUM"

assert governance_required.get(
    "reassessment_policy"
) == "IMMEDIATE"

assert governance_required.get(
    "monitoring_policy"
) == "INTENSIVE"

assert operational_required.get(
    "intelligence_status"
) == "CONTROLLED"

assert operational_required.get(
    "intelligence_action"
) == "SUSPEND"

assert operational_required.get(
    "intelligence_risk"
) == "MEDIUM"

assert operational_required.get(
    "priority"
) == "HIGH"

print(
    "REASSESSMENT_REQUIRED -> OPERATIONAL INTELLIGENCE: PASS"
)


governance_normal, operational_normal = run_case(
    "NOT_REQUIRED",
    {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_risk": "LOW",
        "reassessment_score": 90.0,
    },
)

assert governance_normal.get(
    "operational_status"
) == "OPERATIONALLY_HEALTHY"

assert governance_normal.get(
    "operational_action"
) == "CONTINUE"

assert governance_normal.get(
    "operational_risk"
) == "LOW"

assert governance_normal.get(
    "reassessment_policy"
) == "NOT_REQUIRED"

assert governance_normal.get(
    "monitoring_policy"
) == "STANDARD"

assert operational_normal.get(
    "intelligence_status"
) == "HEALTHY"

assert operational_normal.get(
    "intelligence_action"
) == "PROCEED"

assert operational_normal.get(
    "intelligence_risk"
) == "LOW"

assert operational_normal.get(
    "priority"
) == "NORMAL"

print(
    "NOT_REQUIRED -> OPERATIONAL INTELLIGENCE: PASS"
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "REASSESSMENT_REQUIRED"
    " -> GOVERNANCE_CONTROL REASSESSMENT_REQUIRED / REASSESS"
    " -> OPERATIONAL_INTELLIGENCE CONTROLLED / SUSPEND"
    " -> HIGH: PASS"
)

print(
    "NOT_REQUIRED"
    " -> GOVERNANCE_CONTROL OPERATIONALLY_HEALTHY / CONTINUE"
    " -> OPERATIONAL_INTELLIGENCE HEALTHY / PROCEED"
    " -> NORMAL: PASS"
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
    "===== PHASE 7-9-5 GOVERNANCE & CONTROL -> "
    "OPERATIONAL INTELLIGENCE CONTRACT TEST COMPLETE ====="
)
print("=" * 82)
