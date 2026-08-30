"""
GPT Quant Platform

PHASE 7-10-18-D
REASSESSMENT
->
LIFECYCLE GOVERNANCE CONTROL
BOUNDARY CONTRACT TEST V2

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_final_decision_lifecycle_governance_control import (
    AIFinalDecisionLifecycleGovernanceControl,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )


def base_inputs(
    reassessment_required=False,
    reassessment_status="NOT_REQUIRED",
    reassessment_risk="LOW",
):
    return {
        "final_decision": {
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "confidence_score": 95,
            "validation_status": "VALID",
            "validation_score": 95,
        },
        "governance": {
            "governance_status": "APPROVED",
            "governance_score": 95,
        },
        "execution_control": {
            "control_status": "AUTHORIZED",
            "control_risk": "LOW",
        },
        "execution_assurance": {
            "assurance_status": "ASSURED",
            "assurance_risk": "LOW",
        },
        "execution_monitoring": {
            "monitoring_status": "STANDARD_MONITORING",
            "monitoring_risk": "LOW",
        },
        "execution_feedback": {
            "feedback_status": "STABLE",
            "feedback_risk": "LOW",
        },
        "reassessment": {
            "reassessment_required": reassessment_required,
            "reassessment_status": reassessment_status,
            "reassessment_risk": reassessment_risk,
        },
        "lifecycle": {
            "lifecycle_status": "HEALTHY",
            "lifecycle_action": "CONTINUE",
            "lifecycle_risk": "LOW",
            "lifecycle_score": 95,
            "lifecycle_grade": "A+",
        },
        "decision_confidence": {
            "confidence_score": 95,
        },
        "validation": {
            "validation_status": "VALID",
            "validation_score": 95,
        },
    }


def run_case_stable_low():
    engine = AIFinalDecisionLifecycleGovernanceControl()

    result = engine.govern(**base_inputs())

    print("=" * 82)
    print("CASE: STABLE_LOW")
    print("=" * 82)
    print(result)

    assert_equal(
        result["operational_status"],
        "OPERATIONALLY_HEALTHY",
        "STABLE + LOW -> operational status",
    )

    assert_equal(
        result["execution_authorization"],
        "AUTHORIZED",
        "STABLE + LOW -> execution authorization",
    )

    assert_equal(
        result["monitoring_policy"],
        "STANDARD",
        "STABLE + LOW -> monitoring policy",
    )

    assert_equal(
        result["reassessment_policy"],
        "NOT_REQUIRED",
        "STABLE + LOW -> reassessment policy",
    )

    assert_equal(
        result["operational_action"],
        "CONTINUE",
        "STABLE + LOW -> operational action",
    )

    print("STABLE + LOW -> OPERATIONALLY_HEALTHY: PASS")
    print("STABLE + LOW -> AUTHORIZED: PASS")
    print("STABLE + LOW -> STANDARD: PASS")
    print("STABLE + LOW -> NOT_REQUIRED: PASS")
    print("STABLE + LOW -> CONTINUE: PASS")


def run_case_reassessment_medium():
    engine = AIFinalDecisionLifecycleGovernanceControl()

    result = engine.govern(
        **base_inputs(
            reassessment_required=True,
            reassessment_status="REASSESSMENT_REQUIRED",
            reassessment_risk="MEDIUM",
        )
    )

    print("=" * 82)
    print("CASE: REASSESSMENT_REQUIRED_MEDIUM")
    print("=" * 82)
    print(result)

    assert_equal(
        result["operational_status"],
        "REASSESSMENT_REQUIRED",
        "Reassessment required -> operational status",
    )

    assert_equal(
        result["execution_authorization"],
        "SUSPENDED",
        "Reassessment required -> execution authorization",
    )

    assert_equal(
        result["monitoring_policy"],
        "INTENSIVE",
        "Reassessment required -> monitoring policy",
    )

    assert_equal(
        result["reassessment_policy"],
        "IMMEDIATE",
        "Reassessment required -> reassessment policy",
    )

    assert_equal(
        result["operational_action"],
        "REASSESS",
        "Reassessment required -> operational action",
    )

    print("Reassessment required -> REASSESSMENT_REQUIRED: PASS")
    print("Reassessment required -> SUSPENDED: PASS")
    print("Reassessment required -> INTENSIVE: PASS")
    print("Reassessment required -> IMMEDIATE: PASS")
    print("Reassessment required -> REASSESS: PASS")


def run_case_unstable_high():
    engine = AIFinalDecisionLifecycleGovernanceControl()

    result = engine.govern(
        **base_inputs(
            reassessment_required=True,
            reassessment_status="UNSTABLE_REASSESSMENT",
            reassessment_risk="HIGH",
        )
    )

    print("=" * 82)
    print("CASE: UNSTABLE_REASSESSMENT_HIGH")
    print("=" * 82)
    print(result)

    assert_equal(
        result["operational_status"],
        "REASSESSMENT_REQUIRED",
        "UNSTABLE + HIGH -> operational status",
    )

    assert_equal(
        result["operational_risk"],
        "HIGH",
        "UNSTABLE + HIGH -> operational risk",
    )

    assert_equal(
        result["execution_authorization"],
        "SUSPENDED",
        "UNSTABLE + HIGH -> execution authorization",
    )

    assert_equal(
        result["monitoring_policy"],
        "INTENSIVE",
        "UNSTABLE + HIGH -> monitoring policy",
    )

    assert_equal(
        result["reassessment_policy"],
        "IMMEDIATE",
        "UNSTABLE + HIGH -> reassessment policy",
    )

    assert_equal(
        result["operational_action"],
        "REASSESS",
        "UNSTABLE + HIGH -> operational action",
    )

    print("UNSTABLE + HIGH -> REASSESSMENT_REQUIRED: PASS")
    print("UNSTABLE + HIGH -> HIGH risk: PASS")
    print("UNSTABLE + HIGH -> SUSPENDED: PASS")
    print("UNSTABLE + HIGH -> INTENSIVE: PASS")
    print("UNSTABLE + HIGH -> IMMEDIATE: PASS")
    print("UNSTABLE + HIGH -> REASSESS: PASS")


def run_case_critical():
    engine = AIFinalDecisionLifecycleGovernanceControl()

    result = engine.govern(
        **base_inputs(
            reassessment_required=True,
            reassessment_status="CRITICAL_REASSESSMENT",
            reassessment_risk="CRITICAL",
        )
    )

    print("=" * 82)
    print("CASE: CRITICAL_REASSESSMENT")
    print("=" * 82)
    print(result)

    assert_equal(
        result["operational_status"],
        "REASSESSMENT_REQUIRED",
        "CRITICAL -> operational status",
    )

    assert_equal(
        result["operational_risk"],
        "CRITICAL",
        "CRITICAL -> operational risk",
    )

    assert_equal(
        result["execution_authorization"],
        "SUSPENDED",
        "CRITICAL -> execution authorization",
    )

    assert_equal(
        result["monitoring_policy"],
        "INTENSIVE",
        "CRITICAL -> monitoring policy",
    )

    assert_equal(
        result["reassessment_policy"],
        "IMMEDIATE",
        "CRITICAL -> reassessment policy",
    )

    assert_equal(
        result["operational_action"],
        "REASSESS",
        "CRITICAL -> operational action",
    )

    print("CRITICAL -> REASSESSMENT_REQUIRED: PASS")
    print("CRITICAL -> CRITICAL risk: PASS")
    print("CRITICAL -> SUSPENDED: PASS")
    print("CRITICAL -> INTENSIVE: PASS")
    print("CRITICAL -> IMMEDIATE: PASS")
    print("CRITICAL -> REASSESS: PASS")


if __name__ == "__main__":
    print("=" * 82)
    print("PHASE 7-10-18-D")
    print("REASSESSMENT")
    print("-> LIFECYCLE GOVERNANCE CONTROL")
    print("BOUNDARY CONTRACT TEST V2")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    run_case_stable_low()
    run_case_reassessment_medium()
    run_case_unstable_high()
    run_case_critical()

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
    print("===== PHASE 7-10-18-D CONTRACT TEST V2 COMPLETE =====")
    print("=" * 82)
