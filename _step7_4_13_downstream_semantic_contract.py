from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence
from core.portfolio_intelligence_score import PortfolioIntelligenceScore
from core.decision_confidence_intelligence import DecisionConfidenceIntelligence


print("===== PHASE 7-4-13 DOWNSTREAM SEMANTIC CONTRACT =====")

ai_decision = {
    "decision": "MAINTAIN",
    "decision_score": 85,
    "market_view": "NEUTRAL",
}

decision_quality = {
    "quality_score": 85,
    "quality_level": "GOOD",
}

reliability = {
    "confidence": 90,
}

adaptive_strategy = {
    "strategy": "MAINTAIN",
    "action": "MAINTAIN_ALLOCATION",
    "confidence": 88,
    "score": 85,
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "summary": "Semantic boundary test",
}

rebalance = {
    "rebalance_score": 80,
    "confidence": 80,
}

optimization = {
    "optimization_score": 82,
}

explainability = {
    "summary": "Semantic boundary test",
}


portfolio_engine = PortfolioDecisionIntelligence()

intelligence = portfolio_engine.generate(
    ai_decision,
    decision_quality,
    reliability,
    adaptive_strategy,
    rebalance,
    optimization,
    explainability,
)

print("")
print("===== PORTFOLIO INTELLIGENCE =====")
print(intelligence)

assert "decision_consistency_score" in intelligence
assert isinstance(
    intelligence["decision_consistency_score"],
    (int, float),
)

consistency_score = intelligence["decision_consistency_score"]

print("")
print("DECISION CONSISTENCY BOUNDARY: PASS")


score_engine = PortfolioIntelligenceScore()

intelligence_score = score_engine.calculate(
    ai_decision["decision_score"],
    decision_quality,
    reliability,
    adaptive_strategy,
    consistency_score,
    rebalance,
    optimization,
)

print("")
print("===== PORTFOLIO INTELLIGENCE SCORE =====")
print(intelligence_score)

assert "intelligence_score" in intelligence_score
assert "components" in intelligence_score
assert (
    intelligence_score["components"]["decision_consistency"]
    == consistency_score
)

print("")
print("PORTFOLIO SCORE BOUNDARY: PASS")


confidence_engine = DecisionConfidenceIntelligence()

decision_confidence = confidence_engine.calculate(
    decision_quality,
    reliability,
    adaptive_strategy,
    consistency_score,
    rebalance,
    optimization,
)

print("")
print("===== DECISION CONFIDENCE =====")
print(decision_confidence)

assert "confidence_score" in decision_confidence
assert "components" in decision_confidence
assert (
    decision_confidence["components"]["decision_consistency"]
    == consistency_score
)

print("")
print("CONFIDENCE BOUNDARY: PASS")


print("")
print("===== PHASE 7-4-13 SEMANTIC CONTRACT PASS =====")
