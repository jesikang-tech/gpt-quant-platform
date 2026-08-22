from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence
import inspect

print("===== PHASE 7-4-18 DISCOVERY 2 ACTUAL SIGNATURE INPUT =====")
print("===== ADAPTIVE STRATEGY → PORTFOLIO DECISION INTELLIGENCE =====")
print()

engine = PortfolioDecisionIntelligence()
signature = inspect.signature(engine.generate)

print("===== SIGNATURE =====")
print(signature)

print()
print("===== REQUIRED INPUTS =====")
for name, parameter in signature.parameters.items():
    if name == "self":
        continue
    print(f"{name}: required={parameter.default is inspect.Parameter.empty}")

print()
print("===== MINIMUM SEMANTIC INPUTS =====")

ai_decision = {
    "decision": "MAINTAIN",
    "market_view": "NEUTRAL",
    "confidence": 90,
}

decision_quality = {
    "quality_score": 85,
    "quality": "GOOD",
}

reliability = {
    "reliability_score": 90,
    "reliability": "UNKNOWN",
}

adaptive_strategy = {
    "strategy": "MAINTAIN",
    "action": "MAINTAIN_ALLOCATION",
    "confidence": 100,
    "score": 85,
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "outcome_learning_signal": "NONE",
    "outcome_learning_signal_strength": 0.0,
    "adaptive_learning_required": False,
    "summary": "Phase 7-4-18 downstream boundary test",
}

rebalance = {
    "action": "HOLD",
    "score": 80,
}

optimization = {
    "status": "UNKNOWN",
    "score": 82,
}

explainability = {
    "summary": "Phase 7-4-18 downstream boundary test",
}

inputs = {
    "ai_decision": ai_decision,
    "decision_quality": decision_quality,
    "reliability": reliability,
    "adaptive_strategy": adaptive_strategy,
    "rebalance": rebalance,
    "optimization": optimization,
    "explainability": explainability,
}

for key, value in inputs.items():
    print(f"{key}: {value}")

print()
print("===== GENERATE =====")

result = engine.generate(**inputs)

print(result)

print()
print("===== ADAPTIVE VALUES AT DOWNSTREAM BOUNDARY =====")

for key in [
    "strategy_mode",
    "adaptive_action",
    "adaptive_confidence",
    "adaptive_score",
    "adaptive_direction",
    "adaptive_stability",
    "adaptive_momentum",
    "adaptive_grade_stability",
    "adaptive_consistency",
    "adaptive_summary",
]:
    print(f"{key}: {result.get(key)}")

print()
print("===== SEMANTIC PRESERVATION =====")

expected = {
    "strategy_mode": "MAINTAIN",
    "adaptive_action": "MAINTAIN_ALLOCATION",
    "adaptive_confidence": 100,
    "adaptive_score": 85,
    "adaptive_direction": "STABLE",
    "adaptive_stability": "HIGH",
    "adaptive_momentum": "NEUTRAL",
    "adaptive_grade_stability": "STABLE",
    "adaptive_consistency": "HIGH",
}

for key, value in expected.items():
    actual = result.get(key)
    print(
        f"{key}: "
        f"expected={value!r}, "
        f"actual={actual!r}, "
        f"{'PASS' if actual == value else 'REVIEW'}"
    )

print()
print("===== PHASE 7-4-18 DISCOVERY 2 ACTUAL SIGNATURE INPUT COMPLETE =====")
