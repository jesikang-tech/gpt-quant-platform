from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


ENGINE = AIDecisionAdaptiveStrategy()


print("=" * 60)
print("PHASE 7-2-7 OUTCOME LEARNING OVERRIDE CONTRACT")
print("=" * 60)


def case(
    name,
    strategy,
    signal,
    strength,
    adaptive_required,
    expected,
):
    result = ENGINE._apply_outcome_learning(
        strategy=strategy,
        learning_signal=signal,
        learning_signal_strength=strength,
        adaptive_learning_required=adaptive_required,
    )

    assert result == expected

    print(
        f"{name}: PASS | "
        f"strategy={strategy} | "
        f"signal={signal} | "
        f"strength={strength} | "
        f"adaptive={adaptive_required} | "
        f"result={result}"
    )


print("")
print("=== NEGATIVE OVERRIDE ===")

case(
    "CASE 1 NEGATIVE + ADAPTIVE",
    "BALANCED",
    "NEGATIVE",
    1.0,
    True,
    "DEFENSIVE",
)

case(
    "CASE 2 NEGATIVE WITHOUT ADAPTIVE",
    "BALANCED",
    "NEGATIVE",
    1.0,
    False,
    "BALANCED",
)


print("")
print("=== POSITIVE OVERRIDE ===")

case(
    "CASE 3 POSITIVE + STRONG + BALANCED",
    "BALANCED",
    "POSITIVE",
    0.7,
    False,
    "GROWTH",
)

case(
    "CASE 4 POSITIVE + WEAK + BALANCED",
    "BALANCED",
    "POSITIVE",
    0.69,
    False,
    "BALANCED",
)

case(
    "CASE 5 POSITIVE + STRONG + MAINTAIN",
    "MAINTAIN",
    "POSITIVE",
    0.9,
    False,
    "MAINTAIN",
)


print("")
print("=== NEUTRAL / NO OVERRIDE ===")

case(
    "CASE 6 NONE",
    "BALANCED",
    "NONE",
    0.0,
    False,
    "BALANCED",
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
