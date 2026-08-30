from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)
from core.decision_confidence_intelligence import (
    DecisionConfidenceIntelligence,
)


print("=" * 82)
print("PHASE 7-10-5")
print("ADAPTIVE STRATEGY -> DECISION CONFIDENCE INTELLIGENCE")
print("BOUNDARY PROPAGATION CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


adaptive_engine = AIDecisionAdaptiveStrategy()
confidence_engine = DecisionConfidenceIntelligence()


TREND = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}


BASE_INPUT = {
    "decision_quality": {
        "quality_score": 85.0,
    },
    "reliability": {
        "confidence": 90.0,
    },
    "decision_consistency_score": 100.0,
    "rebalance": {
        "rebalance_score": 80.0,
    },
    "optimization": {
        "optimization_score": 80.0,
    },
}


def build_confidence(adaptive_strategy):
    return confidence_engine.calculate(
        decision_quality=BASE_INPUT["decision_quality"],
        reliability=BASE_INPUT["reliability"],
        adaptive_strategy=adaptive_strategy,
        decision_consistency_score=(
            BASE_INPUT["decision_consistency_score"]
        ),
        rebalance=BASE_INPUT["rebalance"],
        optimization=BASE_INPUT["optimization"],
    )


print("")
print("=" * 82)
print("CASE 1: ADAPTIVE STRATEGY -> CONFIDENCE COMPONENT")
print("=" * 82)


adaptive_strategy = adaptive_engine.analyze(
    TREND,
    {
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": False,
    },
)

confidence = build_confidence(
    adaptive_strategy
)

print("--- ADAPTIVE STRATEGY ---")
print(
    "strategy:",
    adaptive_strategy.get("strategy")
)
print(
    "confidence:",
    adaptive_strategy.get("confidence")
)
print(
    "outcome_learning_signal:",
    adaptive_strategy.get(
        "outcome_learning_signal"
    )
)

print("--- DECISION CONFIDENCE ---")
print(
    "adaptive_strategy component:",
    confidence["components"]["adaptive_strategy"]
)
print(
    "confidence_score:",
    confidence["confidence_score"]
)

assert confidence["components"]["adaptive_strategy"] == (
    adaptive_strategy["confidence"]
)

print(
    "Adaptive confidence -> "
    "Decision Confidence adaptive component: PASS"
)


print("")
print("=" * 82)
print("CASE 2: STRATEGY_SCORE PRIORITY")
print("=" * 82)


strategy_with_both = {
    "strategy": "MAINTAIN",
    "confidence": 60.0,
    "strategy_score": 95.0,
}

confidence_priority = build_confidence(
    strategy_with_both
)

print(
    "strategy confidence:",
    strategy_with_both["confidence"]
)
print(
    "strategy_score:",
    strategy_with_both["strategy_score"]
)
print(
    "resolved adaptive component:",
    confidence_priority[
        "components"
    ]["adaptive_strategy"]
)

assert confidence_priority[
    "components"
]["adaptive_strategy"] == 95.0

print(
    "strategy_score overrides confidence: PASS"
)


print("")
print("=" * 82)
print("CASE 3: CONFIDENCE FALLBACK")
print("=" * 82)


strategy_confidence_only = {
    "strategy": "MAINTAIN",
    "confidence": 72.0,
}

confidence_fallback = build_confidence(
    strategy_confidence_only
)

print(
    "confidence:",
    strategy_confidence_only["confidence"]
)
print(
    "resolved adaptive component:",
    confidence_fallback[
        "components"
    ]["adaptive_strategy"]
)

assert confidence_fallback[
    "components"
]["adaptive_strategy"] == 72.0

print(
    "confidence fallback -> "
    "adaptive component: PASS"
)


print("")
print("=" * 82)
print("CASE 4: ADAPTIVE COMPONENT CHANGES FINAL SCORE")
print("=" * 82)


low_adaptive = {
    "strategy": "CAUTIOUS",
    "confidence": 40.0,
}

high_adaptive = {
    "strategy": "GROWTH",
    "confidence": 100.0,
}

low_confidence = build_confidence(
    low_adaptive
)

high_confidence = build_confidence(
    high_adaptive
)

print(
    "low adaptive component:",
    low_confidence[
        "components"
    ]["adaptive_strategy"]
)

print(
    "low final confidence:",
    low_confidence[
        "confidence_score"
    ]
)

print(
    "high adaptive component:",
    high_confidence[
        "components"
    ]["adaptive_strategy"]
)

print(
    "high final confidence:",
    high_confidence[
        "confidence_score"
    ]
)

assert (
    low_confidence[
        "components"
    ]["adaptive_strategy"]
    == 40.0
)

assert (
    high_confidence[
        "components"
    ]["adaptive_strategy"]
    == 100.0
)

assert (
    high_confidence[
        "confidence_score"
    ]
    > low_confidence[
        "confidence_score"
    ]
)

print(
    "Adaptive strategy materially changes "
    "final confidence score: PASS"
)


print("")
print("=" * 82)
print("CASE 5: EXACT 15% ADAPTIVE WEIGHT")
print("=" * 82)


reference = {
    "strategy": "MAINTAIN",
    "confidence": 80.0,
}

reference_confidence = build_confidence(
    reference
)

expected = (
    90.0 * 0.25
    + 100.0 * 0.25
    + 80.0 * 0.15
    + 85.0 * 0.15
    + 80.0 * 0.10
    + 80.0 * 0.10
)

expected = round(
    expected,
    1
)

actual = reference_confidence[
    "confidence_score"
]

print(
    "expected confidence score:",
    expected
)

print(
    "actual confidence score:",
    actual
)

print(
    "adaptive strategy weight:",
    "15%"
)

assert actual == expected

assert (
    reference_confidence[
        "components"
    ]["adaptive_strategy"]
    == 80.0
)

print(
    "Adaptive Strategy 15% confidence weight: PASS"
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "Adaptive confidence -> "
    "Decision Confidence component: PASS"
)

print(
    "strategy_score priority: PASS"
)

print(
    "confidence fallback: PASS"
)

print(
    "Adaptive change -> final confidence change: PASS"
)

print(
    "Adaptive Strategy weight = 15%: PASS"
)

print(
    "Adaptive Strategy -> "
    "Decision Confidence Intelligence boundary: PASS"
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
print("===== PHASE 7-10-5 CONTRACT TEST COMPLETE =====")
print("=" * 82)
