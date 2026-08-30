from core.ai_final_execution_decision import (
    AIFinalExecutionDecision
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def execute(
    final_decision=None,
    orchestration=None,
    integrated_intelligence=None,
    lifecycle_governance_control=None,
    operational_intelligence=None,
):
    engine = AIFinalExecutionDecision()

    return engine.analyze(
        final_decision=final_decision or {
            "decision": "ACCUMULATE",
            "action": "PROCEED",
            "execution_status": "AUTHORIZED",
        },
        orchestration=orchestration or {
            "decision": "ACCUMULATE",
            "orchestration_action": "PROCEED",
            "orchestration_status": "ORCHESTRATION_READY",
            "orchestration_risk": "LOW",
            "execution_authorization": "AUTHORIZED",
            "reassessment_policy": "NOT_REQUIRED",
            "orchestration_score": 95.0,
            "integrated_score": 95.0,
            "governance_score": 95.0,
            "lifecycle_score": 95.0,
            "operational_score": 95.0,
            "confidence_score": 95.0,
        },
        integrated_intelligence=(
            integrated_intelligence or {
                "integrated_status": "INTEGRATED_HEALTHY",
                "integrated_risk": "LOW",
                "integrated_score": 95.0,
                "execution_authorization": "AUTHORIZED",
            }
        ),
        lifecycle_governance_control=(
            lifecycle_governance_control or {
                "operational_status": "OPERATIONALLY_HEALTHY",
                "operational_risk": "LOW",
                "governance_score": 95.0,
                "lifecycle_score": 95.0,
                "execution_authorization": "AUTHORIZED",
            }
        ),
        operational_intelligence=(
            operational_intelligence or {
                "intelligence_status": "HEALTHY",
                "intelligence_risk": "LOW",
                "operational_score": 95.0,
            }
        ),
    )


print("=" * 82)
print("PHASE 7-10-20-7")
print("ORCHESTRATION -> FINAL EXECUTION DECISION")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: READY + AUTHORIZED + NO REASSESSMENT -> EXECUTION READY")
print("=" * 82)

ready = execute()

assert_equal(
    ready["decision"],
    "ACCUMULATE",
    "READY -> decision propagation",
)

assert_equal(
    ready["action"],
    "PROCEED",
    "READY -> action propagation",
)

assert_equal(
    ready["execution_status"],
    "EXECUTION_READY",
    "READY -> execution status",
)

assert_equal(
    ready["execution_decision"],
    "PROCEED",
    "READY -> execution decision",
)

assert_equal(
    ready["execution_risk"],
    "LOW",
    "READY -> execution risk",
)

assert_equal(
    ready["execution_authorization"],
    "AUTHORIZED",
    "READY -> execution authorization",
)


print("")
print("=" * 82)
print("CASE: ORCHESTRATION BLOCKED -> EXECUTION BLOCKED")
print("=" * 82)

blocked = execute(
    orchestration={
        "decision": "ACCUMULATE",
        "orchestration_action": "HALT",
        "orchestration_status": "ORCHESTRATION_BLOCKED",
        "orchestration_risk": "LOW",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
    }
)

assert_equal(
    blocked["execution_status"],
    "EXECUTION_BLOCKED",
    "BLOCKED -> execution status",
)

assert_equal(
    blocked["execution_decision"],
    "HALT",
    "BLOCKED -> execution decision",
)


print("")
print("=" * 82)
print("CASE: HIGH ORCHESTRATION RISK -> EXECUTION BLOCKED")
print("=" * 82)

high_risk = execute(
    orchestration={
        "decision": "ACCUMULATE",
        "orchestration_action": "PROCEED",
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_risk": "HIGH",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
    }
)

assert_equal(
    high_risk["execution_status"],
    "EXECUTION_BLOCKED",
    "HIGH risk -> execution status",
)

assert_equal(
    high_risk["execution_decision"],
    "HALT",
    "HIGH risk -> execution decision",
)


print("")
print("=" * 82)
print("CASE: UNAUTHORIZED -> EXECUTION REVIEW")
print("=" * 82)

unauthorized = execute(
    orchestration={
        "decision": "ACCUMULATE",
        "orchestration_action": "PROCEED",
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_risk": "LOW",
        "execution_authorization": "UNAUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
    }
)

assert_equal(
    unauthorized["execution_status"],
    "EXECUTION_REVIEW",
    "UNAUTHORIZED -> execution status",
)

assert_equal(
    unauthorized["execution_decision"],
    "REVIEW",
    "UNAUTHORIZED -> execution decision",
)


print("")
print("=" * 82)
print("CASE: REASSESSMENT REQUIRED -> EXECUTION REVIEW")
print("=" * 82)

reassessment = execute(
    orchestration={
        "decision": "ACCUMULATE",
        "orchestration_action": "PROCEED",
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_risk": "LOW",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "REQUIRED",
    }
)

assert_equal(
    reassessment["execution_status"],
    "EXECUTION_REVIEW",
    "REASSESSMENT -> execution status",
)

assert_equal(
    reassessment["execution_decision"],
    "REVIEW",
    "REASSESSMENT -> execution decision",
)


print("")
print("=" * 82)
print("CASE: ORCHESTRATION REVIEW -> EXECUTION REVIEW")
print("=" * 82)

orchestration_review = execute(
    orchestration={
        "decision": "ACCUMULATE",
        "orchestration_action": "REVIEW",
        "orchestration_status": "ORCHESTRATION_REVIEW",
        "orchestration_risk": "MEDIUM",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
    }
)

assert_equal(
    orchestration_review["execution_status"],
    "EXECUTION_REVIEW",
    "ORCHESTRATION REVIEW -> execution status",
)

assert_equal(
    orchestration_review["execution_decision"],
    "REVIEW",
    "ORCHESTRATION REVIEW -> execution decision",
)


print("")
print("=" * 82)
print("CASE: ACTION FALLBACK -> PROCEED")
print("=" * 82)

fallback = execute(
    final_decision={
        "decision": "ACCUMULATE",
        "execution_status": "AUTHORIZED",
    },
    orchestration={
        "decision": "ACCUMULATE",
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_risk": "LOW",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
    },
)

assert_equal(
    fallback["action"],
    "HOLD",
    "missing action -> HOLD fallback",
)

assert_equal(
    fallback["execution_decision"],
    "HOLD",
    "missing action -> execution decision fallback",
)

print("")
print("=" * 82)
print("CASE: RISK PRIORITY")
print("=" * 82)

risk_priority = execute(
    orchestration={
        "decision": "ACCUMULATE",
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_risk": "MEDIUM",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
    },
    integrated_intelligence={
        "integrated_status": "INTEGRATED_HEALTHY",
        "integrated_risk": "CRITICAL",
        "integrated_score": 95.0,
        "execution_authorization": "AUTHORIZED",
    },
    lifecycle_governance_control={
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_risk": "HIGH",
        "governance_score": 95.0,
        "lifecycle_score": 95.0,
        "execution_authorization": "AUTHORIZED",
    },
    operational_intelligence={
        "intelligence_status": "HEALTHY",
        "intelligence_risk": "LOW",
        "operational_score": 95.0,
    },
)

assert_equal(
    risk_priority["execution_risk"],
    "CRITICAL",
    "CRITICAL > HIGH > MEDIUM -> risk priority",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-7 FINAL EXECUTION DECISION BOUNDARY COMPLETE =====")
print("=" * 82)

