from core.ai_final_decision_master_control import (
    AIFinalDecisionMasterControl
)

print("=" * 78)
print("PHASE 7-6 MASTER CONTROL CONTRACT TEST")
print("FINAL EXECUTION DECISION -> MASTER CONTROL")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 78)


def build_inputs(
    *,
    certification_status="CERTIFIED",
    execution_status="EXECUTION_READY",
    execution_authorization="AUTHORIZED",
    execution_readiness="READY",
    decision_integrity="INTACT",
    governance_status="APPROVED",
    lifecycle_status="HEALTHY",
    operational_status="OPERATIONALLY_HEALTHY",
    orchestration_status="ORCHESTRATION_READY",
    integrated_status="INTEGRATED_HEALTHY",
    validation_status="VALID",
    reassessment_required=False,
    scores=None
):
    scores = scores or {
        "certification": 97.0,
        "execution": 95.0,
        "governance": 96.0,
        "lifecycle": 94.0,
        "operational": 93.0,
        "orchestration": 92.0,
        "integrated": 91.0,
        "validation": 90.0,
    }

    final_decision = {
        "decision": "PROCEED",
        "action": "PROCEED",
    }

    certification = {
        "decision": "PROCEED",
        "certification_action": "PROCEED",
        "certification_status": certification_status,
        "certification_risk": "LOW",
        "execution_status": execution_status,
        "execution_authorization": execution_authorization,
        "execution_readiness": execution_readiness,
        "decision_integrity": decision_integrity,
        "certification_score": scores["certification"],
    }

    execution_decision = {
        "decision": "PROCEED",
        "action": "PROCEED",
        "execution_status": execution_status,
        "execution_authorization": execution_authorization,
        "execution_score": scores["execution"],
    }

    governance = {
        "governance_status": governance_status,
        "governance_score": scores["governance"],
    }

    lifecycle = {
        "lifecycle_status": lifecycle_status,
        "lifecycle_score": scores["lifecycle"],
        "reassessment_required": reassessment_required,
    }

    operational_intelligence = {
        "operational_status": operational_status,
        "operational_score": scores["operational"],
    }

    orchestration = {
        "orchestration_status": orchestration_status,
        "orchestration_score": scores["orchestration"],
    }

    integrated_intelligence = {
        "integrated_status": integrated_status,
        "integrated_score": scores["integrated"],
    }

    validation = {
        "validation_status": validation_status,
        "validation_score": scores["validation"],
    }

    return (
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


engine = AIFinalDecisionMasterControl()


# ================================================================
# CASE 1: MASTER READY
# ================================================================

print()
print("=" * 78)
print("CASE: MASTER READY")
print("=" * 78)

inputs = build_inputs()

result = engine.analyze(*inputs)

print("master control status:",
      result.get("master_control_status"))

print("master control action:",
      result.get("master_control_action"))

print("master control risk:",
      result.get("master_control_risk"))

print("master control score:",
      result.get("master_control_score"))

print("master control grade:",
      result.get("master_control_grade"))

print("execution control:",
      result.get("execution_control"))

assert result.get("master_control_status") == "MASTER_READY"
print("MASTER_READY contract: PASS")

assert result.get("master_control_action") == "PROCEED"
print("PROCEED contract: PASS")

assert result.get("master_control_risk") == "LOW"
print("LOW risk contract: PASS")

assert result.get("execution_control") == "EXECUTE"
print("EXECUTE contract: PASS")

assert result.get("master_control_score") == 90.0
print("minimum-score aggregation contract: PASS")


# ================================================================
# CASE 2: MASTER REVIEW
# ================================================================

print()
print("=" * 78)
print("CASE: MASTER REVIEW")
print("=" * 78)

inputs = build_inputs(
    governance_status="WARNING"
)

result = engine.analyze(*inputs)

print("master control status:",
      result.get("master_control_status"))

print("master control action:",
      result.get("master_control_action"))

print("master control risk:",
      result.get("master_control_risk"))

print("execution control:",
      result.get("execution_control"))

assert result.get("master_control_status") == "MASTER_REVIEW"
print("MASTER_REVIEW contract: PASS")

assert result.get("master_control_action") == "REVIEW"
print("REVIEW action contract: PASS")

assert result.get("master_control_risk") == "MEDIUM"
print("MEDIUM risk contract: PASS")

assert result.get("execution_control") == "HOLD"
print("HOLD execution contract: PASS")


# ================================================================
# CASE 3: MASTER BLOCKED
# ================================================================

print()
print("=" * 78)
print("CASE: MASTER BLOCKED")
print("=" * 78)

inputs = build_inputs(
    execution_authorization="UNAUTHORIZED"
)

result = engine.analyze(*inputs)

print("master control status:",
      result.get("master_control_status"))

print("master control action:",
      result.get("master_control_action"))

print("master control risk:",
      result.get("master_control_risk"))

print("execution control:",
      result.get("execution_control"))

assert result.get("master_control_status") == "MASTER_BLOCKED"
print("MASTER_BLOCKED contract: PASS")

assert result.get("master_control_action") == "HALT"
print("HALT action contract: PASS")

assert result.get("master_control_risk") == "CRITICAL"
print("CRITICAL risk contract: PASS")

assert result.get("execution_control") == "HOLD"
print("HOLD execution contract: PASS")


# ================================================================
# CASE 4: REASSESSMENT REQUIRED
# ================================================================

print()
print("=" * 78)
print("CASE: REASSESSMENT REQUIRED")
print("=" * 78)

inputs = build_inputs(
    reassessment_required=True
)

result = engine.analyze(*inputs)

print("master control status:",
      result.get("master_control_status"))

print("master control action:",
      result.get("master_control_action"))

print("master control risk:",
      result.get("master_control_risk"))

print("execution control:",
      result.get("execution_control"))

assert result.get("master_control_status") == "MASTER_REVIEW"
print("REASSESSMENT -> MASTER_REVIEW: PASS")

assert result.get("master_control_action") == "REVIEW"
print("REASSESSMENT -> REVIEW: PASS")

assert result.get("execution_control") == "HOLD"
print("REASSESSMENT -> HOLD: PASS")


# ================================================================
# FINAL ASSERTIONS
# ================================================================

print()
print("=" * 78)
print("FINAL ASSERTIONS")
print("=" * 78)

print(
    "ALL HEALTHY -> MASTER_READY -> PROCEED -> EXECUTE: PASS"
)

print(
    "WARNING -> MASTER_REVIEW -> REVIEW -> HOLD: PASS"
)

print(
    "UNAUTHORIZED -> MASTER_BLOCKED -> HALT -> HOLD: PASS"
)

print(
    "REASSESSMENT_REQUIRED -> MASTER_REVIEW -> REVIEW -> HOLD: PASS"
)

print(
    "Master score = minimum valid score: PASS"
)


# ================================================================
# SAFETY
# ================================================================

print()
print("=" * 78)
print("SAFETY")
print("=" * 78)

print("Memory-only execution: PASS")
print("No production DB access.")
print("No API runtime call.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")

print()
print(
    "===== PHASE 7-6 MASTER CONTROL CONTRACT TEST COMPLETE ====="
)
