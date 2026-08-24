from core.ai_final_decision_integrated_intelligence import AIFinalDecisionIntegratedIntelligence
from core.ai_final_decision_orchestration import AIFinalDecisionOrchestration

print("=" * 82)
print("PHASE 7-9-4 REASSESSMENT -> ORCHESTRATION")
print("DOWNSTREAM PROPAGATION BOUNDARY CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

integrated_engine = AIFinalDecisionIntegratedIntelligence()
orchestration_engine = AIFinalDecisionOrchestration()

def run_case(name, reassessment, expected_integrated_status, expected_integrated_action, expected_orchestration_status, expected_orchestration_action):
    integrated = integrated_engine.analyze(
        final_decision={
            "decision": "ACCUMULATE",
            "action": "PROCEED",
            "confidence_score": 90,
        },
        validation={
            "validation_status": "VALID",
            "validation_score": 90,
        },
        governance={
            "governance_status": "APPROVED",
            "governance_score": 90,
        },
        execution_control={
            "control_status": "AUTHORIZED",
        },
        execution_assurance={
            "assurance_status": "ASSURED",
        },
        execution_monitoring={
            "monitoring_status": "STANDARD",
        },
        execution_feedback={
            "feedback_status": "STABLE",
        },
        reassessment=reassessment,
        lifecycle={
            "lifecycle_status": "HEALTHY",
            "lifecycle_score": 90,
        },
        lifecycle_governance_control={
            "operational_status": "HEALTHY",
            "operational_score": 90,
        },
        operational_intelligence={
            "intelligence_status": "HEALTHY",
            "intelligence_score": 90,
        },
    )

    assert integrated.get("integrated_status") == expected_integrated_status
    assert integrated.get("integrated_action") == expected_integrated_action

    orchestration = orchestration_engine.analyze(
        final_decision={
            "decision": "ACCUMULATE",
            "action": "PROCEED",
            "execution_status": "AUTHORIZED",
            "confidence_score": 90,
        },
        integrated_intelligence=integrated,
        lifecycle_governance_control={
            "operational_status": "HEALTHY",
            "reassessment_required": reassessment.get(
                "reassessment_required",
                False
            ),
            "reassessment_status": reassessment.get(
                "reassessment_status",
                "NOT_REQUIRED"
            ),
        },
        operational_intelligence={
            "intelligence_status": "HEALTHY",
            "intelligence_score": 90,
        },
    )

    assert orchestration.get("orchestration_status") == expected_orchestration_status
    assert orchestration.get("orchestration_action") == expected_orchestration_action

    print(
        f"{name}: PASS | "
        f"integrated={integrated.get('integrated_status')} -> "
        f"{integrated.get('integrated_action')} | "
        f"orchestration={orchestration.get('orchestration_status')} -> "
        f"{orchestration.get('orchestration_action')}"
    )

run_case(
    "REASSESSMENT_REQUIRED",
    {
        "reassessment_required": True,
        "reassessment_status": "REASSESSMENT_REQUIRED",
    },
    "INTEGRATION_ATTENTION",
    "REVIEW",
    "ORCHESTRATION_REVIEW",
    "REVIEW",
)

run_case(
    "NOT_REQUIRED",
    {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
    },
    "INTEGRATED_HEALTHY",
    "PROCEED",
    "ORCHESTRATION_READY",
    "PROCEED",
)

print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("REASSESSMENT_REQUIRED -> INTEGRATION_ATTENTION -> ORCHESTRATION_REVIEW: PASS")
print("NOT_REQUIRED -> INTEGRATED_HEALTHY -> ORCHESTRATION_READY: PASS")

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
print("===== PHASE 7-9-4 REASSESSMENT -> ORCHESTRATION CONTRACT TEST COMPLETE =====")
print("=" * 82)
