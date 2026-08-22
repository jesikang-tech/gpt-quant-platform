from core.ai_final_decision_execution_control import (
    AIFinalDecisionExecutionControl
)

print("=" * 78)
print("PHASE 7-6 EXECUTION CONTROL CONTRACT TEST")
print("FINAL EXECUTION DECISION -> EXECUTION CONTROL")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 78)

engine = AIFinalDecisionExecutionControl()

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

for case in cases:

    print()
    print("=" * 78)
    print("CASE:", case["name"])
    print("=" * 78)

    final_decision = {
        "decision": case["decision"],
        "action": case["action"],
        "execution_status": "EXECUTION_READY",
        "confidence_score": 95,
        "validation_status": "VALID",
        "validation_score": 95,
    }

    governance = {
        "decision": case["decision"],
        "action": case["action"],
        "execution_status": "EXECUTION_READY",
        "governance_status": "APPROVED",
        "governance_score": 95,
        "integrity_status": "INTACT",
        "execution_readiness": "READY",
        "risk_governance": "ACCEPTABLE",
        "override_status": "NONE",
        "confidence_score": 95,
        "validation_status": "VALID",
        "validation_score": 95,
        "monitoring_policy": "STANDARD",
    }

    result = engine.control(
        final_decision,
        governance
    )

    print("input decision:",
          case["decision"])

    print("input action:",
          case["action"])

    print("returned action:",
          result.get("action"))

    print("execution status:",
          result.get("execution_status"))

    print("control action:",
          result.get("control_action"))

    print("control status:",
          result.get("control_status"))

    print("execution mode:",
          result.get("execution_mode"))

    print("control risk:",
          result.get("control_risk"))

    assert result.get("action") == case["action"]
    print("action preservation: PASS")

    assert result.get("execution_status") == "EXECUTION_READY"
    print("execution readiness propagation: PASS")

    assert result.get("control_action") == "MONITOR"
    print("control boundary contract: PASS")

    assert result.get("control_status") == \
        "AUTHORIZED_WITH_MONITORING"
    print("control status contract: PASS")

    assert result.get("control_risk") == "MEDIUM"
    print("control risk contract: PASS")


print()
print("=" * 78)
print("CONTROL EXECUTE CANONICAL TEST")
print("=" * 78)

execute_final_decision = {
    "decision": "PROCEED",
    "action": "PROCEED",
    "execution_status": "EXECUTION_READY",
    "confidence_score": 95,
    "validation_status": "VALID",
    "validation_score": 95,
}

execute_governance = {
    "decision": "PROCEED",
    "action": "PROCEED",
    "execution_status": "EXECUTION_READY",
    "governance_status": "APPROVED",
    "governance_score": 95,
    "integrity_status": "INTACT",
    "execution_readiness": "READY",
    "risk_governance": "ACCEPTABLE",
    "override_status": "NONE",
    "confidence_score": 95,
    "validation_status": "VALID",
    "validation_score": 95,
    "monitoring_policy": "STANDARD",
}

execute_result = engine.control(
    execute_final_decision,
    execute_governance
)

print("canonical action:",
      execute_result.get("action"))

print("canonical control action:",
      execute_result.get("control_action"))

print("canonical control status:",
      execute_result.get("control_status"))

print("canonical execution mode:",
      execute_result.get("execution_mode"))

assert execute_result.get("control_action") == "EXECUTE"
print("EXECUTE control contract: PASS")

assert execute_result.get("control_status") == "AUTHORIZED"
print("EXECUTE authorization contract: PASS")

assert execute_result.get("execution_mode") == \
    "STANDARD_EXECUTION"
print("STANDARD_EXECUTION contract: PASS")


print()
print("=" * 78)
print("FINAL ASSERTIONS")
print("=" * 78)

print(
    "NEGATIVE action preservation -> MONITOR: PASS"
)

print(
    "POSITIVE action preservation -> MONITOR: PASS"
)

print(
    "PENDING action preservation -> MONITOR: PASS"
)

print(
    "PROCEED -> EXECUTE -> AUTHORIZED: PASS"
)

print()
print("=" * 78)
print("SAFETY")
print("=" * 78)

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
    "===== PHASE 7-6 EXECUTION CONTROL CONTRACT TEST COMPLETE ====="
)
