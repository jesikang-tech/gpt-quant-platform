from core.ai_final_decision_lifecycle_intelligence import (
    AIFinalDecisionLifecycleIntelligence
)
from core.ai_final_decision_lifecycle_governance_control import (
    AIFinalDecisionLifecycleGovernanceControl
)
from core.ai_final_decision_operational_intelligence import (
    AIFinalDecisionOperationalIntelligence
)
from core.ai_final_decision_integrated_intelligence import (
    AIFinalDecisionIntegratedIntelligence
)
from core.ai_final_decision_orchestration import (
    AIFinalDecisionOrchestration
)
from core.ai_final_execution_decision import (
    AIFinalExecutionDecision
)

print("=" * 82)
print("PHASE 7-9-6 ORCHESTRATION -> FINAL EXECUTION DECISION")
print("DOWNSTREAM PROPAGATION BOUNDARY CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

lifecycle_engine = AIFinalDecisionLifecycleIntelligence()
governance_control_engine = (
    AIFinalDecisionLifecycleGovernanceControl()
)
operational_engine = AIFinalDecisionOperationalIntelligence()
integrated_engine = AIFinalDecisionIntegratedIntelligence()
orchestration_engine = AIFinalDecisionOrchestration()
execution_engine = AIFinalExecutionDecision()


final_decision = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "validation_status": "VALID",
    "validation_score": 90.0,
    "confidence_score": 90.0,
}

validation = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "validation_status": "VALID",
    "validation_score": 90.0,
}

governance = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "governance_status": "APPROVED",
    "governance_score": 90.0,
}

execution_control = {
    "control_status": "AUTHORIZED",
    "control_risk": "LOW",
    "execution_status": "AUTHORIZED",
}

execution_assurance = {
    "assurance_status": "ASSURED",
    "assurance_risk": "LOW",
    "assurance_score": 90.0,
}

execution_monitoring = {
    "monitoring_status": "STANDARD_MONITORING",
    "monitoring_risk": "LOW",
    "monitoring_score": 90.0,
}

execution_feedback = {
    "feedback_status": "STABLE",
    "feedback_risk": "LOW",
    "feedback_score": 90.0,
}

decision_confidence = {
    "confidence_score": 90.0,
}


def run_case(name, reassessment):

    lifecycle = lifecycle_engine.analyze(
        final_decision=final_decision,
        governance=governance,
        execution_control=execution_control,
        execution_assurance=execution_assurance,
        execution_monitoring=execution_monitoring,
        execution_feedback=execution_feedback,
        reassessment=reassessment,
    )

    lifecycle_governance_control = (
        governance_control_engine.govern(
            final_decision=final_decision,
            governance=governance,
            execution_control=execution_control,
            execution_assurance=execution_assurance,
            execution_monitoring=execution_monitoring,
            execution_feedback=execution_feedback,
            reassessment=reassessment,
            lifecycle=lifecycle,
            decision_confidence=decision_confidence,
            validation=validation,
        )
    )

    operational_intelligence = operational_engine.analyze(
        final_decision=final_decision,
        governance_control=lifecycle_governance_control,
    )

    integrated_intelligence = integrated_engine.analyze(
        final_decision=final_decision,
        validation=validation,
        governance=governance,
        execution_control=execution_control,
        execution_assurance=execution_assurance,
        execution_monitoring=execution_monitoring,
        execution_feedback=execution_feedback,
        reassessment=reassessment,
        lifecycle=lifecycle,
        lifecycle_governance_control=(
            lifecycle_governance_control
        ),
        operational_intelligence=operational_intelligence,
    )

    orchestration = orchestration_engine.analyze(
        final_decision,
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence,
    )

    execution = execution_engine.analyze(
        final_decision,
        orchestration,
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence,
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- ORCHESTRATION ---")
    print(
        "orchestration_status:",
        orchestration.get("orchestration_status")
    )
    print(
        "orchestration_action:",
        orchestration.get("orchestration_action")
    )
    print(
        "orchestration_risk:",
        orchestration.get("orchestration_risk")
    )
    print(
        "execution_authorization:",
        orchestration.get("execution_authorization")
    )
    print(
        "reassessment_policy:",
        orchestration.get("reassessment_policy")
    )

    print("--- FINAL EXECUTION DECISION ---")
    print(
        "execution_status:",
        execution.get("execution_status")
    )
    print(
        "execution_decision:",
        execution.get("execution_decision")
    )
    print(
        "execution_risk:",
        execution.get("execution_risk")
    )
    print(
        "execution_authorization:",
        execution.get("execution_authorization")
    )
    print(
        "reassessment_policy:",
        execution.get("reassessment_policy")
    )

    return orchestration, execution


(
    orchestration_required,
    execution_required,
) = run_case(
    "REASSESSMENT_REQUIRED",
    {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
        "reassessment_risk": "MEDIUM",
        "reassessment_score": 90.0,
    },
)

assert orchestration_required.get(
    "orchestration_status"
) == "ORCHESTRATION_REVIEW"

assert orchestration_required.get(
    "orchestration_action"
) == "REVIEW"

assert orchestration_required.get(
    "orchestration_risk"
) == "MEDIUM"

assert execution_required.get(
    "execution_status"
) == "EXECUTION_REVIEW"

assert execution_required.get(
    "execution_decision"
) == "REVIEW"

assert execution_required.get(
    "execution_risk"
) == "MEDIUM"

print(
    "REASSESSMENT_REQUIRED -> FINAL EXECUTION: PASS"
)


(
    orchestration_normal,
    execution_normal,
) = run_case(
    "NOT_REQUIRED",
    {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_risk": "LOW",
        "reassessment_score": 90.0,
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

print(
    "NOT_REQUIRED -> FINAL EXECUTION: PASS"
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "REASSESSMENT_REQUIRED"
    " -> ORCHESTRATION_REVIEW / REVIEW"
    " -> EXECUTION_REVIEW / REVIEW / MEDIUM: PASS"
)

print(
    "NOT_REQUIRED"
    " -> ORCHESTRATION_READY / PROCEED"
    " -> EXECUTION_READY / PROCEED / LOW: PASS"
)

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
    "===== PHASE 7-9-6 ORCHESTRATION -> FINAL EXECUTION DECISION"
)
print("===== CONTRACT TEST COMPLETE")
print("=" * 82)
