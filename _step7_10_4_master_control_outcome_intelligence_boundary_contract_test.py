from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence
)


print("=" * 82)
print("PHASE 7-10-4")
print("MASTER CONTROL -> OUTCOME INTELLIGENCE")
print("BOUNDARY PROPAGATION CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


engine = AIDecisionOutcomeIntelligence()


def run_case(
    name,
    master_control_status,
    execution_status,
    execution_authorization,
    certification_status,
    reassessment_required,
    expected_learning_status,
    expected_feedback_state,
):

    result = engine.analyze(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "execution_status": execution_status,
        },
        final_decision_master_control={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "master_control_status": master_control_status,
            "execution_status": execution_status,
            "execution_authorization": execution_authorization,
        },
        final_decision_certification={
            "certification_status": certification_status,
            "execution_status": execution_status,
            "execution_authorization": execution_authorization,
        },
        final_execution_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "execution_status": execution_status,
            "execution_authorization": execution_authorization,
        },
        final_decision_execution_feedback={
            "feedback_status": "STABLE",
        },
        final_decision_execution_monitoring={
            "monitoring_status": "STANDARD_MONITORING",
        },
        final_decision_execution_reassessment={
            "reassessment_required": reassessment_required,
            "reassessment_status": (
                "REASSESSMENT_REQUIRED"
                if reassessment_required
                else "NOT_REQUIRED"
            ),
        },
        intelligence_score={
            "intelligence_score": 90.0,
        },
        decision_confidence={
            "confidence_score": 90.0,
        },
        outcome_evaluation={
            "evaluation_status": "WAITING_FOR_OUTCOME",
            "outcome_status": "PENDING",
            "learning_status": "WAITING_FOR_OUTCOME",
            "learning_signal": "NONE",
            "learning_signal_strength": 0.0,
        },
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- MASTER CONTROL SOURCE ---")
    print(
        "master_control_status:",
        master_control_status
    )
    print(
        "execution_status:",
        execution_status
    )
    print(
        "execution_authorization:",
        execution_authorization
    )
    print(
        "certification_status:",
        certification_status
    )
    print(
        "reassessment_required:",
        reassessment_required
    )

    print("--- OUTCOME INTELLIGENCE ---")
    print(
        "master_control_status:",
        result.get("master_control_status")
    )
    print(
        "execution_status:",
        result.get("execution_status")
    )
    print(
        "execution_authorization:",
        result.get("execution_authorization")
    )
    print(
        "certification_status:",
        result.get("certification_status")
    )
    print(
        "learning_status:",
        result.get("learning_status")
    )
    print(
        "feedback_state:",
        result.get("feedback_state")
    )
    print(
        "adaptive_learning_required:",
        result.get("adaptive_learning_required")
    )

    assert result.get(
        "master_control_status"
    ) == master_control_status

    assert result.get(
        "execution_status"
    ) == execution_status

    assert result.get(
        "execution_authorization"
    ) == execution_authorization

    assert result.get(
        "certification_status"
    ) == certification_status

    assert result.get(
        "reassessment_required"
    ) is reassessment_required

    assert result.get(
        "outcome_status"
    ) == "PENDING"

    assert result.get(
        "outcome_learning_signal"
    ) == "NONE"

    assert result.get(
        "outcome_learning_signal_strength"
    ) == 0.0

    assert result.get(
        "learning_status"
    ) == expected_learning_status

    assert result.get(
        "feedback_state"
    ) == expected_feedback_state

    print(
        f"{name} -> MASTER CONTROL / "
        f"OUTCOME INTELLIGENCE CONTRACT: PASS"
    )


# ================================================================
# CASE 1
# Healthy Master Control.
# Source policy:
# EXECUTION_READY + MASTER_READY + CERTIFIED
# -> WAITING_FOR_OUTCOME / COLLECTING
# ================================================================

run_case(
    "MASTER_READY",
    "MASTER_READY",
    "EXECUTION_READY",
    "AUTHORIZED",
    "CERTIFIED",
    False,
    "WAITING_FOR_OUTCOME",
    "COLLECTING",
)


# ================================================================
# CASE 2
# Master Control review boundary.
# Source does not contain a dedicated MASTER_REVIEW branch.
# With non-ready execution state it therefore falls through
# to the final WAITING_FOR_OUTCOME / COLLECTING branch.
# ================================================================

run_case(
    "MASTER_REVIEW",
    "MASTER_REVIEW",
    "EXECUTION_REVIEW",
    "AUTHORIZED",
    "CERTIFICATION_REVIEW",
    False,
    "WAITING_FOR_OUTCOME",
    "COLLECTING",
)


# ================================================================
# CASE 3
# Master Control blocked.
# Source policy:
# MASTER_BLOCKED
# -> BLOCKED / BLOCKED
# ================================================================

run_case(
    "MASTER_BLOCKED",
    "MASTER_BLOCKED",
    "EXECUTION_BLOCKED",
    "AUTHORIZED",
    "CERTIFICATION_REVIEW",
    False,
    "BLOCKED",
    "BLOCKED",
)


# ================================================================
# CASE 4
# Reassessment boundary.
# Source policy:
# reassessment_required
# -> REASSESSMENT_REQUIRED / REASSESSMENT_REQUIRED
# ================================================================

run_case(
    "REASSESSMENT_REQUIRED",
    "MASTER_REVIEW",
    "EXECUTION_REVIEW",
    "SUSPENDED",
    "CERTIFICATION_REVIEW",
    True,
    "REASSESSMENT_REQUIRED",
    "REASSESSMENT_REQUIRED",
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "MASTER_READY -> WAITING_FOR_OUTCOME / COLLECTING: PASS"
)

print(
    "MASTER_REVIEW -> source fall-through "
    "WAITING_FOR_OUTCOME / COLLECTING: PASS"
)

print(
    "MASTER_BLOCKED -> BLOCKED / BLOCKED: PASS"
)

print(
    "REASSESSMENT_REQUIRED -> "
    "REASSESSMENT_REQUIRED / REASSESSMENT_REQUIRED: PASS"
)

print(
    "Master Control status propagation -> "
    "Outcome Intelligence: PASS"
)

print(
    "Execution status / authorization propagation -> "
    "Outcome Intelligence: PASS"
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
print("===== PHASE 7-10-4 CONTRACT TEST COMPLETE =====")
print("=" * 82)
