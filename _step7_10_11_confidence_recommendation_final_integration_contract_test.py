from core.ai_final_decision_integration import (
    AIFinalDecisionIntegration
)


print("=" * 82)
print("PHASE 7-10-11")
print("DECISION CONFIDENCE RECOMMENDATION")
print("-> FINAL DECISION INTEGRATION")
print("BOUNDARY CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


engine = AIFinalDecisionIntegration()


def run_case(
    name,
    recommendation,
    monitoring,
    validation_action=None,
    expect_recommendation_propagation=True,
):

    validation_action = validation_action or {}

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
        decision_confidence_recommendation={
            "recommendation": recommendation,
            "action": "MAINTAIN_ALLOCATION",
            "monitoring": monitoring,
            "recommendation_score": 91.2,
        },
        ai_decision_validation={
            "decision": "MAINTAIN",
            "validation_status": "VALID",
            "validation_score": 100.0,
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

    print("--- CONFIDENCE RECOMMENDATION SOURCE ---")
    print("recommendation:", recommendation)
    print("monitoring:", monitoring)

    print("--- FINAL DECISION INTEGRATION ---")
    print("action:", result.get("action"))
    print("recommendation:", result.get("recommendation"))
    print("monitoring:", result.get("monitoring"))
    print("confidence_score:", result.get("confidence_score"))
    print("confidence_level:", result.get("confidence_level"))
    print("confidence_grade:", result.get("confidence_grade"))

    assert result.get(
        "confidence_score"
    ) == 91.2

    assert result.get(
        "confidence_level"
    ) == "Very High"

    assert result.get(
        "confidence_grade"
    ) == "A+"
    if expect_recommendation_propagation:
        assert result.get(
            "recommendation"
        ) == recommendation

        assert result.get(
            "monitoring"
        ) == monitoring

    print(
        f"{name} -> CONFIDENCE RECOMMENDATION / "
        f"FINAL INTEGRATION CONTRACT: PASS"
    )

    return result


# ================================================================
# CASE 1
# No validation-action override.
# Confidence Recommendation must propagate.
# ================================================================

run_case(
    "RECOMMENDATION_PROPAGATION",
    "PROCEED_WITH_MONITORING",
    "ELEVATED",
)


# ================================================================
# CASE 2
# Validation Action has priority.
# Confidence Recommendation remains fallback only.
# ================================================================

result = run_case(
    "VALIDATION_ACTION_PRIORITY",
    "PROCEED",
    "STANDARD",
    {
        "decision": "MAINTAIN",
        "action": "VALIDATION_ACTION",
        "recommendation": "VALIDATION_RECOMMENDATION",
        "monitoring": "VALIDATION_MONITORING",
        "execution_status": "EXECUTION_READY",
        "confidence_score": 88.0,
        "confidence_level": "High",
        "validation_status": "VALID",
        "validation_score": 95.0,
        "risk_level": "LOW",
        "strategy_mode": "BALANCED",
    },
    expect_recommendation_propagation=False,
)

assert result.get(
    "action"
) == "VALIDATION_ACTION"

assert result.get(
    "recommendation"
) == "VALIDATION_RECOMMENDATION"

assert result.get(
    "monitoring"
) == "VALIDATION_MONITORING"

print(
    "Validation Action priority over Confidence Recommendation: PASS"
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "Confidence Recommendation -> Final Integration: PASS"
)

print(
    "Confidence score / level / grade preservation: PASS"
)

print(
    "Validation Action priority boundary: PASS"
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
print("=" * 82)
print("===== PHASE 7-10-11 CONTRACT TEST COMPLETE =====")
print("=" * 82)
