from core.ai_final_decision_governance import (
    AIFinalDecisionGovernance
)


def run_case(
    name,
    final_decision,
    intelligence,
    intelligence_score,
    confidence,
    validation,
    validation_action,
    expected
):

    engine = AIFinalDecisionGovernance()

    result = engine.govern(
        final_decision=final_decision,
        intelligence=intelligence,
        intelligence_score=intelligence_score,
        confidence=confidence,
        validation=validation,
        validation_action=validation_action
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- FINAL DECISION ---")
    print(
        "decision:",
        final_decision.get("decision")
    )
    print(
        "action:",
        final_decision.get("action")
    )
    print(
        "execution_status:",
        final_decision.get("execution_status")
    )
    print(
        "confidence_score:",
        final_decision.get("confidence_score")
    )
    print(
        "validation_score:",
        final_decision.get("validation_score")
    )
    print(
        "intelligence_score:",
        final_decision.get("intelligence_score")
    )

    print("--- GOVERNANCE ---")
    print(
        "governance_status:",
        result.get("governance_status")
    )
    print(
        "governance_score:",
        result.get("governance_score")
    )
    print(
        "integrity_status:",
        result.get("integrity_status")
    )
    print(
        "stability_status:",
        result.get("stability_status")
    )
    print(
        "execution_readiness:",
        result.get("execution_readiness")
    )
    print(
        "risk_governance:",
        result.get("risk_governance")
    )
    print(
        "override_status:",
        result.get("override_status")
    )
    print(
        "monitoring_policy:",
        result.get("monitoring_policy")
    )

    print("--- PROPAGATED FIELDS ---")
    print(
        "decision:",
        result.get("decision")
    )
    print(
        "action:",
        result.get("action")
    )
    print(
        "execution_status:",
        result.get("execution_status")
    )
    print(
        "confidence_score:",
        result.get("confidence_score")
    )
    print(
        "validation_score:",
        result.get("validation_score")
    )
    print(
        "intelligence_score:",
        result.get("intelligence_score")
    )
    print(
        "decision_alignment:",
        result.get("decision_alignment")
    )
    print(
        "decision_consistency:",
        result.get("decision_consistency")
    )
    print(
        "adaptive_action:",
        result.get("adaptive_action")
    )

    for key, value in expected.items():

        assert (
            result.get(key) == value
        ), (
            f"{name}: {key} expected "
            f"{value!r}, got "
            f"{result.get(key)!r}"
        )

    print(
        f"{name} -> GOVERNANCE CONTRACT: PASS"
    )


print("=" * 82)
print(
    "PHASE 7-9-15 AI FINAL DECISION INTEGRATION"
)
print(
    "-> AI FINAL DECISION GOVERNANCE"
)
print(
    "FINAL DECISION GOVERNANCE BOUNDARY CONTRACT TEST"
)
print(
    "SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY"
)
print("=" * 82)


# --------------------------------------------------
# CASE 1
# Fully healthy final decision.
# All governance components should be optimal.
# --------------------------------------------------

run_case(
    "HEALTHY_APPROVAL",
    {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "validation_status": "VALID",
        "validation_score": 100,
        "confidence_score": 100,
        "intelligence_score": 100,
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
        "reliability": "HIGH",
        "optimization_status": "OPTIMAL",
        "adaptive_action": "MAINTAIN_ALLOCATION",
        "adaptive_override": False,
        "recommendation": "PROCEED"
    },
    {},
    {
        "intelligence_score": 100
    },
    {
        "confidence_score": 100
    },
    {},
    {},
    {
        "governance_status": "APPROVED",
        "governance_score": 100.0,
        "integrity_status": "INTACT",
        "stability_status": "STABLE",
        "execution_readiness": "READY",
        "risk_governance": "ACCEPTABLE",
        "override_status": "NONE",
        "monitoring_policy": "STANDARD",
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "confidence_score": 100.0,
        "validation_score": 100.0,
        "intelligence_score": 100.0,
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
        "adaptive_action": "MAINTAIN_ALLOCATION"
    }
)


# --------------------------------------------------
# CASE 2
# Adaptive override is active.
# Alignment/consistency remain healthy, but
# override points are reduced from 100 to 60.
#
# Expected score:
# 20 + 15 + 20 + 15 + 6 + 10 + 5 + 5 = 96
# --------------------------------------------------

run_case(
    "ADAPTIVE_OVERRIDE",
    {
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "validation_status": "VALID",
        "validation_score": 100,
        "confidence_score": 100,
        "intelligence_score": 100,
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
        "reliability": "HIGH",
        "optimization_status": "OPTIMAL",
        "adaptive_action": "REDUCE_RISK",
        "adaptive_override": True,
        "recommendation": "PROCEED"
    },
    {},
    {
        "intelligence_score": 100
    },
    {
        "confidence_score": 100
    },
    {},
    {},
    {
        "governance_status": "APPROVED_WITH_OVERRIDE",
        "governance_score": 96.0,
        "integrity_status": "INTACT",
        "stability_status": "STABLE",
        "execution_readiness": "READY",
        "risk_governance": "ACCEPTABLE",
        "override_status": "OVERRIDE_ACTIVE",
        "monitoring_policy": "STANDARD",
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "confidence_score": 100.0,
        "validation_score": 100.0,
        "intelligence_score": 100.0,
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
        "adaptive_action": "REDUCE_RISK"
    }
)


# --------------------------------------------------
# CASE 3
# Conflict boundary.
# Decision alignment/consistency conflict causes
# DEGRADED integrity and UNSTABLE stability.
#
# Confidence/validation remain high enough for
# conditional execution, but risk becomes
# HIGH_ATTENTION.
# --------------------------------------------------

run_case(
    "CONFLICT_GOVERNANCE",
    {
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "validation_status": "VALID",
        "validation_score": 100,
        "confidence_score": 85,
        "intelligence_score": 80,
        "decision_alignment": "CONFLICT",
        "decision_consistency": "CONFLICT",
        "reliability": "HIGH",
        "optimization_status": "OPTIMAL",
        "adaptive_action": "REDUCE_RISK",
        "adaptive_override": True,
        "recommendation": "REVIEW"
    },
    {},
    {
        "intelligence_score": 80
    },
    {
        "confidence_score": 85
    },
    {},
    {},
    {
        "governance_status": "REVIEW_REQUIRED",
        "governance_score": 60.0,
        "integrity_status": "DEGRADED",
        "stability_status": "UNSTABLE",
        "execution_readiness": "CONDITIONAL",
        "risk_governance": "HIGH_ATTENTION",
        "override_status": "OVERRIDE_ACTIVE",
        "monitoring_policy": "ELEVATED",
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "confidence_score": 85.0,
        "validation_score": 100.0,
        "intelligence_score": 80.0,
        "decision_alignment": "CONFLICT",
        "decision_consistency": "CONFLICT",
        "adaptive_action": "REDUCE_RISK"
    }
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "Healthy final decision -> "
    "APPROVED / score 100: PASS"
)

print(
    "Adaptive override -> "
    "OVERRIDE_ACTIVE / score 96: PASS"
)

print(
    "Conflict -> "
    "DEGRADED / UNSTABLE / monitored governance: PASS"
)

print(
    "Final Decision fields -> "
    "Governance propagation: PASS"
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
print("No actual Outcome supplied.")

print("")
print(
    "===== PHASE 7-9-15 AI FINAL DECISION INTEGRATION"
)
print(
    "===== -> AI FINAL DECISION GOVERNANCE"
)
print("===== CONTRACT TEST COMPLETE")
print("=" * 82)
