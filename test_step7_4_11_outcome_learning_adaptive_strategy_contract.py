from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy

print("=" * 60)
print("PHASE 7-4-11 OUTCOME LEARNING -> ADAPTIVE STRATEGY CONTRACT")
print("=" * 60)

engine = AIDecisionAdaptiveStrategy()

base = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}

print()
print("=== CASE 1: NEGATIVE + LEARNING REQUIRED ===")

case1 = engine.analyze(
    base,
    {
        "outcome_learning_signal": "NEGATIVE",
        "outcome_learning_signal_strength": 1.0,
        "adaptive_learning_required": True,
    }
)

print("strategy:", case1.get("strategy"))
print("action:", case1.get("action"))
print("adaptive_learning_required:",
      case1.get("adaptive_learning_required"))

case1_pass = (
    case1.get("strategy") == "DEFENSIVE"
    and case1.get("action") == "REDUCE_RISK"
)

print(
    "negative -> defensive:",
    "PASS" if case1_pass else "FAIL"
)


print()
print("=== CASE 2: NEGATIVE + LEARNING NOT REQUIRED ===")

case2 = engine.analyze(
    base,
    {
        "outcome_learning_signal": "NEGATIVE",
        "outcome_learning_signal_strength": 1.0,
        "adaptive_learning_required": False,
    }
)

print("strategy:", case2.get("strategy"))
print("action:", case2.get("action"))
print("adaptive_learning_required:",
      case2.get("adaptive_learning_required"))

case2_pass = (
    case2.get("strategy") != "DEFENSIVE"
    and case2.get("action") != "REDUCE_RISK"
)

print(
    "no forced defensive learning:",
    "PASS" if case2_pass else "FAIL"
)


print()
print("=== CASE 3: POSITIVE + STRONG + BALANCED ===")

balanced_base = {
    "direction": "SIDEWAYS",
    "stability": "MEDIUM",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "MEDIUM",
    "latest_score": 85,
}

case3 = engine.analyze(
    balanced_base,
    {
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 1.0,
        "adaptive_learning_required": False,
    }
)

print("strategy:", case3.get("strategy"))
print("action:", case3.get("action"))
print("adaptive_learning_required:",
      case3.get("adaptive_learning_required"))

case3_pass = (
    case3.get("strategy") == "GROWTH"
    and case3.get("action") == "INCREASE_RISK"
)

print(
    "positive -> growth:",
    "PASS" if case3_pass else "FAIL"
)


print()
print("=== SEMANTIC CONTRACT CHECK ===")

checks = {
    "negative learning required -> defensive":
        case1_pass,

    "negative learning not required -> no forced defensive":
        case2_pass,

    "positive strong balanced -> growth":
        case3_pass,

    "strategy output exists":
        all(
            result.get("strategy") is not None
            for result in [case1, case2, case3]
        ),

    "action output exists":
        all(
            result.get("action") is not None
            for result in [case1, case2, case3]
        ),
}

all_pass = True

for name, result in checks.items():
    status = "PASS" if result else "FAIL"
    print(f"{name}: {status}")
    all_pass = all_pass and result

print()
print(
    "OVERALL RESULT:",
    "PASS" if all_pass else "FAIL"
)
print("=" * 60)

if not all_pass:
    raise SystemExit(1)
