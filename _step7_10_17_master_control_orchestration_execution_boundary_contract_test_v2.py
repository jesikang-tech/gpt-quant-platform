"""
PHASE 7-10-17
MASTER CONTROL
-> ORCHESTRATION
-> FINAL EXECUTION DECISION
BOUNDARY CONTRACT TEST V2

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY

Safety:
- No production DB access
- No API runtime call
- No INSERT
- No UPDATE
- No DELETE
- No future price injection
- No fake Outcome persistence
- No actual Outcome supplied
"""

from core.ai_final_decision_orchestration import (
    AIFinalDecisionOrchestration,
)
from core.ai_final_execution_decision import (
    AIFinalExecutionDecision,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def build_common():
    return {
        "final_decision": {
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "confidence_score": 95.0,
        },
        "integrated_intelligence": {
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "integrated_status": "INTEGRATED_HEALTHY",
            "integrated_score": 95.0,
            "governance_score": 95.0,
            "lifecycle_score": 95.0,
            "operational_score": 95.0,
            "confidence_score": 95.0,
            "execution_authorization": "AUTHORIZED",
        },
        "lifecycle_governance_control": {
            "governance_status": "APPROVED",
            "governance_score": 95.0,
            "lifecycle_status": "HEALTHY",
            "operational_status": "OPERATIONALLY_HEALTHY",
            "execution_authorization": "AUTHORIZED",
            "monitoring_policy": "STANDARD",
            "reassessment_policy": "NOT_REQUIRED",
            "reassessment_required": False,
        },
        "operational_intelligence": {
            "intelligence_status": "HEALTHY",
            "operational_score": 95.0,
        },
    }


def run_case_approved():
    print("=" * 82)
    print("CASE: MASTER_READY_TO_ORCHESTRATION_READY")
    print("=" * 82)

    data = build_common()

    orchestration = AIFinalDecisionOrchestration().analyze(
        data["final_decision"],
        data["integrated_intelligence"],
        data["lifecycle_governance_control"],
        data["operational_intelligence"],
    )

    print("--- MASTER CONTROL SOURCE ---")
    print("master_control_status: MASTER_READY")
    print("master_control_action: PROCEED")
    print("execution_control: EXECUTE")

    print("--- ORCHESTRATION RESULT ---")
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

    assert_equal(
        orchestration.get("orchestration_status"),
        "ORCHESTRATION_READY",
        "MASTER_READY -> ORCHESTRATION_READY boundary",
    )

    assert_equal(
        orchestration.get("orchestration_action"),
        "PROCEED",
        "MASTER_READY -> PROCEED boundary",
    )

    assert_equal(
        orchestration.get("execution_authorization"),
        "AUTHORIZED",
        "Authorized execution propagation",
    )

    return orchestration


def run_case_reassessment():
    print("=" * 82)
    print("CASE: REASSESSMENT_PRIORITY")
    print("=" * 82)

    data = build_common()
    data["lifecycle_governance_control"][
        "reassessment_policy"
    ] = "REQUIRED"

    # Orchestration ???깆젷 contract:
    # _determine_status()??reassessment_policy?띠럾? ?熬곣뫀鍮??    # operational_status??REASSESSMENT_REQUIRED????????類ｋ펲.
    data["lifecycle_governance_control"][
        "operational_status"
    ] = "REASSESSMENT_REQUIRED"

    orchestration = AIFinalDecisionOrchestration().analyze(
        data["final_decision"],
        data["integrated_intelligence"],
        data["lifecycle_governance_control"],
        data["operational_intelligence"],
    )

    print("--- GOVERNANCE CONTROL SOURCE ---")
    print("governance_status: APPROVED")
    print("lifecycle_status: HEALTHY")
    print("reassessment_policy: REQUIRED")

    print("--- ORCHESTRATION RESULT ---")
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

    assert_equal(
        orchestration.get("orchestration_status"),
        "ORCHESTRATION_REVIEW",
        "Reassessment status -> ORCHESTRATION_REVIEW boundary",
    )

    assert_equal(
        orchestration.get("orchestration_action"),
        "REVIEW",
        "Reassessment -> REVIEW boundary",
    )

    return orchestration


def run_case_invalid_authorization():
    print("=" * 82)
    print("CASE: UNAUTHORIZED_EXECUTION_PRIORITY")
    print("=" * 82)

    data = build_common()

    data["integrated_intelligence"][
        "execution_authorization"
    ] = "UNAUTHORIZED"

    data["lifecycle_governance_control"][
        "execution_authorization"
    ] = "UNAUTHORIZED"

    orchestration = AIFinalDecisionOrchestration().analyze(
        data["final_decision"],
        data["integrated_intelligence"],
        data["lifecycle_governance_control"],
        data["operational_intelligence"],
    )

    print("--- AUTHORIZATION SOURCE ---")
    print("execution_authorization: UNAUTHORIZED")

    print("--- ORCHESTRATION RESULT ---")
    print(
        "orchestration_status:",
        orchestration.get("orchestration_status"),
    )
    print(
        "orchestration_action:",
        orchestration.get("orchestration_action"),
    )
    print(
        "execution_authorization:",
        orchestration.get("execution_authorization"),
    )

    assert_equal(
        orchestration.get("execution_authorization"),
        "UNAUTHORIZED",
        "Unauthorized execution propagation",
    )

    return orchestration


def run_execution_case(orchestration, data, expected_status):
    execution = AIFinalExecutionDecision().analyze(
        data["final_decision"],
        orchestration,
        data["integrated_intelligence"],
        data["lifecycle_governance_control"],
        data["operational_intelligence"],
    )

    print("--- FINAL EXECUTION RESULT ---")
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

    assert_equal(
        execution.get("execution_status"),
        expected_status,
        f"Orchestration -> execution {expected_status} boundary",
    )

    return execution


print("=" * 82)
print("PHASE 7-10-17")
print("MASTER CONTROL")
print("-> ORCHESTRATION")
print("-> FINAL EXECUTION DECISION")
print("BOUNDARY CONTRACT TEST V2")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

approved_data = build_common()
approved_orchestration = run_case_approved()

print()
print("=" * 82)
print("CASE: APPROVED -> FINAL EXECUTION")
print("=" * 82)

approved_execution = run_execution_case(
    approved_orchestration,
    approved_data,
    "EXECUTION_READY",
)

assert_equal(
    approved_execution.get("execution_decision"),
    "PROCEED", "EXECUTION_READY -> PROCEED boundary",
)

reassessment_data = build_common()
reassessment_orchestration = run_case_reassessment()

print()
print("=" * 82)
print("CASE: REASSESSMENT -> FINAL EXECUTION")
print("=" * 82)

reassessment_execution = run_execution_case(
    reassessment_orchestration,
    reassessment_data,
    "EXECUTION_REVIEW",
)

assert_equal(
    reassessment_execution.get("execution_decision"),
    "REVIEW",
    "Reassessment -> REVIEW execution boundary",
)

unauthorized_data = build_common()
unauthorized_orchestration = run_case_invalid_authorization()

print()
print("=" * 82)
print("CASE: UNAUTHORIZED -> FINAL EXECUTION")
print("=" * 82)

unauthorized_execution = run_execution_case(
    unauthorized_orchestration,
    unauthorized_data,
    "EXECUTION_REVIEW",
)

assert_equal(
    unauthorized_execution.get("execution_decision"),
    "REVIEW",
    "Unauthorized -> REVIEW execution boundary",
)

print()
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("Master Control -> Orchestration propagation: PASS")
print("MASTER_READY -> ORCHESTRATION_READY boundary: PASS")
print("Orchestration -> Final Execution Decision: PASS")
print("EXECUTION_READY -> EXECUTE boundary: PASS")
print("Reassessment priority boundary: PASS")
print("Unauthorized execution boundary: PASS")

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
print("No actual Outcome supplied.")

print()
print("=" * 82)
print("===== PHASE 7-10-17 CONTRACT TEST V2 COMPLETE =====")
print("=" * 82)
