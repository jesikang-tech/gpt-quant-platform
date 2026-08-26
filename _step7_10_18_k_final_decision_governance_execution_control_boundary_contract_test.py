"""
PHASE 7-10-18-K
AI FINAL DECISION
->
FINAL DECISION GOVERNANCE
->
EXECUTION CONTROL
BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_final_decision_integration import (
    AIFinalDecisionIntegration,
)
from core.ai_final_decision_governance import (
    AIFinalDecisionGovernance,
)
from core.ai_final_decision_execution_control import (
    AIFinalDecisionExecutionControl,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )


def base_final_decision():
    return {
        "decision": "MAINTAIN",
        "action": "REVIEW_REQUIRED",
        "execution_status": "UNDETERMINED",
        "confidence_score": 90,
        "confidence_level": "HIGH",
        "confidence_grade": "A",
        "validation_status": "VALID",
        "validation_score": 95,
        "recommendation": "PROCEED",
        "risk_level": "LOW",
        "monitoring": "STANDARD",
        "strategy": "MAINTAIN",
        "market_view": "NEUTRAL",
        "adaptive_action": "MONITOR_CLOSELY",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
        "reliability": "HIGH",
        "optimization_status": "OPTIMAL",
    }


def run_case_approved_execute():
    print("=" * 82)
    print("CASE: APPROVED + READY -> EXECUTE")
    print("=" * 82)

    final_decision = base_final_decision()
    final_decision.update({
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "confidence_score": 95,
        "validation_score": 95,
    })

    governance = AIFinalDecisionGovernance().govern(
        final_decision
    )

    control = AIFinalDecisionExecutionControl().control(
        final_decision,
        governance,
    )

    print("governance:", governance)
    print("control:", control)

    assert_equal(
        governance["execution_readiness"],
        "READY",
        "APPROVED -> execution readiness",
    )

    assert_equal(
        governance["risk_governance"],
        "ACCEPTABLE",
        "APPROVED -> risk governance",
    )

    assert_equal(
        governance["governance_status"],
        "APPROVED",
        "APPROVED -> governance status",
    )

    assert_equal(
        control["control_action"],
        "EXECUTE",
        "APPROVED -> control action",
    )

    assert_equal(
        control["control_status"],
        "AUTHORIZED",
        "APPROVED -> control status",
    )


def run_case_rejected_block():
    print("=" * 82)
    print("CASE: BLOCKED -> BLOCK")
    print("=" * 82)

    final_decision = base_final_decision()
    final_decision.update({
        "action": "REVIEW_REQUIRED",
        "execution_status": "BLOCKED",
        "confidence_score": 20,
        "validation_status": "INVALID",
        "validation_score": 20,
        "decision_alignment": "CONFLICT",
        "decision_consistency": "OVERRIDDEN",
    })

    governance = AIFinalDecisionGovernance().govern(
        final_decision
    )

    control = AIFinalDecisionExecutionControl().control(
        final_decision,
        governance,
    )

    print("governance:", governance)
    print("control:", control)

    assert_equal(
        governance["governance_status"],
        "BLOCKED",
        "BLOCKED -> governance status",
    )

    assert_equal(
        control["control_action"],
        "BLOCK",
        "BLOCKED -> control action",
    )

    assert_equal(
        control["control_status"],
        "BLOCKED",
        "BLOCKED -> control status",
    )


def run_case_monitor():
    print("=" * 82)
    print("CASE: CONDITIONAL / HIGH ATTENTION -> MONITOR")
    print("=" * 82)

    final_decision = base_final_decision()
    final_decision.update({
        "action": "REVIEW_REQUIRED",
        "execution_status": "EXECUTION_REVIEW",
        "confidence_score": 80,
        "validation_score": 80,
        "monitoring": "HIGH",
    })

    governance = AIFinalDecisionGovernance().govern(
        final_decision
    )

    control = AIFinalDecisionExecutionControl().control(
        final_decision,
        governance,
    )

    print("governance:", governance)
    print("control:", control)

    assert_equal(
        governance["execution_readiness"],
        "CONDITIONAL",
        "MONITOR -> execution readiness",
    )

    assert_equal(
        control["control_action"],
        "MONITOR",
        "MONITOR -> control action",
    )

    assert_equal(
        control["control_status"],
        "AUTHORIZED_WITH_MONITORING",
        "MONITOR -> control status",
    )


def run_case_override():
    print("=" * 82)
    print("CASE: OVERRIDE ACTIVE -> CONTROL PROPAGATION")
    print("=" * 82)

    final_decision = base_final_decision()
    final_decision.update({
        "action": "REDUCE_RISK",
        "execution_status": "EXECUTION_REVIEW",
        "confidence_score": 85,
        "validation_score": 90,
        "decision_alignment": "CONFLICT",
        "decision_consistency": "OVERRIDDEN",
        "adaptive_action": "REDUCE_RISK",
    })

    validation = {
        "decision_alignment": "CONFLICT",
        "decision_consistency": "OVERRIDDEN",
        "reliability": "HIGH",
        "adaptive_action": "REDUCE_RISK",
        "validation_status": "VALID",
        "validation_score": 90,
    }

    intelligence = {
        "adaptive_override": True,
        "adaptive_override_reason": (
            "Adaptive strategy prioritized risk reduction."
        ),
    }

    governance = AIFinalDecisionGovernance().govern(
        final_decision,
        validation=validation,
        intelligence=intelligence,
    )

    control = AIFinalDecisionExecutionControl().control(
        final_decision,
        governance,
    )

    print("governance:", governance)
    print("control:", control)

    assert_equal(
        governance["override_status"],
        "OVERRIDE_ACTIVE",
        "OVERRIDE -> governance override",
    )

    assert_equal(
        control["override_status"],
        "OVERRIDE_ACTIVE",
        "OVERRIDE -> control override propagation",
    )

    assert_equal(
        control["risk_governance"],
        governance["risk_governance"],
        "OVERRIDE -> risk propagation",
    )


def run_case_field_propagation():
    print("=" * 82)
    print("CASE: GOVERNANCE -> CONTROL FIELD PROPAGATION")
    print("=" * 82)

    final_decision = base_final_decision()

    governance = AIFinalDecisionGovernance().govern(
        final_decision
    )

    control = AIFinalDecisionExecutionControl().control(
        final_decision,
        governance,
    )

    print("governance:", governance)
    print("control:", control)

    for field in (
        "governance_status",
        "governance_score",
        "execution_readiness",
        "risk_governance",
        "override_status",
        "monitoring_policy",
        "confidence_score",
        "validation_status",
        "validation_score",
    ):
        assert_equal(
            control.get(field),
            governance.get(field),
            f"FIELD PROPAGATION -> {field}",
        )


def main():
    print("=" * 82)
    print("PHASE 7-10-18-K")
    print("AI FINAL DECISION")
    print("-> FINAL DECISION GOVERNANCE")
    print("-> EXECUTION CONTROL")
    print("BOUNDARY CONTRACT TEST V1")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    run_case_approved_execute()
    run_case_rejected_block()
    run_case_monitor()
    run_case_override()
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
    print("===== PHASE 7-10-18-K CONTRACT TEST V1 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()
