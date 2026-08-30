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
print("PHASE 7-3-16 API FINAL INTEGRATION BOUNDARY CONTRACT")
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

adaptive_strategy = (
    AIDecisionAdaptiveStrategy().analyze(
        trend,
        outcome_intelligence
    )
)

portfolio_decision = (
    PortfolioDecisionIntelligence().generate(
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
        adaptive_strategy,
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
)

portfolio_score = (
    PortfolioIntelligenceScore().calculate(
        decision_score=85,
        decision_quality={
            "quality_level": "GOOD"
        },
        reliability={
            "confidence": 90
        },
        adaptive_strategy=adaptive_strategy,
        decision_consistency_score=95,
        rebalance={
            "rebalance_score": 88
        },
        optimization={
            "optimization_score": 92
        }
    )
)

decision_confidence = (
    DecisionConfidenceIntelligence().calculate(
        decision_quality={
            "quality_level": "GOOD"
        },
        reliability={
            "confidence": 90
        },
        adaptive_strategy=adaptive_strategy,
        decision_consistency_score=95,
        rebalance={
            "rebalance_score": 88
        },
        optimization={
            "optimization_score": 92
        }
    )
)

final_decision = (
    AIFinalDecisionIntegration().integrate(
        intelligence=portfolio_decision,
        intelligence_score=portfolio_score,
        decision_confidence=decision_confidence
    )
)

print("")
print("=== API BOUNDARY SOURCE OBJECTS ===")
print(
    "adaptive_strategy:",
    adaptive_strategy.get("strategy")
)
print(
    "portfolio strategy_mode:",
    portfolio_decision.get("strategy_mode")
)
print(
    "portfolio intelligence_score:",
    portfolio_score.get("intelligence_score")
)
print(
    "decision confidence_score:",
    decision_confidence.get("confidence_score")
)

print("")
print("=== API RESPONSE CONTRACT ===")

response = {
    "success": True,
    "strategy": adaptive_strategy,
    "outcome_intelligence": outcome_intelligence,
    "intelligence": portfolio_decision,
    "intelligence_score": portfolio_score,
    "decision_confidence": decision_confidence,
    "final_decision": final_decision
}

required_top_level = [
    "success",
    "strategy",
    "outcome_intelligence",
    "intelligence",
    "intelligence_score",
    "decision_confidence",
    "final_decision",
]

checks = {}

for field in required_top_level:
    checks[
        f"top-level {field}"
    ] = field in response

checks[
    "strategy.strategy = GROWTH"
] = (
    response["strategy"].get("strategy")
    == "GROWTH"
)

checks[
    "strategy.action = INCREASE_RISK"
] = (
    response["strategy"].get("action")
    == "INCREASE_RISK"
)

checks[
    "intelligence.strategy_mode = GROWTH"
] = (
    response["intelligence"].get("strategy_mode")
    == "GROWTH"
)

checks[
    "intelligence.adaptive_action = INCREASE_RISK"
] = (
    response["intelligence"].get("adaptive_action")
    == "INCREASE_RISK"
)

checks[
    "intelligence_score exists"
] = (
    response["intelligence_score"].get(
        "intelligence_score"
    ) is not None
)

checks[
    "decision_confidence exists"
] = (
    response["decision_confidence"].get(
        "confidence_score"
    ) is not None
)

checks[
    "final_decision.strategy = GROWTH"
] = (
    response["final_decision"].get("strategy")
    == "GROWTH"
)

checks[
    "final_decision.adaptive_action = INCREASE_RISK"
] = (
    response["final_decision"].get(
        "adaptive_action"
    )
    == "INCREASE_RISK"
)

checks[
    "final_decision.intelligence_score propagated"
] = (
    response["final_decision"].get(
        "intelligence_score"
    )
    == response["intelligence_score"].get(
        "intelligence_score"
    )
)

checks[
    "final_decision.confidence_score propagated"
] = (
    response["final_decision"].get(
        "confidence_score"
    )
    == response["decision_confidence"].get(
        "confidence_score"
    )
)

print("")

for name, passed in checks.items():
    print(
        f"{name}: "
        f"{'PASS' if passed else 'FAIL'}"
    )

print("")
print("=== FINAL DECISION ===")
print(final_decision)

overall = all(checks.values())

print("")
print(
    "OVERALL RESULT:",
    "PASS" if overall else "FAIL"
)
print("=" * 60)

if not overall:
    raise SystemExit(1)
