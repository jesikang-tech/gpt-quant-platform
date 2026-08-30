"""
PHASE 7-10-20-16
PORTFOLIO DECISION INTELLIGENCE
-> AI DECISION VALIDATION
BOUNDARY CONTRACT TEST V1
SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_decision_validation import AIDecisionValidation


engine = AIDecisionValidation()


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def base_intelligence(**overrides):
    intelligence = {
        "decision": "MAINTAIN",
        "strategy_mode": "MAINTAIN",
        "adaptive_action": "MAINTAIN_ALLOCATION",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
        "confidence": 90.0,
        "reliability": "HIGH",
        "optimization_status": "OPTIMIZED",
        "adaptive_override": False,
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": False,
    }
    intelligence.update(overrides)
    return intelligence


def run_validation(intelligence):
    return engine.validate(
        intelligence=intelligence,
        confidence={
            "confidence_score": 90.0,
            "confidence_level": "Very High",
        },
        assessment={
            "attention_signals": []
        },
        recommendation={
            "recommendation": "PROCEED"
        },
    )


print("=" * 82)
print("PHASE 7-10-20-16")
print("PORTFOLIO DECISION INTELLIGENCE")
print("-> AI DECISION VALIDATION")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: ALIGNED + CONSISTENT -> VALIDATION")
print("=" * 82)

result = run_validation(
    base_intelligence()
)

assert_equal(
    result["validation_status"],
    "VALID",
    "aligned + consistent -> valid",
)


print("")
print("=" * 82)
print("CASE: DECISION ALIGNMENT CONFLICT -> REVIEW")
print("=" * 82)

result = run_validation(
    base_intelligence(
        decision_alignment="CONFLICT"
    )
)

assert_equal(
    result["validation_status"],
    "REVIEW_REQUIRED",
    "alignment conflict -> review required",
)


print("")
print("=" * 82)
print("CASE: OVERRIDDEN CONSISTENCY -> REVIEW")
print("=" * 82)

result = run_validation(
    base_intelligence(
        decision_consistency="OVERRIDDEN"
    )
)

assert_equal(
    result["validation_status"],
    "REVIEW_REQUIRED",
    "overridden consistency -> review required",
)


print("")
print("=" * 82)
print("CASE: ADAPTIVE OVERRIDE -> REVIEW")
print("=" * 82)

result = run_validation(
    base_intelligence(
        adaptive_override=True
    )
)

assert_equal(
    result["validation_status"],
    "REVIEW_REQUIRED",
    "adaptive override -> review required",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE LEARNING + ADAPTIVE REQUIRED + OVERRIDE")
print("-> REVIEW_REQUIRED")
print("=" * 82)

result = run_validation(
    base_intelligence(
        decision_alignment="CONFLICT",
        decision_consistency="OVERRIDDEN",
        adaptive_override=True,
        outcome_learning_signal="NEGATIVE",
        outcome_learning_signal_strength=84.0,
        adaptive_learning_required=True,
    )
)

assert_equal(
    result["validation_status"],
    "REVIEW_REQUIRED",
    "negative learning override -> review required",
)


print("")
print("=" * 82)
print("CASE: LEARNING FIELDS PRESERVED")
print("=" * 82)

learning_intelligence = base_intelligence(
    outcome_learning_signal="NEGATIVE",
    outcome_learning_signal_strength=84.0,
    adaptive_learning_required=True,
)

result = run_validation(
    learning_intelligence
)

assert_equal(
    result["outcome_learning_signal"],
    "NEGATIVE",
    "learning signal -> preserved",
)

assert_equal(
    result["outcome_learning_signal_strength"],
    84.0,
    "learning signal strength -> preserved",
)

assert_equal(
    result["adaptive_learning_required"],
    True,
    "adaptive learning required -> preserved",
)


print("")
print("=" * 82)
print("CASE: EMPTY INTELLIGENCE -> SAFE DEFAULTS")
print("=" * 82)

result = engine.validate(
    intelligence={},
    confidence={},
    assessment={},
    recommendation={},
)

assert_equal(
    result["validation_status"],
    "REVIEW_REQUIRED",
    "empty intelligence -> review required",
)


print("")
print("=" * 82)
print("CASE: LEARNING DOES NOT FABRICATE INPUT")
print("=" * 82)

result = run_validation(
    base_intelligence()
)

assert_equal(
    result["outcome_learning_signal"],
    "NONE",
    "no learning -> no fabricated signal",
)

assert_equal(
    result["outcome_learning_signal_strength"],
    0.0,
    "no learning -> no fabricated strength",
)

assert_equal(
    result["adaptive_learning_required"],
    False,
    "no learning -> no fabricated requirement",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-16 PORTFOLIO DECISION -> VALIDATION COMPLETE =====")
print("=" * 82)
