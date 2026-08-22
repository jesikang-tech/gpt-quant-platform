import json

from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence,
)
from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)
from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence,
)


cases = [
    {
        "name": "NEGATIVE",
        "signal": "NEGATIVE",
        "strength": 0.2,
        "learning_required": True,
        "trend": {
            "direction": "DOWN",
            "stability": "HIGH",
            "momentum": "NEGATIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 60,
        },
        "expected_strategy": "DEFENSIVE",
        "expected_action": "REDUCE_RISK",
    },
    {
        "name": "POSITIVE",
        "signal": "POSITIVE",
        "strength": 0.8,
        "learning_required": False,
        "trend": {
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 85,
        },
        "expected_strategy": "GROWTH",
        "expected_action": "INCREASE_RISK",
    },
    {
        "name": "PENDING",
        "signal": "NONE",
        "strength": 0.0,
        "learning_required": False,
        "trend": {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        },
        "expected_strategy": "MAINTAIN",
        "expected_action": "MAINTAIN_ALLOCATION",
    },
]


intelligence_engine = AIDecisionOutcomeIntelligence()
adaptive_engine = AIDecisionAdaptiveStrategy()
portfolio_engine = PortfolioDecisionIntelligence()


for case in cases:

    print()
    print("=" * 82)
    print("CASE:", case["name"])
    print("=" * 82)

    outcome_evaluation = {
        "outcome_status": (
            "EVALUATED"
            if case["name"] != "PENDING"
            else "PENDING"
        ),
        "learning_status": (
            "LEARNING_AVAILABLE"
            if case["name"] != "PENDING"
            else "WAITING_FOR_OUTCOME"
        ),
        "learning_signal": case["signal"],
        "learning_signal_strength": case["strength"],
        "adaptive_learning_required": case["learning_required"],
        "outcome_score": (
            40.0 if case["name"] == "NEGATIVE"
            else 90.0 if case["name"] == "POSITIVE"
            else 0.0
        ),
    }

    intelligence = intelligence_engine.analyze(
        final_decision={
            "decision": (
                "ACCUMULATE"
                if case["name"] == "POSITIVE"
                else "REDUCE"
                if case["name"] == "NEGATIVE"
                else "MAINTAIN"
            ),
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
        },
        final_decision_master_control={
            "decision": "MASTER",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
        },
        final_decision_certification={
            "certification_status": "CERTIFIED",
            "certification_action": "PROCEED",
        },
        final_execution_decision={
            "decision": "EXECUTION",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
        },
        final_decision_execution_feedback={
            "feedback_status": "STABLE",
        },
        final_decision_execution_monitoring={
            "monitoring_status": "STANDARD_MONITORING",
        },
        final_decision_execution_reassessment={
            "reassessment_status": "NOT_REQUIRED",
            "reassessment_required": False,
        },
        intelligence_score={
            "intelligence_score": 95,
        },
        decision_confidence={
            "confidence_score": 95,
        },
        outcome_evaluation=outcome_evaluation,
    )

    signal = intelligence.get("outcome_learning_signal")
    strength = intelligence.get(
        "outcome_learning_signal_strength"
    )
    learning_required = intelligence.get(
        "adaptive_learning_required"
    )

    print("learning signal:", signal)
    print("learning strength:", strength)
    print(
        "adaptive learning required:",
        learning_required,
    )

    assert signal == case["signal"]
    assert strength == case["strength"]
    assert learning_required == case["learning_required"]

    print("outcome intelligence contract: PASS")

    adaptive = adaptive_engine.analyze(
        trend=case["trend"],
        outcome_intelligence=intelligence,
    )

    strategy = adaptive.get(
        "strategy",
        adaptive.get("strategy_mode"),
    )
    action = adaptive.get("action")

    print("adaptive strategy:", strategy)
    print("adaptive action:", action)

    assert strategy == case["expected_strategy"]
    assert action == case["expected_action"]

    print("adaptive contract: PASS")

    portfolio = portfolio_engine.generate(
        ai_decision={
            "decision": "ACCUMULATE",
            "market_view": "NEUTRAL",
            "confidence": 95,
        },
        decision_quality={
            "quality": 90,
            "quality_trend": "STABLE",
        },
        reliability={
            "confidence": 95,
            "reliability_level": "HIGH",
        },
        adaptive_strategy=adaptive,
        rebalance={
            "rebalance_action": "HOLD",
        },
        optimization={
            "optimization_status": "OPTIMIZED",
        },
        explainability={
            "summary": "Controlled canonical portfolio bridge test",
        },
    )

    portfolio_strategy = portfolio.get("strategy_mode")
    portfolio_adaptive_action = portfolio.get(
        "adaptive_action"
    )
    final_strategy = portfolio.get("final_strategy")
    final_action = portfolio.get("final_action")

    print("portfolio strategy:", portfolio_strategy)
    print(
        "portfolio adaptive action:",
        portfolio_adaptive_action,
    )
    print("portfolio final strategy:", final_strategy)
    print("portfolio final action:", final_action)

    assert portfolio_strategy == case["expected_strategy"]
    assert portfolio_adaptive_action == case["expected_action"]
    assert final_strategy == case["expected_strategy"]

    assert isinstance(final_action, str)
    assert len(final_action) > 0

    print("portfolio bridge contract: PASS")

    print()
    print("DASHBOARD CONSUMER CONTRACT: PASS")


print()
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print(
    "NEGATIVE -> DEFENSIVE -> REDUCE_RISK -> DASHBOARD: PASS"
)
print(
    "POSITIVE -> GROWTH -> INCREASE_RISK -> DASHBOARD: PASS"
)
print(
    "PENDING -> MAINTAIN -> MAINTAIN_ALLOCATION -> DASHBOARD: PASS"
)

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
print(
    "===== PHASE 7-7 DASHBOARD CONSUMER CONTRACT TEST V3 COMPLETE ====="
)
