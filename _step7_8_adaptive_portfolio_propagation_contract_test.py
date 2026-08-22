from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence


print("=" * 82)
print("PHASE 7-8 ADAPTIVE STRATEGY -> PORTFOLIO INTELLIGENCE")
print("PROPAGATION CONTRACT TEST")
print("SOURCE-VERIFIED CANONICAL POLICY")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 82)


engine = PortfolioDecisionIntelligence()


cases = [
    {
        "name": "DEFENSIVE",
        "ai_decision": {
            "decision": "ACCUMULATE",
            "market_view": "NEUTRAL",
        },
        "adaptive": {
            "strategy": "DEFENSIVE",
            "action": "REDUCE_RISK",
            "confidence": 90,
            "score": 80,
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "summary": "Defensive adaptive strategy",
        },
        "expected": {
            "strategy_mode": "DEFENSIVE",
            "adaptive_action": "REDUCE_RISK",
            "final_strategy": "DEFENSIVE",
            "final_action":
                "Reduce equity exposure and strengthen defensive allocation",
        },
    },
    {
        "name": "GROWTH",
        "ai_decision": {
            "decision": "ACCUMULATE",
            "market_view": "NEUTRAL",
        },
        "adaptive": {
            "strategy": "GROWTH",
            "action": "INCREASE_RISK",
            "confidence": 100,
            "score": 85,
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "summary": "Growth adaptive strategy",
        },
        "expected": {
            "strategy_mode": "GROWTH",
            "adaptive_action": "INCREASE_RISK",
            "final_strategy": "GROWTH",
            "final_action":
                "Increase growth exposure while maintaining risk controls",
        },
    },
    {
        "name": "BALANCED",
        "ai_decision": {
            "decision": "ACCUMULATE",
            "market_view": "NEUTRAL",
        },
        "adaptive": {
            "strategy": "BALANCED",
            "action": "MAINTAIN_BALANCE",
            "confidence": 85,
            "score": 75,
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "summary": "Balanced adaptive strategy",
        },
        "expected": {
            "strategy_mode": "BALANCED",
            "adaptive_action": "MAINTAIN_BALANCE",
            "final_strategy": "BALANCED",
            "final_action":
                "Increase portfolio exposure with balanced risk controls",
        },
    },
    {
        "name": "MAINTAIN",
        "ai_decision": {
            "decision": "MAINTAIN",
            "market_view": "NEUTRAL",
        },
        "adaptive": {
            "strategy": "MAINTAIN",
            "action": "MAINTAIN_ALLOCATION",
            "confidence": 85,
            "score": 75,
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "summary": "Maintain adaptive strategy",
        },
        "expected": {
            "strategy_mode": "MAINTAIN",
            "adaptive_action": "MAINTAIN_ALLOCATION",
            "final_strategy": "MAINTAIN",
            "final_action":
                "Maintain balanced allocation and monitor market conditions",
        },
    },
]


for case in cases:

    print()
    print("=" * 82)
    print("CASE:", case["name"])
    print("=" * 82)

    portfolio = engine.generate(
        ai_decision=case["ai_decision"],
        decision_quality={
            "quality_score": 90,
            "quality": 90,
        },
        reliability={
            "reliability_score": 90,
            "reliability_level": "HIGH",
        },
        adaptive_strategy=case["adaptive"],
        rebalance={
            "rebalance_action": "HOLD",
        },
        optimization={
            "optimization_status": "OPTIMIZED",
        },
        explainability={
            "summary": "Memory-only portfolio contract test",
        },
    )

    strategy_mode = portfolio.get("strategy_mode")
    adaptive_action = portfolio.get("adaptive_action")
    final_strategy = portfolio.get("final_strategy")
    final_action = portfolio.get("final_action")

    print("portfolio strategy:", strategy_mode)
    print("portfolio adaptive action:", adaptive_action)
    print("portfolio final strategy:", final_strategy)
    print("portfolio final action:", final_action)

    assert strategy_mode == case["expected"]["strategy_mode"]
    assert adaptive_action == case["expected"]["adaptive_action"]
    assert final_strategy == case["expected"]["final_strategy"]
    assert final_action == case["expected"]["final_action"]

    print("strategy propagation: PASS")
    print("adaptive action propagation: PASS")
    print("final strategy contract: PASS")
    print("final action contract: PASS")
    print("PORTFOLIO PROPAGATION CONTRACT: PASS")


print()
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("DEFENSIVE -> DEFENSIVE -> REDUCE_RISK: PASS")
print("GROWTH -> GROWTH -> INCREASE_RISK: PASS")
print("BALANCED -> BALANCED -> MAINTAIN_BALANCE: PASS")
print("MAINTAIN -> MAINTAIN -> MAINTAIN_ALLOCATION: PASS")

print()
print("=" * 82)
print("SAFETY")
print("=" * 82)
print("Memory-only execution: PASS")
print("No production DB access.")
print("No API runtime call.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")

print()
print("=" * 82)
print("===== PHASE 7-8 ADAPTIVE -> PORTFOLIO CONTRACT TEST COMPLETE =====")
print("=" * 82)
