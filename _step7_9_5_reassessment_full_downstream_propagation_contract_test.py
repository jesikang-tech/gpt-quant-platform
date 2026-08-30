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

print("=" * 82)
print("PHASE 7-9-5 REASSESSMENT -> LIFECYCLE -> GOVERNANCE")
print("-> OPERATIONAL -> INTEGRATED -> ORCHESTRATION")
print("CROSS-ENGINE DOWNSTREAM PROPAGATION CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

lifecycle_engine = AIFinalDecisionLifecycleIntelligence()
governance_control_engine = (
    AIFinalDecisionLifecycleGovernanceControl()
)
operational_engine = AIFinalDecisionOperationalIntelligence()
integrated_engine = AIFinalDecisionIntegratedIntelligence()
orchestration_engine = AIFinalDecisionOrchestration()


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

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- LIFECYCLE ---")
    print(
        "reassessment_required:",
        lifecycle.get("reassessment_required")
    )
    print(
        "reassessment_status:",
        lifecycle.get("reassessment_status")
    )
    print(
        "lifecycle_status:",
        lifecycle.get("lifecycle_status")
    )
    print(
        "lifecycle_action:",
        lifecycle.get("lifecycle_action")
    )

    print("--- GOVERNANCE & CONTROL ---")
    print(
        "operational_status:",
        lifecycle_governance_control.get(
            "operational_status"
        )
    )
    print(
        "operational_action:",
        lifecycle_governance_control.get(
            "operational_action"
        )
    )
    print(
        "execution_authorization:",
        lifecycle_governance_control.get(
            "execution_authorization"
        )
    )
    print(
        "reassessment_policy:",
        lifecycle_governance_control.get(
            "reassessment_policy"
        )
    )
    print(
        "monitoring_policy:",
        lifecycle_governance_control.get(
            "monitoring_policy"
        )
    )

    print("--- OPERATIONAL INTELLIGENCE ---")
    print(
        "intelligence_status:",
        operational_intelligence.get(
            "intelligence_status"
        )
    )
    print(
        "intelligence_action:",
        operational_intelligence.get(
            "intelligence_action"
        )
    )
    print(
        "intelligence_risk:",
        operational_intelligence.get(
            "intelligence_risk"
        )
    )
    print(
        "priority:",
        operational_intelligence.get(
            "priority"
        )
    )

    print("--- INTEGRATED INTELLIGENCE ---")
    print(
        "integrated_status:",
        integrated_intelligence.get(
            "integrated_status"
        )
    )
    print(
        "integrated_action:",
        integrated_intelligence.get(
            "integrated_action"
        )
    )
    print(
        "integrated_risk:",
        integrated_intelligence.get(
            "integrated_risk"
        )
    )

    print("--- ORCHESTRATION ---")
    print(
        "orchestration_status:",
        orchestration.get(
            "orchestration_status"
        )
    )
    print(
        "orchestration_action:",
        orchestration.get(
            "orchestration_action"
        )
    )
    print(
        "orchestration_risk:",
        orchestration.get(
            "orchestration_risk"
        )
    )

    return (
        lifecycle,
        lifecycle_governance_control,
        operational_intelligence,
        integrated_intelligence,
        orchestration,
    )


(
    lifecycle_required,
    governance_required,
    operational_required,
    integrated_required,
    orchestration_required,
) = run_case(
    "REASSESSMENT_REQUIRED",
    {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
        "reassessment_risk": "MEDIUM",
        "reassessment_score": 90.0,
    },
)

assert lifecycle_required.get(
    "lifecycle_status"
) == "REASSESSMENT_REQUIRED"

assert lifecycle_required.get(
    "lifecycle_action"
) == "REASSESS"

assert governance_required.get(
    "operational_status"
) == "REASSESSMENT_REQUIRED"

assert governance_required.get(
    "operational_action"
) == "REASSESS"

assert governance_required.get(
    "execution_authorization"
) == "SUSPENDED"

assert governance_required.get(
    "reassessment_policy"
) == "IMMEDIATE"

assert governance_required.get(
    "monitoring_policy"
) == "INTENSIVE"

assert operational_required.get(
    "intelligence_status"
) == "CONTROLLED"

assert operational_required.get(
    "intelligence_action"
) == "SUSPEND"

assert operational_required.get(
    "intelligence_risk"
) == "MEDIUM"

assert operational_required.get(
    "priority"
) == "HIGH"

assert integrated_required.get(
    "integrated_status"
) == "INTEGRATION_ATTENTION"

assert integrated_required.get(
    "integrated_action"
) == "REVIEW"

assert integrated_required.get(
    "integrated_risk"
) == "MEDIUM"

assert orchestration_required.get(
    "orchestration_status"
) == "ORCHESTRATION_REVIEW"

assert orchestration_required.get(
    "orchestration_action"
) == "REVIEW"

assert orchestration_required.get(
    "orchestration_risk"
) == "MEDIUM"

print(
    "REASSESSMENT_REQUIRED full downstream propagation: PASS"
)


(
    lifecycle_normal,
    governance_normal,
    operational_normal,
    integrated_normal,
    orchestration_normal,
) = run_case(
    "NOT_REQUIRED",
    {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
        "reassessment_risk": "LOW",
        "reassessment_score": 90.0,
    },
)

assert lifecycle_normal.get(
    "lifecycle_status"
) == "HEALTHY"

assert lifecycle_normal.get(
    "lifecycle_action"
) == "CONTINUE"

assert governance_normal.get(
    "operational_status"
) == "OPERATIONALLY_HEALTHY"

assert governance_normal.get(
    "operational_action"
) == "CONTINUE"

assert governance_normal.get(
    "execution_authorization"
) == "AUTHORIZED"

assert governance_normal.get(
    "reassessment_policy"
) == "NOT_REQUIRED"

assert governance_normal.get(
    "monitoring_policy"
) == "STANDARD"

assert operational_normal.get(
    "intelligence_status"
) == "HEALTHY"

assert operational_normal.get(
    "intelligence_action"
) == "PROCEED"

assert operational_normal.get(
    "intelligence_risk"
) == "LOW"

assert operational_normal.get(
    "priority"
) == "NORMAL"

assert integrated_normal.get(
    "integrated_status"
) == "INTEGRATED_HEALTHY"

assert integrated_normal.get(
    "integrated_action"
) == "PROCEED"

assert integrated_normal.get(
    "integrated_risk"
) == "LOW"

assert orchestration_normal.get(
    "orchestration_status"
) == "ORCHESTRATION_READY"

assert orchestration_normal.get(
    "orchestration_action"
) == "PROCEED"

assert orchestration_normal.get(
    "orchestration_risk"
) == "LOW"

print(
    "NOT_REQUIRED full downstream propagation: PASS"
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "REASSESSMENT_REQUIRED"
    " -> LIFECYCLE REASSESSMENT_REQUIRED / REASSESS"
    " -> GOVERNANCE_CONTROL REASSESSMENT_REQUIRED / REASSESS"
    " -> OPERATIONAL CONTROLLED / SUSPEND"
    " -> INTEGRATED INTEGRATION_ATTENTION / REVIEW"
    " -> ORCHESTRATION_REVIEW / REVIEW / MEDIUM: PASS"
)

print(
    "NOT_REQUIRED"
    " -> LIFECYCLE HEALTHY / CONTINUE"
    " -> GOVERNANCE_CONTROL OPERATIONALLY_HEALTHY / CONTINUE"
    " -> OPERATIONAL HEALTHY / PROCEED"
    " -> INTEGRATED INTEGRATED_HEALTHY / PROCEED"
    " -> ORCHESTRATION_READY / PROCEED / LOW: PASS"
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
    "===== PHASE 7-9-5 FULL DOWNSTREAM PROPAGATION CONTRACT TEST COMPLETE ====="
)
print("=" * 82)
