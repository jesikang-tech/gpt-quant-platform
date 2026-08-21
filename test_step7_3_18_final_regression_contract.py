print("=" * 60)
print("PHASE 7-3-18 FINAL REGRESSION CONTRACT")
print("=" * 60)

from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy
from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence
from core.portfolio_intelligence_score import PortfolioIntelligenceScore
from core.decision_confidence_intelligence import DecisionConfidenceIntelligence
from core.ai_final_decision_integration import AIFinalDecisionIntegration


print("")
print("=== STEP 1 ADAPTIVE STRATEGY ===")

trend = {
    "direction": "UP",
    "stability": "HIGH",
    "momentum": "POSITIVE",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}

adaptive = AIDecisionAdaptiveStrategy().analyze(trend)

print("strategy:", adaptive.get("strategy"))
print("action:", adaptive.get("action"))
print("confidence:", adaptive.get("confidence"))
print("score:", adaptive.get("score"))


print("")
print("=== STEP 2 PORTFOLIO DECISION ===")

portfolio_decision = PortfolioDecisionIntelligence().generate(
    {
        "decision": "ACCUMULATE",
        "market_view": "BULLISH",
        "confidence": 92,
    },
    {
        "quality_level": "GOOD",
        "recent_trend": "STABLE",
    },
    {
        "confidence": 90,
        "reliability_level": "HIGH",
    },
    adaptive,
    {
        "rebalance_action": "HOLD",
    },
    {
        "optimization_status": "OPTIMIZED",
    },
    {
        "summary": "Portfolio intelligence summary.",
    },
)

print("strategy_mode:", portfolio_decision.get("strategy_mode"))
print("adaptive_action:", portfolio_decision.get("adaptive_action"))
print("final_strategy:", portfolio_decision.get("final_strategy"))


print("")
print("=== STEP 3 PORTFOLIO INTELLIGENCE SCORE ===")

portfolio_score = PortfolioIntelligenceScore().calculate(
    decision_score=85,
    decision_quality={"quality_level": "GOOD"},
    reliability={"confidence": 90},
    adaptive_strategy=adaptive,
    decision_consistency_score=95,
    rebalance={"rebalance_score": 88},
    optimization={"optimization_score": 92},
)

print("intelligence_score:", portfolio_score.get("intelligence_score"))
print("grade:", portfolio_score.get("grade"))
print(
    "adaptive_strategy:",
    portfolio_score.get("components", {}).get("adaptive_strategy"),
)


print("")
print("=== STEP 4 DECISION CONFIDENCE ===")

confidence = DecisionConfidenceIntelligence().calculate(
    decision_quality={"quality_level": "GOOD"},
    reliability={"confidence": 90},
    adaptive_strategy=adaptive,
    decision_consistency_score=95,
    rebalance={"rebalance_score": 88},
    optimization={"optimization_score": 92},
)

print("confidence_score:", confidence.get("confidence_score"))
print("grade:", confidence.get("confidence_grade"))
print(
    "adaptive_strategy:",
    confidence.get("components", {}).get("adaptive_strategy"),
)


print("")
print("=== STEP 5 FINAL DECISION ===")

final_decision = AIFinalDecisionIntegration().integrate(
    intelligence=portfolio_decision,
    intelligence_score=portfolio_score,
    decision_confidence=confidence,
    ai_decision_validation={
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "validation_status": "VALID",
        "validation_score": 100,
        "risk_level": "LOW",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
        "reliability": "HIGH",
        "optimization_status": "OPTIMIZED",
    },
    ai_decision_validation_action={
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "execution_status": "AUTHORIZED",
        "validation_status": "VALID",
        "validation_score": 100,
        "risk_level": "LOW",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
        "reliability": "HIGH",
        "optimization_status": "OPTIMIZED",
    },
    decision_confidence_recommendation={
        "action": "PROCEED",
        "recommendation": "EXECUTE",
        "risk_level": "LOW",
        "monitoring": "STANDARD",
    },
)

print(final_decision)


print("")
print("=== FINAL REGRESSION CHECK ===")

checks = {
    "adaptive strategy": adaptive.get("strategy") == "GROWTH",
    "adaptive action": adaptive.get("action") == "INCREASE_RISK",
    "portfolio strategy": portfolio_decision.get("strategy_mode") == "GROWTH",
    "portfolio adaptive action": (
        portfolio_decision.get("adaptive_action") == "INCREASE_RISK"
    ),
    "portfolio final strategy": (
        portfolio_decision.get("final_strategy") == "GROWTH"
    ),
    "intelligence score": (
        portfolio_score.get("intelligence_score") == 89.2
    ),
    "intelligence adaptive component": (
        portfolio_score.get("components", {}).get("adaptive_strategy") == 100
    ),
    "confidence score": (
        confidence.get("confidence_score") == 92.0
    ),
    "confidence adaptive component": (
        confidence.get("components", {}).get("adaptive_strategy") == 100
    ),
    "final strategy": final_decision.get("strategy") == "GROWTH",
    "final adaptive action": (
        final_decision.get("adaptive_action") == "INCREASE_RISK"
    ),
    "final intelligence score": (
        final_decision.get("intelligence_score") == 89.2
    ),
    "final confidence score": (
        final_decision.get("confidence_score") == 92.0
    ),
}

all_pass = True

for name, result in checks.items():
    status = "PASS" if result else "FAIL"
    print(f"{name}: {status}")
    if not result:
        all_pass = False

print("")
print(
    "OVERALL RESULT:",
    "PASS" if all_pass else "FAIL",
)
print("=" * 60)

if not all_pass:
    raise AssertionError("Phase 7-3-18 final regression failed")
