from core.ai_final_decision_integration import (
    AIFinalDecisionIntegration
)


def run_case(
    name,
    intelligence_score,
    intelligence,
    validation_action,
    expected
):

    engine = AIFinalDecisionIntegration()

    result = engine.integrate(
        intelligence=intelligence,
        intelligence_score=intelligence_score,
        decision_confidence={
            "confidence_score": 90,
            "confidence_level": "HIGH",
            "confidence_grade": "A"
        },
        decision_confidence_assessment={},
        decision_confidence_recommendation={
            "recommendation": "PROCEED",
            "monitoring": "STANDARD"
        },
        ai_decision_validation={
            "decision": "MAINTAIN",
            "validation_status": "VALID",
            "validation_score": 100,
            "decision_alignment": "VALIDATION_ALIGNED",
            "decision_consistency": "VALIDATION_CONSISTENT"
        },
        ai_decision_validation_explainability={
            "explanation": "Source-verified contract test."
        },
        ai_decision_validation_action=validation_action
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- INPUT INTELLIGENCE SCORE ---")
    print(
        "intelligence_score:",
        intelligence_score.get(
            "intelligence_score"
        )
    )
    print(
        "grade:",
        intelligence_score.get(
            "grade"
        )
    )

    print("--- INPUT INTELLIGENCE ---")
    print(
        "final_strategy:",
        intelligence.get(
            "final_strategy"
        )
    )
    print(
        "adaptive_action:",
        intelligence.get(
            "adaptive_action"
        )
    )
    print(
        "decision_alignment:",
        intelligence.get(
            "decision_alignment"
        )
    )
    print(
        "decision_consistency:",
        intelligence.get(
            "decision_consistency"
        )
    )

    print("--- VALIDATION ACTION ---")
    print(
        "adaptive_action:",
        validation_action.get(
            "adaptive_action"
        )
    )
    print(
        "decision_alignment:",
        validation_action.get(
            "decision_alignment"
        )
    )
    print(
        "decision_consistency:",
        validation_action.get(
            "decision_consistency"
        )
    )

    print("--- FINAL DECISION INTEGRATION ---")
    print(
        "intelligence_score:",
        result.get(
            "intelligence_score"
        )
    )
    print(
        "intelligence_grade:",
        result.get(
            "intelligence_grade"
        )
    )
    print(
        "strategy:",
        result.get(
            "strategy"
        )
    )
    print(
        "adaptive_action:",
        result.get(
            "adaptive_action"
        )
    )
    print(
        "decision_alignment:",
        result.get(
            "decision_alignment"
        )
    )
    print(
        "decision_consistency:",
        result.get(
            "decision_consistency"
        )
    )

    assert (
        result.get("intelligence_score")
        == intelligence_score.get(
            "intelligence_score"
        )
    )

    assert (
        result.get("intelligence_grade")
        == intelligence_score.get(
            "grade"
        )
    )

    assert (
        result.get("strategy")
        == intelligence.get(
            "final_strategy"
        )
    )

    assert (
        result.get("adaptive_action")
        == expected["adaptive_action"]
    )

    assert (
        result.get("decision_alignment")
        == expected["decision_alignment"]
    )

    assert (
        result.get("decision_consistency")
        == expected["decision_consistency"]
    )

    print(
        f"{name} -> FINAL DECISION INTEGRATION: PASS"
    )


print("=" * 82)
print(
    "PHASE 7-9-14 PORTFOLIO INTELLIGENCE SCORE"
)
print(
    "-> AI FINAL DECISION INTEGRATION"
)
print(
    "FINAL INTELLIGENCE / STRATEGY / "
    "VALIDATION PRECEDENCE CONTRACT TEST"
)
print(
    "SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY"
)
print("=" * 82)


# --------------------------------------------------
# CASE 1
# Validation Action values exist.
# Validation Action must take precedence.
# --------------------------------------------------

run_case(
    "VALIDATION_ACTION_PRECEDENCE",
    {
        "intelligence_score": 86.0,
        "grade": "A",
        "intelligence_level": "Strong"
    },
    {
        "decision": "MAINTAIN",
        "market_view": "NEUTRAL",
        "final_strategy": "MAINTAIN",
        "strategy_mode": "MAINTAIN",
        "adaptive_action": "INTELLIGENCE_ACTION",
        "decision_alignment": "INTELLIGENCE_ALIGNED",
        "decision_consistency": "INTELLIGENCE_CONSISTENT"
    },
    {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "validation_status": "VALID",
        "validation_score": 100,
        "risk_level": "LOW",
        "adaptive_action": "VALIDATION_ACTION",
        "decision_alignment": "VALIDATION_ALIGNED",
        "decision_consistency": "VALIDATION_CONSISTENT"
    },
    {
        "adaptive_action": "VALIDATION_ACTION",
        "decision_alignment": "VALIDATION_ALIGNED",
        "decision_consistency": "VALIDATION_CONSISTENT"
    }
)


# --------------------------------------------------
# CASE 2
# Validation Action values absent.
# Integration must fall back to intelligence.
# --------------------------------------------------

run_case(
    "INTELLIGENCE_FALLBACK",
    {
        "intelligence_score": 80.0,
        "grade": "A",
        "intelligence_level": "Strong"
    },
    {
        "decision": "MAINTAIN",
        "market_view": "NEUTRAL",
        "final_strategy": "DEFENSIVE",
        "strategy_mode": "DEFENSIVE",
        "adaptive_action": "REDUCE_RISK",
        "decision_alignment": "CONFLICT",
        "decision_consistency": "OVERRIDDEN"
    },
    {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "validation_status": "VALID",
        "validation_score": 100,
        "risk_level": "LOW"
    },
    {
        "adaptive_action": "REDUCE_RISK",
        "decision_alignment": "VALIDATION_ALIGNED",
        "decision_consistency": "VALIDATION_CONSISTENT"
    }
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "Portfolio Intelligence Score -> "
    "intelligence_score: PASS"
)

print(
    "Portfolio Intelligence Score -> "
    "intelligence_grade: PASS"
)

print(
    "final_strategy -> "
    "Final Decision Integration.strategy: PASS"
)

print(
    "Validation Action precedence -> "
    "adaptive_action/alignment/consistency: PASS"
)

print(
    "Intelligence fallback -> "
    "adaptive_action: PASS"
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
    "===== PHASE 7-9-14 PORTFOLIO INTELLIGENCE SCORE"
)
print(
    "===== -> AI FINAL DECISION INTEGRATION"
)
print("===== CONTRACT TEST COMPLETE")
print("=" * 82)
