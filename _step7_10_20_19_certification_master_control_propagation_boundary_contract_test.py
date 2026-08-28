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
    certification_action="PROCEED",
    certification_risk="LOW",
    certification_score=95.0,
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
):
    engine = AIFinalDecisionMasterControl()

    final_decision = {
        "decision": "MAINTAIN",
        "action": "PROCEED",
    }

    certification = {
        "decision": "MAINTAIN",
        "certification_status": certification_status,
        "certification_action": certification_action,
        "certification_risk": certification_risk,
        "certification_score": certification_score,
        "execution_status": execution_status,
        "execution_authorization": execution_authorization,
        "execution_readiness": execution_readiness,
        "decision_integrity": decision_integrity,
    }

    execution_decision = {
        "decision": "MAINTAIN",
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
print("PHASE 7-10-20-19")
print("FINAL DECISION CERTIFICATION -> MASTER CONTROL")
print("PROPAGATION BOUNDARY CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: CERTIFICATION ACTION PROCEED -> MASTER PROCEED")
print("=" * 82)

result = control(
    certification_action="PROCEED",
)

assert_equal(
    result["action"],
    "PROCEED",
    "certification action -> master action",
)
assert_equal(
    result["master_control_status"],
    "MASTER_READY",
    "certified -> master ready",
)
assert_equal(
    result["execution_control"],
    "EXECUTE",
    "certified -> execute",
)


print("")
print("=" * 82)
print("CASE: CERTIFICATION ACTION REVIEW -> MASTER REVIEW")
print("=" * 82)

result = control(
    certification_status="CERTIFICATION_REVIEW",
    certification_action="REVIEW",
)

assert_equal(
    result["action"],
    "REVIEW",
    "certification review action -> master action",
)
assert_equal(
    result["master_control_status"],
    "MASTER_REVIEW",
    "certification review -> master review",
)
assert_equal(
    result["execution_control"],
    "HOLD",
    "certification review -> hold",
)


print("")
print("=" * 82)
print("CASE: CERTIFICATION BLOCKED -> MASTER HALT")
print("=" * 82)

result = control(
    certification_status="CERTIFICATION_BLOCKED",
    certification_action="HALT",
    certification_risk="CRITICAL",
)

assert_equal(
    result["action"],
    "HALT",
    "certification halt -> master action",
)
assert_equal(
    result["master_control_status"],
    "MASTER_BLOCKED",
    "certification blocked -> master blocked",
)
assert_equal(
    result["master_control_risk"],
    "CRITICAL",
    "certification blocked -> critical risk",
)
assert_equal(
    result["execution_control"],
    "HOLD",
    "certification blocked -> hold",
)


print("")
print("=" * 82)
print("CASE: CERTIFICATION SCORE -> MASTER MINIMUM SCORE")
print("=" * 82)

result = control(
    certification_score=70.0,
)

assert_equal(
    result["master_control_score"],
    70.0,
    "certification score -> master minimum score",
)
assert_equal(
    result["certification_score"],
    70.0,
    "certification score -> preserved",
)


print("")
print("=" * 82)
print("CASE: EXECUTION READINESS NOT READY -> MASTER REVIEW")
print("=" * 82)

result = control(
    execution_readiness="NOT_READY",
)

assert_equal(
    result["master_control_status"],
    "MASTER_REVIEW",
    "not ready -> master review",
)
assert_equal(
    result["master_control_action"],
    "REVIEW",
    "not ready -> review action",
)
assert_equal(
    result["execution_control"],
    "HOLD",
    "not ready -> hold",
)


print("")
print("=" * 82)
print("CASE: DECISION INTEGRITY REVIEW -> MASTER REVIEW")
print("=" * 82)

result = control(
    decision_integrity="REVIEW_REQUIRED",
)

assert_equal(
    result["master_control_status"],
    "MASTER_REVIEW",
    "integrity review -> master review",
)
assert_equal(
    result["master_control_action"],
    "REVIEW",
    "integrity review -> review action",
)
assert_equal(
    result["execution_control"],
    "HOLD",
    "integrity review -> hold",
)


print("")
print("=" * 82)
print("CASE: CERTIFICATION RISK PRESERVED")
print("=" * 82)

result = control(
    certification_risk="MEDIUM",
)

assert_equal(
    result["certification_risk"],
    "MEDIUM",
    "certification risk -> preserved",
)
assert_equal(
    result["master_control_status"],
    "MASTER_READY",
    "certification risk alone -> no fabricated block",
)


print("")
print("=" * 82)
print("CASE: EMPTY CERTIFICATION -> SAFE DEFAULTS")
print("=" * 82)

engine = AIFinalDecisionMasterControl()

result = engine.analyze(
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
)

assert_equal(
    result["decision"],
    None,
    "empty certification chain -> unknown decision",
)
assert_equal(
    result["action"],
    "HOLD",
    "empty certification chain -> hold",
)
assert_equal(
    result["master_control_status"],
    "MASTER_BLOCKED",
    "empty certification chain -> blocked",
)
assert_equal(
    result["execution_control"],
    "HOLD",
    "empty certification chain -> hold",
)


print("")
print("=" * 82)
print("CASE: LEARNING FIELDS NOT FABRICATED")
print("=" * 82)

result = control()

assert_equal(
    "learning_signal" in result,
    False,
    "learning signal -> not fabricated",
)
assert_equal(
    "learning_strength" in result,
    False,
    "learning strength -> not fabricated",
)
assert_equal(
    "adaptive_learning_required" in result,
    False,
    "adaptive learning requirement -> not fabricated",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-19 CERTIFICATION -> MASTER CONTROL COMPLETE =====")
print("=" * 82)
