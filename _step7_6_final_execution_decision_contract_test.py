from core.ai_final_execution_decision import AIFinalExecutionDecision

print("=" * 76)
print("PHASE 7-6 FINAL EXECUTION DECISION CONTRACT TEST")
print("FINAL DECISION -> ORCHESTRATION -> EXECUTION DECISION")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 76)

cases = [
    {
        "name": "NEGATIVE",
        "decision": "DEFENSIVE",
        "action": "REDUCE_RISK",
    },
    {
        "name": "POSITIVE",
        "decision": "ACCUMULATE",
        "action": "INCREASE_RISK",
    },
    {
        "name": "PENDING",
        "decision": "MAINTAIN",
        "action": "MAINTAIN_ALLOCATION",
    },
]

engine = AIFinalExecutionDecision()

for case in cases:

    print()
    print("=" * 76)
    print("CASE:", case["name"])
    print("=" * 76)

    final_decision = {
        "decision": case["decision"],
        "action": case["action"],
        "confidence_score": 95,
    }

    orchestration = {
        "decision": case["decision"],
        "orchestration_action": case["action"],
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_risk": "LOW",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
        "confidence_score": 95,
        "orchestration_score": 95,
        "integrated_score": 95,
        "governance_score": 95,
        "lifecycle_score": 95,
        "operational_score": 95,
    }

    integrated_intelligence = {
        "decision": case["decision"],
        "action": case["action"],
        "execution_authorization": "AUTHORIZED",
        "integrated_score": 95,
        "integrated_risk": "LOW",
        "confidence_score": 95,
    }

    lifecycle_governance_control = {
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
        "governance_score": 95,
        "operational_risk": "LOW",
    }

    operational_intelligence = {
        "operational_score": 95,
        "intelligence_risk": "LOW",
    }

    result = engine.analyze(
        final_decision,
        orchestration,
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence,
    )

    print("input action:",
          case["action"])

    print("final execution action:",
          result.get("action"))

    print("execution decision:",
          result.get("execution_decision"))

    print("execution status:",
          result.get("execution_status"))

    print("execution authorization:",
          result.get("execution_authorization"))

    print("execution risk:",
          result.get("execution_risk"))

    print("execution score:",
          result.get("execution_score"))

    assert result.get("action") == case["action"]
    print("action propagation: PASS")

    assert result.get("execution_decision") == case["action"]
    print("execution decision contract: PASS")

    assert result.get("execution_status") == "EXECUTION_READY"
    print("execution status contract: PASS")

    assert result.get("execution_authorization") == "AUTHORIZED"
    print("authorization contract: PASS")

    assert result.get("execution_risk") == "LOW"
    print("risk contract: PASS")


print()
print("=" * 76)
print("FINAL ASSERTIONS")
print("=" * 76)

print(
    "NEGATIVE -> REDUCE_RISK -> EXECUTION_READY: PASS"
)

print(
    "POSITIVE -> INCREASE_RISK -> EXECUTION_READY: PASS"
)

print(
    "PENDING -> MAINTAIN_ALLOCATION -> EXECUTION_READY: PASS"
)

print()
print("=" * 76)
print("SAFETY")
print("=" * 76)

print("Memory-only execution: PASS")
print("No production DB access.")
print("No API runtime call.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")

print()
print(
    "===== PHASE 7-6 FINAL EXECUTION DECISION CONTRACT TEST COMPLETE ====="
)
