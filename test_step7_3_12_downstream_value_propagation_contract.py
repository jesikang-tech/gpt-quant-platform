from core.portfolio_intelligence_score import PortfolioIntelligenceScore
from core.decision_confidence_intelligence import DecisionConfidenceIntelligence

print("=" * 60)
print("PHASE 7-3-12 DOWNSTREAM VALUE PROPAGATION CONTRACT")
print("=" * 60)

decision_quality = {
    "quality_level": "GOOD"
}

reliability = {
    "confidence": 90
}

adaptive_strategy = {
    "strategy": "GROWTH",
    "action": "INCREASE_RISK",
    "confidence": 100,
    "strategy_score": 100,
}

rebalance = {
    "rebalance_score": 88
}

optimization = {
    "optimization_score": 92
}

decision_consistency_score = 95

portfolio_engine = PortfolioIntelligenceScore()

portfolio_result = portfolio_engine.calculate(
    decision_score=85,
    decision_quality=decision_quality,
    reliability=reliability,
    adaptive_strategy=adaptive_strategy,
    decision_consistency_score=decision_consistency_score,
    rebalance=rebalance,
    optimization=optimization,
)

portfolio_pass = (
    portfolio_result["intelligence_score"] == 89.2
    and portfolio_result["grade"] == "A"
    and portfolio_result["intelligence_level"] == "Strong"
    and portfolio_result["components"]["adaptive_strategy"] == 100
)

print(
    "PORTFOLIO INTELLIGENCE: "
    + ("PASS" if portfolio_pass else "FAIL")
    + f" | score={portfolio_result['intelligence_score']}"
    + f" | grade={portfolio_result['grade']}"
    + f" | adaptive={portfolio_result['components']['adaptive_strategy']}"
)

confidence_engine = DecisionConfidenceIntelligence()

confidence_result = confidence_engine.calculate(
    decision_quality=decision_quality,
    reliability=reliability,
    adaptive_strategy=adaptive_strategy,
    decision_consistency_score=decision_consistency_score,
    rebalance=rebalance,
    optimization=optimization,
)

confidence_pass = (
    confidence_result["confidence_score"] == 92.0
    and confidence_result["confidence_level"] == "Very High"
    and confidence_result["confidence_grade"] == "A+"
    and confidence_result["confidence_status"] == "STRONG"
    and confidence_result["components"]["adaptive_strategy"] == 100
)

print(
    "DECISION CONFIDENCE: "
    + ("PASS" if confidence_pass else "FAIL")
    + f" | score={confidence_result['confidence_score']}"
    + f" | grade={confidence_result['confidence_grade']}"
    + f" | adaptive={confidence_result['components']['adaptive_strategy']}"
)

print("")
print("=== ADAPTIVE STRATEGY VALUE PROPAGATION ===")

print(
    "Portfolio adaptive_strategy -> score: "
    + ("PASS" if portfolio_result["components"]["adaptive_strategy"] == 100 else "FAIL")
)

print(
    "Confidence adaptive_strategy -> score: "
    + ("PASS" if confidence_result["components"]["adaptive_strategy"] == 100 else "FAIL")
)

overall_pass = portfolio_pass and confidence_pass

print("")
print("=" * 60)
print(
    "OVERALL RESULT: "
    + ("PASS" if overall_pass else "FAIL")
)
print("=" * 60)

if not overall_pass:
    raise SystemExit(1)
