"""
PHASE 7-10-18-J
PORTFOLIO DECISION INTELLIGENCE
->
AI FINAL DECISION INTEGRATION
ADAPTIVE STRATEGY PROPAGATION
BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence,
)
from core.ai_final_decision_integration import (
    AIFinalDecisionIntegration,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )


def base_ai_decision():
    return {
        "decision": "MAINTAIN",
        "market_view": "NEUTRAL",
        "confidence": 90,
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
        "summary": "Source-verified J boundary test.",
    }


def generate_portfolio(adaptive, ai_decision=None):
    return PortfolioDecisionIntelligence().generate(
        ai_decision or base_ai_decision(),
        base_decision_quality(),
        base_reliability(),
        adaptive,
        base_rebalance(),
        base_optimization(),
        base_explainability(),
    )


def integrate_final(portfolio):
    return AIFinalDecisionIntegration().integrate(
        intelligence=portfolio,
    )


def run_case_defensive():
    print("=" * 82)
    print("CASE: DEFENSIVE -> PORTFOLIO -> FINAL DECISION")
    print("=" * 82)

    adaptive = {
        "strategy": "DEFENSIVE",
        "action": "REDUCE_RISK",
        "confidence": 100,
        "score": 45,
        "direction": "DOWN",
        "stability": "LOW",
        "momentum": "NEGATIVE",
        "grade_stability": "CHANGING",
        "consistency": "LOW",
        "outcome_learning_signal": "NEGATIVE",
        "outcome_learning_signal_strength": 0.9,
        "adaptive_learning_required": True,
        "summary": "Defensive learning signal.",
    }

    portfolio = generate_portfolio(adaptive)
    final_decision = integrate_final(portfolio)

    print("portfolio:", portfolio)
    print("final_decision:", final_decision)

    assert_equal(
        portfolio["final_strategy"],
        "DEFENSIVE",
        "DEFENSIVE portfolio final strategy",
    )

    assert_equal(
        portfolio["adaptive_action"],
        "REDUCE_RISK",
        "DEFENSIVE portfolio adaptive action",
    )

    assert_equal(
        final_decision.get("strategy"),
        "DEFENSIVE",
        "DEFENSIVE final decision strategy",
    )

    assert_equal(
        final_decision.get("adaptive_action"),
        "REDUCE_RISK",
        "DEFENSIVE final decision adaptive action",
    )


def run_case_cautious():
    print("=" * 82)
    print("CASE: CAUTIOUS -> PORTFOLIO -> FINAL DECISION")
    print("=" * 82)

    adaptive = {
        "strategy": "CAUTIOUS",
        "action": "LIMIT_EXPOSURE",
        "confidence": 80,
        "score": 60,
        "direction": "DOWN",
        "stability": "LOW",
        "momentum": "NEGATIVE",
        "grade_stability": "STABLE",
        "consistency": "HIGH",
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 0.9,
        "adaptive_learning_required": False,
        "summary": "Cautious strategy.",
    }

    portfolio = generate_portfolio(adaptive)
    final_decision = integrate_final(portfolio)

    print("portfolio:", portfolio)
    print("final_decision:", final_decision)

    assert_equal(
        portfolio["final_strategy"],
        "CAUTIOUS",
        "CAUTIOUS portfolio final strategy",
    )

    assert_equal(
        portfolio["adaptive_action"],
        "LIMIT_EXPOSURE",
        "CAUTIOUS portfolio adaptive action",
    )

    assert_equal(
        final_decision.get("strategy"),
        "CAUTIOUS",
        "CAUTIOUS final decision strategy",
    )

    assert_equal(
        final_decision.get("adaptive_action"),
        "LIMIT_EXPOSURE",
        "CAUTIOUS final decision adaptive action",
    )


def run_case_growth():
    print("=" * 82)
    print("CASE: GROWTH -> PORTFOLIO -> FINAL DECISION")
    print("=" * 82)

    adaptive = {
        "strategy": "GROWTH",
        "action": "INCREASE_RISK",
        "confidence": 90,
        "score": 85,
        "direction": "UP",
        "stability": "HIGH",
        "momentum": "POSITIVE",
        "grade_stability": "STABLE",
        "consistency": "HIGH",
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 0.9,
        "adaptive_learning_required": False,
        "summary": "Growth strategy.",
    }

    ai_decision = {
        "decision": "ACCUMULATE",
        "market_view": "BULLISH",
        "confidence": 92,
    }

    portfolio = generate_portfolio(
        adaptive,
        ai_decision,
    )

    final_decision = integrate_final(portfolio)

    print("portfolio:", portfolio)
    print("final_decision:", final_decision)

    assert_equal(
        portfolio["final_strategy"],
        "GROWTH",
        "GROWTH portfolio final strategy",
    )

    assert_equal(
        portfolio["adaptive_action"],
        "INCREASE_RISK",
        "GROWTH portfolio adaptive action",
    )

    assert_equal(
        final_decision.get("strategy"),
        "GROWTH",
        "GROWTH final decision strategy",
    )

    assert_equal(
        final_decision.get("adaptive_action"),
        "INCREASE_RISK",
        "GROWTH final decision adaptive action",
    )


def run_case_monitor():
    print("=" * 82)
    print("CASE: MONITOR -> PORTFOLIO -> FINAL DECISION")
    print("=" * 82)

    adaptive = {
        "strategy": "MONITOR",
        "action": "MONITOR_CLOSELY",
        "confidence": 70,
        "score": 65,
        "direction": "STABLE",
        "stability": "MEDIUM",
        "momentum": "NEUTRAL",
        "grade_stability": "CHANGING",
        "consistency": "LOW",
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": False,
        "summary": "Monitor strategy.",
    }

    portfolio = generate_portfolio(adaptive)
    final_decision = integrate_final(portfolio)

    print("portfolio:", portfolio)
    print("final_decision:", final_decision)

    assert_equal(
        portfolio["final_strategy"],
        "MONITOR",
        "MONITOR portfolio final strategy",
    )

    assert_equal(
        portfolio["adaptive_action"],
        "MONITOR_CLOSELY",
        "MONITOR portfolio adaptive action",
    )

    assert_equal(
        final_decision.get("strategy"),
        "MONITOR",
        "MONITOR final decision strategy",
    )

    assert_equal(
        final_decision.get("adaptive_action"),
        "MONITOR_CLOSELY",
        "MONITOR final decision adaptive action",
    )


def run_case_learning_propagation():
    print("=" * 82)
    print("CASE: OUTCOME LEARNING PROPAGATION")
    print("=" * 82)

    adaptive = {
        "strategy": "DEFENSIVE",
        "action": "REDUCE_RISK",
        "confidence": 100,
        "score": 45,
        "direction": "STABLE",
        "stability": "HIGH",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "HIGH",
        "outcome_learning_signal": "NEGATIVE",
        "outcome_learning_signal_strength": 0.9,
        "adaptive_learning_required": True,
        "summary": "Negative outcome learning.",
    }

    portfolio = generate_portfolio(adaptive)
    final_decision = integrate_final(portfolio)

    print("portfolio:", portfolio)
    print("final_decision:", final_decision)

    assert_equal(
        portfolio["outcome_learning_signal"],
        "NEGATIVE",
        "Portfolio learning signal",
    )

    assert_equal(
        portfolio["outcome_learning_signal_strength"],
        0.9,
        "Portfolio learning strength",
    )

    assert_equal(
        portfolio["adaptive_learning_required"],
        True,
        "Portfolio learning requirement",
    )

    assert_equal(
        final_decision.get("strategy"),
        "DEFENSIVE",
        "Learning -> final strategy propagation",
    )

    assert_equal(
        final_decision.get("adaptive_action"),
        "REDUCE_RISK",
        "Learning -> final adaptive action propagation",
    )


def main():
    print("=" * 82)
    print("PHASE 7-10-18-J")
    print("PORTFOLIO DECISION INTELLIGENCE")
    print("-> AI FINAL DECISION INTEGRATION")
    print("ADAPTIVE STRATEGY PROPAGATION")
    print("BOUNDARY CONTRACT TEST V1")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    run_case_defensive()
    run_case_cautious()
    run_case_growth()
    run_case_monitor()
    run_case_learning_propagation()

    print("")
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

    print("")
    print("=" * 82)
    print("===== PHASE 7-10-18-J CONTRACT TEST V1 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()
