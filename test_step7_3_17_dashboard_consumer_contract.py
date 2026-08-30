print("=" * 60)
print("PHASE 7-3-17 DASHBOARD CONSUMER CONTRACT")
print("=" * 60)

from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy
from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence
from core.portfolio_intelligence_score import PortfolioIntelligenceScore
from core.decision_confidence_intelligence import DecisionConfidenceIntelligence

trend = {
    "direction": "UP",
    "stability": "HIGH",
    "momentum": "POSITIVE",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}

outcome_intelligence = {
    "outcome_learning_status": "LEARNING_AVAILABLE",
    "outcome_learning_signal": "POSITIVE",
    "outcome_learning_signal_strength": 100,
}

adaptive = AIDecisionAdaptiveStrategy().analyze(
    trend,
    outcome_intelligence,
)

ai_decision = {
    "decision": "ACCUMULATE",
    "market_view": "BULLISH",
    "confidence": 92,
}

decision_quality = {
    "quality_level": "GOOD",
    "recent_trend": "STABLE",
}

reliability = {
    "confidence": 90,
    "reliability_level": "HIGH",
}

rebalance = {
    "rebalance_action": "HOLD",
}

optimization = {
    "optimization_status": "OPTIMIZED",
}

explainability = {
    "summary": "Portfolio intelligence summary.",
}

portfolio = PortfolioDecisionIntelligence().generate(
    ai_decision,
    decision_quality,
    reliability,
    adaptive,
    rebalance,
    optimization,
    explainability,
)

portfolio_score = PortfolioIntelligenceScore().calculate(
    decision_score=85,
    decision_quality=decision_quality,
    reliability=reliability,
    adaptive_strategy=adaptive,
    decision_consistency_score=95,
    rebalance={"rebalance_score": 88},
    optimization={"optimization_score": 92},
)

confidence = DecisionConfidenceIntelligence().calculate(
    decision_quality=decision_quality,
    reliability=reliability,
    adaptive_strategy=adaptive,
    decision_consistency_score=95,
    rebalance={"rebalance_score": 88},
    optimization={"optimization_score": 92},
)

api_response = {
    "success": True,
    "intelligence": portfolio,
    "intelligence_score": portfolio_score,
    "decision_confidence": confidence,
    "decision_confidence_assessment": {
        "confidence_score": confidence["confidence_score"],
    },
    "decision_confidence_recommendation": {
        "action": "PROCEED",
    },
    "ai_decision_validation": {
        "strategy_mode": portfolio["strategy_mode"],
        "confidence_score": confidence["confidence_score"],
    },
    "ai_decision_validation_explainability": {
        "validation_status": "VALID",
        "strategy_mode": portfolio["strategy_mode"],
    },
}

checks = {
    "intelligence.strategy_mode":
        api_response["intelligence"].get("strategy_mode") == "GROWTH",

    "intelligence.final_strategy":
        api_response["intelligence"].get("final_strategy") == "GROWTH",

    "intelligence.adaptive_action":
        api_response["intelligence"].get("adaptive_action") == "INCREASE_RISK",

    "intelligence.rebalance_action":
        api_response["intelligence"].get("rebalance_action") == "HOLD",

    "intelligence.final_action":
        bool(api_response["intelligence"].get("final_action")),

    "intelligence_score.intelligence_score":
        api_response["intelligence_score"].get("intelligence_score") == 89.2,

    "decision_confidence.confidence_score":
        api_response["decision_confidence"].get("confidence_score") == 92.0,

    "decision_confidence_assessment.confidence_score":
        api_response["decision_confidence_assessment"].get(
            "confidence_score"
        ) == 92.0,

    "decision_confidence_recommendation.action":
        api_response["decision_confidence_recommendation"].get(
            "action"
        ) == "PROCEED",

    "ai_decision_validation.strategy_mode":
        api_response["ai_decision_validation"].get(
            "strategy_mode"
        ) == "GROWTH",

    "ai_decision_validation.confidence_score":
        api_response["ai_decision_validation"].get(
            "confidence_score"
        ) == 92.0,

    "validation_explainability.validation_status":
        api_response[
            "ai_decision_validation_explainability"
        ].get("validation_status") == "VALID",

    "validation_explainability.strategy_mode":
        api_response[
            "ai_decision_validation_explainability"
        ].get("strategy_mode") == "GROWTH",
}

print("")
print("=== DASHBOARD CONSUMER FIELD CHECK ===")

all_pass = True

for field, result in checks.items():
    status = "PASS" if result else "FAIL"
    print(f"{field}: {status}")
    all_pass = all_pass and result

print("")
print("=== DASHBOARD CONSUMER VALUES ===")
print("strategy_mode:", api_response["intelligence"]["strategy_mode"])
print("final_strategy:", api_response["intelligence"]["final_strategy"])
print("adaptive_action:", api_response["intelligence"]["adaptive_action"])
print("rebalance_action:", api_response["intelligence"]["rebalance_action"])
print("final_action:", api_response["intelligence"]["final_action"])
print(
    "intelligence_score:",
    api_response["intelligence_score"]["intelligence_score"],
)
print(
    "confidence_score:",
    api_response["decision_confidence"]["confidence_score"],
)

print("")
print("OVERALL RESULT:", "PASS" if all_pass else "FAIL")
print("=" * 60)

if not all_pass:
    raise SystemExit(1)
