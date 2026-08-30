"""
PHASE 7-10-18-O-9
LIFECYCLE INTELLIGENCE
->
LIFECYCLE GOVERNANCE CONTROL
BOUNDARY CONTRACT TEST V1

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


def base_final_decision():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "validation_status": "VALID",
        "validation_score": 95,
        "confidence_score": 95,
    }


def base_governance():
    return {
        "governance_status": "APPROVED",
        "governance_score": 95,
    }


def base_control():
    return {
        "control_status": "AUTHORIZED",
        "control_risk": "LOW",
    }


def base_assurance():
    return {
        "assurance_status": "ASSURED",
        "assurance_risk": "LOW",
    }


def base_monitoring():
    return {
        "monitoring_status": "STANDARD_MONITORING",
        "monitoring_risk": "LOW",
    }


def base_feedback():
    return {
        "feedback_status": "STABLE",
        "feedback_risk": "LOW",
    }


def healthy_lifecycle():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "lifecycle_status": "HEALTHY",
        "lifecycle_action": "CONTINUE",
        "lifecycle_risk": "LOW",
        "lifecycle_score": 97.0,
        "lifecycle_grade": "A+",
    }


def reassessment_required_lifecycle():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "lifecycle_status": "REASSESSMENT_REQUIRED",
        "lifecycle_action": "REASSESS",
        "lifecycle_risk": "HIGH",
        "lifecycle_score": 70.0,
        "lifecycle_grade": "B",
    }


def critical_lifecycle():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "lifecycle_status": "REASSESSMENT_REQUIRED",
        "lifecycle_action": "HALT_AND_REASSESS",
        "lifecycle_risk": "CRITICAL",
        "lifecycle_score": 31.2,
        "lifecycle_grade": "F",
    }


def base_reassessment():
    return {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_risk": "LOW",
    }


def high_reassessment():
    return {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
        "reassessment_risk": "HIGH",
    }


def critical_reassessment():
    return {
        "reassessment_required": True,
        "reassessment_status": "CRITICAL_REASSESSMENT",
        "reassessment_risk": "CRITICAL",
    }


def run_governance(lifecycle, reassessment):
    return AIFinalDecisionLifecycleGovernanceControl().govern(
        final_decision=base_final_decision(),
        governance=base_governance(),
        execution_control=base_control(),
        execution_assurance=base_assurance(),
        execution_monitoring=base_monitoring(),
        execution_feedback=base_feedback(),
        reassessment=reassessment,
        lifecycle=lifecycle,
        decision_confidence={
            "confidence_score": 95,
        },
        validation={
            "validation_status": "VALID",
            "validation_score": 95,
        },
    )


def run_case_healthy():
    print("=" * 82)
    print("CASE: HEALTHY / LOW -> OPERATIONALLY_HEALTHY")
    print("=" * 82)

    lifecycle = healthy_lifecycle()
    result = run_governance(
        lifecycle,
        base_reassessment(),
    )

    print("governance/control:", result)

    assert_equal(
        result["decision"],
        lifecycle["decision"],
        "HEALTHY -> decision",
    )
    assert_equal(
        result["action"],
        lifecycle["action"],
        "HEALTHY -> action",
    )
    assert_equal(
        result["lifecycle_status"],
        "HEALTHY",
        "HEALTHY -> lifecycle status",
    )
    assert_equal(
        result["lifecycle_action"],
        "CONTINUE",
        "HEALTHY -> lifecycle action",
    )
    assert_equal(
        result["lifecycle_risk"],
        "LOW",
        "HEALTHY -> lifecycle risk",
    )
    assert_equal(
        result["lifecycle_score"],
        97.0,
        "HEALTHY -> lifecycle score",
    )
    assert_equal(
        result["lifecycle_grade"],
        "A+",
        "HEALTHY -> lifecycle grade",
    )
    assert_equal(
        result["operational_status"],
        "OPERATIONALLY_HEALTHY",
        "HEALTHY -> operational status",
    )
    assert_equal(
        result["operational_action"],
        "CONTINUE",
        "HEALTHY -> operational action",
    )
    assert_equal(
        result["operational_risk"],
        "LOW",
        "HEALTHY -> operational risk",
    )
    assert_equal(
        result["execution_authorization"],
        "AUTHORIZED",
        "HEALTHY -> execution authorization",
    )
    assert_equal(
        result["monitoring_policy"],
        "STANDARD",
        "HEALTHY -> monitoring policy",
    )
    assert_equal(
        result["reassessment_policy"],
        "NOT_REQUIRED",
        "HEALTHY -> reassessment policy",
    )


def run_case_reassessment():
    print("=" * 82)
    print("CASE: REASSESSMENT_REQUIRED / HIGH -> SUSPENDED")
    print("=" * 82)

    lifecycle = reassessment_required_lifecycle()
    result = run_governance(
        lifecycle,
        high_reassessment(),
    )

    print("governance/control:", result)

    assert_equal(
        result["lifecycle_status"],
        "REASSESSMENT_REQUIRED",
        "REASSESSMENT -> lifecycle status",
    )
    assert_equal(
        result["lifecycle_action"],
        "REASSESS",
        "REASSESSMENT -> lifecycle action",
    )
    assert_equal(
        result["lifecycle_risk"],
        "HIGH",
        "REASSESSMENT -> lifecycle risk",
    )
    assert_equal(
        result["lifecycle_score"],
        70.0,
        "REASSESSMENT -> lifecycle score",
    )
    assert_equal(
        result["reassessment_required"],
        True,
        "REASSESSMENT -> required",
    )
    assert_equal(
        result["reassessment_status"],
        "REASSESSMENT_REQUIRED",
        "REASSESSMENT -> status",
    )
    assert_equal(
        result["reassessment_risk"],
        "HIGH",
        "REASSESSMENT -> risk",
    )
    assert_equal(
        result["operational_status"],
        "REASSESSMENT_REQUIRED",
        "REASSESSMENT -> operational status",
    )
    assert_equal(
        result["operational_action"],
        "REASSESS",
        "REASSESSMENT -> operational action",
    )
    assert_equal(
        result["operational_risk"],
        "HIGH",
        "REASSESSMENT -> operational risk",
    )
    assert_equal(
        result["execution_authorization"],
        "SUSPENDED",
        "REASSESSMENT -> execution authorization",
    )
    assert_equal(
        result["monitoring_policy"],
        "INTENSIVE",
        "REASSESSMENT -> monitoring policy",
    )
    assert_equal(
        result["reassessment_policy"],
        "IMMEDIATE",
        "REASSESSMENT -> reassessment policy",
    )


def run_case_critical():
    print("=" * 82)
    print("CASE: CRITICAL / HALT_AND_REASSESS -> CRITICAL CONTROL")
    print("=" * 82)

    lifecycle = critical_lifecycle()
    result = run_governance(
        lifecycle,
        critical_reassessment(),
    )

    print("governance/control:", result)

    assert_equal(
        result["lifecycle_status"],
        "REASSESSMENT_REQUIRED",
        "CRITICAL -> lifecycle status",
    )
    assert_equal(
        result["lifecycle_action"],
        "HALT_AND_REASSESS",
        "CRITICAL -> lifecycle action",
    )
    assert_equal(
        result["lifecycle_risk"],
        "CRITICAL",
        "CRITICAL -> lifecycle risk",
    )
    assert_equal(
        result["lifecycle_score"],
        31.2,
        "CRITICAL -> lifecycle score",
    )
    assert_equal(
        result["reassessment_required"],
        True,
        "CRITICAL -> required",
    )
    assert_equal(
        result["reassessment_status"],
        "CRITICAL_REASSESSMENT",
        "CRITICAL -> reassessment status",
    )
    assert_equal(
        result["reassessment_risk"],
        "CRITICAL",
        "CRITICAL -> reassessment risk",
    )
    assert_equal(
        result["operational_status"],
        "REASSESSMENT_REQUIRED",
        "CRITICAL -> operational status",
    )
    assert_equal(
        result["operational_action"],
        "REASSESS",
        "CRITICAL -> operational action",
    )
    assert_equal(
        result["operational_risk"],
        "CRITICAL",
        "CRITICAL -> operational risk",
    )
    assert_equal(
        result["operational_score"],
        39.5,
        "CRITICAL -> operational score",
    )
    assert_equal(
        result["operational_grade"],
        "F",
        "CRITICAL -> operational grade",
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


def run_case_lifecycle_field_propagation():
    print("=" * 82)
    print("CASE: LIFECYCLE -> GOVERNANCE CONTROL FIELD PROPAGATION")
    print("=" * 82)

    lifecycle = healthy_lifecycle()
    result = run_governance(
        lifecycle,
        base_reassessment(),
    )

    for field in (
        "decision",
        "action",
        "lifecycle_status",
        "lifecycle_action",
        "lifecycle_risk",
        "lifecycle_score",
        "lifecycle_grade",
    ):
        assert_equal(
            result.get(field),
            lifecycle.get(field),
            f"FIELD PROPAGATION -> {field}",
        )

    print("LIFECYCLE PROPAGATION: PASS")


def run_case_reassessment_propagation():
    print("=" * 82)
    print("CASE: REASSESSMENT -> GOVERNANCE CONTROL FIELD PROPAGATION")
    print("=" * 82)

    reassessment = high_reassessment()
    result = run_governance(
        reassessment_required_lifecycle(),
        reassessment,
    )

    for field in (
        "reassessment_required",
        "reassessment_status",
        "reassessment_risk",
    ):
        assert_equal(
            result.get(field),
            reassessment.get(field),
            f"REASSESSMENT PROPAGATION -> {field}",
        )

    print("REASSESSMENT PROPAGATION: PASS")


def main():
    print("=" * 82)
    print("PHASE 7-10-18-O-9")
    print("LIFECYCLE INTELLIGENCE")
    print("-> LIFECYCLE GOVERNANCE CONTROL")
    print("BOUNDARY CONTRACT TEST V1")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    run_case_healthy()
    run_case_reassessment()
    run_case_critical()
    run_case_lifecycle_field_propagation()
    run_case_reassessment_propagation()

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
    print("=" * 82)
    print("===== PHASE 7-10-18-O-9 CONTRACT TEST V1 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()
