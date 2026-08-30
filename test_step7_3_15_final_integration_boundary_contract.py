from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy
)
from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence
)
from core.portfolio_intelligence_score import (
    PortfolioIntelligenceScore
)
from core.decision_confidence_intelligence import (
    DecisionConfidenceIntelligence
)
from core.ai_final_decision_integration import (
    AIFinalDecisionIntegration
)

print("=" * 60)
print("PHASE 7-3-15 FINAL INTEGRATION BOUNDARY CONTRACT")
print("=" * 60)

trend = {
    "direction": "UP",
    "stability": "HIGH",
    "momentum": "POSITIVE",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 92
}

outcome_intelligence = {
    "outcome_status": "EVALUATED",
    "outcome_score": 85,
    "outcome_grade": "A",
    "outcome_learning_status": "LEARNING_AVAILABLE",
    "feedback_state": "COLLECTING",
    "adaptive_learning_required": False,
    "reassessment_required": False,
    "reassessment_status": "NOT_REQUIRED",
    "outcome_learning_signal": "POSITIVE",
    "outcome_learning_signal_strength": 0.7,
    "source_history_id": 1
}

adaptive = AIDecisionAdaptiveStrategy().analyze(
    trend,
    outcome_intelligence
)

print("")
print("=== STEP 1 ADAPTIVE STRATEGY ===")
print(
    "strategy:",
    adaptive.get("strategy")
)
print(
    "action:",
    adaptive.get("action")
)
print(
    "confidence:",
    adaptive.get("confidence")
)
print(
    "score:",
    adaptive.get("score")
)

portfolio_decision = PortfolioDecisionIntelligence().generate(
    {
        "decision": "ACCUMULATE",
        "market_view": "BULLISH",
        "confidence": 92
    },
    {
        "quality_level": "GOOD",
        "recent_trend": "STABLE"
    },
    {
        "confidence": 90,
        "reliability_level": "HIGH"
    },
    adaptive,
    {
        "rebalance_action": "HOLD"
    },
    {
        "optimization_status": "OPTIMIZED"
    },
    {
        "summary": "Portfolio intelligence summary."
    }
)

print("")
print("=== STEP 2 PORTFOLIO DECISION ===")
print(
    "strategy_mode:",
    portfolio_decision.get("strategy_mode")
)
print(
    "adaptive_action:",
    portfolio_decision.get("adaptive_action")
)
print(
    "adaptive_score:",
    portfolio_decision.get("adaptive_score")
)
print(
    "final_strategy:",
    portfolio_decision.get("final_strategy")
)

portfolio_score = PortfolioIntelligenceScore().calculate(
    decision_score=85,
    decision_quality={
        "quality_level": "GOOD"
    },
    reliability={
        "confidence": 90
    },
    adaptive_strategy=adaptive,
    decision_consistency_score=95,
    rebalance={
        "rebalance_score": 88
    },
    optimization={
        "optimization_score": 92
    }
)

print("")
print("=== STEP 3 PORTFOLIO INTELLIGENCE SCORE ===")
print(
    "intelligence_score:",
    portfolio_score.get("intelligence_score")
)
print(
    "adaptive_strategy_component:",
    portfolio_score.get(
        "components", {}
    ).get("adaptive_strategy")
)

confidence_result = DecisionConfidenceIntelligence().calculate(
    decision_quality={
        "quality_level": "GOOD"
    },
    reliability={
        "confidence": 90
    },
    adaptive_strategy=adaptive,
    decision_consistency_score=95,
    rebalance={
        "rebalance_score": 88
    },
    optimization={
        "optimization_score": 92
    }
)

print("")
print("=== STEP 4 DECISION CONFIDENCE ===")
print(
    "confidence_score:",
    confidence_result.get("confidence_score")
)
print(
    "adaptive_strategy_component:",
    confidence_result.get(
        "components", {}
    ).get("adaptive_strategy")
)

final_result = AIFinalDecisionIntegration().integrate(
    intelligence=portfolio_decision,
    intelligence_score=portfolio_score,
    decision_confidence=confidence_result
)

print("")
print("=== STEP 5 FINAL DECISION ===")
print(final_result)

checks = {
    "adaptive strategy exists":
        adaptive.get("strategy") == "GROWTH",

    "adaptive action":
        adaptive.get("action") == "INCREASE_RISK",

    "portfolio strategy propagation":
        portfolio_decision.get("strategy_mode") == "GROWTH",

    "portfolio action propagation":
        portfolio_decision.get("adaptive_action")
        == "INCREASE_RISK",

    "portfolio adaptive score":
        portfolio_score.get("components", {})
        .get("adaptive_strategy") == 100,

    "confidence adaptive score":
        confidence_result.get("components", {})
        .get("adaptive_strategy") == 100,

    "final strategy":
        final_result.get("strategy") == "GROWTH",

    "final adaptive action":
        final_result.get("adaptive_action")
        == "INCREASE_RISK",

    "final intelligence score":
        final_result.get("intelligence_score")
        == portfolio_score.get("intelligence_score"),

    "final confidence score":
        final_result.get("confidence_score")
        == confidence_result.get("confidence_score"),
}

print("")
print("=== FINAL BOUNDARY CHECK ===")

for name, passed in checks.items():
    print(
        f"{name}: "
        f"{'PASS' if passed else 'FAIL'}"
    )

overall = all(checks.values())

print("")
print(
    "OVERALL RESULT:",
    "PASS" if overall else "FAIL"
)
print("=" * 60)

if not overall:
    raise SystemExit(1)
