from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def generate(decision, strategy, signal, strength, adaptive_required):
    engine = PortfolioDecisionIntelligence()

    return engine.generate(
        ai_decision={
            "decision": decision,
            "market_view": "NEUTRAL",
            "confidence": 90,
        },
        decision_quality={
            "quality_level": "HIGH",
            "recent_trend": "STABLE",
        },
        reliability={
            "confidence": 90,
            "reliability_level": "HIGH",
        },
        adaptive_strategy={
            "strategy": strategy,
            "action": {
                "GROWTH": "INCREASE_RISK",
                "DEFENSIVE": "REDUCE_RISK",
                "BALANCED": "MAINTAIN_BALANCE",
            }.get(strategy, "MONITOR_CLOSELY"),
            "confidence": 80,
            "score": 75,
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "summary": "",
            "outcome_learning_signal": signal,
            "outcome_learning_signal_strength": strength,
            "adaptive_learning_required": adaptive_required,
        },
        rebalance={
            "rebalance_action": "HOLD",
        },
        optimization={
            "optimization_status": "OPTIMIZED",
        },
        explainability={
            "summary": "",
        },
    )


print("=" * 82)
print("PHASE 7-10-20-3")
print("CANONICAL LEARNING -> ADAPTIVE STRATEGY -> PORTFOLIO DECISION")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: POSITIVE -> GROWTH -> PORTFOLIO DECISION")
print("=" * 82)

positive = generate(
    "MAINTAIN",
    "GROWTH",
    "POSITIVE",
    100.0,
    False,
)

assert_equal(
    positive["outcome_learning_signal"],
    "POSITIVE",
    "POSITIVE -> learning signal",
)

assert_equal(
    positive["final_strategy"],
    "GROWTH",
    "POSITIVE -> final strategy",
)

assert_equal(
    positive["adaptive_override"],
    False,
    "POSITIVE -> no adaptive override",
)

assert_equal(
    positive["decision_alignment"],
    "CONFLICT",
    "POSITIVE -> decision alignment",
)

assert_equal(
    positive["decision_consistency"],
    "CONFLICT",
    "POSITIVE -> decision consistency",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE -> DEFENSIVE -> ADAPTIVE OVERRIDE")
print("=" * 82)

negative = generate(
    "MAINTAIN",
    "DEFENSIVE",
    "NEGATIVE",
    100.0,
    True,
)

assert_equal(
    negative["outcome_learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> learning signal",
)

assert_equal(
    negative["adaptive_learning_required"],
    True,
    "NEGATIVE -> adaptive learning required",
)

assert_equal(
    negative["final_strategy"],
    "DEFENSIVE",
    "NEGATIVE -> final strategy",
)

assert_equal(
    negative["adaptive_override"],
    True,
    "NEGATIVE -> adaptive override",
)

assert_equal(
    negative["decision_consistency"],
    "OVERRIDDEN",
    "NEGATIVE -> decision consistency",
)

assert_equal(
    negative["decision_consistency_score"],
    60,
    "NEGATIVE -> consistency score",
)


print("")
print("=" * 82)
print("CASE: STABLE -> BALANCED -> CONSISTENT")
print("=" * 82)

stable = generate(
    "MAINTAIN",
    "BALANCED",
    "STABLE",
    50.0,
    False,
)

assert_equal(
    stable["outcome_learning_signal"],
    "STABLE",
    "STABLE -> learning signal",
)

assert_equal(
    stable["final_strategy"],
    "BALANCED",
    "STABLE -> final strategy",
)

assert_equal(
    stable["adaptive_override"],
    False,
    "STABLE -> no adaptive override",
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

assert_equal(
    stable["decision_consistency_score"],
    100,
    "STABLE -> consistency score",
)


print("")
print("=" * 82)
print("CASE: NONE -> EXISTING STRATEGY")
print("=" * 82)

none_signal = generate(
    "MAINTAIN",
    "BALANCED",
    "NONE",
    0.0,
    False,
)

assert_equal(
    none_signal["final_strategy"],
    "BALANCED",
    "NONE -> existing strategy",
)

assert_equal(
    none_signal["adaptive_override"],
    False,
    "NONE -> no adaptive override",
)

assert_equal(
    none_signal["decision_alignment"],
    "ALIGNED",
    "NONE -> decision alignment",
)

assert_equal(
    none_signal["decision_consistency"],
    "CONSISTENT",
    "NONE -> decision consistency",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-3 PORTFOLIO DECISION BOUNDARY COMPLETE =====")
print("=" * 82)
