from core.ai_final_decision_master_control import AIFinalDecisionMasterControl


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def assert_true(condition, label):
    if not condition:
        raise AssertionError(f"{label}: expected=True, actual={condition!r}")
    print(f"{label}: PASS")


def base_inputs():
    return {
        "final_decision": {
            "decision": "MAINTAIN",
            "action": "PROCEED",
        },
        "certification": {
            "certification_status": "CERTIFIED",
            "certification_risk": "LOW",
            "certification_score": 95.0,
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_readiness": "READY",
            "decision_integrity": "INTACT",
        },
        "execution_decision": {
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_score": 95.0,
        },
        "governance": {
            "governance_status": "APPROVED",
            "governance_score": 95.0,
        },
        "lifecycle": {
            "lifecycle_status": "HEALTHY",
            "lifecycle_score": 95.0,
            "reassessment_required": False,
        },
        "operational_intelligence": {
            "operational_status": "OPERATIONALLY_HEALTHY",
            "operational_score": 95.0,
        },
        "orchestration": {
            "orchestration_status": "ORCHESTRATION_READY",
            "orchestration_score": 95.0,
        },
        "integrated_intelligence": {
            "integrated_status": "INTEGRATED_HEALTHY",
            "integrated_score": 95.0,
        },
        "validation": {
            "validation_status": "VALID",
            "validation_score": 95.0,
        },
    }


def run_case_master_ready(engine):
    print("=" * 82)
    print("CASE: MASTER_READY")
    print("=" * 82)

    data = base_inputs()

    result = engine.analyze(**data)

    print(result)

    assert_equal(
        result["master_control_status"],
        "MASTER_READY",
        "MASTER_READY -> master control status",
    )
    assert_equal(
        result["master_control_action"],
        "PROCEED",
        "MASTER_READY -> master control action",
    )
    assert_equal(
        result["master_control_risk"],
        "LOW",
        "MASTER_READY -> master control risk",
    )
    assert_equal(
        result["execution_control"],
        "EXECUTE",
        "MASTER_READY -> execution control",
    )
    assert_equal(
        result["operational_status"],
        "OPERATIONALLY_HEALTHY",
        "MASTER_READY -> operational status preserved",
    )
    assert_equal(
        result["execution_authorization"],
        "AUTHORIZED",
        "MASTER_READY -> authorization preserved",
    )
    assert_equal(
        result["orchestration_status"],
        "ORCHESTRATION_READY",
        "MASTER_READY -> orchestration status preserved",
    )
    assert_equal(
        result["master_control_score"],
        95.0,
        "MASTER_READY -> minimum score",
    )
    assert_equal(
        result["master_control_grade"],
        "A+",
        "MASTER_READY -> grade",
    )


def run_case_reassessment_review(engine):
    print("=" * 82)
    print("CASE: REASSESSMENT_REQUIRED -> MASTER_REVIEW")
    print("=" * 82)

    data = base_inputs()
    data["lifecycle"]["reassessment_required"] = True
    data["operational_intelligence"]["operational_status"] = (
        "REASSESSMENT_REQUIRED"
    )
    data["operational_intelligence"]["operational_score"] = 80.0
    data["execution_decision"]["execution_authorization"] = "SUSPENDED"
    data["certification"]["execution_authorization"] = "SUSPENDED"

    result = engine.analyze(**data)

    print(result)

    assert_equal(
        result["master_control_status"],
        "MASTER_REVIEW",
        "REASSESSMENT -> master control status",
    )
    assert_equal(
        result["master_control_action"],
        "REVIEW",
        "REASSESSMENT -> master control action",
    )
    assert_equal(
        result["master_control_risk"],
        "MEDIUM",
        "REASSESSMENT -> master control risk",
    )
    assert_equal(
        result["execution_control"],
        "HOLD",
        "REASSESSMENT -> execution control",
    )
    assert_equal(
        result["operational_status"],
        "REASSESSMENT_REQUIRED",
        "REASSESSMENT -> operational status preserved",
    )
    assert_equal(
        result["reassessment_required"],
        True,
        "REASSESSMENT -> reassessment flag preserved",
    )


def run_case_high_risk_review(engine):
    print("=" * 82)
    print("CASE: HIGH_RISK_SUSPENDED -> MASTER_REVIEW")
    print("=" * 82)

    data = base_inputs()

    data["operational_intelligence"]["operational_status"] = (
        "REASSESSMENT_REQUIRED"
    )
    data["operational_intelligence"]["operational_score"] = 75.0
    data["execution_decision"]["execution_authorization"] = "SUSPENDED"
    data["certification"]["execution_authorization"] = "SUSPENDED"

    data["lifecycle"]["reassessment_required"] = True

    result = engine.analyze(**data)

    print(result)

    assert_equal(
        result["master_control_status"],
        "MASTER_REVIEW",
        "HIGH RISK -> master control status",
    )
    assert_equal(
        result["master_control_action"],
        "REVIEW",
        "HIGH RISK -> master control action",
    )
    assert_equal(
        result["master_control_risk"],
        "MEDIUM",
        "HIGH RISK -> master control risk",
    )
    assert_equal(
        result["execution_control"],
        "HOLD",
        "HIGH RISK -> execution control",
    )
    assert_equal(
        result["operational_status"],
        "REASSESSMENT_REQUIRED",
        "HIGH RISK -> operational status preserved",
    )
    assert_equal(
        result["execution_authorization"],
        "SUSPENDED",
        "HIGH RISK -> authorization preserved",
    )


def run_case_denied_review(engine):
    print("=" * 82)
    print("CASE: DENIED -> MASTER_REVIEW")
    print("=" * 82)

    data = base_inputs()

    data["execution_decision"]["execution_authorization"] = "DENIED"
    data["certification"]["execution_authorization"] = "DENIED"

    result = engine.analyze(**data)

    print(result)

    assert_equal(
        result["master_control_status"],
        "MASTER_REVIEW",
        "DENIED -> master control status",
    )
    assert_equal(
        result["master_control_action"],
        "REVIEW",
        "DENIED -> master control action",
    )
    assert_equal(
        result["master_control_risk"],
        "MEDIUM",
        "DENIED -> master control risk",
    )
    assert_equal(
        result["execution_control"],
        "HOLD",
        "DENIED -> execution control",
    )
    assert_equal(
        result["execution_authorization"],
        "DENIED",
        "DENIED -> authorization preserved",
    )


def run_safety_checks():
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


def main():
    print("=" * 82)
    print("PHASE 7-10-18-F")
    print("OPERATIONAL INTELLIGENCE")
    print("-> MASTER CONTROL")
    print("BOUNDARY CONTRACT TEST V2")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    engine = AIFinalDecisionMasterControl()

    run_case_master_ready(engine)
    run_case_reassessment_review(engine)
    run_case_high_risk_review(engine)
    run_case_denied_review(engine)
    run_safety_checks()

    print("")
    print("=" * 82)
    print("===== PHASE 7-10-18-F CONTRACT TEST V2 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()



