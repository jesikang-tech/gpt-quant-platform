from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )

    print(f"{label}: PASS")


print("=" * 82)
print("PHASE 7-10-20-15")
print("ADAPTIVE STRATEGY -> PORTFOLIO DECISION INTELLIGENCE")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

engine = PortfolioDecisionIntelligence()


def empty_inputs():
    return {}, {}, {}, {}, {}, {}, {}


print("")
print("=" * 82)
print("CASE: GROWTH ADAPTIVE STRATEGY PRESERVED")
print("=" * 82)

result = engine.generate(
    {"decision": "ACCUMULATE", "market_view": "BULLISH", "confidence": 90},
    {},
    {"confidence": 90, "reliability_level": "HIGH"},
    {
        "strategy": "GROWTH",
        "action": "INCREASE_RISK",
        "confidence": 85,
        "score": 90,
        "direction": "UP",
        "stability": "HIGH",
        "momentum": "POSITIVE",
        "grade_stability": "STABLE",
        "consistency": "HIGH",
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 84.0,
        "adaptive_learning_required": False,
        "summary": "Growth adaptive strategy",
    },
    {},
    {},
    {"summary": "Growth decision"},
)

assert_equal(
    result["final_strategy"],
    "GROWTH",
    "growth strategy -> final strategy",
)

assert_equal(
    result["adaptive_override"],
    False,
    "growth strategy -> no override",
)


print("")
print("=" * 82)
print("CASE: DEFENSIVE ADAPTIVE OVERRIDE")
print("=" * 82)

result = engine.generate(
    {"decision": "ACCUMULATE", "market_view": "BULLISH", "confidence": 90},
    {},
    {"confidence": 90, "reliability_level": "HIGH"},
    {
        "strategy": "DEFENSIVE",
        "action": "REDUCE_RISK",
        "confidence": 85,
        "score": 40,
        "direction": "DOWN",
        "stability": "LOW",
        "momentum": "NEGATIVE",
        "grade_stability": "CHANGING",
        "consistency": "LOW",
        "outcome_learning_signal": "NEGATIVE",
        "outcome_learning_signal_strength": 84.0,
        "adaptive_learning_required": True,
        "summary": "Defensive adaptive strategy",
    },
    {},
    {},
    {"summary": "Defensive override decision"},
)

assert_equal(
    result["final_strategy"],
    "DEFENSIVE",
    "defensive adaptive -> final strategy",
)

assert_equal(
    result["adaptive_override"],
    True,
    "defensive adaptive -> override",
)

assert_equal(
    result["decision_consistency"],
    "OVERRIDDEN",
    "defensive adaptive -> consistency overridden",
)

assert_equal(
    result["decision_consistency_score"],
    60,
    "defensive adaptive -> consistency score",
)


print("")
print("=" * 82)
print("CASE: MAINTAIN + MAINTAIN STRATEGY ALIGNMENT")
print("=" * 82)

result = engine.generate(
    {"decision": "MAINTAIN", "market_view": "NEUTRAL", "confidence": 80},
    {},
    {"confidence": 80, "reliability_level": "HIGH"},
    {
        "strategy": "MAINTAIN",
        "action": "MAINTAIN_ALLOCATION",
        "confidence": 80,
        "score": 85,
        "direction": "STABLE",
        "stability": "HIGH",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "HIGH",
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": False,
        "summary": "Maintain adaptive strategy",
    },
    {},
    {},
    {"summary": "Maintain decision"},
)

assert_equal(
    result["decision_alignment"],
    "ALIGNED",
    "maintain + maintain -> aligned",
)

assert_equal(
    result["decision_consistency"],
    "CONSISTENT",
    "maintain + maintain -> consistent",
)


print("")
print("=" * 82)
print("CASE: LEARNING FIELDS PROPAGATED")
print("=" * 82)

result = engine.generate(
    {"decision": "MAINTAIN", "market_view": "NEUTRAL", "confidence": 80},
    {},
    {"confidence": 80, "reliability_level": "HIGH"},
    {
        "strategy": "GROWTH",
        "action": "INCREASE_RISK",
        "confidence": 85,
        "score": 90,
        "direction": "UP",
        "stability": "HIGH",
        "momentum": "POSITIVE",
        "grade_stability": "STABLE",
        "consistency": "HIGH",
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 84.0,
        "adaptive_learning_required": True,
        "summary": "Learning-driven strategy",
    },
    {},
    {},
    {"summary": "Learning decision"},
)

assert_equal(
    result["outcome_learning_signal"],
    "POSITIVE",
    "learning signal -> propagated",
)

assert_equal(
    result["outcome_learning_signal_strength"],
    84.0,
    "learning signal strength -> propagated",
)

assert_equal(
    result["adaptive_learning_required"],
    True,
    "adaptive learning required -> propagated",
)


print("")
print("=" * 82)
print("CASE: EMPTY ADAPTIVE STRATEGY -> SAFE DEFAULTS")
print("=" * 82)

result = engine.generate(
    {"decision": "MAINTAIN", "market_view": "NEUTRAL", "confidence": 70},
    {},
    {},
    {},
    {},
    {},
    {},
)

assert_equal(
    result["strategy_mode"],
    "BALANCED",
    "empty adaptive -> strategy default",
)

assert_equal(
    result["adaptive_action"],
    "MONITOR_CLOSELY",
    "empty adaptive -> action default",
)

assert_equal(
    result["adaptive_learning_required"],
    None,
    "empty adaptive -> learning requirement default",
)


print("")
print("=" * 82)
print("CASE: IDENTITY FIELDS PRESERVED")
print("=" * 82)

result = engine.generate(
    {
        "decision": "ACCUMULATE",
        "market_view": "BULLISH",
        "confidence": 92,
    },
    {},
    {"confidence": 92, "reliability_level": "HIGH"},
    {
        "strategy": "GROWTH",
        "action": "INCREASE_RISK",
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 84.0,
        "adaptive_learning_required": False,
    },
    {},
    {},
    {},
)

assert_equal(
    result["decision"],
    "ACCUMULATE",
    "decision identity -> preserved",
)

assert_equal(
    result["market_view"],
    "BULLISH",
    "market view -> preserved",
)

assert_equal(
    result["confidence"],
    92,
    "confidence -> preserved",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-15 ADAPTIVE STRATEGY -> PORTFOLIO DECISION INTELLIGENCE COMPLETE =====")
print("=" * 82)
