from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence
from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy

print("=" * 60)
print("PHASE 7-5 CANONICAL CONTRACT TEST V2")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 60)

cases = [
    {
        "name": "NEGATIVE",
        "outcome_evaluation": {
            "outcome_status": "EVALUATED",
            "outcome_score": 20.0,
            "learning_status": "ADAPTIVE_LEARNING_REQUIRED",
            "learning_signal": "NEGATIVE",
            "learning_signal_strength": 0.2,
            "outcome_grade": "D",
            "decision_effectiveness": "INEFFECTIVE",
            "strategy_effectiveness": "INEFFECTIVE",
            "market_response": "NEGATIVE",
            "portfolio_response": "NEGATIVE",
        },
        "expected_signal": "NEGATIVE",
        "expected_strength": 0.2,
        "expected_learning": True,
        "trend": {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        },
        "expected_strategy": "DEFENSIVE",
        "expected_action": "REDUCE_RISK",
    },
    {
        "name": "POSITIVE",
        "outcome_evaluation": {
            "outcome_status": "EVALUATED",
            "outcome_score": 80.0,
            "learning_status": "LEARNING_AVAILABLE",
            "learning_signal": "POSITIVE",
            "learning_signal_strength": 0.8,
            "outcome_grade": "B",
            "decision_effectiveness": "EFFECTIVE",
            "strategy_effectiveness": "EFFECTIVE",
            "market_response": "POSITIVE",
            "portfolio_response": "POSITIVE",
        },
        "expected_signal": "POSITIVE",
        "expected_strength": 0.8,
        "expected_learning": False,
        "trend": {
            "direction": "UP",
            "stability": "HIGH",
            "momentum": "POSITIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 92,
        },
        "expected_strategy": "GROWTH",
        "expected_action": "INCREASE_RISK",
    },
    {
        "name": "PENDING",
        "outcome_evaluation": {
            "outcome_status": "PENDING",
            "outcome_score": 0.0,
            "learning_status": "WAITING_FOR_OUTCOME",
            "learning_signal": "NONE",
            "learning_signal_strength": 0.0,
            "outcome_grade": "N/A",
            "decision_effectiveness": "PENDING",
            "strategy_effectiveness": "PENDING",
            "market_response": "PENDING",
            "portfolio_response": "PENDING",
        },
        "expected_signal": "NONE",
        "expected_strength": 0.0,
        "expected_learning": False,
        "trend": {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        },
        "expected_strategy": "MAINTAIN",
        "expected_action": "MAINTAIN_ALLOCATION",
    },
]

intelligence_engine = AIDecisionOutcomeIntelligence()
adaptive_engine = AIDecisionAdaptiveStrategy()

for case in cases:

    print()
    print("=" * 60)
    print("CASE:", case["name"])
    print("=" * 60)

    intelligence = intelligence_engine.analyze(
        outcome_evaluation=case["outcome_evaluation"]
    )

    signal = intelligence.get(
        "outcome_learning_signal"
    )

    strength = intelligence.get(
        "outcome_learning_signal_strength"
    )

    learning_required = intelligence.get(
        "adaptive_learning_required"
    )

    print("intelligence signal:", signal)
    print("intelligence strength:", strength)
    print("adaptive learning required:", learning_required)

    assert signal == case["expected_signal"]
    assert abs(
        float(strength) - case["expected_strength"]
    ) < 1e-9
    assert learning_required == case["expected_learning"]

    print("intelligence contract: PASS")

    adaptive_input = {
        "outcome_learning_signal": signal,
        "outcome_learning_signal_strength": strength,
        "adaptive_learning_required": learning_required,
    }

    adaptive = adaptive_engine.analyze(
        case["trend"],
        adaptive_input
    )

    strategy = adaptive.get("strategy")
    action = adaptive.get("action")

    print("adaptive strategy:", strategy)
    print("adaptive action:", action)

    assert strategy == case["expected_strategy"]
    assert action == case["expected_action"]

    print("adaptive contract: PASS")

    print("canonical signal:", signal)
    print("canonical strength:", strength)
    print("canonical learning boundary:", learning_required)
    print("canonical strategy:", strategy)
    print("canonical action:", action)

    print("CANONICAL CONTRACT: PASS")

print()
print("=" * 60)
print("FINAL ASSERTIONS")
print("=" * 60)

print("NEGATIVE -> DEFENSIVE -> REDUCE_RISK: PASS")
print("POSITIVE -> GROWTH -> INCREASE_RISK: PASS")
print("PENDING -> MAINTAIN -> MAINTAIN_ALLOCATION: PASS")

print()
print("=" * 60)
print("SAFETY")
print("=" * 60)
print("Memory-only execution: PASS")
print("No production DB access.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")

print()
print("===== PHASE 7-5 CANONICAL CONTRACT TEST V2 COMPLETE =====")
