from core.ai_final_decision_orchestration import (
    AIFinalDecisionOrchestration,
)
from core.ai_final_execution_decision import (
    AIFinalExecutionDecision,
)

print("=" * 82)
print("PHASE 7-10-18-P")
print("ORCHESTRATION")
print("-> FINAL EXECUTION DECISION")
print("CRITICAL RISK PRECEDENCE BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

orchestration_engine = AIFinalDecisionOrchestration()
execution_engine = AIFinalExecutionDecision()

final_decision = {
    "decision": "MAINTAIN",
    "action": "PROCEED",
}

def run_case(name, integrated, lifecycle, operational):
    orchestration = orchestration_engine.analyze(
        final_decision,
        integrated,
        lifecycle,
        operational,
    )

    execution = execution_engine.analyze(
        final_decision,
        orchestration,
        integrated,
        lifecycle,
        operational,
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- ORCHESTRATION ---")
    print(
        "orchestration_status:",
        orchestration.get("orchestration_status"),
    )
    print(
        "orchestration_action:",
        orchestration.get("orchestration_action"),
    )
    print(
        "orchestration_risk:",
        orchestration.get("orchestration_risk"),
    )
    print(
        "execution_authorization:",
        orchestration.get("execution_authorization"),
    )
    print(
        "reassessment_policy:",
        orchestration.get("reassessment_policy"),
    )

    print("--- FINAL EXECUTION DECISION ---")
    print(
        "execution_status:",
        execution.get("execution_status"),
    )
    print(
        "execution_decision:",
        execution.get("execution_decision"),
    )
    print(
        "execution_risk:",
        execution.get("execution_risk"),
    )
    print(
        "execution_authorization:",
        execution.get("execution_authorization"),
    )
    print(
        "reassessment_policy:",
        execution.get("reassessment_policy"),
    )

    return orchestration, execution


(
    orchestration_critical,
    execution_critical,
) = run_case(
    "CRITICAL RISK -> BLOCKED / HALT",
    {
        "integrated_status": "INTEGRATION_CRITICAL",
        "integrated_risk": "CRITICAL",
        "execution_authorization": "SUSPENDED",
        "reassessment_policy": "IMMEDIATE",
    },
    {
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_risk": "LOW",
        "execution_authorization": "SUSPENDED",
        "reassessment_policy": "IMMEDIATE",
    },
    {
        "intelligence_status": "HEALTHY",
        "intelligence_risk": "LOW",
    },
)

assert orchestration_critical.get(
    "orchestration_status"
) == "ORCHESTRATION_BLOCKED"

assert orchestration_critical.get(
    "orchestration_action"
) == "HALT"

assert orchestration_critical.get(
    "orchestration_risk"
) == "CRITICAL"

assert execution_critical.get(
    "execution_status"
) == "EXECUTION_BLOCKED"

assert execution_critical.get(
    "execution_decision"
) == "HALT"

assert execution_critical.get(
    "execution_risk"
) == "CRITICAL"

assert execution_critical.get(
    "execution_authorization"
) == "SUSPENDED"

assert execution_critical.get(
    "reassessment_policy"
) == "IMMEDIATE"

print("CRITICAL risk -> orchestration blocked: PASS")
print("ORCHESTRATION_BLOCKED -> HALT: PASS")
print("CRITICAL risk -> execution blocked: PASS")
print("EXECUTION_BLOCKED -> HALT: PASS")
print("Execution risk remains CRITICAL: PASS")
print("Execution authorization preserves suspension: PASS")
print("Reassessment policy preserves immediacy: PASS")


(
    orchestration_high,
    execution_high,
) = run_case(
    "HIGH RISK -> BLOCKED / HALT",
    {
        "integrated_status": "INTEGRATION_ATTENTION",
        "integrated_risk": "HIGH",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
    },
    {
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_risk": "LOW",
    },
    {
        "intelligence_status": "HEALTHY",
        "intelligence_risk": "LOW",
    },
)

assert orchestration_high.get(
    "orchestration_risk"
) == "HIGH"

assert execution_high.get(
    "execution_status"
) == "EXECUTION_BLOCKED"

assert execution_high.get(
    "execution_decision"
) == "HALT"

assert execution_high.get(
    "execution_risk"
) == "HIGH"

print("HIGH risk -> execution blocked: PASS")
print("HIGH risk -> HALT: PASS")


(
    orchestration_normal,
    execution_normal,
) = run_case(
    "LOW RISK -> READY / PROCEED",
    {
        "integrated_status": "INTEGRATION_READY",
        "integrated_risk": "LOW",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
    },
    {
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_risk": "LOW",
    },
    {
        "intelligence_status": "HEALTHY",
        "intelligence_risk": "LOW",
    },
)

assert orchestration_normal.get(
    "orchestration_status"
) == "ORCHESTRATION_READY"

assert orchestration_normal.get(
    "orchestration_action"
) == "PROCEED"

assert orchestration_normal.get(
    "orchestration_risk"
) == "LOW"

assert execution_normal.get(
    "execution_status"
) == "EXECUTION_READY"

assert execution_normal.get(
    "execution_decision"
) == "PROCEED"

assert execution_normal.get(
    "execution_risk"
) == "LOW"

print("LOW risk -> orchestration ready: PASS")
print("ORCHESTRATION_READY -> PROCEED: PASS")
print("LOW risk -> execution ready: PASS")
print("EXECUTION_READY -> PROCEED: PASS")


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
print(
    "===== PHASE 7-10-18-P CONTRACT TEST V1 COMPLETE ====="
)
print("=" * 82)
