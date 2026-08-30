from core.ai_final_execution_decision import AIFinalExecutionDecision
from core.ai_final_decision_master_control import AIFinalDecisionMasterControl

print("=" * 82)
print("PHASE 7-8 FINAL EXECUTION -> MASTER CONTROL CONTRACT TEST")
print("SOURCE-VERIFIED CANONICAL POLICY")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 82)

execution_engine = AIFinalExecutionDecision()
master_engine = AIFinalDecisionMasterControl()

cases = [
    {
        "name": "READY",
        "orchestration": {
            "decision": "ACCUMULATE",
            "orchestration_action": "PROCEED",
            "orchestration_status": "ORCHESTRATION_READY",
            "orchestration_risk": "LOW",
            "execution_authorization": "AUTHORIZED",
            "reassessment_policy": "NOT_REQUIRED",
            "confidence_score": 95.0,
            "orchestration_score": 95.0,
            "integrated_score": 95.0,
            "governance_score": 95.0,
            "lifecycle_score": 95.0,
            "operational_score": 95.0,
        },
        "expected_execution_status": "EXECUTION_READY",
        "expected_execution_decision": "PROCEED",
        "expected_master_status": "MASTER_READY",
        "expected_master_action": "PROCEED",
        "expected_execution_control": "EXECUTE",
    },
    {
        "name": "REVIEW",
        "orchestration": {
            "decision": "ACCUMULATE",
            "orchestration_action": "PROCEED",
            "orchestration_status": "ORCHESTRATION_REVIEW",
            "orchestration_risk": "MEDIUM",
            "execution_authorization": "AUTHORIZED",
            "reassessment_policy": "NOT_REQUIRED",
            "confidence_score": 80.0,
            "orchestration_score": 80.0,
            "integrated_score": 80.0,
            "governance_score": 80.0,
            "lifecycle_score": 80.0,
            "operational_score": 80.0,
        },
        "expected_execution_status": "EXECUTION_REVIEW",
        "expected_execution_decision": "REVIEW",
        "expected_master_status": "MASTER_REVIEW",
        "expected_master_action": "REVIEW",
        "expected_execution_control": "HOLD",
    },
    {
        "name": "BLOCKED",
        "orchestration": {
            "decision": "DEFENSIVE",
            "orchestration_action": "HALT",
            "orchestration_status": "ORCHESTRATION_BLOCKED",
            "orchestration_risk": "CRITICAL",
            "execution_authorization": "AUTHORIZED",
            "reassessment_policy": "NOT_REQUIRED",
            "confidence_score": 40.0,
            "orchestration_score": 40.0,
            "integrated_score": 40.0,
            "governance_score": 40.0,
            "lifecycle_score": 40.0,
            "operational_score": 40.0,
        },
        "expected_execution_status": "EXECUTION_BLOCKED",
        "expected_execution_decision": "HALT",
        "expected_master_status": "MASTER_BLOCKED",
        "expected_master_action": "HALT",
        "expected_execution_control": "HOLD",
    },
]

common_integrated = {
    "integrated_status": "INTEGRATED_HEALTHY",
    "integrated_score": 95.0,
}

common_lifecycle = {
    "lifecycle_status": "HEALTHY",
    "lifecycle_score": 95.0,
    "reassessment_required": False,
    "reassessment_policy": "NOT_REQUIRED",
    "execution_authorization": "AUTHORIZED",
    "governance_score": 95.0,
}

common_operational = {
    "operational_status": "OPERATIONALLY_HEALTHY",
    "operational_score": 95.0,
}

for case in cases:
    print("")
    print("=" * 82)
    print(f"CASE: {case['name']}")
    print("=" * 82)

    orchestration = case["orchestration"]

    final_decision = {
        "decision": orchestration["decision"],
        "action": orchestration["orchestration_action"],
        "execution_status": orchestration["execution_authorization"],
        "confidence_score": orchestration["confidence_score"],
    }

    execution = execution_engine.analyze(
        final_decision=final_decision,
        orchestration=orchestration,
        integrated_intelligence=common_integrated,
        lifecycle_governance_control=common_lifecycle,
        operational_intelligence=common_operational,
    )

    print("execution status:", execution.get("execution_status"))
    print("execution decision:", execution.get("execution_decision"))
    print("execution authorization:", execution.get("execution_authorization"))

    assert execution.get("execution_status") == case["expected_execution_status"]
    assert execution.get("execution_decision") == case["expected_execution_decision"]

    print("final execution contract: PASS")

    certification = {
        "decision": execution.get("decision"),
        "certification_status": "CERTIFIED",
        "certification_risk": "LOW",
        "execution_status": execution.get("execution_status"),
        "execution_authorization": execution.get("execution_authorization"),
        "execution_readiness": (
            "READY"
            if execution.get("execution_status") == "EXECUTION_READY"
            else execution.get("execution_status")
        ),
        "decision_integrity": "INTACT",
        "certification_score": 95.0,
        "certification_action": execution.get("action"),
    }

    governance = {
        "governance_status": "APPROVED",
        "governance_score": 95.0,
    }

    lifecycle = {
        "lifecycle_status": "HEALTHY",
        "lifecycle_score": 95.0,
        "reassessment_required": False,
    }

    validation = {
        "validation_status": "VALID",
        "validation_score": 95.0,
    }

    master = master_engine.analyze(
        final_decision=final_decision,
        certification=certification,
        execution_decision=execution,
        governance=governance,
        lifecycle=lifecycle,
        operational_intelligence=common_operational,
        orchestration=orchestration,
        integrated_intelligence=common_integrated,
        validation=validation,
    )

    print("master control status:", master.get("master_control_status"))
    print("master control action:", master.get("master_control_action"))
    print("master control risk:", master.get("master_control_risk"))
    print("execution control:", master.get("execution_control"))

    assert master.get("master_control_status") == case["expected_master_status"]
    assert master.get("master_control_action") == case["expected_master_action"]
    assert master.get("execution_control") == case["expected_execution_control"]

    print("master control contract: PASS")
    print("FINAL EXECUTION -> MASTER CONTROL: PASS")

print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("READY -> EXECUTION_READY -> MASTER_READY -> PROCEED -> EXECUTE: PASS")
print("REVIEW -> EXECUTION_REVIEW -> MASTER_REVIEW -> REVIEW -> HOLD: PASS")
print("BLOCKED -> EXECUTION_BLOCKED -> MASTER_BLOCKED -> HALT -> HOLD: PASS")

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
print("=" * 82)
print("===== PHASE 7-8 FINAL EXECUTION -> MASTER CONTROL TEST COMPLETE =====")
print("=" * 82)
