from core.portfolio_intelligence_score import PortfolioIntelligenceScore
from core.decision_confidence_intelligence import DecisionConfidenceIntelligence
from core.ai_final_decision_integration import AIFinalDecisionIntegration

print("=" * 60)
print("PHASE 7-3-13 DOWNSTREAM VALUE PROPAGATION CONTRACT")
print("=" * 60)

decision_quality = {"quality_level": "GOOD"}
reliability = {"confidence": 90}

adaptive_strategy = {
    "strategy": "GROWTH",
    "action": "INCREASE_RISK",
    "confidence": 100,
    "strategy_score": 100
}

portfolio_result = PortfolioIntelligenceScore().calculate(
    decision_score=85,
    decision_quality=decision_quality,
    reliability=reliability,
    adaptive_strategy=adaptive_strategy,
    decision_consistency_score=95,
    rebalance={"rebalance_score": 88},
    optimization={"optimization_score": 92}
)

confidence_result = DecisionConfidenceIntelligence().calculate(
    decision_quality=decision_quality,
    reliability=reliability,
    adaptive_strategy=adaptive_strategy,
    decision_consistency_score=95,
    rebalance={"rebalance_score": 88},
    optimization={"optimization_score": 92}
)

final_result = AIFinalDecisionIntegration().integrate(
    intelligence={
        "decision": "BUY",
        "final_strategy": "GROWTH",
        "strategy_mode": "GROWTH",
        "adaptive_action": "INCREASE_RISK",
        "market_view": "BULLISH"
    },
    intelligence_score=portfolio_result,
    decision_confidence=confidence_result,
    decision_confidence_recommendation={
        "action": "PROCEED",
        "recommendation": "EXECUTE",
        "risk_level": "LOW",
        "monitoring": "STANDARD"
    },
    ai_decision_validation={
        "decision": "BUY",
        "action": "PROCEED",
        "validation_status": "VALID",
        "validation_score": 100,
        "risk_level": "LOW"
    },
    ai_decision_validation_action={
        "decision": "BUY",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "validation_status": "VALID",
        "validation_score": 100,
        "risk_level": "LOW"
    }
)

checks = {
    "decision": final_result.get("decision") == "BUY",
    "action": final_result.get("action") == "PROCEED",
    "execution_status": final_result.get("execution_status") == "AUTHORIZED",
    "confidence_score": final_result.get("confidence_score") == 92.0,
    "validation_status": final_result.get("validation_status") == "VALID",
    "validation_score": final_result.get("validation_score") == 100,
    "intelligence_score": final_result.get("intelligence_score") == 89.2,
    "intelligence_grade": final_result.get("intelligence_grade") == "A",
    "strategy": final_result.get("strategy") == "GROWTH",
    "adaptive_action": final_result.get("adaptive_action") == "INCREASE_RISK"
}

for name, passed in checks.items():
    print(f"{name}: {'PASS' if passed else 'FAIL'}")

print("")
print("=== FINAL RESULT ===")
print(final_result)

print("")
print(
    "OVERALL RESULT:",
    "PASS" if all(checks.values()) else "FAIL"
)
print("=" * 60)

if not all(checks.values()):
    raise SystemExit(1)
