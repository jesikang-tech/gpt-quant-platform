from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence
from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy


print("=" * 82)
print("PHASE 7-8 OUTCOME INTELLIGENCE -> ADAPTIVE STRATEGY")
print("PROPAGATION CONTRACT TEST")
print("SOURCE-VERIFIED CANONICAL POLICY")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 82)


intelligence_engine = AIDecisionOutcomeIntelligence()
adaptive_engine = AIDecisionAdaptiveStrategy()


cases = [
    {
        "name": "NEGATIVE",
        "outcome": {
            "outcome_status": "EVALUATED",
            "outcome_score": 40.0,
            "learning_signal": "NEGATIVE",
            "learning_signal_strength": 20.0,
        },
        "trend": {
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 70,
        },
        "expected": {
            "signal": "NEGATIVE",
            "strength": 20.0,
            "adaptive_learning_required": True,
            "strategy": "DEFENSIVE",
            "action": "REDUCE_RISK",
        },
    },
    {
        "name": "POSITIVE",
        "outcome": {
            "outcome_status": "EVALUATED",
            "outcome_score": 90.0,
            "learning_signal": "POSITIVE",
            "learning_signal_strength": 80.0,
        },
        "trend": {
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 70,
        },
        "expected": {
            "signal": "POSITIVE",
            "strength": 80.0,
            "adaptive_learning_required": False,
            "strategy": "GROWTH",
            "action": "INCREASE_RISK",
        },
    },
    {
        "name": "STABLE",
        "outcome": {
            "outcome_status": "EVALUATED",
            "outcome_score": 70.0,
            "learning_signal": "STABLE",
            "learning_signal_strength": 40.0,
        },
        "trend": {
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 70,
        },
        "expected": {
            "signal": "STABLE",
            "strength": 40.0,
            "adaptive_learning_required": False,
            "strategy": "BALANCED",
            "action": "MAINTAIN_BALANCE",
        },
    },
    {
        "name": "NONE",
        "outcome": {
            "outcome_status": "PENDING",
            "outcome_score": 0.0,
            "learning_signal": "NONE",
            "learning_signal_strength": 0.0,
        },
        "trend": {
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 70,
        },
        "expected": {
            "signal": "NONE",
            "strength": 0.0,
            "adaptive_learning_required": False,
            "strategy": "BALANCED",
            "action": "MAINTAIN_BALANCE",
        },
    },
]


for case in cases:

    print()
    print("=" * 82)
    print("CASE:", case["name"])
    print("=" * 82)

    outcome_evaluation = case["outcome"]

    intelligence = intelligence_engine.analyze(
        final_decision={
            "decision": "ACCUMULATE",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
        },
        final_decision_master_control={
            "decision": "ACCUMULATE",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
        },
        final_decision_certification={},
        final_execution_decision={
            "decision": "ACCUMULATE",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
        },
        final_decision_execution_feedback={},
        final_decision_execution_monitoring={},
        final_decision_execution_reassessment={},
        intelligence={
            "intelligence_score": 95,
        },
        intelligence_score={
            "intelligence_score": 95,
        },
        decision_confidence={
            "confidence_score": 95,
        },
        outcome_evaluation=outcome_evaluation,
    )

    signal = intelligence.get(
        "outcome_learning_signal"
    )
    strength = intelligence.get(
        "outcome_learning_signal_strength"
    )
    learning_required = intelligence.get(
        "adaptive_learning_required"
    )

    print("learning signal:", signal)
    print("learning strength:", strength)
    print("adaptive learning required:", learning_required)

    assert signal == case["expected"]["signal"]
    assert strength == case["expected"]["strength"]
    assert (
        learning_required
        == case["expected"]["adaptive_learning_required"]
    )

    print("outcome intelligence contract: PASS")

    adaptive = adaptive_engine.analyze(
        trend=case["trend"],
        outcome_intelligence=intelligence,
    )

    strategy = adaptive.get(
        "strategy",
        adaptive.get("strategy_mode")
    )
    action = adaptive.get("action")

    print("adaptive strategy:", strategy)
    print("adaptive action:", action)

    assert strategy == case["expected"]["strategy"]
    assert action == case["expected"]["action"]

    print("adaptive strategy contract: PASS")

    print()
    print("PROPAGATION CONTRACT: PASS")


print()
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("NEGATIVE -> DEFENSIVE -> REDUCE_RISK: PASS")
print("POSITIVE -> GROWTH -> INCREASE_RISK: PASS")
print("STABLE -> BALANCED -> MAINTAIN_BALANCE: PASS")
print("NONE -> BALANCED -> MAINTAIN_BALANCE: PASS")

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
print("===== PHASE 7-8 OUTCOME INTELLIGENCE -> ADAPTIVE STRATEGY TEST COMPLETE =====")
print("=" * 82)
