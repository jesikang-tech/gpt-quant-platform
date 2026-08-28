from core.ai_decision_outcome_collector import (
    AIDecisionOutcomeDataCollector
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def collect(
    final_decision=None,
    master_control=None,
    certification=None,
    execution=None,
    feedback=None,
    monitoring=None,
    reassessment=None,
    governance=None,
    lifecycle=None,
    operational=None,
    orchestration=None,
    integrated=None,
    intelligence=None,
    intelligence_score=None,
    decision_confidence=None,
):
    collector = AIDecisionOutcomeDataCollector()

    return collector.collect(
        final_decision=final_decision,
        final_decision_master_control=master_control,
        final_decision_certification=certification,
        final_execution_decision=execution,
        final_decision_execution_feedback=feedback,
        final_decision_execution_monitoring=monitoring,
        final_decision_execution_reassessment=reassessment,
        final_decision_governance=governance,
        final_decision_lifecycle=lifecycle,
        final_decision_operational_intelligence=operational,
        final_decision_orchestration=orchestration,
        final_decision_integrated_intelligence=integrated,
        intelligence=intelligence,
        intelligence_score=intelligence_score,
        decision_confidence=decision_confidence,
    )


print("=" * 82)
print("PHASE 7-10-20-10")
print("MASTER CONTROL -> OUTCOME SNAPSHOT")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: FINAL DECISION + MASTER CONTROL -> SNAPSHOT")
print("=" * 82)

snapshot = collect(
    final_decision={
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "strategy": "GROWTH",
        "market_view": "BULLISH",
        "risk_level": "LOW",
        "validation_score": 91.0,
    },
    master_control={
        "decision": "MASTER_DECISION",
        "master_control_action": "REVIEW",
    },
    certification={
        "certification_risk": "LOW",
        "certification_status": "CERTIFIED",
        "certification_score": 95.0,
    },
    execution={
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
        "execution_score": 94.0,
    },
    governance={
        "governance_status": "APPROVED",
        "governance_score": 93.0,
    },
    lifecycle={
        "lifecycle_status": "HEALTHY",
        "lifecycle_score": 92.0,
    },
    operational={
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_score": 91.0,
    },
    orchestration={
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_score": 90.0,
    },
    integrated={
        "integrated_status": "INTEGRATED_HEALTHY",
        "integrated_score": 89.0,
    },
    intelligence={
        "final_strategy": "GROWTH",
        "market_view": "BULLISH",
    },
    intelligence_score={
        "intelligence_score": 88.0,
    },
    decision_confidence={
        "confidence_score": 87.0,
    },
    feedback={
        "feedback_status": "STABLE",
    },
    monitoring={
        "monitoring_status": "STANDARD_MONITORING",
    },
    reassessment={
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_required": False,
    },
)

assert_equal(
    snapshot["snapshot_status"],
    "COLLECTED",
    "snapshot -> collected status",
)

assert_equal(
    snapshot["snapshot_purpose"],
    "FUTURE_OUTCOME_EVALUATION",
    "snapshot -> future outcome purpose",
)

assert_equal(
    snapshot["outcome_status"],
    "PENDING",
    "snapshot -> pending outcome status",
)

assert_equal(
    snapshot["decision"],
    "ACCUMULATE",
    "final decision -> decision propagation",
)

assert_equal(
    snapshot["action"],
    "PROCEED",
    "final decision -> action propagation",
)

assert_equal(
    snapshot["strategy"],
    "GROWTH",
    "final decision -> strategy propagation",
)

assert_equal(
    snapshot["market_view"],
    "BULLISH",
    "final decision -> market view propagation",
)

assert_equal(
    snapshot["risk_level"],
    "LOW",
    "final decision -> risk propagation",
)


print("")
print("=" * 82)
print("CASE: MASTER CONTROL FALLBACKS")
print("=" * 82)

fallback = collect(
    final_decision={},
    master_control={
        "decision": "MASTER_DECISION",
        "master_control_action": "PROCEED",
    },
)

assert_equal(
    fallback["decision"],
    "MASTER_DECISION",
    "missing final decision -> master decision fallback",
)

assert_equal(
    fallback["action"],
    "PROCEED",
    "missing final action -> master action fallback",
)


print("")
print("=" * 82)
print("CASE: ACTION REVIEW FALLBACK")
print("=" * 82)

action_fallback = collect(
    final_decision={},
    master_control={},
)

assert_equal(
    action_fallback["action"],
    "REVIEW",
    "missing action sources -> REVIEW fallback",
)


print("")
print("=" * 82)
print("CASE: STRATEGY / MARKET / RISK FALLBACKS")
print("=" * 82)

fallback_context = collect(
    final_decision={},
    master_control={},
    certification={
        "certification_risk": "MEDIUM",
    },
    intelligence={
        "final_strategy": "DEFENSIVE",
        "market_view": "NEUTRAL",
    },
)

assert_equal(
    fallback_context["strategy"],
    "DEFENSIVE",
    "strategy -> intelligence fallback",
)

assert_equal(
    fallback_context["market_view"],
    "NEUTRAL",
    "market view -> intelligence fallback",
)

assert_equal(
    fallback_context["risk_level"],
    "MEDIUM",
    "risk -> certification fallback",
)


print("")
print("=" * 82)
print("CASE: SCORE PROPAGATION")
print("=" * 82)

assert_equal(
    snapshot["confidence_score"],
    87.0,
    "confidence score propagation",
)

assert_equal(
    snapshot["intelligence_score"],
    88.0,
    "intelligence score propagation",
)

assert_equal(
    snapshot["validation_score"],
    91.0,
    "validation score propagation",
)

assert_equal(
    snapshot["certification_score"],
    95.0,
    "certification score propagation",
)

assert_equal(
    snapshot["execution_score"],
    94.0,
    "execution score propagation",
)

assert_equal(
    snapshot["governance_score"],
    93.0,
    "governance score propagation",
)

assert_equal(
    snapshot["lifecycle_score"],
    92.0,
    "lifecycle score propagation",
)

assert_equal(
    snapshot["operational_score"],
    91.0,
    "operational score propagation",
)

assert_equal(
    snapshot["orchestration_score"],
    90.0,
    "orchestration score propagation",
)

assert_equal(
    snapshot["integrated_score"],
    89.0,
    "integrated score propagation",
)


print("")
print("=" * 82)
print("CASE: DOWNSTREAM STATUS PROPAGATION")
print("=" * 82)

assert_equal(
    snapshot["execution_status"],
    "EXECUTION_READY",
    "execution status propagation",
)

assert_equal(
    snapshot["execution_authorization"],
    "AUTHORIZED",
    "execution authorization propagation",
)

assert_equal(
    snapshot["certification_status"],
    "CERTIFIED",
    "certification status propagation",
)

assert_equal(
    snapshot["governance_status"],
    "APPROVED",
    "governance status propagation",
)

assert_equal(
    snapshot["monitoring_status"],
    "STANDARD_MONITORING",
    "monitoring status propagation",
)

assert_equal(
    snapshot["feedback_status"],
    "STABLE",
    "feedback status propagation",
)

assert_equal(
    snapshot["reassessment_status"],
    "NOT_REQUIRED",
    "reassessment status propagation",
)

assert_equal(
    snapshot["reassessment_required"],
    False,
    "reassessment required propagation",
)


print("")
print("=" * 82)
print("CASE: REASSESSMENT REQUIRED -> BOOLEAN PRESERVED")
print("=" * 82)

reassessment_case = collect(
    reassessment={
        "reassessment_status": "REASSESS_REQUIRED",
        "reassessment_required": True,
    },
)

assert_equal(
    reassessment_case["reassessment_status"],
    "REASSESS_REQUIRED",
    "reassessment status -> required state",
)

assert_equal(
    reassessment_case["reassessment_required"],
    True,
    "reassessment required -> true",
)

assert_equal(
    reassessment_case["outcome_status"],
    "PENDING",
    "reassessment does not fabricate outcome",
)


print("")
print("=" * 82)
print("CASE: EMPTY INPUT -> SAFE SNAPSHOT DEFAULTS")
print("=" * 82)

empty = collect()

assert_equal(
    empty["snapshot_status"],
    "COLLECTED",
    "empty input -> collected snapshot",
)

assert_equal(
    empty["decision"],
    "UNKNOWN",
    "empty input -> unknown decision",
)

assert_equal(
    empty["action"],
    "REVIEW",
    "empty input -> review action",
)

assert_equal(
    empty["outcome_status"],
    "PENDING",
    "empty input -> pending outcome",
)

assert_equal(
    empty["reassessment_required"],
    False,
    "empty input -> reassessment false",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-10 OUTCOME SNAPSHOT BOUNDARY COMPLETE =====")
print("=" * 82)
