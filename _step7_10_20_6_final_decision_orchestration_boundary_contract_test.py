from core.ai_final_decision_orchestration import (
    AIFinalDecisionOrchestration
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def orchestrate(
    final_decision=None,
    integrated_intelligence=None,
    lifecycle_governance_control=None,
    operational_intelligence=None,
):
    engine = AIFinalDecisionOrchestration()

    return engine.analyze(
        final_decision=final_decision or {
            "decision": "ACCUMULATE",
            "action": "PROCEED",
            "execution_status": "AUTHORIZED",
        },
        integrated_intelligence=integrated_intelligence or {
            "integrated_status": "INTEGRATED_HEALTHY",
            "integrated_action": "PROCEED",
            "integrated_risk": "LOW",
            "execution_authorization": "AUTHORIZED",
        },
        lifecycle_governance_control=(
            lifecycle_governance_control or {
                "operational_status": "OPERATIONALLY_HEALTHY",
                "operational_risk": "LOW",
                "execution_authorization": "AUTHORIZED",
            }
        ),
        operational_intelligence=operational_intelligence or {
            "intelligence_status": "HEALTHY",
            "intelligence_risk": "LOW",
        },
    )


print("=" * 82)
print("PHASE 7-10-20-6")
print("FINAL DECISION -> ORCHESTRATION")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: HEALTHY -> ORCHESTRATION READY")
print("=" * 82)

ready = orchestrate()

assert_equal(
    ready["orchestration_status"],
    "ORCHESTRATION_READY",
    "READY -> orchestration status",
)

assert_equal(
    ready["orchestration_action"],
    "PROCEED",
    "READY -> orchestration action",
)

assert_equal(
    ready["orchestration_risk"],
    "LOW",
    "READY -> orchestration risk",
)

assert_equal(
    ready["execution_authorization"],
    "AUTHORIZED",
    "READY -> execution authorization",
)


print("")
print("=" * 82)
print("CASE: CRITICAL -> ORCHESTRATION BLOCKED")
print("=" * 82)

blocked = orchestrate(
    integrated_intelligence={
        "integrated_status": "INTEGRATION_CRITICAL",
        "integrated_action": "PROCEED",
        "integrated_risk": "CRITICAL",
        "execution_authorization": "AUTHORIZED",
    }
)

assert_equal(
    blocked["orchestration_status"],
    "ORCHESTRATION_BLOCKED",
    "CRITICAL -> orchestration status",
)

assert_equal(
    blocked["orchestration_action"],
    "HALT",
    "CRITICAL -> orchestration action",
)

assert_equal(
    blocked["orchestration_risk"],
    "CRITICAL",
    "CRITICAL -> orchestration risk",
)


print("")
print("=" * 82)
print("CASE: WARNING -> ORCHESTRATION REVIEW")
print("=" * 82)

review = orchestrate(
    operational_intelligence={
        "intelligence_status": "WARNING",
        "intelligence_risk": "HIGH",
    }
)

assert_equal(
    review["orchestration_status"],
    "ORCHESTRATION_REVIEW",
    "WARNING -> orchestration status",
)

assert_equal(
    review["orchestration_action"],
    "REVIEW",
    "WARNING -> orchestration action",
)

assert_equal(
    review["orchestration_risk"],
    "HIGH",
    "WARNING -> orchestration risk",
)


print("")
print("=" * 82)
print("CASE: EXECUTION AUTHORIZATION PRIORITY")
print("=" * 82)

priority = orchestrate(
    final_decision={
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "FINAL_AUTHORIZED",
    },
    integrated_intelligence={
        "integrated_status": "INTEGRATED_HEALTHY",
        "integrated_action": "PROCEED",
        "integrated_risk": "LOW",
        "execution_authorization": "INTEGRATED_AUTHORIZED",
    },
    lifecycle_governance_control={
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_risk": "LOW",
        "execution_authorization": "LIFECYCLE_AUTHORIZED",
    },
    operational_intelligence={
        "intelligence_status": "HEALTHY",
        "intelligence_risk": "LOW",
    },
)

assert_equal(
    priority["execution_authorization"],
    "INTEGRATED_AUTHORIZED",
    "integrated -> execution authorization priority",
)


print("")
print("=" * 82)
print("CASE: FALLBACK EXECUTION AUTHORIZATION")
print("=" * 82)

fallback = orchestrate(
    integrated_intelligence={
        "integrated_status": "INTEGRATED_HEALTHY",
        "integrated_action": "PROCEED",
        "integrated_risk": "LOW",
    },
    lifecycle_governance_control={
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_risk": "LOW",
    },
    final_decision={
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "FINAL_AUTHORIZED",
    },
)

assert_equal(
    fallback["execution_authorization"],
    "FINAL_AUTHORIZED",
    "final decision -> execution authorization fallback",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-6 FINAL DECISION ORCHESTRATION BOUNDARY COMPLETE =====")
print("=" * 82)
