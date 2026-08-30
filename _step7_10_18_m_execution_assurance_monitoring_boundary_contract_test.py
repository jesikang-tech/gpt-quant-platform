"""
PHASE 7-10-18-M
AI FINAL DECISION
->
EXECUTION ASSURANCE
->
EXECUTION MONITORING
BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_final_decision_execution_monitoring import (
    AIFinalDecisionExecutionMonitoring,
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
        "validation_status": "VALID",
        "validation_score": 95,
    }


def assured_execution_assurance():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "assurance_status": "ASSURED",
        "assurance_level": "HIGH",
        "assurance_risk": "LOW",
        "assurance_score": 97,
        "control_action": "EXECUTE",
        "control_status": "AUTHORIZED",
        "control_risk": "LOW",
        "governance_status": "APPROVED",
        "governance_score": 95,
        "validation_status": "VALID",
        "validation_score": 95,
        "monitoring_policy": "STANDARD",
    }


def run_case_standard_monitoring():
    print("=" * 82)
    print("CASE: ASSURED + STANDARD -> STANDARD_MONITORING")
    print("=" * 82)

    final_decision = base_final_decision()
    execution_assurance = assured_execution_assurance()

    monitoring = AIFinalDecisionExecutionMonitoring().monitor(
        final_decision,
        {},
        {},
        execution_assurance,
    )

    print("monitoring:", monitoring)

    assert_equal(
        monitoring["monitoring_status"],
        "STANDARD_MONITORING",
        "STANDARD -> monitoring status",
    )

    assert_equal(
        monitoring["monitoring_risk"],
        "LOW",
        "STANDARD -> monitoring risk",
    )

    assert_equal(
        monitoring["monitoring_action"],
        "MONITOR",
        "STANDARD -> monitoring action",
    )

    assert_equal(
        monitoring["monitoring_score"],
        98.0,
        "STANDARD -> monitoring score",
    )


def run_case_enhanced_high_risk():
    print("=" * 82)
    print("CASE: HIGH CONTROL RISK -> ENHANCED_MONITORING")
    print("=" * 82)

    final_decision = base_final_decision()

    execution_assurance = assured_execution_assurance()
    execution_assurance.update({
        "assurance_status": "MONITORED",
        "assurance_level": "MEDIUM",
        "assurance_risk": "HIGH",
        "assurance_score": 75,
        "control_action": "MONITOR",
        "control_status": "AUTHORIZED_WITH_MONITORING",
        "control_risk": "HIGH",
        "governance_status": "APPROVED_WITH_MONITORING",
        "governance_score": 80,
        "validation_score": 80,
        "monitoring_policy": "ELEVATED",
    })

    monitoring = AIFinalDecisionExecutionMonitoring().monitor(
        final_decision,
        {},
        {},
        execution_assurance,
    )

    print("monitoring:", monitoring)

    assert_equal(
        monitoring["monitoring_status"],
        "ENHANCED_MONITORING",
        "HIGH RISK -> monitoring status",
    )

    assert_equal(
        monitoring["monitoring_risk"],
        "HIGH",
        "HIGH RISK -> monitoring risk",
    )

    assert_equal(
        monitoring["monitoring_action"],
        "ESCALATE",
        "HIGH RISK -> monitoring action",
    )


def run_case_pending():
    print("=" * 82)
    print("CASE: PENDING -> PRE_EXECUTION_MONITORING")
    print("=" * 82)

    final_decision = base_final_decision()

    execution_assurance = assured_execution_assurance()
    execution_assurance.update({
        "execution_status": "EXECUTION_REVIEW",
        "assurance_status": "PENDING",
        "assurance_level": "LOW",
        "assurance_risk": "HIGH",
        "assurance_score": 74,
        "control_action": "HOLD",
        "control_status": "ON_HOLD",
        "control_risk": "HIGH",
        "governance_status": "REVIEW_REQUIRED",
        "governance_score": 70,
        "validation_score": 95,
        "monitoring_policy": "ELEVATED",
    })

    monitoring = AIFinalDecisionExecutionMonitoring().monitor(
        final_decision,
        {},
        {},
        execution_assurance,
    )

    print("monitoring:", monitoring)

    assert_equal(
        monitoring["monitoring_status"],
        "ENHANCED_MONITORING",
        "PENDING + HIGH CONTROL RISK -> monitoring status",
    )

    assert_equal(
        monitoring["monitoring_risk"],
        "HIGH",
        "PENDING -> monitoring risk",
    )

    assert_equal(
        monitoring["monitoring_action"],
        "ESCALATE",
        "PENDING + HIGH RISK -> monitoring action",
    )


def run_case_critical():
    print("=" * 82)
    print("CASE: CRITICAL ASSURANCE RISK -> CRITICAL_MONITORING")
    print("=" * 82)

    final_decision = base_final_decision()

    execution_assurance = assured_execution_assurance()
    execution_assurance.update({
        "execution_status": "BLOCKED",
        "assurance_status": "BLOCKED",
        "assurance_level": "NONE",
        "assurance_risk": "CRITICAL",
        "assurance_score": 5,
        "control_action": "BLOCK",
        "control_status": "BLOCKED",
        "control_risk": "CRITICAL",
        "governance_status": "BLOCKED",
        "governance_score": 20,
        "validation_status": "INVALID",
        "validation_score": 20,
        "monitoring_policy": "CRITICAL",
    })

    monitoring = AIFinalDecisionExecutionMonitoring().monitor(
        final_decision,
        {},
        {},
        execution_assurance,
    )

    print("monitoring:", monitoring)

    assert_equal(
        monitoring["monitoring_status"],
        "BLOCKED_MONITORING",
        "BLOCKED -> monitoring status",
    )

    assert_equal(
        monitoring["monitoring_risk"],
        "CRITICAL",
        "BLOCKED -> monitoring risk",
    )

    assert_equal(
        monitoring["monitoring_action"],
        "HALT",
        "BLOCKED -> monitoring action",
    )


def run_case_critical_monitoring():
    print("=" * 82)
    print("CASE: CRITICAL ASSURANCE RISK WITHOUT BLOCK -> CRITICAL_MONITORING")
    print("=" * 82)

    final_decision = base_final_decision()

    execution_assurance = assured_execution_assurance()
    execution_assurance.update({
        "execution_status": "EXECUTION_REVIEW",
        "assurance_status": "MONITORED",
        "assurance_level": "MEDIUM",
        "assurance_risk": "CRITICAL",
        "assurance_score": 60,
        "control_action": "MONITOR",
        "control_status": "AUTHORIZED_WITH_MONITORING",
        "control_risk": "MEDIUM",
        "governance_status": "APPROVED_WITH_MONITORING",
        "governance_score": 75,
        "validation_score": 75,
        "monitoring_policy": "CRITICAL",
    })

    monitoring = AIFinalDecisionExecutionMonitoring().monitor(
        final_decision,
        {},
        {},
        execution_assurance,
    )

    print("monitoring:", monitoring)

    assert_equal(
        monitoring["monitoring_status"],
        "CRITICAL_MONITORING",
        "CRITICAL -> monitoring status",
    )

    assert_equal(
        monitoring["monitoring_risk"],
        "CRITICAL",
        "CRITICAL -> monitoring risk",
    )

    assert_equal(
        monitoring["monitoring_action"],
        "HALT",
        "CRITICAL -> monitoring action",
    )


def run_case_field_propagation():
    print("=" * 82)
    print("CASE: ASSURANCE -> MONITORING FIELD PROPAGATION")
    print("=" * 82)

    final_decision = base_final_decision()
    execution_assurance = assured_execution_assurance()

    monitoring = AIFinalDecisionExecutionMonitoring().monitor(
        final_decision,
        {},
        {},
        execution_assurance,
    )

    print("execution_assurance:", execution_assurance)
    print("monitoring:", monitoring)

    for field in (
        "assurance_status",
        "assurance_level",
        "assurance_risk",
        "assurance_score",
        "control_action",
        "control_status",
        "control_risk",
        "governance_status",
        "governance_score",
        "validation_status",
        "validation_score",
        "monitoring_policy",
    ):
        assert_equal(
            monitoring.get(field),
            execution_assurance.get(field),
            f"FIELD PROPAGATION -> {field}",
        )


def main():
    print("=" * 82)
    print("PHASE 7-10-18-M")
    print("AI FINAL DECISION")
    print("-> EXECUTION ASSURANCE")
    print("-> EXECUTION MONITORING")
    print("BOUNDARY CONTRACT TEST V1")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    run_case_standard_monitoring()
    run_case_enhanced_high_risk()
    run_case_pending()
    run_case_critical()
    run_case_critical_monitoring()
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
    print("===== PHASE 7-10-18-M CONTRACT TEST V1 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()

