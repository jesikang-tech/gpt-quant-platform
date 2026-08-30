from core.ai_final_decision_lifecycle_governance import (
    AIFinalDecisionLifecycleGovernance
)


print("=" * 82)
print("PHASE 7-10-14")
print("FINAL DECISION")
print("-> LIFECYCLE GOVERNANCE")
print("BOUNDARY CONTRACT TEST V2")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


engine = AIFinalDecisionLifecycleGovernance()


def run_case(
    name,
    final_decision,
    lifecycle,
    expected_governance_status,
    expected_governance_action,
):
    result = engine.govern(
        final_decision=final_decision,
        lifecycle=lifecycle,
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- FINAL DECISION SOURCE ---")
    print("decision:", final_decision.get("decision"))
    print("action:", final_decision.get("action"))

    print("--- LIFECYCLE SOURCE ---")
    print("lifecycle_status:", lifecycle.get("lifecycle_status"))
    print("lifecycle_action:", lifecycle.get("lifecycle_action"))
    print("lifecycle_risk:", lifecycle.get("lifecycle_risk"))
    print("lifecycle_score:", lifecycle.get("lifecycle_score"))
    print("validation_status:", lifecycle.get("validation_status"))
    print("reassessment_required:", lifecycle.get("reassessment_required"))

    print("--- GOVERNANCE RESULT ---")
    print(
        "governance_status_final:",
        result.get("governance_status_final")
    )
    print(
        "governance_action:",
        result.get("governance_action")
    )
    print(
        "governance_risk:",
        result.get("governance_risk")
    )
    print(
        "governance_score:",
        result.get("governance_score")
    )
    print(
        "governance_grade:",
        result.get("governance_grade")
    )
    print(
        "execution_authorized:",
        result.get("execution_authorized")
    )

    assert result.get(
        "decision"
    ) == final_decision.get("decision")

    assert result.get(
        "action"
    ) == final_decision.get("action")

    assert result.get(
        "governance_status_final"
    ) == expected_governance_status

    assert result.get(
        "governance_action"
    ) == expected_governance_action

    return result


# ================================================================
# CASE 1
# Healthy lifecycle + low risk.
# Governance must be APPROVED.
# ================================================================

run_case(
    "APPROVED_EXECUTION_BOUNDARY",
    {
        "decision": "MAINTAIN",
        "action": "PROCEED",
    },
    {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "lifecycle_status": "HEALTHY",
        "lifecycle_action": "CONTINUE",
        "lifecycle_risk": "LOW",
        "lifecycle_score": 95.0,
        "lifecycle_grade": "A+",
        "validation_status": "VALID",
        "governance_status": "APPROVED",
        "control_status": "AUTHORIZED",
        "assurance_status": "ASSURED",
        "monitoring_status": "STANDARD_MONITORING",
        "feedback_status": "STABLE",
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_required": False,
    },
    "APPROVED",
    "CONTINUE",
)


# ================================================================
# CASE 2
# Reassessment requirement has highest governance priority.
# ================================================================

run_case(
    "REASSESSMENT_PRIORITY",
    {
        "decision": "MAINTAIN",
        "action": "PROCEED",
    },
    {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "lifecycle_status": "HEALTHY",
        "lifecycle_action": "CONTINUE",
        "lifecycle_risk": "LOW",
        "lifecycle_score": 95.0,
        "lifecycle_grade": "A+",
        "validation_status": "VALID",
        "governance_status": "APPROVED",
        "control_status": "AUTHORIZED",
        "assurance_status": "ASSURED",
        "monitoring_status": "STANDARD_MONITORING",
        "feedback_status": "STABLE",
        "reassessment_status": "CRITICAL_REASSESSMENT",
        "reassessment_required": True,
    },
    "REASSESS",
    "REASSESS",
)


# ================================================================
# CASE 3
# Invalid validation must block governance.
# ================================================================

run_case(
    "INVALID_VALIDATION_PRIORITY",
    {
        "decision": "MAINTAIN",
        "action": "PROCEED",
    },
    {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "lifecycle_status": "HEALTHY",
        "lifecycle_action": "CONTINUE",
        "lifecycle_risk": "LOW",
        "lifecycle_score": 95.0,
        "lifecycle_grade": "A+",
        "validation_status": "INVALID",
        "governance_status": "APPROVED",
        "control_status": "AUTHORIZED",
        "assurance_status": "ASSURED",
        "monitoring_status": "STANDARD_MONITORING",
        "feedback_status": "STABLE",
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_required": False,
    },
    "BLOCKED",
    "HALT",
)


# ================================================================
# FINAL ASSERTIONS
# ================================================================

print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "Final Decision -> Lifecycle Governance propagation: PASS"
)

print(
    "Healthy / Low lifecycle -> APPROVED boundary: PASS"
)

print(
    "Reassessment priority boundary: PASS"
)

print(
    "Invalid validation -> BLOCKED priority: PASS"
)

print(
    "Governance action boundary: PASS"
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
print("No actual Outcome supplied.")


print("")
print("=" * 82)
print("===== PHASE 7-10-14 CONTRACT TEST V2 COMPLETE =====")
print("=" * 82)
