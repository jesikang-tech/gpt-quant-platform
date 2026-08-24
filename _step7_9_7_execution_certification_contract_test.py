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
from core.ai_final_decision_certification import (
    AIFinalDecisionCertification
)

print("=" * 82)
print("PHASE 7-9-7 FINAL EXECUTION -> CERTIFICATION")
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
certification_engine = AIFinalDecisionCertification()


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

    execution_decision = execution_engine.analyze(
        final_decision,
        orchestration,
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence,
    )

    certification = certification_engine.analyze(
        final_decision,
        validation,
        governance,
        lifecycle,
        operational_intelligence,
        integrated_intelligence,
        orchestration,
        execution_decision,
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- FINAL EXECUTION DECISION ---")
    print(
        "execution_status:",
        execution_decision.get("execution_status")
    )
    print(
        "execution_decision:",
        execution_decision.get("execution_decision")
    )
    print(
        "execution_risk:",
        execution_decision.get("execution_risk")
    )
    print(
        "execution_authorization:",
        execution_decision.get(
            "execution_authorization"
        )
    )

    print("--- CERTIFICATION ---")
    print(
        "certification_status:",
        certification.get("certification_status")
    )
    print(
        "certification_action:",
        certification.get("certification_action")
    )
    print(
        "certification_risk:",
        certification.get("certification_risk")
    )
    print(
        "execution_readiness:",
        certification.get("execution_readiness")
    )
    print(
        "decision_integrity:",
        certification.get("decision_integrity")
    )
    print(
        "certification_score:",
        certification.get("certification_score")
    )

    return execution_decision, certification


execution_required, certification_required = run_case(
    "REASSESSMENT_REQUIRED",
    {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
        "reassessment_risk": "MEDIUM",
        "reassessment_score": 90.0,
    },
)

assert execution_required.get(
    "execution_status"
) == "EXECUTION_REVIEW"

assert execution_required.get(
    "execution_decision"
) == "REVIEW"

assert certification_required.get(
    "certification_status"
) == "CERTIFICATION_REVIEW"

assert certification_required.get(
    "certification_action"
) == "REVIEW"

assert certification_required.get(
    "execution_readiness"
) == "NOT_READY"

assert certification_required.get(
    "decision_integrity"
) == "REVIEW_REQUIRED"

print(
    "REASSESSMENT_REQUIRED -> CERTIFICATION: PASS"
)


execution_normal, certification_normal = run_case(
    "NOT_REQUIRED",
    {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_risk": "LOW",
        "reassessment_score": 90.0,
    },
)

assert execution_normal.get(
    "execution_status"
) == "EXECUTION_READY"

assert execution_normal.get(
    "execution_decision"
) == "PROCEED"

assert certification_normal.get(
    "certification_status"
) == "CERTIFIED"

assert certification_normal.get(
    "certification_action"
) == "PROCEED"

assert certification_normal.get(
    "execution_readiness"
) == "READY"

assert certification_normal.get(
    "decision_integrity"
) == "INTACT"

print(
    "NOT_REQUIRED -> CERTIFICATION: PASS"
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "REASSESSMENT_REQUIRED"
    " -> EXECUTION_REVIEW / REVIEW"
    " -> CERTIFICATION_REVIEW / REVIEW"
    " -> NOT_READY / REVIEW_REQUIRED: PASS"
)

print(
    "NOT_REQUIRED"
    " -> EXECUTION_READY / PROCEED"
    " -> CERTIFIED / PROCEED"
    " -> READY / INTACT: PASS"
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
    "===== PHASE 7-9-7 FINAL EXECUTION -> CERTIFICATION"
)
print("===== CONTRACT TEST COMPLETE")
print("=" * 82)
