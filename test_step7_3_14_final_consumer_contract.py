from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence
)

print("=" * 60)
print("PHASE 7-3-14 FINAL CONSUMER CONTRACT")
print("=" * 60)

adaptive_strategy = {
    "strategy": "GROWTH",
    "action": "INCREASE_RISK",
    "confidence": 100,
    "score": 100,
    "direction": "UP",
    "stability": "HIGH",
    "momentum": "POSITIVE",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "summary": "Adaptive strategy is GROWTH."
}

result = PortfolioDecisionIntelligence().generate(
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

checks = {
    "strategy_mode": result.get("strategy_mode") == "GROWTH",
    "adaptive_action": result.get("adaptive_action") == "INCREASE_RISK",
    "adaptive_confidence": result.get("adaptive_confidence") == 100,
    "adaptive_score": result.get("adaptive_score") == 100,
    "adaptive_direction": result.get("adaptive_direction") == "UP",
    "adaptive_stability": result.get("adaptive_stability") == "HIGH",
    "adaptive_momentum": result.get("adaptive_momentum") == "POSITIVE",
    "adaptive_grade_stability": (
        result.get("adaptive_grade_stability") == "STABLE"
    ),
    "adaptive_consistency": (
        result.get("adaptive_consistency") == "HIGH"
    ),
    "decision_alignment": (
        result.get("decision_alignment") == "ALIGNED"
    ),
    "decision_consistency": (
        result.get("decision_consistency") == "CONSISTENT"
    ),
    "decision_consistency_score": (
        result.get("decision_consistency_score") == 100
    ),
    "final_strategy": result.get("final_strategy") == "GROWTH",
    "final_action": bool(result.get("final_action")),
}

print("")
print("=== ADAPTIVE STRATEGY CONSUMPTION ===")

for name in [
    "strategy_mode",
    "adaptive_action",
    "adaptive_confidence",
    "adaptive_score",
    "adaptive_direction",
    "adaptive_stability",
    "adaptive_momentum",
    "adaptive_grade_stability",
    "adaptive_consistency",
]:
    print(
        f"{name}: "
        f"{'PASS' if checks[name] else 'FAIL'}"
    )

print("")
print("=== FINAL STRATEGY PROPAGATION ===")

for name in [
    "decision_alignment",
    "decision_consistency",
    "decision_consistency_score",
    "final_strategy",
    "final_action",
]:
    print(
        f"{name}: "
        f"{'PASS' if checks[name] else 'FAIL'}"
    )

print("")
print("=== FINAL RESULT ===")
print(result)

overall = all(checks.values())

print("")
print(
    "OVERALL RESULT:",
    "PASS" if overall else "FAIL"
)
print("=" * 60)

if not overall:
    raise SystemExit(1)
