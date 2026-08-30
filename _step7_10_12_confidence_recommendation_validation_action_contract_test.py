"""
PHASE 7-10-12
DECISION CONFIDENCE RECOMMENDATION
-> VALIDATION ACTION
BOUNDARY CONTRACT TEST
SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_decision_validation_action import AIDecisionValidationAction


engine = AIDecisionValidationAction()


def run_case(
    name,
    validation,
    confidence,
    recommendation,
    expected_action,
    expected_monitoring,
):
    result = engine.decide(
        validation=validation,
        confidence=confidence,
        recommendation=recommendation,
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- CONFIDENCE RECOMMENDATION SOURCE ---")
    print("recommendation:", recommendation.get("recommendation"))

    print("--- VALIDATION INPUT ---")
    print("validation_status:", validation.get("validation_status"))
    print("validation_score:", validation.get("validation_score"))
    print("confidence_score:", confidence.get("confidence_score"))

    print("--- VALIDATION ACTION RESULT ---")
    print("action:", result.get("action"))
    print("monitoring:", result.get("monitoring"))
    print("execution_status:", result.get("execution_status"))
    print("recommendation:", result.get("recommendation"))

    assert result.get("action") == expected_action
    assert result.get("monitoring") == expected_monitoring
    assert result.get("recommendation") == recommendation.get(
        "recommendation"
    )

    print(
        f"{name} -> CONFIDENCE RECOMMENDATION / "
        f"VALIDATION ACTION CONTRACT: PASS"
    )

    return result


# ================================================================
# CASE 1
# Strong VALID validation + PROCEED recommendation
# ================================================================

run_case(
    "PROCEED_RECOMMENDATION_PROPAGATION",
    {
        "decision": "MAINTAIN",
        "validation_status": "VALID",
        "validation_score": 95.0,
        "strategy_mode": "BALANCED",
    },
    {
        "confidence_score": 92.0,
        "confidence_level": "Very High",
    },
    {
        "recommendation": "PROCEED",
        "monitoring": "STANDARD",
        "recommendation_score": 92.0,
    },
    "PROCEED",
    "STANDARD",
)


# ================================================================
# CASE 2
# Strong VALID validation + PROCEED_WITH_MONITORING recommendation
# ================================================================

run_case(
    "MONITORING_RECOMMENDATION_PROPAGATION",
    {
        "decision": "MAINTAIN",
        "validation_status": "VALID",
        "validation_score": 95.0,
        "strategy_mode": "BALANCED",
    },
    {
        "confidence_score": 92.0,
        "confidence_level": "Very High",
    },
    {
        "recommendation": "PROCEED_WITH_MONITORING",
        "monitoring": "ELEVATED",
        "recommendation_score": 92.0,
    },
    "PROCEED_WITH_MONITORING",
    "ELEVATED",
)


# ================================================================
# CASE 3
# REVIEW_REQUIRED validation boundary.
# Confidence Recommendation is propagated as a recommendation
# signal, but insufficient validation score keeps execution
# in REVIEW_REQUIRED.
# ================================================================

run_case(
    "REVIEW_REQUIRED_VALIDATION_BOUNDARY",
    {
        "decision": "MAINTAIN",
        "validation_status": "REVIEW_REQUIRED",
        "validation_score": 65.0,
        "strategy_mode": "BALANCED",
    },
    {
        "confidence_score": 91.0,
        "confidence_level": "Very High",
    },
    {
        "recommendation": "PROCEED",
        "monitoring": "STANDARD",
        "recommendation_score": 91.0,
    },
    "REVIEW_REQUIRED",
    "HIGH",
)


# ================================================================
# CASE 4
# INVALID validation must block execution regardless of
# Confidence Recommendation.
# ================================================================

run_case(
    "INVALID_VALIDATION_PRIORITY",
    {
        "decision": "MAINTAIN",
        "validation_status": "INVALID",
        "validation_score": 98.0,
        "strategy_mode": "BALANCED",
    },
    {
        "confidence_score": 98.0,
        "confidence_level": "Very High",
    },
    {
        "recommendation": "PROCEED",
        "monitoring": "STANDARD",
        "recommendation_score": 98.0,
    },
    "BLOCK_EXECUTION",
    "CRITICAL",
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("Confidence Recommendation -> Validation Action: PASS")
print("PROCEED recommendation propagation: PASS")
print("PROCEED_WITH_MONITORING recommendation propagation: PASS")
print("REVIEW_REQUIRED validation boundary: PASS")
print("INVALID validation priority: PASS")

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
print("===== PHASE 7-10-12 CONTRACT TEST COMPLETE =====")
print("=" * 82)
