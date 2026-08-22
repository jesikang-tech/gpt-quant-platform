from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence

print("===== PHASE 7-4-18 ADAPTIVE → PORTFOLIO SEMANTIC CONTRACT =====")

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
    "summary": "Phase 7-4-18 semantic contract",
}

result = PortfolioDecisionIntelligence().generate(
    ai_decision={
        "decision": "MAINTAIN",
        "market_view": "NEUTRAL",
        "confidence": 90,
    },
    decision_quality={
        "quality_score": 85,
        "quality": "GOOD",
    },
    reliability={
        "reliability_score": 90,
        "reliability": "UNKNOWN",
    },
    adaptive_strategy=adaptive_strategy,
    rebalance={
        "action": "HOLD",
        "score": 80,
    },
    optimization={
        "status": "UNKNOWN",
        "score": 82,
    },
    explainability={
        "summary": "Phase 7-4-18 semantic contract",
    },
)

print()
print("===== RESULT =====")
print(result)

print()
print("===== CONTRACT ASSERTIONS =====")

assert result["strategy_mode"] == "MAINTAIN"
print("strategy preservation: PASS")

assert result["adaptive_action"] == "MAINTAIN_ALLOCATION"
print("adaptive action preservation: PASS")

assert result["adaptive_confidence"] == 100
print("adaptive confidence preservation: PASS")

assert result["adaptive_score"] == 85
print("adaptive score preservation: PASS")

assert result["adaptive_direction"] == "STABLE"
print("direction preservation: PASS")

assert result["adaptive_stability"] == "HIGH"
print("stability preservation: PASS")

assert result["adaptive_momentum"] == "NEUTRAL"
print("momentum preservation: PASS")

assert result["adaptive_grade_stability"] == "STABLE"
print("grade stability preservation: PASS")

assert result["adaptive_consistency"] == "HIGH"
print("consistency preservation: PASS")

assert result["decision_alignment"] == "ALIGNED"
print("decision alignment: PASS")

assert result["decision_consistency"] == "CONSISTENT"
print("decision consistency: PASS")

assert result["final_strategy"] == "MAINTAIN"
print("final strategy preservation: PASS")

assert result["rebalance_action"] == "HOLD"
print("rebalance boundary: PASS")

assert result["adaptive_override"] is False
print("adaptive override boundary: PASS")

print()
print("===== PHASE 7-4-18 SEMANTIC CONTRACT PASS =====")
