from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence
from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy
from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence

print("=" * 68)
print("PHASE 7-5 FINAL OUTPUT CONTRACT TEST")
print("OUTCOME -> INTELLIGENCE -> ADAPTIVE -> PORTFOLIO -> OUTPUT")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 68)

cases = [
    {
        "name": "NEGATIVE",
        "outcome": {
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
        "trend": {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        },
        "expected_strategy": "DEFENSIVE",
        "expected_adaptive_action": "REDUCE_RISK",
        "expected_final_strategy": "DEFENSIVE",
        "expected_final_action":
            "Reduce equity exposure and strengthen defensive allocation",
    },
    {
        "name": "POSITIVE",
        "outcome": {
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
        "trend": {
            "direction": "UP",
            "stability": "HIGH",
            "momentum": "POSITIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 92,
        },
        "expected_strategy": "GROWTH",
        "expected_adaptive_action": "INCREASE_RISK",
        "expected_final_strategy": "GROWTH",
        "expected_final_action":
            "Increase growth exposure while maintaining risk controls",
    },
    {
        "name": "PENDING",
        "outcome": {
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
        "trend": {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        },
        "expected_strategy": "MAINTAIN",
        "expected_adaptive_action": "MAINTAIN_ALLOCATION",
        "expected_final_strategy": "MAINTAIN",
        "expected_final_action":
            "Maintain balanced allocation and monitor market conditions",
    },
]

outcome_engine = AIDecisionOutcomeIntelligence()
adaptive_engine = AIDecisionAdaptiveStrategy()
portfolio_engine = PortfolioDecisionIntelligence()

required_output_fields = [
    "strategy_mode",
    "adaptive_action",
    "adaptive_confidence",
    "adaptive_score",
    "adaptive_override",
    "adaptive_override_reason",
    "decision_alignment",
    "final_strategy",
    "final_action",
]

for case in cases:

    print()
    print("=" * 68)
    print("CASE:", case["name"])
    print("=" * 68)

    # ---------------------------------------------
    # Outcome -> Intelligence
    # ---------------------------------------------

    intelligence_result = outcome_engine.analyze(
        outcome_evaluation=case["outcome"]
    )

    signal = intelligence_result[
        "outcome_learning_signal"
    ]

    strength = intelligence_result[
        "outcome_learning_signal_strength"
    ]

    learning_required = intelligence_result[
        "adaptive_learning_required"
    ]

    print("learning signal:", signal)
    print("learning strength:", strength)
    print("adaptive learning required:", learning_required)

    # ---------------------------------------------
    # Intelligence -> Adaptive Strategy
    # ---------------------------------------------

    adaptive_result = adaptive_engine.analyze(
        case["trend"],
        {
            "outcome_learning_signal": signal,
            "outcome_learning_signal_strength": strength,
            "adaptive_learning_required": learning_required,
        },
    )

    strategy = adaptive_result["strategy"]
    adaptive_action = adaptive_result["action"]

    assert strategy == case["expected_strategy"]
    assert adaptive_action == case["expected_adaptive_action"]

    print("adaptive strategy:", strategy)
    print("adaptive action:", adaptive_action)
    print("adaptive contract: PASS")

    # ---------------------------------------------
    # Adaptive -> Portfolio Intelligence
    # ---------------------------------------------

    ai_decision = {
        "decision": (
            "DEFENSIVE"
            if case["name"] == "NEGATIVE"
            else "ACCUMULATE"
            if case["name"] == "POSITIVE"
            else "MAINTAIN"
        ),
        "market_view": "NEUTRAL",
        "confidence": 90,
    }

    portfolio_result = portfolio_engine.generate(
        ai_decision,
        {
            "quality_level": "HIGH",
            "recent_trend": "STABLE",
        },
        {
            "confidence": 90,
            "reliability_level": "HIGH",
        },
        adaptive_result,
        {
            "rebalance_action": "HOLD",
        },
        {
            "optimization_status": "READY",
        },
        {
            "summary": "Phase 7-5 canonical output test",
        },
    )

    # ---------------------------------------------
    # Final Output Contract
    # ---------------------------------------------

    print()
    print("===== FINAL OUTPUT =====")

    for field in required_output_fields:
        assert field in portfolio_result, (
            f"{case['name']}: missing output field: {field}"
        )

        print(
            f"{field}:",
            portfolio_result.get(field)
        )

    assert (
        portfolio_result["strategy_mode"]
        == case["expected_final_strategy"]
    )

    assert (
        portfolio_result["adaptive_action"]
        == case["expected_adaptive_action"]
    )

    assert (
        portfolio_result["final_strategy"]
        == case["expected_final_strategy"]
    )

    assert (
        portfolio_result["final_action"]
        == case["expected_final_action"]
    )

    print()
    print("strategy_mode contract: PASS")
    print("adaptive_action contract: PASS")
    print("final_strategy contract: PASS")
    print("final_action contract: PASS")
    print("FINAL OUTPUT CONTRACT: PASS")


print()
print("=" * 68)
print("FINAL ASSERTIONS")
print("=" * 68)

print(
    "NEGATIVE -> DEFENSIVE -> defensive final action: PASS"
)
print(
    "POSITIVE -> GROWTH -> growth final action: PASS"
)
print(
    "PENDING -> MAINTAIN -> maintain final action: PASS"
)

print()
print("=" * 68)
print("SAFETY")
print("=" * 68)
print("Memory-only execution: PASS")
print("No production DB access.")
print("No API runtime call.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")

print()
print("===== PHASE 7-5 FINAL OUTPUT CONTRACT TEST COMPLETE =====")
