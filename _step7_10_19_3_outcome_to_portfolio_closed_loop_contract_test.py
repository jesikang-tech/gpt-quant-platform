"""
PHASE 7-10-19-3
OUTCOME EVALUATION
-> OUTCOME INTELLIGENCE
-> ADAPTIVE STRATEGY
-> PORTFOLIO DECISION INTELLIGENCE
CLOSED-LOOP BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_decision_outcome_evaluation import (
    AIDecisionOutcomeEvaluation,
)
from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence,
)
from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)
from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence,
)


evaluation_engine = AIDecisionOutcomeEvaluation()
outcome_intelligence_engine = AIDecisionOutcomeIntelligence()
adaptive_strategy_engine = AIDecisionAdaptiveStrategy()
portfolio_decision_engine = PortfolioDecisionIntelligence()


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def base_snapshot():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "strategy": "BALANCED",
        "snapshot_status": "COLLECTED",
        "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
    }


def base_final_decision():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
    }


def base_master_control():
    return {
        "decision": "MAINTAIN",
        "master_control_action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
        "master_control_status": "MASTER_READY",
    }


def base_certification():
    return {
        "certification_status": "CERTIFIED",
    }


def base_execution():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
    }


def base_feedback():
    return {
        "feedback_status": "STABLE",
    }


def base_monitoring():
    return {
        "monitoring_status": "STANDARD_MONITORING",
    }


def base_reassessment():
    return {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
    }


def base_intelligence():
    return {
        "intelligence_score": 90.0,
    }


def base_confidence():
    return {
        "confidence_score": 90.0,
    }


def base_decision_quality():
    return {
        "quality_score": 90,
    }


def base_reliability():
    return {
        "confidence": 90,
        "reliability_level": "HIGH",
    }


def base_rebalance():
    return {
        "rebalance_action": "HOLD",
    }


def base_optimization():
    return {
        "optimization_status": "OPTIMAL",
    }


def base_explainability():
    return {
        "summary": "Source-verified closed-loop test summary.",
    }


def build_closed_loop(portfolio_return, trend):
    evaluation = evaluation_engine.evaluate(
        outcome_snapshot=base_snapshot(),
        actual_outcome={
            "portfolio_return": portfolio_return,
            "market_response": "EVALUATED",
            "portfolio_response": "EVALUATED",
        },
    )

    intelligence = outcome_intelligence_engine.analyze(
        final_decision=base_final_decision(),
        final_decision_master_control=base_master_control(),
        final_decision_certification=base_certification(),
        final_execution_decision=base_execution(),
        final_decision_execution_feedback=base_feedback(),
        final_decision_execution_monitoring=base_monitoring(),
        final_decision_execution_reassessment=base_reassessment(),
        intelligence=base_intelligence(),
        intelligence_score=base_intelligence(),
        decision_confidence=base_confidence(),
        outcome_evaluation=evaluation,
    )

    adaptive_strategy = adaptive_strategy_engine.analyze(
        trend=trend,
        outcome_intelligence=intelligence,
    )

    portfolio_decision = portfolio_decision_engine.generate(
        {
            "decision": "MAINTAIN",
            "market_view": "NEUTRAL",
            "confidence": 90,
        },
        base_decision_quality(),
        base_reliability(),
        adaptive_strategy,
        base_rebalance(),
        base_optimization(),
        base_explainability(),
    )

    return (
        evaluation,
        intelligence,
        adaptive_strategy,
        portfolio_decision,
    )


growth_trend = {
    "direction": "STABLE",
    "stability": "MEDIUM",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "MEDIUM",
    "latest_score": 75,
}


print("=" * 82)
print("CASE: POSITIVE OUTCOME -> GROWTH -> PORTFOLIO DECISION")
print("=" * 82)

evaluation, intelligence, adaptive, portfolio = build_closed_loop(
    10.0,
    growth_trend,
)

print("evaluation:", evaluation)
print("intelligence:", intelligence)
print("adaptive_strategy:", adaptive)
print("portfolio_decision:", portfolio)

assert_equal(
    evaluation["learning_signal"],
    "POSITIVE",
    "POSITIVE -> evaluation signal",
)

assert_equal(
    intelligence["outcome_learning_signal"],
    "POSITIVE",
    "POSITIVE -> intelligence signal",
)

assert_equal(
    adaptive["outcome_learning_signal"],
    "POSITIVE",
    "POSITIVE -> adaptive signal",
)

assert_equal(
    adaptive["strategy"],
    "GROWTH",
    "POSITIVE -> adaptive strategy",
)

assert_equal(
    adaptive["action"],
    "INCREASE_RISK",
    "POSITIVE -> adaptive action",
)

assert_equal(
    portfolio["outcome_learning_signal"],
    "POSITIVE",
    "POSITIVE -> portfolio signal",
)

assert_equal(
    portfolio["outcome_learning_signal_strength"],
    100.0,
    "POSITIVE -> portfolio signal strength",
)

assert_equal(
    portfolio["adaptive_learning_required"],
    False,
    "POSITIVE -> portfolio learning requirement",
)

assert_equal(
    portfolio["strategy_mode"],
    "GROWTH",
    "POSITIVE -> portfolio strategy mode",
)

assert_equal(
    portfolio["final_strategy"],
    "GROWTH",
    "POSITIVE -> portfolio final strategy",
)

assert_equal(
    portfolio["adaptive_override"],
    False,
    "POSITIVE -> portfolio override",
)

assert_equal(
    portfolio["final_action"],
    "Gradually increase growth exposure "
    "while monitoring market conditions",
    "POSITIVE -> portfolio final action",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE OUTCOME -> DEFENSIVE -> PORTFOLIO OVERRIDE")
print("=" * 82)

evaluation, intelligence, adaptive, portfolio = build_closed_loop(
    -10.0,
    growth_trend,
)

print("evaluation:", evaluation)
print("intelligence:", intelligence)
print("adaptive_strategy:", adaptive)
print("portfolio_decision:", portfolio)

assert_equal(
    evaluation["learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> evaluation signal",
)

assert_equal(
    intelligence["outcome_learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> intelligence signal",
)

assert_equal(
    intelligence["learning_status"],
    "ADAPTIVE_LEARNING_REQUIRED",
    "NEGATIVE -> intelligence learning status",
)

assert_equal(
    intelligence["adaptive_learning_required"],
    True,
    "NEGATIVE -> intelligence adaptive requirement",
)

assert_equal(
    adaptive["outcome_learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> adaptive signal",
)

assert_equal(
    adaptive["adaptive_learning_required"],
    True,
    "NEGATIVE -> adaptive learning requirement",
)

assert_equal(
    adaptive["strategy"],
    "DEFENSIVE",
    "NEGATIVE -> adaptive strategy",
)

assert_equal(
    adaptive["action"],
    "REDUCE_RISK",
    "NEGATIVE -> adaptive action",
)

assert_equal(
    portfolio["outcome_learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> portfolio signal",
)

assert_equal(
    portfolio["adaptive_learning_required"],
    True,
    "NEGATIVE -> portfolio learning requirement",
)

assert_equal(
    portfolio["strategy_mode"],
    "DEFENSIVE",
    "NEGATIVE -> portfolio strategy mode",
)

assert_equal(
    portfolio["final_strategy"],
    "DEFENSIVE",
    "NEGATIVE -> portfolio final strategy",
)

assert_equal(
    portfolio["adaptive_override"],
    True,
    "NEGATIVE -> portfolio override",
)

assert_equal(
    portfolio["final_action"],
    "Reduce equity exposure "
    "and strengthen defensive allocation",
    "NEGATIVE -> portfolio final action",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-19-3 CLOSED-LOOP BOUNDARY COMPLETE =====")
print("=" * 82)
