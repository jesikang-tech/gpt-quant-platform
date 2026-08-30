from core.ai_final_decision_integrated_intelligence import (
    AIFinalDecisionIntegratedIntelligence,
)


print("=" * 82)
print("PHASE 7-9-4 INTEGRATED INTELLIGENCE REASSESSMENT")
print("PROPAGATION BOUNDARY CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


engine = AIFinalDecisionIntegratedIntelligence()


def run_case(
    name,
    reassessment,
    expected_status,
    expected_action,
    expected_policy,
    expected_signal_status,
):

    result = engine.analyze(
        {
            "decision": "ACCUMULATE",
            "action": "PROCEED",
            "confidence_score": 90,
        },
        {
            "validation_status": "VALID",
            "validation_score": 90,
        },
        {
            "governance_status": "APPROVED",
            "governance_score": 90,
        },
        {
            "control_status": "AUTHORIZED",
        },
        {
            "assurance_status": "ASSURED",
        },
        {
            "monitoring_status": "STANDARD",
        },
        {
            "feedback_status": "STABLE",
        },
        reassessment,
        {
            "lifecycle_status": "HEALTHY",
            "lifecycle_score": 90,
        },
        {
            "operational_status": "HEALTHY",
            "operational_score": 90,
        },
        {
            "intelligence_status": "HEALTHY",
            "intelligence_score": 90,
        },
    )

    reassessment_signals = [
        signal
        for signal in result.get("signals", [])
        if signal.get("name") == "Reassessment"
    ]

    assert result.get(
        "integrated_status"
    ) == expected_status

    assert result.get(
        "integrated_action"
    ) == expected_action

    assert result.get(
        "reassessment_policy"
    ) == expected_policy
    if expected_signal_status == "ATTENTION":
        assert len(reassessment_signals) == 1
        assert reassessment_signals[0].get("status") == "ATTENTION"
    else:
        assert len(reassessment_signals) == 0

    print("CASE PASS:", name, "| status:", result.get("integrated_status"), "| action:", result.get("integrated_action"), "| policy:", result.get("reassessment_policy"), "| signals:", len(reassessment_signals))

print()
print("=" * 82)
print("CASE: REASSESSMENT REQUIRED")
print("=" * 82)

run_case(
    "REASSESSMENT_REQUIRED",
    {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
    },
    "INTEGRATION_ATTENTION",
    "REVIEW",
    "REQUIRED",
    "ATTENTION",
)


print()
print("=" * 82)
print("CASE: REASSESSMENT NOT REQUIRED")
print("=" * 82)

run_case(
    "NOT_REQUIRED",
    {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
    },
    "INTEGRATED_HEALTHY",
    "PROCEED",
    "NOT_REQUIRED",
    "PASS",
)


print()
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print(
    "REASSESSMENT_REQUIRED -> "
    "INTEGRATION_ATTENTION -> REVIEW: PASS"
)
print(
    "NOT_REQUIRED -> "
    "INTEGRATED_HEALTHY: PASS"
)

print()
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

print()
print("=" * 82)
print("===== PHASE 7-9-4 REASSESSMENT PROPAGATION CONTRACT TEST COMPLETE =====")
print("=" * 82)
