from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence
from core.portfolio_intelligence_score import PortfolioIntelligenceScore
from core.decision_confidence_intelligence import DecisionConfidenceIntelligence
from core.ai_decision_validation import AIDecisionValidation
from core.ai_final_decision_integration import AIFinalDecisionIntegration


print("===== PHASE 7-4-13 COMPOSITE SEMANTIC CONTRACT =====")

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
    "summary": "Composite boundary test",
}

rebalance = {
    "rebalance_score": 80,
    "confidence": 80,
}

optimization = {
    "optimization_score": 82,
}

explainability = {
    "summary": "Composite boundary test",
}


portfolio_intelligence = (
    PortfolioDecisionIntelligence().generate(
        ai_decision,
        decision_quality,
        reliability,
        adaptive_strategy,
        rebalance,
        optimization,
        explainability,
    )
)

assert portfolio_intelligence["strategy_mode"] == "MAINTAIN"
assert portfolio_intelligence["adaptive_action"] == "MAINTAIN_ALLOCATION"
assert portfolio_intelligence["decision_alignment"] == "ALIGNED"
assert portfolio_intelligence["decision_consistency"] == "CONSISTENT"

print("")
print("PORTFOLIO INTELLIGENCE COMPOSITE: PASS")


consistency_score = (
    portfolio_intelligence["decision_consistency_score"]
)

portfolio_score = PortfolioIntelligenceScore().calculate(
    ai_decision["decision_score"],
    decision_quality,
    reliability,
    adaptive_strategy,
    consistency_score,
    rebalance,
    optimization,
)

confidence = DecisionConfidenceIntelligence().calculate(
    decision_quality,
    reliability,
    adaptive_strategy,
    consistency_score,
    rebalance,
    optimization,
)

print("")
print("PORTFOLIO SCORE:")
print(portfolio_score)

print("")
print("DECISION CONFIDENCE:")
print(confidence)


validation = AIDecisionValidation().validate(
    portfolio_intelligence,
    confidence,
)

print("")
print("===== VALIDATION =====")
print(validation)

assert validation["decision"] == "MAINTAIN"
assert validation["strategy_mode"] == "MAINTAIN"
assert validation["adaptive_action"] == "MAINTAIN_ALLOCATION"
assert validation["decision_alignment"] == "ALIGNED"
assert validation["decision_consistency"] == "CONSISTENT"

print("")
print("VALIDATION COMPOSITE BOUNDARY: PASS")


final_decision = AIFinalDecisionIntegration().integrate(
    intelligence=portfolio_intelligence,
    intelligence_score=portfolio_score,
    decision_confidence=confidence,
    ai_decision_validation=validation,
)

print("")
print("===== FINAL DECISION =====")
print(final_decision)

assert final_decision["strategy"] == "MAINTAIN"
assert final_decision["adaptive_action"] == "MAINTAIN_ALLOCATION"
assert final_decision["decision_alignment"] == "ALIGNED"
assert final_decision["decision_consistency"] == "CONSISTENT"
assert final_decision["intelligence_score"] == portfolio_score["intelligence_score"]
assert final_decision["intelligence_grade"] == portfolio_score["grade"]

print("")
print("FINAL DECISION COMPOSITE BOUNDARY: PASS")

print("")
print("===== PHASE 7-4-13 COMPOSITE SEMANTIC CONTRACT PASS =====")
