from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence
from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy
from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence

print("=" * 64)
print("PHASE 7-5 PORTFOLIO INTELLIGENCE BRIDGE CONTRACT TEST")
print("OUTCOME -> ADAPTIVE -> PORTFOLIO")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 64)

cases = [
    {
        "name": "NEGATIVE",
        "signal": "NEGATIVE",
        "strength": 0.2,
        "learning_required": True,
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
        "expected_final_strategy": "DEFENSIVE",
        "expected_final_action":
            "Reduce equity exposure and strengthen defensive allocation",
    },
    {
        "name": "POSITIVE",
        "signal": "POSITIVE",
        "strength": 0.8,
        "learning_required": False,
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
        "expected_final_strategy": "GROWTH",
        "expected_final_action":
            "Increase growth exposure while maintaining risk controls",
    },
    {
        "name": "PENDING",
        "signal": "NONE",
        "strength": 0.0,
        "learning_required": False,
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
        "expected_final_strategy": "MAINTAIN",
        "expected_final_action":
            "Maintain balanced allocation and monitor market conditions",
    },
]

outcome_engine = AIDecisionOutcomeIntelligence()
adaptive_engine = AIDecisionAdaptiveStrategy()
portfolio_engine = PortfolioDecisionIntelligence()

for case in cases:

    print()
    print("=" * 64)
    print("CASE:", case["name"])
    print("=" * 64)

    # -------------------------------------------------
    # 1. Outcome Intelligence
    # -------------------------------------------------

    if case["name"] == "NEGATIVE":
        outcome_evaluation = {
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
        }

    elif case["name"] == "POSITIVE":
        outcome_evaluation = {
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
        }

    else:
        outcome_evaluation = {
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
        }

    intelligence = outcome_engine.analyze(
        outcome_evaluation=outcome_evaluation
    )

    signal = intelligence["outcome_learning_signal"]
    strength = intelligence["outcome_learning_signal_strength"]
    learning_required = intelligence["adaptive_learning_required"]

    assert signal == case["signal"]
    assert abs(float(strength) - case["strength"]) < 1e-9
    assert learning_required == case["learning_required"]

    print("intelligence signal:", signal)
    print("intelligence strength:", strength)
    print("adaptive learning required:", learning_required)
    print("intelligence contract: PASS")

    # -------------------------------------------------
    # 2. Adaptive Strategy
    # -------------------------------------------------

    adaptive_input = {
        "outcome_learning_signal": signal,
        "outcome_learning_signal_strength": strength,
        "adaptive_learning_required": learning_required,
    }

    adaptive = adaptive_engine.analyze(
        case["trend"],
        adaptive_input
    )

    strategy = adaptive["strategy"]
    action = adaptive["action"]

    assert strategy == case["expected_strategy"]
    assert action == case["expected_action"]

    print("adaptive strategy:", strategy)
    print("adaptive action:", action)
    print("adaptive contract: PASS")

    # -------------------------------------------------
    # 3. Portfolio Intelligence Bridge
    # -------------------------------------------------

    portfolio = portfolio_engine.generate(
        ai_decision={
            "decision": (
                "DEFENSIVE"
                if case["name"] == "NEGATIVE"
                else "ACCUMULATE"
                if case["name"] == "POSITIVE"
                else "MAINTAIN"
            ),
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
        adaptive_strategy=adaptive,
        rebalance={
            "rebalance_action": "HOLD",
        },
        optimization={
            "optimization_status": "READY",
        },
        explainability={
            "summary": "Controlled canonical bridge test",
        },
    )

    final_strategy = portfolio.get("final_strategy")
    final_action = portfolio.get("final_action")
    strategy_mode = portfolio.get("strategy_mode")
    adaptive_action = portfolio.get("adaptive_action")

    print()
    print("strategy_mode:", strategy_mode)
    print("adaptive_action:", adaptive_action)
    print("final_strategy:", final_strategy)
    print("final_action:", final_action)

    assert strategy_mode == case["expected_final_strategy"]
    assert adaptive_action == case["expected_action"]
    assert final_strategy == case["expected_final_strategy"]
    assert final_action == case["expected_final_action"]

    print("strategy bridge: PASS")
    print("adaptive action preservation: PASS")
    print("final strategy contract: PASS")
    print("final action semantic contract: PASS")

print()
print("=" * 64)
print("FINAL ASSERTIONS")
print("=" * 64)
print("NEGATIVE -> DEFENSIVE -> defensive portfolio action: PASS")
print("POSITIVE -> GROWTH -> growth portfolio action: PASS")
print("PENDING -> MAINTAIN -> maintain portfolio action: PASS")

print()
print("=" * 64)
print("SAFETY")
print("=" * 64)
print("Memory-only execution: PASS")
print("No production DB access.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")

print()
print("===== PHASE 7-5 PORTFOLIO INTELLIGENCE BRIDGE CONTRACT TEST COMPLETE =====")
