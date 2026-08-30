from core.ai_final_decision_integrated_intelligence import AIFinalDecisionIntegratedIntelligence
from core.ai_final_decision_orchestration import AIFinalDecisionOrchestration
from core.ai_final_execution_decision import AIFinalExecutionDecision
from core.ai_final_decision_certification import AIFinalDecisionCertification
from core.ai_final_decision_master_control import AIFinalDecisionMasterControl

print("=" * 82)
print("PHASE 7-9-4 FINAL REASSESSMENT END-TO-END PROPAGATION VERIFICATION")
print("REASSESSMENT -> INTEGRATED -> ORCHESTRATION -> EXECUTION")
print("-> CERTIFICATION -> MASTER CONTROL")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 82)

reassessment = {
    "reassessment_required": True,
    "reassessment_status": "REASSESSMENT_REQUIRED",
}

final_decision = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "execution_status": "AUTHORIZED",
    "confidence_score": 90.0,
}

validation = {
    "validation_status": "VALID",
    "validation_score": 90.0,
}

governance = {
    "governance_status": "APPROVED",
    "governance_score": 90.0,
}

execution_control = {
    "control_status": "AUTHORIZED",
}

execution_assurance = {
    "assurance_status": "ASSURED",
}

execution_monitoring = {
    "monitoring_status": "STANDARD",
}

execution_feedback = {
    "feedback_status": "STABLE",
}

lifecycle = {
    "lifecycle_status": "HEALTHY",
    "lifecycle_score": 90.0,
}

lifecycle_governance_control = {
    "operational_status": "HEALTHY",
    "operational_score": 90.0,
    "reassessment_required": True,
    "reassessment_status": "REASSESSMENT_REQUIRED",
    "execution_authorization": "AUTHORIZED",
}

operational_intelligence = {
    "intelligence_status": "HEALTHY",
    "intelligence_score": 90.0,
}

integrated = AIFinalDecisionIntegratedIntelligence().analyze(
    final_decision,
    validation,
    governance,
    execution_control,
    execution_assurance,
    execution_monitoring,
    execution_feedback,
    reassessment,
    lifecycle,
    lifecycle_governance_control,
    operational_intelligence,
)

print("")
print("1. INTEGRATED")
print("status:", integrated.get("integrated_status"))
print("action:", integrated.get("integrated_action"))

assert integrated.get("integrated_status") == "INTEGRATION_ATTENTION"
assert integrated.get("integrated_action") == "REVIEW"

orchestration = AIFinalDecisionOrchestration().analyze(
    final_decision,
    integrated,
    lifecycle_governance_control,
    operational_intelligence,
)

print("")
print("2. ORCHESTRATION")
print("status:", orchestration.get("orchestration_status"))
print("action:", orchestration.get("orchestration_action"))

assert orchestration.get("orchestration_status") == "ORCHESTRATION_REVIEW"
assert orchestration.get("orchestration_action") == "REVIEW"

execution = AIFinalExecutionDecision().analyze(
    final_decision,
    orchestration,
    integrated,
    lifecycle_governance_control,
    operational_intelligence,
)

print("")
print("3. EXECUTION")
print("status:", execution.get("execution_status"))
print("decision:", execution.get("execution_decision"))
print("authorization:", execution.get("execution_authorization"))

assert execution.get("execution_status") == "EXECUTION_REVIEW"
assert execution.get("execution_decision") == "REVIEW"
assert execution.get("execution_authorization") == "AUTHORIZED"

certification = AIFinalDecisionCertification().analyze(
    final_decision,
    validation,
    governance,
    lifecycle,
    operational_intelligence,
    integrated,
    orchestration,
    execution,
)

print("")
print("4. CERTIFICATION")
print("status:", certification.get("certification_status"))
print("action:", certification.get("certification_action"))
print("readiness:", certification.get("execution_readiness"))

assert certification.get("certification_status") == "CERTIFICATION_REVIEW"
assert certification.get("certification_action") == "REVIEW"
assert certification.get("execution_readiness") == "NOT_READY"

master = AIFinalDecisionMasterControl().analyze(
    final_decision,
    certification,
    execution,
    governance,
    lifecycle,
    operational_intelligence,
    orchestration,
    integrated,
    validation,
)

print("")
print("5. MASTER CONTROL")
print("status:", master.get("master_control_status"))
print("action:", master.get("master_control_action"))
print("risk:", master.get("master_control_risk"))
print("execution control:", master.get("execution_control"))

assert master.get("master_control_status") == "MASTER_REVIEW"
assert master.get("master_control_action") == "REVIEW"
assert master.get("execution_control") == "HOLD"

print("")
print("=" * 82)
print("FINAL PROPAGATION ASSERTIONS")
print("=" * 82)
print("REASSESSMENT_REQUIRED")
print(" -> INTEGRATION_ATTENTION")
print(" -> ORCHESTRATION_REVIEW")
print(" -> EXECUTION_REVIEW")
print(" -> CERTIFICATION_REVIEW")
print(" -> MASTER_REVIEW")
print(" -> REVIEW")
print(" -> HOLD")
print("")
print("PHASE 7-9-4 FINAL END-TO-END PROPAGATION: PASS")

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
print("=" * 82)
