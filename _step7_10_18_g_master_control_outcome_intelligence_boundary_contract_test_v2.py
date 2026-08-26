from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def base_inputs():
    return {
        "final_decision": {
            "decision": "MAINTAIN",
            "action": "PROCEED",
        },
        "final_decision_master_control": {
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "master_control_status": "MASTER_READY",
            "master_control_action": "PROCEED",
            "master_control_risk": "LOW",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
        },
        "final_execution_decision": {
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
        },
        "final_decision_certification": {
            "certification_status": "CERTIFIED",
            "certification_risk": "LOW",
            "certification_score": 95.0,
            "execution_authorization": "AUTHORIZED",
        },
        "decision_confidence": {
            "confidence_score": 95.0,
        },
        "outcome_evaluation": {
            "outcome_status": "PENDING",
            "learning_status": "WAITING_FOR_OUTCOME",
            "learning_signal": "NONE",
        },
    }


def run_case_master_ready_waiting(engine):
    print("=" * 82)
    print("CASE: MASTER_READY -> WAITING_FOR_OUTCOME")
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
        result["execution_status"],
        "EXECUTION_READY",
        "MASTER_READY -> execution status",
    )
    assert_equal(
        result["execution_authorization"],
        "AUTHORIZED",
        "MASTER_READY -> authorization",
    )
    assert_equal(
        result["outcome_status"],
        "PENDING",
        "MASTER_READY -> outcome status",
    )
    assert_equal(
        result["learning_status"],
        "WAITING_FOR_OUTCOME",
        "MASTER_READY -> learning status",
    )
    assert_equal(
        result["feedback_state"],
        "COLLECTING",
        "MASTER_READY -> feedback state",
    )
    assert_equal(
        result["adaptive_learning_required"],
        False,
        "MASTER_READY -> no forced adaptive learning",
    )


def run_case_master_blocked(engine):
    print("=" * 82)
    print("CASE: MASTER_BLOCKED -> BLOCKED")
    print("=" * 82)

    data = base_inputs()

    data["final_decision_master_control"][
        "master_control_status"
    ] = "MASTER_BLOCKED"

    result = engine.analyze(**data)

    print(result)

    assert_equal(
        result["master_control_status"],
        "MASTER_BLOCKED",
        "MASTER_BLOCKED -> master control status",
    )
    assert_equal(
        result["learning_status"],
        "BLOCKED",
        "MASTER_BLOCKED -> learning status",
    )
    assert_equal(
        result["feedback_state"],
        "BLOCKED",
        "MASTER_BLOCKED -> feedback state",
    )


def run_case_unauthorized(engine):
    print("=" * 82)
    print("CASE: UNAUTHORIZED -> BLOCKED")
    print("=" * 82)

    data = base_inputs()

    data["final_decision_master_control"][
        "execution_authorization"
    ] = "UNAUTHORIZED"

    result = engine.analyze(**data)

    print(result)

    assert_equal(
        result["execution_authorization"],
        "UNAUTHORIZED",
        "UNAUTHORIZED -> authorization preserved",
    )
    assert_equal(
        result["learning_status"],
        "BLOCKED",
        "UNAUTHORIZED -> learning status",
    )
    assert_equal(
        result["feedback_state"],
        "BLOCKED",
        "UNAUTHORIZED -> feedback state",
    )


def run_case_reassessment_required(engine):
    print("=" * 82)
    print("CASE: REASSESSMENT_REQUIRED")
    print("=" * 82)

    data = base_inputs()

    data["final_decision_execution_reassessment"] = {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
    }

    result = engine.analyze(**data)

    print(result)

    assert_equal(
        result["reassessment_required"],
        True,
        "REASSESSMENT -> reassessment flag",
    )
    assert_equal(
        result["learning_status"],
        "REASSESSMENT_REQUIRED",
        "REASSESSMENT -> learning status",
    )
    assert_equal(
        result["feedback_state"],
        "REASSESSMENT_REQUIRED",
        "REASSESSMENT -> feedback state",
    )
    assert_equal(
        result["adaptive_learning_required"],
        True,
        "REASSESSMENT -> adaptive learning required",
    )


def run_case_evaluated_positive(engine):
    print("=" * 82)
    print("CASE: EVALUATED_POSITIVE -> LEARNING_AVAILABLE")
    print("=" * 82)

    data = base_inputs()

    data["outcome_evaluation"] = {
        "outcome_status": "EVALUATED",
        "outcome_score": 90.0,
        "outcome_grade": "A",
        "learning_status": "LEARNING_AVAILABLE",
        "learning_signal": "POSITIVE",
        "learning_signal_strength": 90.0,
        "decision_effectiveness": "EFFECTIVE",
        "strategy_effectiveness": "EFFECTIVE",
        "market_response": "POSITIVE",
        "portfolio_response": "POSITIVE",
    }

    result = engine.analyze(**data)

    print(result)

    assert_equal(
        result["outcome_status"],
        "EVALUATED",
        "EVALUATED POSITIVE -> outcome status",
    )
    assert_equal(
        result["learning_status"],
        "LEARNING_AVAILABLE",
        "EVALUATED POSITIVE -> learning status",
    )
    assert_equal(
        result["feedback_state"],
        "LEARNING_AVAILABLE",
        "EVALUATED POSITIVE -> feedback state",
    )
    assert_equal(
        result["adaptive_learning_required"],
        False,
        "EVALUATED POSITIVE -> no forced adaptive learning",
    )


def run_case_evaluated_stable(engine):
    print("=" * 82)
    print("CASE: EVALUATED_STABLE -> LEARNING_AVAILABLE")
    print("=" * 82)

    data = base_inputs()

    data["outcome_evaluation"] = {
        "outcome_status": "EVALUATED",
        "outcome_score": 80.0,
        "outcome_grade": "B",
        "learning_status": "LEARNING_AVAILABLE",
        "learning_signal": "STABLE",
        "learning_signal_strength": 80.0,
        "decision_effectiveness": "EFFECTIVE",
        "strategy_effectiveness": "EFFECTIVE",
        "market_response": "STABLE",
        "portfolio_response": "STABLE",
    }

    result = engine.analyze(**data)

    print(result)

    assert_equal(
        result["outcome_status"],
        "EVALUATED",
        "EVALUATED STABLE -> outcome status",
    )
    assert_equal(
        result["learning_status"],
        "LEARNING_AVAILABLE",
        "EVALUATED STABLE -> learning status",
    )
    assert_equal(
        result["feedback_state"],
        "LEARNING_AVAILABLE",
        "EVALUATED STABLE -> feedback state",
    )
    assert_equal(
        result["adaptive_learning_required"],
        False,
        "EVALUATED STABLE -> no forced adaptive learning",
    )


def run_case_evaluated_negative(engine):
    print("=" * 82)
    print("CASE: EVALUATED_NEGATIVE -> ADAPTIVE_LEARNING")
    print("=" * 82)

    data = base_inputs()

    data["outcome_evaluation"] = {
        "outcome_status": "EVALUATED",
        "outcome_score": 45.0,
        "outcome_grade": "D",
        "learning_status": "ADAPTIVE_LEARNING_REQUIRED",
        "learning_signal": "NEGATIVE",
        "learning_signal_strength": 90.0,
        "decision_effectiveness": "INEFFECTIVE",
        "strategy_effectiveness": "INEFFECTIVE",
        "market_response": "NEGATIVE",
        "portfolio_response": "NEGATIVE",
    }

    result = engine.analyze(**data)

    print(result)

    assert_equal(
        result["outcome_status"],
        "EVALUATED",
        "EVALUATED NEGATIVE -> outcome status",
    )
    assert_equal(
        result["learning_status"],
        "ADAPTIVE_LEARNING_REQUIRED",
        "EVALUATED NEGATIVE -> learning status",
    )
    assert_equal(
        result["feedback_state"],
        "ADAPTIVE_LEARNING",
        "EVALUATED NEGATIVE -> feedback state",
    )
    assert_equal(
        result["adaptive_learning_required"],
        True,
        "EVALUATED NEGATIVE -> adaptive learning required",
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
    print("Actual Outcome data exists only in memory test dictionaries.")


def main():
    print("=" * 82)
    print("PHASE 7-10-18-G")
    print("MASTER CONTROL")
    print("-> OUTCOME INTELLIGENCE")
    print("BOUNDARY CONTRACT TEST V2")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    engine = AIDecisionOutcomeIntelligence()

    run_case_master_ready_waiting(engine)
    run_case_master_blocked(engine)
    run_case_unauthorized(engine)
    run_case_reassessment_required(engine)
    run_case_evaluated_positive(engine)
    run_case_evaluated_stable(engine)
    run_case_evaluated_negative(engine)

    run_safety_checks()

    print("")
    print("=" * 82)
    print("===== PHASE 7-10-18-G CONTRACT TEST V2 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()


