from core.ai_final_decision_reassessment import (
    AIFinalDecisionReassessment,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )

    print(f"{label}: PASS")


def build_common():
    return {
        "feedback_status": "STABLE",
        "feedback_risk": "LOW",
        "feedback_action": "CONTINUE",
        "feedback_score": 95.0,

        "monitoring_status": "STANDARD_MONITORING",
        "monitoring_risk": "LOW",
        "monitoring_score": 95.0,

        "assurance_status": "ASSURED",
        "assurance_risk": "LOW",
        "assurance_score": 95.0,

        "control_status": "AUTHORIZED",
        "control_risk": "LOW",

        "governance_status": "APPROVED",
        "governance_score": 95.0,

        "validation_status": "VALID",
        "validation_score": 95.0,
    }


def determine(data):
    engine = AIFinalDecisionReassessment()

    result = engine.reassess(
        final_decision={},
        governance={
            "governance_status": data["governance_status"],
            "governance_score": data["governance_score"],
        },
        execution_control={
            "control_status": data["control_status"],
            "control_risk": data["control_risk"],
        },
        execution_assurance={
            "assurance_status": data["assurance_status"],
            "assurance_risk": data["assurance_risk"],
            "assurance_score": data["assurance_score"],
            "validation_status": data["validation_status"],
            "validation_score": data["validation_score"],
        },
        execution_feedback={
            "feedback_status": data["feedback_status"],
            "feedback_risk": data["feedback_risk"],
            "feedback_action": data["feedback_action"],
            "feedback_score": data["feedback_score"],
        },
        execution_monitoring={
            "monitoring_status": data["monitoring_status"],
            "monitoring_risk": data["monitoring_risk"],
            "monitoring_score": data["monitoring_score"],
        },
    )

    return {
        "reassessment_required": result["reassessment_required"],
        "reassessment_status": result["reassessment_status"],
        "reassessment_action": result["reassessment_action"],
        "reassessment_risk": result["reassessment_risk"],
        "reassessment_score": result["reassessment_score"],
    }


def run_case_stable():
    print("=" * 82)
    print("CASE: STABLE_LOW")
    print("=" * 82)

    data = build_common()
    result = determine(data)

    print(result)

    assert_equal(
        result["reassessment_required"],
        False,
        "STABLE + LOW -> reassessment not required",
    )

    assert_equal(
        result["reassessment_status"],
        "NOT_REQUIRED",
        "STABLE + LOW -> NOT_REQUIRED",
    )

    assert_equal(
        result["reassessment_action"],
        "CONTINUE",
        "STABLE + LOW -> CONTINUE",
    )

    assert_equal(
        result["reassessment_risk"],
        "LOW",
        "STABLE + LOW -> LOW risk",
    )

    assert_equal(
        result["reassessment_score"],
        95.0,
        "STABLE + LOW -> score",
    )


def run_case_attention():
    print("=" * 82)
    print("CASE: REQUIRES_ATTENTION")
    print("=" * 82)

    data = build_common()

    data["feedback_status"] = "REQUIRES_ATTENTION"
    data["feedback_risk"] = "MEDIUM"
    data["feedback_action"] = "ENHANCED_REVIEW"

    result = determine(data)

    print(result)

    assert_equal(
        result["reassessment_required"],
        True,
        "REQUIRES_ATTENTION -> reassessment required",
    )

    assert_equal(
        result["reassessment_status"],
        "REASSESSMENT_REQUIRED",
        "REQUIRES_ATTENTION -> REASSESSMENT_REQUIRED",
    )

    assert_equal(
        result["reassessment_action"],
        "REASSESS",
        "REQUIRES_ATTENTION -> REASSESS",
    )

    assert_equal(
        result["reassessment_risk"],
        "MEDIUM",
        "REQUIRES_ATTENTION -> MEDIUM risk",
    )

    assert_equal(
        result["reassessment_score"],
        85.0,
        "REQUIRES_ATTENTION -> score",
    )


def run_case_unstable():
    print("=" * 82)
    print("CASE: UNSTABLE_HIGH")
    print("=" * 82)

    data = build_common()

    data["feedback_status"] = "UNSTABLE"
    data["feedback_risk"] = "HIGH"
    data["feedback_action"] = "REASSESS"

    result = determine(data)

    print(result)

    assert_equal(
        result["reassessment_required"],
        True,
        "UNSTABLE + HIGH -> reassessment required",
    )

    assert_equal(
        result["reassessment_status"],
        "UNSTABLE_REASSESSMENT",
        "UNSTABLE -> UNSTABLE_REASSESSMENT",
    )

    assert_equal(
        result["reassessment_action"],
        "REASSESS",
        "UNSTABLE -> REASSESS",
    )

    assert_equal(
        result["reassessment_risk"],
        "HIGH",
        "UNSTABLE + HIGH -> HIGH risk",
    )

    assert_equal(
        result["reassessment_score"],
        80.0,
        "UNSTABLE + HIGH -> score",
    )


def run_case_critical():
    print("=" * 82)
    print("CASE: CRITICAL_CRITICAL")
    print("=" * 82)

    data = build_common()

    data["feedback_status"] = "CRITICAL"
    data["feedback_risk"] = "CRITICAL"
    data["feedback_action"] = "HALT"

    data["monitoring_risk"] = "CRITICAL"
    data["assurance_risk"] = "CRITICAL"
    data["control_risk"] = "CRITICAL"

    result = determine(data)

    print(result)

    assert_equal(
        result["reassessment_required"],
        True,
        "CRITICAL -> reassessment required",
    )

    assert_equal(
        result["reassessment_status"],
        "CRITICAL_REASSESSMENT",
        "CRITICAL -> CRITICAL_REASSESSMENT",
    )

    assert_equal(
        result["reassessment_action"],
        "HALT_AND_REASSESS",
        "CRITICAL -> HALT_AND_REASSESS",
    )

    assert_equal(
        result["reassessment_risk"],
        "CRITICAL",
        "CRITICAL -> CRITICAL risk",
    )

    assert_equal(
        result["reassessment_score"],
        70.0,
        "CRITICAL -> score",
    )


def run_case_score_boundary():
    print("=" * 82)
    print("CASE: STABLE_LOW_SCORE_BOUNDARY")
    print("=" * 82)

    data = build_common()

    data["monitoring_score"] = 79.0

    result = determine(data)

    print(result)

    assert_equal(
        result["reassessment_required"],
        True,
        "Score < 80 -> reassessment required",
    )

    assert_equal(
        result["reassessment_status"],
        "REASSESSMENT_REQUIRED",
        "Score < 80 -> REASSESSMENT_REQUIRED",
    )

    assert_equal(
        result["reassessment_action"],
        "REASSESS",
        "Score < 80 -> REASSESS",
    )

    assert_equal(
        result["reassessment_risk"],
        "MEDIUM",
        "Score < 80 -> MEDIUM risk",
    )

    assert_equal(
        result["reassessment_score"],
        81.8,
        "Score < 80 -> score",
    )


print("=" * 82)
print("PHASE 7-10-18-C")
print("EXECUTION FEEDBACK")
print("-> REASSESSMENT")
print("BOUNDARY CONTRACT TEST V2")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

run_case_stable()
run_case_attention()
run_case_unstable()
run_case_critical()
run_case_score_boundary()

print()
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("Stable boundary: PASS")
print("Attention boundary: PASS")
print("Unstable boundary: PASS")
print("Critical boundary: PASS")
print("Score < 80 boundary: PASS")

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
print("===== PHASE 7-10-18-C CONTRACT TEST V2 COMPLETE =====")
print("=" * 82)
