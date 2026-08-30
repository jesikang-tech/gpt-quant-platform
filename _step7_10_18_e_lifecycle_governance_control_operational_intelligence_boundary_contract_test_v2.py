"""
GPT Quant Platform

Phase 7-10-18-E
Lifecycle Governance Control
-> Operational Intelligence
Boundary Contract Test V2

Source-verified / memory-only / read-only.

No production DB access.
No API runtime call.
No INSERT / UPDATE / DELETE.
No future price injection.
No fake Outcome persistence.
"""

from core.ai_final_decision_lifecycle_governance_control import (
    AIFinalDecisionLifecycleGovernanceControl,
)
from core.ai_final_decision_operational_intelligence import (
    AIFinalDecisionOperationalIntelligence,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )

    print(f"{label}: PASS")


def build_governance_control(
    reassessment_required=False,
    reassessment_status="NOT_REQUIRED",
    reassessment_risk="LOW",
):
    lifecycle = {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "lifecycle_status": "HEALTHY",
        "lifecycle_action": "CONTINUE",
        "lifecycle_risk": "LOW",
        "lifecycle_score": 95.0,
        "lifecycle_grade": "A+",
    }

    governance = {
        "governance_status": "APPROVED",
        "governance_score": 95.0,
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
        "reassessment_status": reassessment_status,
        "reassessment_risk": reassessment_risk,
    }

    validation = {
        "validation_status": "VALID",
        "validation_score": 95.0,
    }

    decision_confidence = {
        "confidence_score": 95.0,
    }

    engine = AIFinalDecisionLifecycleGovernanceControl()

    return engine.govern(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "validation_status": "VALID",
            "validation_score": 95.0,
            "confidence_score": 95.0,
        },
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


def analyze(governance_control):
    engine = AIFinalDecisionOperationalIntelligence()

    return engine.analyze(
        governance_control=governance_control
    )


def run_case_stable_low():
    print("=" * 82)
    print("CASE: STABLE_LOW")
    print("=" * 82)

    result = analyze(
        build_governance_control()
    )

    print(result)

    assert_equal(
        result["operational_status"],
        "OPERATIONALLY_HEALTHY",
        "STABLE + LOW -> operational status preserved",
    )

    assert_equal(
        result["operational_action"],
        "CONTINUE",
        "STABLE + LOW -> operational action preserved",
    )

    assert_equal(
        result["operational_risk"],
        "LOW",
        "STABLE + LOW -> operational risk preserved",
    )

    assert_equal(
        result["execution_authorization"],
        "AUTHORIZED",
        "STABLE + LOW -> AUTHORIZED",
    )

    assert_equal(
        result["monitoring_policy"],
        "STANDARD",
        "STABLE + LOW -> STANDARD monitoring",
    )

    assert_equal(
        result["reassessment_policy"],
        "NOT_REQUIRED",
        "STABLE + LOW -> NOT_REQUIRED reassessment",
    )

    assert_equal(
        result["intelligence_status"],
        "HEALTHY",
        "STABLE + LOW -> HEALTHY intelligence status",
    )

    assert_equal(
        result["intelligence_action"],
        "PROCEED",
        "STABLE + LOW -> PROCEED intelligence action",
    )

    assert_equal(
        result["intelligence_risk"],
        "LOW",
        "STABLE + LOW -> LOW intelligence risk",
    )

    assert_equal(
        result["intelligence_score"],
        95.0,
        "STABLE + LOW -> intelligence score",
    )

    assert_equal(
        result["intelligence_grade"],
        "A+",
        "STABLE + LOW -> intelligence grade",
    )

    assert_equal(
        result["priority"],
        "NORMAL",
        "STABLE + LOW -> NORMAL priority",
    )


def run_case_reassessment_medium():
    print("=" * 82)
    print("CASE: REASSESSMENT_REQUIRED_MEDIUM")
    print("=" * 82)

    result = analyze(
        build_governance_control(
            reassessment_required=True,
            reassessment_status="REASSESSMENT_REQUIRED",
            reassessment_risk="MEDIUM",
        )
    )

    print(result)

    assert_equal(
        result["operational_status"],
        "REASSESSMENT_REQUIRED",
        "REASSESSMENT MEDIUM -> operational status",
    )

    assert_equal(
        result["operational_risk"],
        "MEDIUM",
        "REASSESSMENT MEDIUM -> operational risk",
    )

    assert_equal(
        result["execution_authorization"],
        "SUSPENDED",
        "REASSESSMENT MEDIUM -> SUSPENDED",
    )

    assert_equal(
        result["monitoring_policy"],
        "INTENSIVE",
        "REASSESSMENT MEDIUM -> INTENSIVE monitoring",
    )

    assert_equal(
        result["reassessment_policy"],
        "IMMEDIATE",
        "REASSESSMENT MEDIUM -> IMMEDIATE reassessment",
    )

    assert_equal(
        result["intelligence_status"],
        "CONTROLLED",
        "REASSESSMENT MEDIUM -> CONTROLLED intelligence status",
    )

    assert_equal(
        result["intelligence_action"],
        "SUSPEND",
        "REASSESSMENT MEDIUM -> SUSPEND intelligence action",
    )

    assert_equal(
        result["intelligence_risk"],
        "MEDIUM",
        "REASSESSMENT MEDIUM -> MEDIUM intelligence risk",
    )

    assert_equal(
        result["intelligence_score"],
        86.0,
        "REASSESSMENT MEDIUM -> intelligence score",
    )

    assert_equal(
        result["intelligence_grade"],
        "B+",
        "REASSESSMENT MEDIUM -> intelligence grade",
    )

    assert_equal(
        result["priority"],
        "HIGH",
        "REASSESSMENT MEDIUM -> HIGH priority",
    )


def run_case_unstable_high():
    print("=" * 82)
    print("CASE: UNSTABLE_REASSESSMENT_HIGH")
    print("=" * 82)

    result = analyze(
        build_governance_control(
            reassessment_required=True,
            reassessment_status="UNSTABLE_REASSESSMENT",
            reassessment_risk="HIGH",
        )
    )

    print(result)

    assert_equal(
        result["operational_status"],
        "REASSESSMENT_REQUIRED",
        "UNSTABLE HIGH -> operational status",
    )

    assert_equal(
        result["operational_risk"],
        "HIGH",
        "UNSTABLE HIGH -> operational risk",
    )

    assert_equal(
        result["execution_authorization"],
        "SUSPENDED",
        "UNSTABLE HIGH -> SUSPENDED",
    )

    assert_equal(
        result["monitoring_policy"],
        "INTENSIVE",
        "UNSTABLE HIGH -> INTENSIVE monitoring",
    )

    assert_equal(
        result["reassessment_policy"],
        "IMMEDIATE",
        "UNSTABLE HIGH -> IMMEDIATE reassessment",
    )

    assert_equal(
        result["intelligence_status"],
        "CONTROLLED",
        "UNSTABLE HIGH -> CONTROLLED intelligence status",
    )

    assert_equal(
        result["intelligence_action"],
        "SUSPEND",
        "UNSTABLE HIGH -> SUSPEND intelligence action",
    )

    assert_equal(
        result["intelligence_risk"],
        "HIGH",
        "UNSTABLE HIGH -> HIGH intelligence risk",
    )

    assert_equal(
        result["intelligence_score"],
        83.0,
        "UNSTABLE HIGH -> intelligence score",
    )

    assert_equal(
        result["intelligence_grade"],
        "B",
        "UNSTABLE HIGH -> intelligence grade",
    )

    assert_equal(
        result["priority"],
        "HIGH",
        "UNSTABLE HIGH -> HIGH priority",
    )


def run_case_critical():
    print("=" * 82)
    print("CASE: CRITICAL_REASSESSMENT")
    print("=" * 82)

    result = analyze(
        build_governance_control(
            reassessment_required=True,
            reassessment_status="CRITICAL_REASSESSMENT",
            reassessment_risk="CRITICAL",
        )
    )

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
        "CRITICAL -> SUSPENDED",
    )

    assert_equal(
        result["monitoring_policy"],
        "INTENSIVE",
        "CRITICAL -> INTENSIVE monitoring",
    )

    assert_equal(
        result["reassessment_policy"],
        "IMMEDIATE",
        "CRITICAL -> IMMEDIATE reassessment",
    )

    assert_equal(
        result["intelligence_status"],
        "CONTROLLED",
        "CRITICAL -> CONTROLLED intelligence status",
    )

    assert_equal(
        result["intelligence_action"],
        "SUSPEND",
        "CRITICAL -> SUSPEND intelligence action",
    )

    assert_equal(
        result["intelligence_risk"],
        "CRITICAL",
        "CRITICAL -> CRITICAL intelligence risk",
    )

    assert_equal(
        result["intelligence_score"],
        77.0,
        "CRITICAL -> intelligence score",
    )

    assert_equal(
        result["intelligence_grade"],
        "C",
        "CRITICAL -> intelligence grade",
    )

    assert_equal(
        result["priority"],
        "HIGH",
        "CRITICAL -> HIGH priority",
    )


def main():
    print("=" * 82)
    print("PHASE 7-10-18-E")
    print("LIFECYCLE GOVERNANCE CONTROL")
    print("-> OPERATIONAL INTELLIGENCE")
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
    print("===== PHASE 7-10-18-E CONTRACT TEST V2 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()
