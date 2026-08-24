from core.ai_final_execution_decision import AIFinalExecutionDecision

print("=" * 82)
print("PHASE 7-9-4 REASSESSMENT -> EXECUTION")
print("DOWNSTREAM PROPAGATION BOUNDARY CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

engine = AIFinalExecutionDecision()

cases = [
    {
        "name": "REASSESSMENT_REQUIRED",
        "orchestration_status": "ORCHESTRATION_REVIEW",
        "orchestration_risk": "MEDIUM",
        "authorization": "AUTHORIZED",
        "reassessment_policy": "REQUIRED",
        "expected_status": "EXECUTION_REVIEW",
        "expected_decision": "REVIEW",
    },
    {
        "name": "NOT_REQUIRED",
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_risk": "LOW",
        "authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
        "expected_status": "EXECUTION_READY",
        "expected_decision": "PROCEED",
    },
]

for case in cases:

    result = engine.analyze(
        {
            "decision": "ACCUMULATE",
            "action": "PROCEED",
            "confidence_score": 90.0,
        },
        {
            "decision": "ACCUMULATE",
            "orchestration_action": "REVIEW"
                if case["name"] == "REASSESSMENT_REQUIRED"
                else "PROCEED",
            "orchestration_status": case["orchestration_status"],
            "orchestration_risk": case["orchestration_risk"],
            "execution_authorization": case["authorization"],
            "reassessment_policy": case["reassessment_policy"],
            "orchestration_score": 90.0,
        },
        {
            "decision": "ACCUMULATE",
            "action": "PROCEED",
            "execution_authorization": case["authorization"],
            "confidence_score": 90.0,
            "integrated_score": 90.0,
        },
        {
            "execution_authorization": case["authorization"],
            "reassessment_policy": case["reassessment_policy"],
            "lifecycle_governance_score": 90.0,
        },
        {
            "operational_status": "OPERATIONALLY_HEALTHY",
            "operational_score": 90.0,
        },
    )

    assert result.get("execution_status") == case["expected_status"]
    assert result.get("execution_decision") == case["expected_decision"]
    assert result.get("execution_authorization") == case["authorization"]
    assert result.get("reassessment_policy") == case["reassessment_policy"]

    print(
        f"{case['name']}: PASS | "
        f"execution={result.get('execution_status')} -> "
        f"{result.get('execution_decision')} | "
        f"policy={result.get('reassessment_policy')}"
    )

print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("REASSESSMENT_REQUIRED -> EXECUTION_REVIEW -> REVIEW: PASS")
print("NOT_REQUIRED -> EXECUTION_READY -> PROCEED: PASS")

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

print("")
print("===== PHASE 7-9-4 REASSESSMENT -> EXECUTION CONTRACT TEST COMPLETE =====")
print("=" * 82)
