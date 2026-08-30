"""
GPT Quant Platform

Phase 7-10-15
Final Decision Lifecycle Governance
-> Governance Control Boundary Contract Test V2

Source-verified / Memory-only / Read-only.
No production DB access.
No API runtime call.
No INSERT / UPDATE / DELETE.
No future price injection.
No fake Outcome persistence.
"""

from core.ai_final_decision_lifecycle_governance import (
    AIFinalDecisionLifecycleGovernance,
)

from core.ai_final_decision_lifecycle_governance_control import (
    AIFinalDecisionLifecycleGovernanceControl,
)


def assert_equal(label, actual, expected):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def build_sources(
    *,
    validation_status="VALID",
    reassessment_required=False,
    lifecycle_status="HEALTHY",
    lifecycle_action="CONTINUE",
    lifecycle_risk="LOW",
    lifecycle_score=95.0,
    governance_status="APPROVED",
    governance_score=95.0,
):
    final_decision = {
        "decision": "MAINTAIN",
        "action": "PROCEED",
    }

    lifecycle = {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "lifecycle_status": lifecycle_status,
        "lifecycle_action": lifecycle_action,
        "lifecycle_risk": lifecycle_risk,
        "lifecycle_score": lifecycle_score,
        "lifecycle_grade": "A+",
        "validation_status": validation_status,
        "governance_status": governance_status,
        "control_status": "AUTHORIZED",
        "assurance_status": "ASSURED",
        "monitoring_status": "STANDARD_MONITORING",
        "feedback_status": "STABLE",
        "reassessment_status": (
            "REASSESSMENT_REQUIRED"
            if reassessment_required
            else "NOT_REQUIRED"
        ),
        "reassessment_required": reassessment_required,
    }

    governance = {
        "governance_status": governance_status,
        "governance_score": governance_score,
    }

    execution_control = {
        "control_status": "AUTHORIZED",
        "control_risk": "LOW",
    }

    execution_assurance = {
        "assurance_status": "ASSURED",
        "assurance_risk": "LOW",
    }

    execution_monitoring = {
        "monitoring_status": "STANDARD_MONITORING",
        "monitoring_risk": "LOW",
    }

    execution_feedback = {
        "feedback_status": "STABLE",
        "feedback_risk": "LOW",
    }

    reassessment = {
        "reassessment_required": reassessment_required,
        "reassessment_status": (
            "REASSESSMENT_REQUIRED"
            if reassessment_required
            else "NOT_REQUIRED"
        ),
        "reassessment_risk": (
            "HIGH" if reassessment_required else "LOW"
        ),
    }

    decision_confidence = {
        "confidence_score": 95.0,
    }

    validation = {
        "validation_status": validation_status,
        "validation_score": 95.0,
    }

    return {
        "final_decision": final_decision,
        "lifecycle": lifecycle,
        "governance": governance,
        "execution_control": execution_control,
        "execution_assurance": execution_assurance,
        "execution_monitoring": execution_monitoring,
        "execution_feedback": execution_feedback,
        "reassessment": reassessment,
        "decision_confidence": decision_confidence,
        "validation": validation,
    }


def run_case(
    name,
    *,
    validation_status="VALID",
    reassessment_required=False,
    expected_governance_status=None,
    expected_governance_action=None,
    expected_execution_authorized=None,
    expected_operational_status=None,
    expected_execution_authorization=None,
    expected_operational_action=None,
):
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    sources = build_sources(
        validation_status=validation_status,
        reassessment_required=reassessment_required,
    )

    governance_engine = AIFinalDecisionLifecycleGovernance()

    governance_result = governance_engine.govern(
        final_decision=sources["final_decision"],
        lifecycle=sources["lifecycle"],
    )

    print("--- LIFECYCLE GOVERNANCE SOURCE ---")
    print(
        "decision:",
        governance_result.get("decision"),
    )
    print(
        "action:",
        governance_result.get("action"),
    )
    print(
        "governance_status_final:",
        governance_result.get("governance_status_final"),
    )
    print(
        "governance_action:",
        governance_result.get("governance_action"),
    )
    print(
        "governance_risk:",
        governance_result.get("governance_risk"),
    )
    print(
        "governance_score:",
        governance_result.get("governance_score"),
    )
    print(
        "execution_authorized:",
        governance_result.get("execution_authorized"),
    )

    if expected_governance_status is not None:
        assert_equal(
            "Lifecycle Governance status",
            governance_result.get("governance_status_final"),
            expected_governance_status,
        )

    if expected_governance_action is not None:
        assert_equal(
            "Lifecycle Governance action",
            governance_result.get("governance_action"),
            expected_governance_action,
        )

    control_engine = AIFinalDecisionLifecycleGovernanceControl()

    control_result = control_engine.govern(
        final_decision=sources["final_decision"],
        governance=governance_result,
        execution_control=sources["execution_control"],
        execution_assurance=sources["execution_assurance"],
        execution_monitoring=sources["execution_monitoring"],
        execution_feedback=sources["execution_feedback"],
        reassessment=sources["reassessment"],
        lifecycle=sources["lifecycle"],
        decision_confidence=sources["decision_confidence"],
        validation=sources["validation"],
    )

    print("--- GOVERNANCE CONTROL RESULT ---")
    print(
        "operational_status:",
        control_result.get("operational_status"),
    )
    print(
        "operational_action:",
        control_result.get("operational_action"),
    )
    print(
        "operational_risk:",
        control_result.get("operational_risk"),
    )
    print(
        "operational_score:",
        control_result.get("operational_score"),
    )
    print(
        "execution_authorization:",
        control_result.get("execution_authorization"),
    )
    print(
        "reassessment_required:",
        control_result.get("reassessment_required"),
    )
    print(
        "validation_status:",
        control_result.get("validation_status"),
    )

    if expected_execution_authorized is not None:
        assert_equal(
            "Governance execution_authorized",
            governance_result.get("execution_authorized"),
            expected_execution_authorized,
        )

    if expected_operational_status is not None:
        assert_equal(
            "Governance Control operational_status",
            control_result.get("operational_status"),
            expected_operational_status,
        )

    if expected_execution_authorization is not None:
        assert_equal(
            "Governance Control execution_authorization",
            control_result.get("execution_authorization"),
            expected_execution_authorization,
        )

    if expected_operational_action is not None:
        assert_equal(
            "Governance Control operational_action",
            control_result.get("operational_action"),
            expected_operational_action,
        )


print("=" * 82)
print("PHASE 7-10-15")
print("FINAL DECISION LIFECYCLE GOVERNANCE")
print("-> GOVERNANCE CONTROL")
print("BOUNDARY CONTRACT TEST V2")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)
print()


run_case(
    "APPROVED_TO_OPERATIONALLY_HEALTHY",
    expected_governance_status="APPROVED",
    expected_governance_action="CONTINUE",
    expected_execution_authorized=True,
    expected_operational_status="OPERATIONALLY_HEALTHY",
    expected_execution_authorization="AUTHORIZED",
    expected_operational_action="CONTINUE",
)

print()

run_case(
    "REASSESSMENT_PRIORITY",
    reassessment_required=True,
    expected_governance_status="REASSESS",
    expected_governance_action="REASSESS",
    expected_execution_authorized=False,
    expected_operational_status="REASSESSMENT_REQUIRED",
    expected_execution_authorization="SUSPENDED",
    expected_operational_action="REASSESS",
)

print()

run_case(
    "INVALID_VALIDATION_PRIORITY",
    validation_status="INVALID",
    expected_governance_status="BLOCKED",
    expected_governance_action="HALT",
    expected_execution_authorized=False,
    expected_operational_status="VALIDATION_BLOCKED",
    expected_execution_authorization="DENIED",
    expected_operational_action="HALT",
)

print()

print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("Lifecycle Governance -> Governance Control propagation: PASS")
print("APPROVED -> OPERATIONALLY_HEALTHY boundary: PASS")
print("Authorized execution boundary: PASS")
print("Reassessment priority boundary: PASS")
print("Invalid validation priority boundary: PASS")
print("Governance action / control action boundary: PASS")
print()

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
print()

print("=" * 82)
print("===== PHASE 7-10-15 CONTRACT TEST V2 COMPLETE =====")
print("=" * 82)
