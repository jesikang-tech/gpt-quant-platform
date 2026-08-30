from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


print("=" * 82)
print("PHASE 7-10-20-14")
print("OUTCOME EVALUATION / LEARNING -> ADAPTIVE STRATEGY")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

engine = AIDecisionAdaptiveStrategy()

stable_trend = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}

balanced_trend = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "MEDIUM",
    "latest_score": 85,
}


print("")
print("=" * 82)
print("CASE: NO OUTCOME LEARNING -> BASE STRATEGY PRESERVED")
print("=" * 82)

result = engine.analyze(
    stable_trend,
    {
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": False,
    },
)

assert_equal(
    result["strategy"],
    "MAINTAIN",
    "no learning -> base strategy preserved",
)

assert_equal(
    result["action"],
    "MAINTAIN_ALLOCATION",
    "no learning -> base action preserved",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE WITHOUT ADAPTIVE REQUIREMENT -> NO OVERRIDE")
print("=" * 82)

result = engine.analyze(
    stable_trend,
    {
        "outcome_learning_signal": "NEGATIVE",
        "outcome_learning_signal_strength": 84.0,
        "adaptive_learning_required": False,
    },
)

assert_equal(
    result["strategy"],
    "MAINTAIN",
    "negative + adaptive false -> strategy preserved",
)

assert_equal(
    result["action"],
    "MAINTAIN_ALLOCATION",
    "negative + adaptive false -> action preserved",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE + ADAPTIVE REQUIRED -> DEFENSIVE")
print("=" * 82)

result = engine.analyze(
    stable_trend,
    {
        "outcome_learning_signal": "NEGATIVE",
        "outcome_learning_signal_strength": 84.0,
        "adaptive_learning_required": True,
    },
)

assert_equal(
    result["strategy"],
    "DEFENSIVE",
    "negative + adaptive true -> defensive strategy",
)

assert_equal(
    result["action"],
    "REDUCE_RISK",
    "negative + adaptive true -> reduce risk",
)


print("")
print("=" * 82)
print("CASE: POSITIVE + STRONG + BALANCED -> GROWTH")
print("=" * 82)

result = engine.analyze(
    balanced_trend,
    {
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 0.7,
        "adaptive_learning_required": False,
    },
)

assert_equal(
    result["strategy"],
    "GROWTH",
    "positive + threshold + balanced -> growth",
)

assert_equal(
    result["action"],
    "INCREASE_RISK",
    "positive + growth -> increase risk",
)


print("")
print("=" * 82)
print("CASE: POSITIVE + WEAK -> BASE STRATEGY PRESERVED")
print("=" * 82)

result = engine.analyze(
    stable_trend,
    {
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 0.6,
        "adaptive_learning_required": False,
    },
)

assert_equal(
    result["strategy"],
    "MAINTAIN",
    "positive + weak -> strategy preserved",
)

assert_equal(
    result["action"],
    "MAINTAIN_ALLOCATION",
    "positive + weak -> action preserved",
)


print("")
print("=" * 82)
print("CASE: POSITIVE + STRONG + NON-BALANCED -> NO OVERRIDE")
print("=" * 82)

growth_trend = {
    "direction": "POSITIVE",
    "stability": "HIGH",
    "momentum": "POSITIVE",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 90,
}

result = engine.analyze(
    growth_trend,
    {
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 84.0,
        "adaptive_learning_required": False,
    },
)

assert_equal(
    result["strategy"],
    "GROWTH",
    "positive + strong + non-balanced -> existing growth preserved",
)


print("")
print("=" * 82)
print("CASE: LEARNING INPUTS PRESERVED")
print("=" * 82)

learning_input = {
    "outcome_learning_signal": "POSITIVE",
    "outcome_learning_signal_strength": 84.0,
    "adaptive_learning_required": True,
}

result = engine.analyze(
    stable_trend,
    learning_input,
)

assert_equal(
    result["outcome_learning_signal"],
    "POSITIVE",
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
print("CASE: EMPTY OUTCOME INTELLIGENCE -> SAFE DEFAULTS")
print("=" * 82)

result = engine.analyze(
    stable_trend,
    None,
)

assert_equal(
    result["outcome_learning_signal"],
    "NONE",
    "empty outcome intelligence -> signal NONE",
)

assert_equal(
    result["outcome_learning_signal_strength"],
    0.0,
    "empty outcome intelligence -> strength zero",
)

assert_equal(
    result["adaptive_learning_required"],
    False,
    "empty outcome intelligence -> adaptive false",
)

assert_equal(
    result["strategy"],
    "MAINTAIN",
    "empty outcome intelligence -> base strategy preserved",
)


print("")
print("=" * 82)
print("CASE: LEARNING DOES NOT FABRICATE OUTCOME")
print("=" * 82)

result = engine.analyze(
    stable_trend,
    {
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": False,
    },
)

assert_equal(
    result["outcome_learning_signal"],
    "NONE",
    "learning boundary -> no fabricated signal",
)

assert_equal(
    result["outcome_learning_signal_strength"],
    0.0,
    "learning boundary -> no fabricated strength",
)

assert_equal(
    result["adaptive_learning_required"],
    False,
    "learning boundary -> no fabricated adaptive requirement",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-14 ADAPTIVE STRATEGY BOUNDARY COMPLETE =====")
print("=" * 82)

