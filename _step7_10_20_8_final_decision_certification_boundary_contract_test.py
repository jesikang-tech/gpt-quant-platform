from core.ai_final_decision_certification import (
    AIFinalDecisionCertification
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def certify(
    statuses,
    action="PROCEED",
):
    engine = AIFinalDecisionCertification()

    final_decision = {
        "decision": "ACCUMULATE",
        "action": action,
    }

    validation = {
        "validation_status": statuses.get(
            "Decision Validation",
            "VALID"
        ),
        "validation_score": 95.0,
    }

    governance = {
        "governance_status": statuses.get(
            "Governance",
            "APPROVED"
        ),
        "governance_score": 95.0,
    }

    lifecycle = {
        "lifecycle_status": statuses.get(
            "Lifecycle",
            "HEALTHY"
        ),
        "lifecycle_score": 95.0,
    }

    operational_intelligence = {
        "operational_status": statuses.get(
            "Operational Intelligence",
            "OPERATIONALLY_HEALTHY"
        ),
        "operational_score": 95.0,
    }

    integrated_intelligence = {
        "integrated_status": statuses.get(
            "Integrated Intelligence",
            "INTEGRATED_HEALTHY"
        ),
        "integrated_score": 95.0,
    }

    orchestration = {
        "orchestration_status": statuses.get(
            "Orchestration",
            "ORCHESTRATION_READY"
        ),
        "orchestration_score": 95.0,
    }

    execution_decision = {
        "execution_status": statuses.get(
            "Execution Decision",
            "EXECUTION_READY"
        ),
        "execution_authorization": "AUTHORIZED",
        "decision": "ACCUMULATE",
        "action": action,
    }

    return engine.analyze(
        final_decision,
        validation,
        governance,
        lifecycle,
        operational_intelligence,
        integrated_intelligence,
        orchestration,
        execution_decision,
    )


print("=" * 82)
print("PHASE 7-10-20-8")
print("FINAL EXECUTION DECISION -> FINAL DECISION CERTIFICATION")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: ALL REQUIRED HEALTHY -> CERTIFIED")
print("=" * 82)

certified = certify({})

assert_equal(
    certified["certification_status"],
    "CERTIFIED",
    "CERTIFIED -> certification status",
)

assert_equal(
    certified["certification_action"],
    "PROCEED",
    "CERTIFIED -> certification action",
)

assert_equal(
    certified["execution_status"],
    "EXECUTION_READY",
    "CERTIFIED -> execution status",
)

assert_equal(
    certified["decision_integrity"],
    "INTACT",
    "CERTIFIED -> decision integrity",
)


print("")
print("=" * 82)
print("CASE: EXECUTION BLOCKED -> CERTIFICATION BLOCKED")
print("=" * 82)

blocked = certify({
    "Execution Decision": "EXECUTION_BLOCKED",
})

assert_equal(
    blocked["certification_status"],
    "CERTIFICATION_BLOCKED",
    "EXECUTION BLOCKED -> certification status",
)

assert_equal(
    blocked["certification_action"],
    "HALT",
    "EXECUTION BLOCKED -> certification action",
)


print("")
print("=" * 82)
print("CASE: UNAUTHORIZED -> CERTIFICATION BLOCKED")
print("=" * 82)

unauthorized = certify({
    "Execution Decision": "UNAUTHORIZED",
})

assert_equal(
    unauthorized["certification_status"],
    "CERTIFICATION_BLOCKED",
    "UNAUTHORIZED -> certification status",
)

assert_equal(
    unauthorized["certification_action"],
    "HALT",
    "UNAUTHORIZED -> certification action",
)


print("")
print("=" * 82)
print("CASE: WARNING -> CERTIFICATION REVIEW")
print("=" * 82)

warning = certify({
    "Operational Intelligence": "WARNING",
})

assert_equal(
    warning["certification_status"],
    "CERTIFICATION_REVIEW",
    "WARNING -> certification status",
)

assert_equal(
    warning["certification_action"],
    "REVIEW",
    "WARNING -> certification action",
)


print("")
print("=" * 82)
print("CASE: UNKNOWN -> CERTIFICATION REVIEW")
print("=" * 82)

unknown = certify({
    "Orchestration": "UNKNOWN",
})

assert_equal(
    unknown["certification_status"],
    "CERTIFICATION_REVIEW",
    "UNKNOWN -> certification status",
)

assert_equal(
    unknown["certification_action"],
    "REVIEW",
    "UNKNOWN -> certification action",
)


print("")
print("=" * 82)
print("CASE: BLOCKED PRIORITY OVER REVIEW")
print("=" * 82)

priority = certify({
    "Operational Intelligence": "WARNING",
    "Execution Decision": "EXECUTION_BLOCKED",
})

assert_equal(
    priority["certification_status"],
    "CERTIFICATION_BLOCKED",
    "BLOCKED > REVIEW priority",
)

assert_equal(
    priority["certification_action"],
    "HALT",
    "BLOCKED > REVIEW action priority",
)


print("")
print("=" * 82)
print("CASE: CERTIFIED ACTION FALLBACK")
print("=" * 82)

fallback = certify({}, action=None)

assert_equal(
    fallback["certification_status"],
    "CERTIFIED",
    "missing action -> certification remains certified",
)

assert_equal(
    fallback["certification_action"],
    "HOLD",
    "missing action -> HOLD fallback",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-8 FINAL DECISION CERTIFICATION BOUNDARY COMPLETE =====")
print("=" * 82)


