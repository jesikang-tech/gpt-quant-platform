"""
PHASE 7-10-18-L
AI FINAL DECISION
->
EXECUTION CONTROL
->
EXECUTION ASSURANCE
BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_final_decision_execution_assurance import (
    AIFinalDecisionExecutionAssurance,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )


def base_final_decision():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "confidence_score": 95,
        "validation_status": "VALID",
        "validation_score": 95,
        "monitoring": "STANDARD",
    }


def assured_execution_control():
    return {
        "execution_status": "AUTHORIZED",
        "control_action": "EXECUTE",
        "control_status": "AUTHORIZED",
        "execution_mode": "STANDARD_EXECUTION",
        "control_risk": "LOW",
        "governance_status": "APPROVED",
        "governance_score": 95,
        "integrity_status": "INTACT",
        "execution_readiness": "READY",
        "risk_governance": "ACCEPTABLE",
        "confidence_score": 95,
        "validation_status": "VALID",
        "validation_score": 95,
        "monitoring_policy": "STANDARD",
    }


def run_case_assured():
    print("=" * 82)
    print("CASE: AUTHORIZED EXECUTE -> ASSURED")
    print("=" * 82)

    final_decision = base_final_decision()
    execution_control = assured_execution_control()

    assurance = AIFinalDecisionExecutionAssurance().assure(
        final_decision,
        {},
        execution_control,
    )

    print("assurance:", assurance)

    assert_equal(
        assurance["assurance_status"],
        "ASSURED",
        "ASSURED -> assurance status",
    )

    assert_equal(
        assurance["assurance_level"],
        "HIGH",
        "ASSURED -> assurance level",
    )

    assert_equal(
        assurance["monitoring_status"],
        "STANDARD_MONITORING",
        "ASSURED -> monitoring status",
    )

    assert_equal(
        assurance["assurance_risk"],
        "LOW",
        "ASSURED -> assurance risk",
    )


def run_case_blocked():
    print("=" * 82)
    print("CASE: BLOCK -> BLOCKED")
    print("=" * 82)

    final_decision = base_final_decision()

    execution_control = assured_execution_control()
    execution_control.update({
        "execution_status": "BLOCKED",
        "control_action": "BLOCK",
        "control_status": "BLOCKED",
        "execution_mode": "NO_EXECUTION",
        "control_risk": "CRITICAL",
        "governance_status": "BLOCKED",
        "governance_score": 20,
        "integrity_status": "BROKEN",
        "execution_readiness": "NOT_READY",
        "risk_governance": "UNACCEPTABLE",
        "confidence_score": 20,
        "validation_status": "INVALID",
        "validation_score": 20,
        "monitoring_policy": "CRITICAL",
    })

    assurance = AIFinalDecisionExecutionAssurance().assure(
        final_decision,
        {},
        execution_control,
    )

    print("assurance:", assurance)

    assert_equal(
        assurance["assurance_status"],
        "BLOCKED",
        "BLOCKED -> assurance status",
    )

    assert_equal(
        assurance["assurance_level"],
        "NONE",
        "BLOCKED -> assurance level",
    )

    assert_equal(
        assurance["monitoring_status"],
        "MONITORING_SUSPENDED",
        "BLOCKED -> monitoring status",
    )


def run_case_pending():
    print("=" * 82)
    print("CASE: HOLD -> PENDING")
    print("=" * 82)

    final_decision = base_final_decision()

    execution_control = assured_execution_control()
    execution_control.update({
        "execution_status": "EXECUTION_REVIEW",
        "control_action": "HOLD",
        "control_status": "ON_HOLD",
        "execution_mode": "NO_EXECUTION",
        "control_risk": "HIGH",
        "governance_status": "REVIEW_REQUIRED",
        "governance_score": 70,
        "execution_readiness": "NOT_READY",
        "risk_governance": "MONITORED",
        "confidence_score": 75,
        "monitoring_policy": "ELEVATED",
    })

    assurance = AIFinalDecisionExecutionAssurance().assure(
        final_decision,
        {},
        execution_control,
    )

    print("assurance:", assurance)

    assert_equal(
        assurance["assurance_status"],
        "PENDING",
        "PENDING -> assurance status",
    )

    assert_equal(
        assurance["assurance_level"],
        "LOW",
        "PENDING -> assurance level",
    )

    assert_equal(
        assurance["monitoring_status"],
        "PRE_EXECUTION_MONITORING",
        "PENDING -> monitoring status",
    )


def run_case_monitored():
    print("=" * 82)
    print("CASE: MONITOR -> MONITORED")
    print("=" * 82)

    final_decision = base_final_decision()

    execution_control = assured_execution_control()
    execution_control.update({
        "execution_status": "EXECUTION_REVIEW",
        "control_action": "MONITOR",
        "control_status": "AUTHORIZED_WITH_MONITORING",
        "execution_mode": "CONTROLLED_EXECUTION_ELEVATED",
        "control_risk": "HIGH",
        "governance_status": "APPROVED_WITH_MONITORING",
        "governance_score": 80,
        "execution_readiness": "CONDITIONAL",
        "risk_governance": "MONITORED",
        "confidence_score": 80,
        "validation_score": 80,
        "monitoring_policy": "ELEVATED",
    })

    assurance = AIFinalDecisionExecutionAssurance().assure(
        final_decision,
        {},
        execution_control,
    )

    print("assurance:", assurance)

    assert_equal(
        assurance["assurance_status"],
        "MONITORED",
        "MONITOR -> assurance status",
    )

    assert_equal(
        assurance["assurance_level"],
        "MEDIUM",
        "MONITOR -> assurance level",
    )

    assert_equal(
        assurance["monitoring_status"],
        "ACTIVE_MONITORING",
        "MONITOR -> monitoring status",
    )


def run_case_field_propagation():
    print("=" * 82)
    print("CASE: CONTROL -> ASSURANCE FIELD PROPAGATION")
    print("=" * 82)

    final_decision = base_final_decision()
    execution_control = assured_execution_control()

    assurance = AIFinalDecisionExecutionAssurance().assure(
        final_decision,
        {},
        execution_control,
    )

    print("execution_control:", execution_control)
    print("assurance:", assurance)

    for field in (
        "execution_status",
        "control_action",
        "control_status",
        "execution_mode",
        "control_risk",
        "governance_status",
        "governance_score",
        "integrity_status",
        "execution_readiness",
        "risk_governance",
        "confidence_score",
        "validation_status",
        "validation_score",
        "monitoring_policy",
    ):
        assert_equal(
            assurance.get(field),
            execution_control.get(field),
            f"FIELD PROPAGATION -> {field}",
        )


def main():
    print("=" * 82)
    print("PHASE 7-10-18-L")
    print("AI FINAL DECISION")
    print("-> EXECUTION CONTROL")
    print("-> EXECUTION ASSURANCE")
    print("BOUNDARY CONTRACT TEST V1")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    run_case_assured()
    run_case_blocked()
    run_case_pending()
    run_case_monitored()
    run_case_field_propagation()

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
    print("===== PHASE 7-10-18-L CONTRACT TEST V1 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()

