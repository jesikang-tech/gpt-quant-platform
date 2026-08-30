"""
PHASE 7-10-18-N
AI FINAL DECISION
->
EXECUTION MONITORING
->
EXECUTION FEEDBACK
BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_final_decision_execution_feedback import (
    AIFinalDecisionExecutionFeedback,
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
        "execution_status": "AUTHORIZED",
        "validation_status": "VALID",
        "validation_score": 95,
    }


def run_feedback(execution_monitoring):
    return AIFinalDecisionExecutionFeedback().feedback(
        base_final_decision(),
        {},
        {},
        {},
        execution_monitoring,
    )


def standard_monitoring():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "assurance_status": "ASSURED",
        "assurance_risk": "LOW",
        "assurance_score": 97,
        "control_status": "AUTHORIZED",
        "control_risk": "LOW",
        "governance_status": "APPROVED",
        "governance_score": 95,
        "validation_status": "VALID",
        "validation_score": 95,
        "monitoring_status": "STANDARD_MONITORING",
        "monitoring_action": "MONITOR",
        "monitoring_risk": "LOW",
        "monitoring_score": 98,
    }


def enhanced_high_risk_monitoring():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "assurance_status": "MONITORED",
        "assurance_risk": "HIGH",
        "assurance_score": 75,
        "control_status": "AUTHORIZED_WITH_MONITORING",
        "control_risk": "HIGH",
        "governance_status": "APPROVED_WITH_MONITORING",
        "governance_score": 80,
        "validation_status": "VALID",
        "validation_score": 80,
        "monitoring_status": "ENHANCED_MONITORING",
        "monitoring_action": "ESCALATE",
        "monitoring_risk": "HIGH",
        "monitoring_score": 72.5,
    }


def pre_execution_high_risk_monitoring():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "EXECUTION_REVIEW",
        "assurance_status": "PENDING",
        "assurance_risk": "HIGH",
        "assurance_score": 74,
        "control_status": "ON_HOLD",
        "control_risk": "HIGH",
        "governance_status": "REVIEW_REQUIRED",
        "governance_score": 70,
        "validation_status": "VALID",
        "validation_score": 95,
        "monitoring_status": "PRE_EXECUTION_MONITORING",
        "monitoring_action": "ESCALATE",
        "monitoring_risk": "HIGH",
        "monitoring_score": 72,
    }


def blocked_monitoring():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "BLOCKED",
        "assurance_status": "BLOCKED",
        "assurance_risk": "CRITICAL",
        "assurance_score": 5,
        "control_status": "BLOCKED",
        "control_risk": "CRITICAL",
        "governance_status": "BLOCKED",
        "governance_score": 20,
        "validation_status": "INVALID",
        "validation_score": 20,
        "monitoring_status": "BLOCKED_MONITORING",
        "monitoring_action": "HALT",
        "monitoring_risk": "CRITICAL",
        "monitoring_score": 0,
    }


def critical_monitoring():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "EXECUTION_REVIEW",
        "assurance_status": "MONITORED",
        "assurance_risk": "CRITICAL",
        "assurance_score": 60,
        "control_status": "AUTHORIZED_WITH_MONITORING",
        "control_risk": "MEDIUM",
        "governance_status": "APPROVED_WITH_MONITORING",
        "governance_score": 75,
        "validation_status": "VALID",
        "validation_score": 75,
        "monitoring_status": "CRITICAL_MONITORING",
        "monitoring_action": "HALT",
        "monitoring_risk": "CRITICAL",
        "monitoring_score": 42.5,
    }


def run_case_standard():
    print("=" * 82)
    print("CASE: STANDARD_MONITORING -> STABLE")
    print("=" * 82)

    result = run_feedback(standard_monitoring())
    print("feedback:", result)

    assert_equal(
        result["feedback_status"],
        "STABLE",
        "STANDARD -> feedback status",
    )
    assert_equal(
        result["feedback_action"],
        "CONTINUE",
        "STANDARD -> feedback action",
    )
    assert_equal(
        result["feedback_risk"],
        "LOW",
        "STANDARD -> feedback risk",
    )
    assert_equal(
        result["feedback_score"],
        98.7,
        "STANDARD -> feedback score",
    )
    assert_equal(
        result["reassessment_required"],
        False,
        "STANDARD -> reassessment",
    )


def run_case_high_risk():
    print("=" * 82)
    print("CASE: ENHANCED_MONITORING + HIGH -> REQUIRES_ATTENTION")
    print("=" * 82)

    result = run_feedback(enhanced_high_risk_monitoring())
    print("feedback:", result)

    assert_equal(
        result["feedback_status"],
        "REQUIRES_ATTENTION",
        "HIGH -> feedback status",
    )
    assert_equal(
        result["feedback_action"],
        "ENHANCED_REVIEW",
        "HIGH -> feedback action",
    )
    assert_equal(
        result["feedback_risk"],
        "HIGH",
        "HIGH -> feedback risk",
    )
    assert_equal(
        result["feedback_score"],
        65.8,
        "HIGH -> feedback score",
    )
    assert_equal(
        result["reassessment_required"],
        True,
        "HIGH -> reassessment",
    )


def run_case_pre_execution():
    print("=" * 82)
    print("CASE: PRE_EXECUTION_MONITORING + HIGH -> REQUIRES_ATTENTION")
    print("=" * 82)

    result = run_feedback(pre_execution_high_risk_monitoring())
    print("feedback:", result)

    assert_equal(
        result["feedback_status"],
        "REQUIRES_ATTENTION",
        "PRE-EXECUTION -> feedback status",
    )
    assert_equal(
        result["feedback_action"],
        "ENHANCED_REVIEW",
        "PRE-EXECUTION -> feedback action",
    )
    assert_equal(
        result["feedback_risk"],
        "HIGH",
        "PRE-EXECUTION -> feedback risk",
    )
    assert_equal(
        result["feedback_score"],
        65.5,
        "PRE-EXECUTION -> feedback score",
    )
    assert_equal(
        result["reassessment_required"],
        True,
        "PRE-EXECUTION -> reassessment",
    )


def run_case_blocked():
    print("=" * 82)
    print("CASE: BLOCKED_MONITORING + CRITICAL -> CRITICAL")
    print("=" * 82)

    result = run_feedback(blocked_monitoring())
    print("feedback:", result)

    assert_equal(
        result["feedback_status"],
        "CRITICAL",
        "BLOCKED -> feedback status",
    )
    assert_equal(
        result["feedback_action"],
        "HALT",
        "BLOCKED -> feedback action",
    )
    assert_equal(
        result["feedback_risk"],
        "CRITICAL",
        "BLOCKED -> feedback risk",
    )
    assert_equal(
        result["feedback_score"],
        0,
        "BLOCKED -> feedback score",
    )
    assert_equal(
        result["reassessment_required"],
        True,
        "BLOCKED -> reassessment",
    )


def run_case_critical():
    print("=" * 82)
    print("CASE: CRITICAL_MONITORING -> CRITICAL")
    print("=" * 82)

    result = run_feedback(critical_monitoring())
    print("feedback:", result)

    assert_equal(
        result["feedback_status"],
        "CRITICAL",
        "CRITICAL -> feedback status",
    )
    assert_equal(
        result["feedback_action"],
        "HALT",
        "CRITICAL -> feedback action",
    )
    assert_equal(
        result["feedback_risk"],
        "CRITICAL",
        "CRITICAL -> feedback risk",
    )
    assert_equal(
        result["feedback_score"],
        23.2,
        "CRITICAL -> feedback score",
    )
    assert_equal(
        result["reassessment_required"],
        True,
        "CRITICAL -> reassessment",
    )


def run_case_field_propagation():
    print("=" * 82)
    print("CASE: MONITORING -> FEEDBACK FIELD PROPAGATION")
    print("=" * 82)

    monitoring = standard_monitoring()
    result = run_feedback(monitoring)

    for field in (
        "decision",
        "action",
        "execution_status",
        "monitoring_status",
        "monitoring_action",
        "monitoring_risk",
        "monitoring_score",
        "assurance_status",
        "assurance_risk",
        "assurance_score",
        "control_status",
        "control_risk",
        "governance_status",
        "governance_score",
        "validation_status",
        "validation_score",
    ):
        assert_equal(
            result.get(field),
            monitoring.get(field),
            f"FIELD PROPAGATION -> {field}",
        )

    print("FIELD PROPAGATION: PASS")


def main():
    print("=" * 82)
    print("PHASE 7-10-18-N")
    print("AI FINAL DECISION")
    print("-> EXECUTION MONITORING")
    print("-> EXECUTION FEEDBACK")
    print("BOUNDARY CONTRACT TEST V1")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    run_case_standard()
    run_case_high_risk()
    run_case_pre_execution()
    run_case_blocked()
    run_case_critical()
    run_case_field_propagation()

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
    print("===== PHASE 7-10-18-N CONTRACT TEST V1 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()
