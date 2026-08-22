from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy
from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence


print("===== PHASE 7-4-12 DOWNSTREAM SEMANTIC CONTRACT =====")

trend = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}

outcome_intelligence = {
    "outcome_learning_signal": "POSITIVE",
    "outcome_learning_signal_strength": 0.8,
    "adaptive_learning_required": True,
}

adaptive_engine = AIDecisionAdaptiveStrategy()

adaptive_strategy = adaptive_engine.analyze(
    trend,
    outcome_intelligence,
)

print("")
print("===== ADAPTIVE STRATEGY RESULT =====")
print(adaptive_strategy)

required_adaptive_fields = {
    "strategy",
    "action",
    "confidence",
    "score",
    "direction",
    "stability",
    "momentum",
    "grade_stability",
    "consistency",
    "summary",
    "outcome_learning_signal",
    "outcome_learning_signal_strength",
    "adaptive_learning_required",
}

assert required_adaptive_fields.issubset(
    adaptive_strategy.keys()
)

assert adaptive_strategy["outcome_learning_signal"] == "POSITIVE"
assert adaptive_strategy["outcome_learning_signal_strength"] == 0.8
assert adaptive_strategy["adaptive_learning_required"] is True

print("")
print("ADAPTIVE CONTRACT: PASS")

portfolio_engine = PortfolioDecisionIntelligence()

ai_decision = {
    "decision": "MAINTAIN",
    "market_view": "NEUTRAL",
    "confidence": 80,
}

decision_quality = {
    "quality_level": "GOOD",
}

reliability = {
    "confidence": 80,
    "reliability_level": "HIGH",
}

rebalance = {
    "rebalance_action": "HOLD",
}

optimization = {
    "optimization_status": "READY",
}

explainability = {
    "summary": "Semantic contract test",
}

portfolio_result = portfolio_engine.generate(
    ai_decision,
    decision_quality,
    reliability,
    adaptive_strategy,
    rebalance,
    optimization,
    explainability,
)

print("")
print("===== DOWNSTREAM RESULT =====")
print(portfolio_result)

assert portfolio_result["strategy_mode"] == adaptive_strategy["strategy"]
assert portfolio_result["adaptive_action"] == adaptive_strategy["action"]
assert portfolio_result["adaptive_confidence"] == adaptive_strategy["confidence"]
assert portfolio_result["adaptive_score"] == adaptive_strategy["score"]
assert portfolio_result["adaptive_direction"] == adaptive_strategy["direction"]
assert portfolio_result["adaptive_stability"] == adaptive_strategy["stability"]
assert portfolio_result["adaptive_momentum"] == adaptive_strategy["momentum"]
assert portfolio_result["adaptive_grade_stability"] == adaptive_strategy["grade_stability"]
assert portfolio_result["adaptive_consistency"] == adaptive_strategy["consistency"]
assert portfolio_result["adaptive_summary"] == adaptive_strategy["summary"]

print("")
print("DOWNSTREAM BOUNDARY: PASS")

print("")
print("===== PHASE 7-4-12 SEMANTIC CONTRACT PASS =====")
