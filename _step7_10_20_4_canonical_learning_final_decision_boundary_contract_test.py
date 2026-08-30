from core.ai_final_decision_integration import AIFinalDecisionIntegration


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def integrate(
    decision="MAINTAIN",
    strategy="BALANCED",
    adaptive_action="MAINTAIN_BALANCE",
    decision_alignment="ALIGNED",
    decision_consistency="CONSISTENT",
):
    engine = AIFinalDecisionIntegration()

    return engine.integrate(
        intelligence={
            "decision": decision,
            "final_strategy": strategy,
            "strategy_mode": strategy,
            "adaptive_action": adaptive_action,
            "decision_alignment": decision_alignment,
            "decision_consistency": decision_consistency,
            "market_view": "NEUTRAL",
            "reliability": "HIGH",
            "optimization_status": "OPTIMIZED",
            "summary": "Test intelligence",
        },
        intelligence_score={
            "intelligence_score": 90.0,
            "grade": "A",
        },
        decision_confidence={
            "confidence_score": 90.0,
            "confidence_level": "HIGH",
            "confidence_grade": "A",
        },
        decision_confidence_assessment={},
        decision_confidence_recommendation={
            "recommendation": "PROCEED",
            "monitoring": "STANDARD",
        },
        ai_decision_validation={
            "decision": decision,
            "validation_status": "VALID",
            "validation_score": 100.0,
            "decision_alignment": decision_alignment,
            "decision_consistency": decision_consistency,
        },
        ai_decision_validation_explainability={
            "explanation": "Test explanation",
        },
        ai_decision_validation_action={
            "decision": decision,
            "action": "PROCEED",
            "execution_status": "AUTHORIZED",
            "confidence_score": 90.0,
            "confidence_level": "HIGH",
            "validation_status": "VALID",
            "validation_score": 100.0,
            "recommendation": "PROCEED",
            "risk_level": "LOW",
            "monitoring": "STANDARD",
            "strategy_mode": strategy,
            "adaptive_action": adaptive_action,
            "decision_alignment": decision_alignment,
            "decision_consistency": decision_consistency,
            "reliability": "HIGH",
            "optimization_status": "OPTIMIZED",
        },
    )


print("=" * 82)
print("PHASE 7-10-20-4")
print("CANONICAL LEARNING -> ADAPTIVE STRATEGY -> FINAL DECISION")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: POSITIVE -> GROWTH -> FINAL DECISION")
print("=" * 82)

positive = integrate(
    decision="ACCUMULATE",
    strategy="GROWTH",
    adaptive_action="INCREASE_RISK",
    decision_alignment="ALIGNED",
    decision_consistency="CONSISTENT",
)

assert_equal(
    positive["decision"],
    "ACCUMULATE",
    "POSITIVE -> final decision",
)

assert_equal(
    positive["strategy"],
    "GROWTH",
    "POSITIVE -> final strategy",
)

assert_equal(
    positive["adaptive_action"],
    "INCREASE_RISK",
    "POSITIVE -> adaptive action",
)

assert_equal(
    positive["decision_consistency"],
    "CONSISTENT",
    "POSITIVE -> decision consistency",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE -> DEFENSIVE -> FINAL DECISION")
print("=" * 82)

negative = integrate(
    decision="ACCUMULATE",
    strategy="DEFENSIVE",
    adaptive_action="REDUCE_RISK",
    decision_alignment="CONFLICT",
    decision_consistency="OVERRIDDEN",
)

assert_equal(
    negative["decision"],
    "ACCUMULATE",
    "NEGATIVE -> original decision preserved",
)

assert_equal(
    negative["strategy"],
    "DEFENSIVE",
    "NEGATIVE -> final strategy",
)

assert_equal(
    negative["adaptive_action"],
    "REDUCE_RISK",
    "NEGATIVE -> adaptive action",
)

assert_equal(
    negative["decision_consistency"],
    "OVERRIDDEN",
    "NEGATIVE -> decision consistency",
)


print("")
print("=" * 82)
print("CASE: STABLE -> BALANCED -> FINAL DECISION")
print("=" * 82)

stable = integrate(
    decision="MAINTAIN",
    strategy="BALANCED",
    adaptive_action="MAINTAIN_BALANCE",
    decision_alignment="ALIGNED",
    decision_consistency="CONSISTENT",
)

assert_equal(
    stable["decision"],
    "MAINTAIN",
    "STABLE -> final decision",
)

assert_equal(
    stable["strategy"],
    "BALANCED",
    "STABLE -> final strategy",
)

assert_equal(
    stable["decision_alignment"],
    "ALIGNED",
    "STABLE -> decision alignment",
)

assert_equal(
    stable["decision_consistency"],
    "CONSISTENT",
    "STABLE -> decision consistency",
)


print("")
print("=" * 82)
print("CASE: PRIORITY CONTRACT")
print("=" * 82)

priority = integrate(
    decision="MAINTAIN",
    strategy="GROWTH",
    adaptive_action="INCREASE_RISK",
    decision_alignment="ALIGNED",
    decision_consistency="CONSISTENT",
)

assert_equal(priority["strategy"], "GROWTH", "strategy -> final_strategy propagation")

assert_equal(
    priority["strategy"],
    "GROWTH",
    "strategy -> intelligence final_strategy priority",
)

assert_equal(
    priority["decision"],
    "MAINTAIN",
    "decision -> validation action priority",
)

assert_equal(
    priority["decision_consistency"],
    "CONSISTENT",
    "decision consistency -> validation action priority",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-4 FINAL DECISION BOUNDARY COMPLETE =====")
print("=" * 82)

