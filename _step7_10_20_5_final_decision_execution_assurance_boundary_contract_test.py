from core.ai_final_decision_execution_assurance import (
    AIFinalDecisionExecutionAssurance
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def assure(
    final_decision=None,
    execution_control=None,
    governance=None,
    confidence_score=95.0,
    validation_status="VALID",
    validation_score=95.0,
):
    engine = AIFinalDecisionExecutionAssurance()

    final_decision = final_decision or {
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
    }

    execution_control = execution_control or {
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "control_action": "EXECUTE",
        "control_status": "AUTHORIZED",
        "control_risk": "LOW",
        "execution_readiness": "READY",
        "governance_status": "APPROVED",
        "governance_score": 95.0,
        "integrity_status": "INTACT",
        "risk_governance": "ACCEPTABLE",
        "confidence_score": confidence_score,
        "validation_status": validation_status,
        "validation_score": validation_score,
        "monitoring_policy": "STANDARD",
    }

    governance = governance or {
        "governance_status": "APPROVED",
        "governance_score": 95.0,
        "integrity_status": "INTACT",
        "execution_readiness": "READY",
        "risk_governance": "ACCEPTABLE",
    }

    return engine.assure(
        final_decision=final_decision,
        governance=governance,
        execution_control=execution_control,
    )



print("=" * 82)
print("PHASE 7-10-20-5")
print("FINAL DECISION -> EXECUTION ASSURANCE")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: FULLY AUTHORIZED FINAL DECISION -> ASSURED")
print("=" * 82)

assured = assure()

assert_equal(
    assured["decision"],
    "ACCUMULATE",
    "ASSURED -> decision propagation",
)

assert_equal(
    assured["execution_status"],
    "AUTHORIZED",
    "ASSURED -> execution status",
)

assert_equal(
    assured["assurance_status"],
    "ASSURED",
    "ASSURED -> assurance status",
)

assert_equal(
    assured["assurance_level"],
    "HIGH",
    "ASSURED -> assurance level",
)

assert_equal(
    assured["assurance_risk"],
    "LOW",
    "ASSURED -> assurance risk",
)

assert_equal(
    assured["monitoring_status"],
    "STANDARD_MONITORING",
    "ASSURED -> standard monitoring",
)

assert_equal(
    assured["assurance_score"],
    97.0,
    "ASSURED -> assurance score",
)


print("")
print("=" * 82)
print("CASE: BLOCK CONTROL -> BLOCKED")
print("=" * 82)

blocked = assure(
    execution_control={
        "decision": "ACCUMULATE",
        "action": "BLOCK",
        "control_action": "BLOCK",
        "execution_status": "BLOCKED",
        "control_status": "BLOCKED",
        "control_risk": "CRITICAL",
        "execution_readiness": "BLOCKED",
    }
)

assert_equal(
    blocked["assurance_status"],
    "BLOCKED",
    "BLOCK -> assurance status",
)

assert_equal(
    blocked["assurance_level"],
    "NONE",
    "BLOCK -> assurance level",
)

assert_equal(
    blocked["assurance_risk"],
    "CRITICAL",
    "BLOCK -> assurance risk",
)

assert_equal(
    blocked["monitoring_status"],
    "MONITORING_SUSPENDED",
    "BLOCK -> monitoring suspended",
)


print("")
print("=" * 82)
print("CASE: HOLD CONTROL -> PENDING")
print("=" * 82)

pending = assure(
    execution_control={
        "decision": "MAINTAIN",
        "action": "HOLD",
        "control_action": "HOLD",
        "execution_status": "PENDING",
        "control_status": "AUTHORIZED",
        "control_risk": "MEDIUM",
        "execution_readiness": "READY",
    }
)

assert_equal(
    pending["assurance_status"],
    "PENDING",
    "HOLD -> assurance status",
)

assert_equal(
    pending["assurance_level"],
    "LOW",
    "HOLD -> assurance level",
)

assert_equal(
    pending["assurance_risk"],
    "HIGH",
    "HOLD -> assurance risk",
)

assert_equal(
    pending["monitoring_status"],
    "PRE_EXECUTION_MONITORING",
    "HOLD -> pre-execution monitoring",
)


print("")
print("=" * 82)
print("CASE: INVALID VALIDATION -> BLOCKED")
print("=" * 82)

invalid = assure(
    validation_status="INVALID",
    validation_score=40.0,
)

assert_equal(
    invalid["assurance_status"],
    "BLOCKED",
    "INVALID -> assurance status",
)

assert_equal(
    invalid["assurance_level"],
    "NONE",
    "INVALID -> assurance level",
)

assert_equal(
    invalid["assurance_risk"],
    "CRITICAL",
    "INVALID -> assurance risk",
)


print("")
print("=" * 82)
print("CASE: ASSURANCE THRESHOLD")
print("=" * 82)

threshold = assure(
    confidence_score=90.0,
    validation_score=90.0,
    governance={
        "governance_status": "APPROVED",
        "integrity_status": "INTACT",
        "risk_governance": "ACCEPTABLE",
        "governance_score": 90.0,
    },
)

assert_equal(
    threshold["assurance_status"],
    "ASSURED",
    "90/90/90 -> assurance threshold",
)

assert_equal(
    threshold["assurance_score"],
    94.0,
    "95/90/90 -> assurance score",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-5 EXECUTION ASSURANCE BOUNDARY COMPLETE =====")
print("=" * 82)




