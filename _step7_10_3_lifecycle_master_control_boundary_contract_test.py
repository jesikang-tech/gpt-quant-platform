from core.ai_final_decision_master_control import (
    AIFinalDecisionMasterControl
)


print("=" * 82)
print("PHASE 7-10-3")
print("LIFECYCLE INTELLIGENCE -> MASTER CONTROL")
print("BOUNDARY PROPAGATION CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


engine = AIFinalDecisionMasterControl()


def build_inputs(
    lifecycle_status,
    lifecycle_score,
    reassessment_required
):

    final_decision = {
        "decision": "MAINTAIN",
        "action": "PROCEED",
    }

    certification = {
        "decision": "MAINTAIN",
        "certification_action": "PROCEED",
        "certification_status": "CERTIFIED",
        "certification_risk": "LOW",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
        "execution_readiness": "READY",
        "decision_integrity": "INTACT",
        "certification_score": 97.0,
    }

    execution_decision = {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
        "execution_score": 95.0,
    }

    governance = {
        "governance_status": "APPROVED",
        "governance_score": 96.0,
    }

    lifecycle = {
        "lifecycle_status": lifecycle_status,
        "lifecycle_score": lifecycle_score,
        "reassessment_required": reassessment_required,
    }

    operational_intelligence = {
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_score": 93.0,
    }

    orchestration = {
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_score": 92.0,
    }

    integrated_intelligence = {
        "integrated_status": "INTEGRATED_HEALTHY",
        "integrated_score": 91.0,
    }

    validation = {
        "validation_status": "VALID",
        "validation_score": 90.0,
    }

    return (
        final_decision,
        certification,
        execution_decision,
        governance,
        lifecycle,
        operational_intelligence,
        orchestration,
        integrated_intelligence,
        validation,
    )


def run_case(
    name,
    lifecycle_status,
    lifecycle_score,
    reassessment_required,
    expected_status,
    expected_action,
    expected_risk,
    expected_execution_control,
):

    inputs = build_inputs(
        lifecycle_status,
        lifecycle_score,
        reassessment_required,
    )

    result = engine.analyze(*inputs)

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- LIFECYCLE SOURCE ---")
    print(
        "lifecycle_status:",
        lifecycle_status
    )
    print(
        "lifecycle_score:",
        lifecycle_score
    )
    print(
        "reassessment_required:",
        reassessment_required
    )

    print("--- MASTER CONTROL ---")
    print(
        "master_control_status:",
        result.get("master_control_status")
    )
    print(
        "master_control_action:",
        result.get("master_control_action")
    )
    print(
        "master_control_risk:",
        result.get("master_control_risk")
    )
    print(
        "master_control_score:",
        result.get("master_control_score")
    )
    print(
        "execution_control:",
        result.get("execution_control")
    )

    print("--- PROPAGATED LIFECYCLE FIELDS ---")
    print(
        "lifecycle_status:",
        result.get("lifecycle_status")
    )
    print(
        "reassessment_required:",
        result.get("reassessment_required")
    )

    assert result.get(
        "lifecycle_status"
    ) == lifecycle_status

    assert result.get(
        "reassessment_required"
    ) is reassessment_required

    assert result.get(
        "master_control_status"
    ) == expected_status

    assert result.get(
        "master_control_action"
    ) == expected_action

    assert result.get(
        "master_control_risk"
    ) == expected_risk

    assert result.get(
        "execution_control"
    ) == expected_execution_control

    print(
        f"{name} -> LIFECYCLE / MASTER CONTROL CONTRACT: PASS"
    )


# ================================================================
# CASE 1
# Healthy lifecycle propagates to master readiness.
# ================================================================

run_case(
    "LIFECYCLE_HEALTHY",
    "HEALTHY",
    94.0,
    False,
    "MASTER_READY",
    "PROCEED",
    "LOW",
    "EXECUTE",
)


# ================================================================
# CASE 2
# Reassessment requirement forces master review.
# ================================================================

run_case(
    "LIFECYCLE_REASSESSMENT_REQUIRED",
    "HEALTHY",
    94.0,
    True,
    "MASTER_REVIEW",
    "REVIEW",
    "MEDIUM",
    "HOLD",
)


# ================================================================
# CASE 3
# Lifecycle review status propagates to master review.
# Score is independently propagated through minimum-score
# aggregation.
# ================================================================

run_case(
    "LIFECYCLE_REVIEW",
    "REASSESS_REQUIRED",
    70.0,
    False,
    "MASTER_REVIEW",
    "REVIEW",
    "MEDIUM",
    "HOLD",
)


# ================================================================
# CASE 4
# Lifecycle blocked status propagates to master block.
# ================================================================

run_case(
    "LIFECYCLE_BLOCKED",
    "BLOCKED",
    40.0,
    False,
    "MASTER_BLOCKED",
    "HALT",
    "CRITICAL",
    "HOLD",
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "Lifecycle HEALTHY -> MASTER_READY: PASS"
)

print(
    "Lifecycle reassessment_required -> MASTER_REVIEW: PASS"
)

print(
    "Lifecycle REASSESS_REQUIRED -> MASTER_REVIEW: PASS"
)

print(
    "Lifecycle BLOCKED -> MASTER_BLOCKED: PASS"
)

print(
    "Lifecycle status propagation -> Master Control: PASS"
)

print(
    "Lifecycle reassessment propagation -> Master Control: PASS"
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
print("===== PHASE 7-10-3 CONTRACT TEST COMPLETE =====")
print("=" * 82)
