from core.ai_final_decision_master_control import (
    AIFinalDecisionMasterControl
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def control(
    certification_status="CERTIFIED",
    execution_status="EXECUTION_READY",
    execution_authorization="AUTHORIZED",
    execution_readiness="READY",
    decision_integrity="INTACT",
    governance_status="APPROVED",
    lifecycle_status="HEALTHY",
    operational_status="OPERATIONALLY_HEALTHY",
    orchestration_status="ORCHESTRATION_READY",
    integrated_status="INTEGRATED_HEALTHY",
    validation_status="VALID",
    reassessment_required=False,
    certification_action="PROCEED",
):
    engine = AIFinalDecisionMasterControl()

    final_decision = {
        "decision": "ACCUMULATE",
        "action": "PROCEED",
    }

    certification = {
        "decision": "ACCUMULATE",
        "certification_status": certification_status,
        "certification_action": certification_action,
        "certification_risk": "LOW",
        "certification_score": 95.0,
        "execution_status": execution_status,
        "execution_authorization": execution_authorization,
        "execution_readiness": execution_readiness,
        "decision_integrity": decision_integrity,
    }

    execution_decision = {
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": execution_status,
        "execution_authorization": execution_authorization,
        "execution_readiness": execution_readiness,
        "execution_score": 95.0,
        "confidence_score": 95.0,
    }

    governance = {
        "governance_status": governance_status,
        "governance_score": 95.0,
    }

    lifecycle = {
        "lifecycle_status": lifecycle_status,
        "lifecycle_score": 95.0,
        "reassessment_required": reassessment_required,
    }

    operational_intelligence = {
        "operational_status": operational_status,
        "operational_score": 95.0,
    }

    orchestration = {
        "orchestration_status": orchestration_status,
        "orchestration_score": 95.0,
    }

    integrated_intelligence = {
        "integrated_status": integrated_status,
        "integrated_score": 95.0,
    }

    validation = {
        "validation_status": validation_status,
        "validation_score": 95.0,
    }

    return engine.analyze(
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


print("=" * 82)
print("PHASE 7-10-20-9")
print("FINAL DECISION CERTIFICATION -> MASTER CONTROL")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: ALL REQUIRED CONDITIONS -> MASTER READY")
print("=" * 82)

ready = control()

assert_equal(
    ready["master_control_status"],
    "MASTER_READY",
    "READY -> master control status",
)

assert_equal(
    ready["master_control_action"],
    "PROCEED",
    "READY -> master control action",
)

assert_equal(
    ready["master_control_risk"],
    "LOW",
    "READY -> master control risk",
)

assert_equal(
    ready["execution_control"],
    "EXECUTE",
    "READY -> execution control",
)


print("")
print("=" * 82)
print("CASE: CERTIFICATION BLOCKED -> MASTER BLOCKED")
print("=" * 82)

blocked = control(
    certification_status="CERTIFICATION_BLOCKED",
)

assert_equal(
    blocked["master_control_status"],
    "MASTER_BLOCKED",
    "CERTIFICATION BLOCKED -> master status",
)

assert_equal(
    blocked["master_control_action"],
    "HALT",
    "CERTIFICATION BLOCKED -> master action",
)

assert_equal(
    blocked["master_control_risk"],
    "CRITICAL",
    "CERTIFICATION BLOCKED -> master risk",
)

assert_equal(
    blocked["execution_control"],
    "HOLD",
    "CERTIFICATION BLOCKED -> execution control",
)


print("")
print("=" * 82)
print("CASE: EXECUTION BLOCKED -> MASTER BLOCKED")
print("=" * 82)

execution_blocked = control(
    execution_status="EXECUTION_BLOCKED",
)

assert_equal(
    execution_blocked["master_control_status"],
    "MASTER_BLOCKED",
    "EXECUTION BLOCKED -> master status",
)

assert_equal(
    execution_blocked["master_control_action"],
    "HALT",
    "EXECUTION BLOCKED -> master action",
)


print("")
print("=" * 82)
print("CASE: CERTIFICATION REVIEW -> MASTER REVIEW")
print("=" * 82)

review = control(
    certification_status="CERTIFICATION_REVIEW",
)

assert_equal(
    review["master_control_status"],
    "MASTER_REVIEW",
    "CERTIFICATION REVIEW -> master status",
)

assert_equal(
    review["master_control_action"],
    "REVIEW",
    "CERTIFICATION REVIEW -> master action",
)

assert_equal(
    review["master_control_risk"],
    "MEDIUM",
    "CERTIFICATION REVIEW -> master risk",
)

assert_equal(
    review["execution_control"],
    "HOLD",
    "CERTIFICATION REVIEW -> execution control",
)


print("")
print("=" * 82)
print("CASE: REASSESSMENT REQUIRED -> MASTER REVIEW")
print("=" * 82)

reassessment = control(
    reassessment_required=True,
)

assert_equal(
    reassessment["master_control_status"],
    "MASTER_REVIEW",
    "REASSESSMENT -> master status",
)

assert_equal(
    reassessment["master_control_action"],
    "REVIEW",
    "REASSESSMENT -> master action",
)


print("")
print("=" * 82)
print("CASE: MISSING READY CONDITION -> MASTER REVIEW")
print("=" * 82)

missing_ready = control(
    decision_integrity="UNKNOWN",
)

assert_equal(
    missing_ready["master_control_status"],
    "MASTER_REVIEW",
    "missing ready condition -> master status",
)

assert_equal(
    missing_ready["execution_control"],
    "HOLD",
    "missing ready condition -> execution control",
)


print("")
print("=" * 82)
print("CASE: BLOCKED PRIORITY OVER REVIEW")
print("=" * 82)

priority = control(
    certification_status="CERTIFICATION_BLOCKED",
    governance_status="WARNING",
)

assert_equal(
    priority["master_control_status"],
    "MASTER_BLOCKED",
    "BLOCKED > REVIEW priority",
)

assert_equal(
    priority["master_control_action"],
    "HALT",
    "BLOCKED > REVIEW action priority",
)


print("")
print("=" * 82)
print("CASE: MASTER SCORE USES MINIMUM")
print("=" * 82)

score_case = control()

assert_equal(
    score_case["master_control_score"],
    95.0,
    "all component scores 95 -> master score",
)

print("")
print("=" * 82)
print("===== PHASE 7-10-20-9 MASTER CONTROL BOUNDARY COMPLETE =====")
print("=" * 82)
