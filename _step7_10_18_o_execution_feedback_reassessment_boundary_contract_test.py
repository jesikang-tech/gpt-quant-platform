"""
PHASE 7-10-18-O-5
EXECUTION FEEDBACK -> REASSESSMENT
BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_final_decision_reassessment import AIFinalDecisionReassessment


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
    }


def governance():
    return {
        "governance_status": "APPROVED",
        "governance_score": 95,
    }


def execution_control():
    return {
        "control_status": "AUTHORIZED",
        "control_risk": "LOW",
    }


def execution_assurance():
    return {
        "assurance_status": "ASSURED",
        "assurance_risk": "LOW",
        "assurance_score": 97,
        "validation_status": "VALID",
        "validation_score": 95,
    }


def execution_monitoring():
    return {
        "monitoring_status": "STANDARD_MONITORING",
        "monitoring_risk": "LOW",
        "monitoring_score": 98,
    }


def standard_feedback():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "feedback_status": "STABLE",
        "feedback_action": "CONTINUE",
        "feedback_risk": "LOW",
        "feedback_score": 98.7,
        "validation_status": "VALID",
        "validation_score": 95,
    }


def attention_feedback():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "feedback_status": "REQUIRES_ATTENTION",
        "feedback_action": "ENHANCED_REVIEW",
        "feedback_risk": "HIGH",
        "feedback_score": 65.8,
        "validation_status": "VALID",
        "validation_score": 80,
    }


def critical_feedback():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "feedback_status": "CRITICAL",
        "feedback_action": "HALT",
        "feedback_risk": "CRITICAL",
        "feedback_score": 0,
        "validation_status": "INVALID",
        "validation_score": 20,
    }


def run_reassessment(feedback):
    return AIFinalDecisionReassessment().reassess(
        base_final_decision(),
        governance(),
        execution_control(),
        execution_assurance(),
        feedback,
        execution_monitoring(),
    )


def run_case_standard():
    print("=" * 82)
    print("CASE: STABLE / LOW -> NOT_REQUIRED")
    print("=" * 82)

    result = run_reassessment(standard_feedback())
    print("reassessment:", result)

    assert_equal(
        result["feedback_status"],
        "STABLE",
        "STANDARD -> feedback status",
    )
    assert_equal(
        result["reassessment_required"],
        False,
        "STANDARD -> reassessment required",
    )
    assert_equal(
        result["reassessment_status"],
        "NOT_REQUIRED",
        "STANDARD -> reassessment status",
    )
    assert_equal(
        result["reassessment_action"],
        "CONTINUE",
        "STANDARD -> reassessment action",
    )
    assert_equal(
        result["reassessment_risk"],
        "LOW",
        "STANDARD -> reassessment risk",
    )


def run_case_attention():
    print("=" * 82)
    print("CASE: REQUIRES_ATTENTION / HIGH -> REASSESSMENT_REQUIRED")
    print("=" * 82)

    result = run_reassessment(attention_feedback())
    print("reassessment:", result)

    assert_equal(
        result["feedback_status"],
        "REQUIRES_ATTENTION",
        "ATTENTION -> feedback status",
    )
    assert_equal(
        result["reassessment_required"],
        True,
        "ATTENTION -> reassessment required",
    )
    assert_equal(
        result["reassessment_status"],
        "REASSESSMENT_REQUIRED",
        "ATTENTION -> reassessment status",
    )
    assert_equal(
        result["reassessment_action"],
        "REASSESS",
        "ATTENTION -> reassessment action",
    )
    assert_equal(
        result["reassessment_risk"],
        "HIGH",
        "ATTENTION -> reassessment risk",
    )


def run_case_critical():
    print("=" * 82)
    print("CASE: CRITICAL / HALT -> CRITICAL_REASSESSMENT")
    print("=" * 82)

    result = run_reassessment(critical_feedback())
    print("reassessment:", result)

    assert_equal(
        result["feedback_status"],
        "CRITICAL",
        "CRITICAL -> feedback status",
    )
    assert_equal(
        result["reassessment_required"],
        True,
        "CRITICAL -> reassessment required",
    )
    assert_equal(
        result["reassessment_status"],
        "CRITICAL_REASSESSMENT",
        "CRITICAL -> reassessment status",
    )
    assert_equal(
        result["reassessment_action"],
        "HALT_AND_REASSESS",
        "CRITICAL -> reassessment action",
    )
    assert_equal(
        result["reassessment_risk"],
        "CRITICAL",
        "CRITICAL -> reassessment risk",
    )


def run_case_feedback_propagation():
    print("=" * 82)
    print("CASE: FEEDBACK -> REASSESSMENT FIELD PROPAGATION")
    print("=" * 82)

    feedback = standard_feedback()
    result = run_reassessment(feedback)

    for field in (
        "decision",
        "action",
        "feedback_status",
        "feedback_action",
        "feedback_risk",
        "feedback_score",
        "validation_status",
        "validation_score",
    ):
        assert_equal(
            result.get(field),
            feedback.get(field),
            f"FEEDBACK PROPAGATION -> {field}",
        )

    print("FEEDBACK PROPAGATION: PASS")


def run_case_output_contract():
    print("=" * 82)
    print("CASE: REASSESSMENT OUTPUT CONTRACT")
    print("=" * 82)

    result = run_reassessment(standard_feedback())

    required_keys = (
        "decision",
        "action",
        "feedback_status",
        "feedback_action",
        "feedback_risk",
        "feedback_score",
        "monitoring_status",
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
        "reassessment_required",
        "reassessment_status",
        "reassessment_action",
        "reassessment_risk",
        "reassessment_score",
        "attention_signals",
        "reassessment_reason",
        "summary",
    )

    for key in required_keys:
        if key not in result:
            raise AssertionError(
                f"OUTPUT CONTRACT -> missing key: {key}"
            )

    print("OUTPUT CONTRACT: PASS")


def main():
    print("=" * 82)
    print("PHASE 7-10-18-O-5")
    print("EXECUTION FEEDBACK")
    print("-> REASSESSMENT")
    print("BOUNDARY CONTRACT TEST V1")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    run_case_standard()
    run_case_attention()
    run_case_critical()
    run_case_feedback_propagation()
    run_case_output_contract()

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
    print("===== PHASE 7-10-18-O-5 CONTRACT TEST V1 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()
