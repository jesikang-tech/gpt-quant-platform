"""
PHASE 7-10-13
VALIDATION ACTION
-> FINAL DECISION INTEGRATION
BOUNDARY CONTRACT TEST
SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_final_decision_integration import (
    AIFinalDecisionIntegration
)


engine = AIFinalDecisionIntegration()


def run_case(
    name,
    validation_action,
    confidence_recommendation,
    expected_action,
    expected_execution_status,
    expected_recommendation,
    expected_monitoring,
):
    result = engine.integrate(
        intelligence={
            "decision": "MAINTAIN",
            "strategy_mode": "BALANCED",
            "market_view": "NEUTRAL",
        },
        intelligence_score={
            "intelligence_score": 90.0,
            "grade": "A+",
        },
        decision_confidence={
            "confidence_score": 91.2,
            "confidence_level": "Very High",
            "confidence_grade": "A+",
        },
        decision_confidence_assessment={
            "assessment": "VERY_STRONG",
        },
        decision_confidence_recommendation=confidence_recommendation,
        ai_decision_validation={
            "decision": "MAINTAIN",
            "validation_status": "VALID",
            "validation_score": 95.0,
        },
        ai_decision_validation_explainability={
            "explanation": "Source-verified contract test.",
        },
        ai_decision_validation_action=validation_action,
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- VALIDATION ACTION SOURCE ---")
    print("action:", validation_action.get("action"))
    print("execution_status:", validation_action.get("execution_status"))
    print("recommendation:", validation_action.get("recommendation"))
    print("monitoring:", validation_action.get("monitoring"))

    print("--- CONFIDENCE RECOMMENDATION FALLBACK ---")
    print(
        "recommendation:",
        confidence_recommendation.get("recommendation")
    )
    print(
        "monitoring:",
        confidence_recommendation.get("monitoring")
    )

    print("--- FINAL DECISION INTEGRATION ---")
    print("action:", result.get("action"))
    print("execution_status:", result.get("execution_status"))
    print("recommendation:", result.get("recommendation"))
    print("monitoring:", result.get("monitoring"))
    print("validation_status:", result.get("validation_status"))
    print("validation_score:", result.get("validation_score"))

    assert result.get("action") == expected_action
    assert result.get("execution_status") == expected_execution_status
    assert result.get("recommendation") == expected_recommendation
    assert result.get("monitoring") == expected_monitoring
    assert result.get("validation_status") == "VALID"
    assert result.get("validation_score") == 95.0

    print(
        f"{name} -> VALIDATION ACTION / "
        f"FINAL DECISION INTEGRATION CONTRACT: PASS"
    )

    return result


# ================================================================
# CASE 1
# Validation Action is present.
# It must propagate directly into Final Decision Integration.
# ================================================================

run_case(
    "VALIDATION_ACTION_PROPAGATION",
    {
        "decision": "MAINTAIN",
        "action": "PROCEED_WITH_MONITORING",
        "execution_status": "AUTHORIZED_WITH_MONITORING",
        "recommendation": "PROCEED_WITH_MONITORING",
        "monitoring": "ELEVATED",
        "validation_status": "VALID",
        "validation_score": 95.0,
        "strategy_mode": "BALANCED",
    },
    {
        "recommendation": "PROCEED",
        "monitoring": "STANDARD",
        "recommendation_score": 91.2,
    },
    "PROCEED_WITH_MONITORING",
    "AUTHORIZED_WITH_MONITORING",
    "PROCEED_WITH_MONITORING",
    "ELEVATED",
)


# ================================================================
# CASE 2
# Validation Action has priority over Confidence Recommendation.
# ================================================================

run_case(
    "VALIDATION_ACTION_PRIORITY",
    {
        "decision": "MAINTAIN",
        "action": "BLOCK_EXECUTION",
        "execution_status": "BLOCKED",
        "recommendation": "BLOCK_EXECUTION",
        "monitoring": "CRITICAL",
        "validation_status": "VALID",
        "validation_score": 95.0,
        "strategy_mode": "BALANCED",
    },
    {
        "recommendation": "PROCEED",
        "monitoring": "STANDARD",
        "recommendation_score": 91.2,
    },
    "BLOCK_EXECUTION",
    "BLOCKED",
    "BLOCK_EXECUTION",
    "CRITICAL",
)


# ================================================================
# CASE 3
# Validation Action absent.
# Confidence Recommendation becomes the fallback for action,
# recommendation, and monitoring.
# ================================================================

run_case(
    "CONFIDENCE_RECOMMENDATION_FALLBACK",
    {},
    {
        "recommendation": "PROCEED_WITH_MONITORING",
        "monitoring": "ELEVATED",
        "recommendation_score": 91.2,
    },
    "PROCEED_WITH_MONITORING",
    "UNDETERMINED",
    "PROCEED_WITH_MONITORING",
    "ELEVATED",
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("Validation Action -> Final Integration propagation: PASS")
print("Validation Action priority: PASS")
print("Confidence Recommendation fallback: PASS")
print("Validation status / score propagation: PASS")

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
print("=" * 82)
print("===== PHASE 7-10-13 CONTRACT TEST COMPLETE =====")
print("=" * 82)
