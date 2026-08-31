from core.ai_final_decision_integration import AIFinalDecisionIntegration
from core.ai_final_decision_governance import AIFinalDecisionGovernance
from core.ai_final_decision_execution_control import AIFinalDecisionExecutionControl
from core.ai_final_decision_execution_assurance import AIFinalDecisionExecutionAssurance
from core.ai_final_decision_execution_monitoring import AIFinalDecisionExecutionMonitoring
from core.ai_final_decision_execution_feedback import AIFinalDecisionExecutionFeedback
from core.ai_final_decision_reassessment import AIFinalDecisionReassessment
from core.ai_final_decision_lifecycle_governance_control import AIFinalDecisionLifecycleGovernanceControl
from core.ai_final_decision_lifecycle_intelligence import AIFinalDecisionLifecycleIntelligence
from core.ai_final_decision_integrated_intelligence import AIFinalDecisionIntegratedIntelligence
from core.ai_final_decision_operational_intelligence import AIFinalDecisionOperationalIntelligence
from core.ai_final_execution_decision import AIFinalExecutionDecision
from core.ai_final_decision_orchestration import AIFinalDecisionOrchestration
from core.ai_final_decision_certification import AIFinalDecisionCertification
from core.ai_final_decision_master_control import AIFinalDecisionMasterControl

print("=" * 60)
print("PHASE 7-4-4 DOWNSTREAM VALUE PROPAGATION CONTRACT")
print("=" * 60)

# ------------------------------------------------------------
# STEP 1
# Canonical in-memory Final Decision
# ------------------------------------------------------------

final_decision = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "execution_status": "AUTHORIZED",
    "confidence_score": 92.0,
    "validation_status": "VALID",
    "validation_score": 100,
    "intelligence_score": 89.2,
    "strategy": "GROWTH",
    "adaptive_action": "INCREASE_RISK",
    "decision_alignment": "ALIGNED",
    "decision_consistency": "CONSISTENT",
    "reliability": "HIGH",
    "optimization_status": "OPTIMIZED",
}

intelligence = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "confidence_score": 92.0,
    "intelligence_score": 89.2,
    "adaptive_action": "INCREASE_RISK",
    "decision_alignment": "ALIGNED",
    "decision_consistency": "CONSISTENT",
    "reliability": "HIGH",
    "optimization_status": "OPTIMIZED",
}

intelligence_score = {
    "intelligence_score": 89.2,
}

confidence = {
    "confidence_score": 92.0,
}

validation = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "execution_status": "AUTHORIZED",
    "validation_status": "VALID",
    "validation_score": 100,
    "confidence_score": 92.0,
    "risk_level": "LOW",
}

validation_action = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "execution_status": "AUTHORIZED",
    "validation_status": "VALID",
    "validation_score": 100,
    "confidence_score": 92.0,
    "risk_level": "LOW",
}

# ------------------------------------------------------------
# STEP 2
# Governance
# ------------------------------------------------------------

governance = AIFinalDecisionGovernance().govern(
    final_decision,
    intelligence,
    intelligence_score,
    confidence,
    validation,
    validation_action,
)

print()
print("=== STEP 1 GOVERNANCE ===")
print("decision:", governance.get("decision"))
print("action:", governance.get("action"))
print("execution_status:", governance.get("execution_status"))
print("confidence_score:", governance.get("confidence_score"))
print("validation_score:", governance.get("validation_score"))
print("adaptive_action:", governance.get("adaptive_action"))
print("governance_score:", governance.get("governance_score"))

# ------------------------------------------------------------
# STEP 3
# Execution Control
# ------------------------------------------------------------

execution_control = AIFinalDecisionExecutionControl().control(
    final_decision,
    governance,
)

print()
print("=== STEP 2 EXECUTION CONTROL ===")
print("decision:", execution_control.get("decision"))
print("action:", execution_control.get("action"))
print("execution_status:", execution_control.get("execution_status"))
print("confidence_score:", execution_control.get("confidence_score"))
print("validation_score:", execution_control.get("validation_score"))
print("governance_score:", execution_control.get("governance_score"))

# ------------------------------------------------------------
# STEP 4
# Execution Assurance
# ------------------------------------------------------------

execution_assurance = AIFinalDecisionExecutionAssurance().assure(
    final_decision,
    governance,
    execution_control,
)

print()
print("=== STEP 3 EXECUTION ASSURANCE ===")
print("decision:", execution_assurance.get("decision"))
print("action:", execution_assurance.get("action"))
print("execution_status:", execution_assurance.get("execution_status"))
print("confidence_score:", execution_assurance.get("confidence_score"))
print("validation_score:", execution_assurance.get("validation_score"))
print("governance_score:", execution_assurance.get("governance_score"))
print("assurance_score:", execution_assurance.get("assurance_score"))

# ------------------------------------------------------------
# STEP 5
# Execution Monitoring
# ------------------------------------------------------------

execution_monitoring = AIFinalDecisionExecutionMonitoring().monitor(
    final_decision,
    governance,
    execution_control,
    execution_assurance,
)

print()
print("=== STEP 4 EXECUTION MONITORING ===")
print("decision:", execution_monitoring.get("decision"))
print("action:", execution_monitoring.get("action"))
print("execution_status:", execution_monitoring.get("execution_status"))
print("governance_score:", execution_monitoring.get("governance_score"))
print("validation_score:", execution_monitoring.get("validation_score"))
print("assurance_score:", execution_monitoring.get("assurance_score"))
print("monitoring_score:", execution_monitoring.get("monitoring_score"))

# ------------------------------------------------------------
# STEP 6
# Execution Feedback
# ------------------------------------------------------------

execution_feedback = AIFinalDecisionExecutionFeedback().feedback(
    final_decision,
    governance,
    execution_control,
    execution_assurance,
    execution_monitoring,
)

print()
print("=== STEP 5 EXECUTION FEEDBACK ===")
print("decision:", execution_feedback.get("decision"))
print("action:", execution_feedback.get("action"))
print("execution_status:", execution_feedback.get("execution_status"))
print("governance_score:", execution_feedback.get("governance_score"))
print("validation_score:", execution_feedback.get("validation_score"))
print("assurance_score:", execution_feedback.get("assurance_score"))
print("monitoring_score:", execution_feedback.get("monitoring_score"))
print("reassessment_required:", execution_feedback.get("reassessment_required"))

# ------------------------------------------------------------
# STEP 6A
# Reassessment
# ------------------------------------------------------------

reassessment = AIFinalDecisionReassessment().reassess(
    final_decision,
    governance,
    execution_control,
    execution_assurance,
    execution_feedback,
    execution_monitoring
)

print()
print("=== STEP 5A REASSESSMENT ===")
print("decision:", reassessment.get("decision"))
print("action:", reassessment.get("action"))
print("reassessment_required:", reassessment.get("reassessment_required"))
print("reassessment_status:", reassessment.get("reassessment_status"))
print("reassessment_action:", reassessment.get("reassessment_action"))
print("reassessment_risk:", reassessment.get("reassessment_risk"))
print("reassessment_score:", reassessment.get("reassessment_score"))

# ------------------------------------------------------------
lifecycle = AIFinalDecisionLifecycleIntelligence().analyze(
    final_decision,
    governance,
    execution_control,
    execution_assurance,
    execution_monitoring,
    execution_feedback,
    reassessment
)
print()
print("=== STEP 8 LIFECYCLE INTELLIGENCE ===")
print("lifecycle_status:", lifecycle.get("lifecycle_status"))
print("lifecycle_action:", lifecycle.get("lifecycle_action"))
print("lifecycle_risk:", lifecycle.get("lifecycle_risk"))
print("lifecycle_score:", lifecycle.get("lifecycle_score"))
print("lifecycle_grade:", lifecycle.get("lifecycle_grade"))
print("reassessment_required:", lifecycle.get("reassessment_required"))
print("reassessment_status:", lifecycle.get("reassessment_status"))

lifecycle_governance_control = AIFinalDecisionLifecycleGovernanceControl().govern(
    final_decision,
    governance,
    execution_control,
    execution_assurance,
    execution_monitoring,
    execution_feedback,
    reassessment,
    lifecycle,
    confidence,
    validation
)

# STEP 7
# Operational Intelligence
# ------------------------------------------------------------

operational_intelligence = AIFinalDecisionOperationalIntelligence().analyze(
    final_decision,
    lifecycle_governance_control,
)

print()
print("=== STEP 6 OPERATIONAL INTELLIGENCE ===")
print("decision:", operational_intelligence.get("decision"))
print("action:", operational_intelligence.get("action"))
print("execution_status:", operational_intelligence.get("execution_status"))
print("confidence_score:", operational_intelligence.get("confidence_score"))
print("validation_score:", operational_intelligence.get("validation_score"))
print("operational_score:", operational_intelligence.get("operational_score"))

# ------------------------------------------------------------
# STEP 8
# Orchestration
# ------------------------------------------------------------

integrated_intelligence = AIFinalDecisionIntegratedIntelligence().analyze(
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

orchestration = AIFinalDecisionOrchestration().analyze(
    final_decision,
    integrated_intelligence,
    lifecycle_governance_control,
    operational_intelligence,
)

print()
print("=== STEP 7 ORCHESTRATION ===")
print("decision:", orchestration.get("decision"))
print("action:", orchestration.get("action"))
print("confidence_score:", orchestration.get("confidence_score"))
print("governance_score:", orchestration.get("governance_score"))
print("operational_score:", orchestration.get("operational_score"))
print("orchestration_score:", orchestration.get("orchestration_score"))

# ------------------------------------------------------------
# STEP 9
# Certification
# ------------------------------------------------------------

execution_decision = AIFinalExecutionDecision().analyze(
    final_decision,
    orchestration,
    integrated_intelligence,
    lifecycle_governance_control,
    operational_intelligence
)

certification = AIFinalDecisionCertification().analyze(
    final_decision,
    validation,
    governance,
    lifecycle,
    operational_intelligence,
    integrated_intelligence,
    orchestration,
    execution_decision,
)

print()
print("=== STEP 8 CERTIFICATION ===")
print("decision:", certification.get("decision"))
print("action:", certification.get("action"))
print("validation_score:", certification.get("validation_score"))
print("governance_score:", certification.get("governance_score"))
print("operational_score:", certification.get("operational_score"))
print("orchestration_score:", certification.get("orchestration_score"))
print("confidence_score:", certification.get("confidence_score"))
print("certification_score:", certification.get("certification_score"))
print("certification_status:", certification.get("certification_status"))
print("certification_action:", certification.get("certification_action"))
print("certification_risk:", certification.get("certification_risk"))
print("execution_readiness:", certification.get("execution_readiness"))
print("decision_integrity:", certification.get("decision_integrity"))
print("validation_status:", certification.get("validation_status"))
print("governance_status:", certification.get("governance_status"))
print("lifecycle_status:", certification.get("lifecycle_status"))
print("operational_status:", certification.get("operational_status"))
print("integrated_status:", certification.get("integrated_status"))
print("orchestration_status:", certification.get("orchestration_status"))
print("execution_status:", certification.get("execution_status"))
print("execution_authorization:", certification.get("execution_authorization"))

# ------------------------------------------------------------
# STEP 10
# Master Control
# ------------------------------------------------------------

master_control = AIFinalDecisionMasterControl().analyze(
    final_decision,
    certification,
    execution_decision,
    governance,
    lifecycle,
    operational_intelligence,
    orchestration,
    integrated_intelligence,
    validation,
)

print()
print("=== STEP 9 MASTER CONTROL ===")
print("decision:", master_control.get("decision"))
print("action:", master_control.get("action"))
print("execution_status:", master_control.get("execution_status"))
print("execution_readiness:", master_control.get("execution_readiness"))
print("certification_status:", master_control.get("certification_status"))
print("certification_score:", master_control.get("certification_score"))
print("reassessment_required:", master_control.get("reassessment_required"))

# ------------------------------------------------------------
# CONTRACT CHECK
# ------------------------------------------------------------

checks = {
    "governance decision": governance.get("decision") == "ACCUMULATE",
    "governance action": governance.get("action") == "PROCEED",
    "governance confidence": governance.get("confidence_score") == 92.0,
    "governance validation": governance.get("validation_score") == 100,
    "governance adaptive action": governance.get("adaptive_action") == "INCREASE_RISK",

    "control decision": execution_control.get("decision") == governance.get("decision"),
    "control action": execution_control.get("action") == governance.get("action"),
    "control confidence": execution_control.get("confidence_score") == 92.0,
    "control validation": execution_control.get("validation_score") == 100,
    "control governance score": execution_control.get("governance_score") == governance.get("governance_score"),

    "assurance decision": execution_assurance.get("decision") == "ACCUMULATE",
    "assurance action": execution_assurance.get("action") == "PROCEED",
    "assurance confidence": execution_assurance.get("confidence_score") == 92.0,
    "assurance validation": execution_assurance.get("validation_score") == 100,
    "assurance governance score": execution_assurance.get("governance_score") == governance.get("governance_score"),

    "monitoring decision": execution_monitoring.get("decision") == "ACCUMULATE",
    "monitoring action": execution_monitoring.get("action") == "PROCEED",
    "monitoring governance score": execution_monitoring.get("governance_score") == governance.get("governance_score"),
    "monitoring validation": execution_monitoring.get("validation_score") == 100,
    "monitoring assurance score": execution_monitoring.get("assurance_score") == execution_assurance.get("assurance_score"),

    "feedback decision": execution_feedback.get("decision") == "ACCUMULATE",
    "feedback action": execution_feedback.get("action") == "PROCEED",
    "feedback governance score": execution_feedback.get("governance_score") == governance.get("governance_score"),
    "feedback validation": execution_feedback.get("validation_score") == 100,
    "feedback assurance score": execution_feedback.get("assurance_score") == execution_assurance.get("assurance_score"),
    "feedback monitoring score": execution_feedback.get("monitoring_score") == execution_monitoring.get("monitoring_score"),

    "operational decision": operational_intelligence.get("decision") == "ACCUMULATE",
    "operational action": operational_intelligence.get("action") == "PROCEED",
    "operational confidence": operational_intelligence.get("confidence_score") == 92.0,
    "operational validation": operational_intelligence.get("validation_score") == 100,

    "orchestration decision": orchestration.get("decision") == "ACCUMULATE",
    "orchestration action": orchestration.get("action") == "PROCEED",
    "orchestration confidence": orchestration.get("confidence_score") == 92.0,
    "orchestration governance score": orchestration.get("governance_score") == governance.get("governance_score"),
    "orchestration operational score": orchestration.get("operational_score") == operational_intelligence.get("operational_score"),

    "certification decision": certification.get("decision") == "ACCUMULATE",
    "certification action": certification.get("action") == "PROCEED",
    "certification validation": certification.get("validation_score") == 100,
    "certification governance": certification.get("governance_score") == governance.get("governance_score"),
    "certification operational": certification.get("operational_score") == operational_intelligence.get("operational_score"),
    "certification orchestration": certification.get("orchestration_score") == orchestration.get("orchestration_score"),
    "certification confidence": certification.get("confidence_score") == 92.0,

    "master decision": master_control.get("decision") == "ACCUMULATE",
    "master action": master_control.get("action") == "PROCEED",
    "master execution status": master_control.get("execution_status") == "EXECUTION_READY",
    "master certification score": master_control.get("certification_score") == certification.get("certification_score"),
    "master execution readiness exists": master_control.get("execution_readiness") is not None,
    "master reassessment field exists": "reassessment_required" in master_control,
}

print()
print("=== FINAL PROPAGATION CHECK ===")

for name, passed in checks.items():
    print(f"{name}: {'PASS' if passed else 'FAIL'}")

overall = all(checks.values())

print()
print("OVERALL RESULT:", "PASS" if overall else "FAIL")
print("=" * 60)

if not overall:
    raise SystemExit(1)
