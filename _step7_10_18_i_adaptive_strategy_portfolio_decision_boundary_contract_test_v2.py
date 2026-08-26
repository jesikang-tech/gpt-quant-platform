"""
PHASE 7-10-18-I
ADAPTIVE STRATEGY
-> PORTFOLIO DECISION INTELLIGENCE
BOUNDARY CONTRACT TEST V2

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence,
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
        "summary": "Source-verified test summary.",
    }


def run_case_defensive_override(engine):
    print("=" * 82)
    print("CASE: DEFENSIVE -> OVERRIDE")
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

    result = engine.generate(
        base_ai_decision(),
        base_decision_quality(),
        base_reliability(),
        adaptive,
        base_rebalance(),
        base_optimization(),
        base_explainability(),
    )

    print(result)

    assert_equal(
        result["strategy_mode"],
        "DEFENSIVE",
        "DEFENSIVE -> strategy mode",
    )
    assert_equal(
        result["adaptive_action"],
        "REDUCE_RISK",
        "DEFENSIVE -> adaptive action",
    )
    assert_equal(
        result["adaptive_learning_required"],
        True,
        "DEFENSIVE -> adaptive learning",
    )
    assert_equal(
        result["final_strategy"],
        "DEFENSIVE",
        "DEFENSIVE -> final strategy",
    )
    assert_equal(
        result["adaptive_override"],
        True,
        "DEFENSIVE -> override",
    )
    assert_equal(
        result["final_action"],
        "Reduce equity exposure "
        "and strengthen defensive allocation",
        "DEFENSIVE -> final action",
    )


def run_case_cautious_override(engine):
    print("=" * 82)
    print("CASE: CAUTIOUS -> EXPOSURE LIMIT")
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

    result = engine.generate(
        base_ai_decision(),
        base_decision_quality(),
        base_reliability(),
        adaptive,
        base_rebalance(),
        base_optimization(),
        base_explainability(),
    )

    print(result)

    assert_equal(
        result["strategy_mode"],
        "CAUTIOUS",
        "CAUTIOUS -> strategy mode",
    )
    assert_equal(
        result["adaptive_action"],
        "LIMIT_EXPOSURE",
        "CAUTIOUS -> adaptive action",
    )
    assert_equal(
        result["final_strategy"],
        "CAUTIOUS",
        "CAUTIOUS -> final strategy",
    )
    assert_equal(
        result["adaptive_override"],
        True,
        "CAUTIOUS -> override",
    )
    assert_equal(
        result["final_action"],
        "Limit portfolio exposure "
        "and monitor risk conditions closely",
        "CAUTIOUS -> final action",
    )


def run_case_accumulate_growth(engine):
    print("=" * 82)
    print("CASE: ACCUMULATE + GROWTH")
    print("=" * 82)

    ai_decision = {
        "decision": "ACCUMULATE",
        "market_view": "BULLISH",
        "confidence": 92,
    }

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

    result = engine.generate(
        ai_decision,
        base_decision_quality(),
        base_reliability(),
        adaptive,
        base_rebalance(),
        base_optimization(),
        base_explainability(),
    )

    print(result)

    assert_equal(
        result["strategy_mode"],
        "GROWTH",
        "ACCUMULATE GROWTH -> strategy mode",
    )
    assert_equal(
        result["adaptive_action"],
        "INCREASE_RISK",
        "ACCUMULATE GROWTH -> adaptive action",
    )
    assert_equal(
        result["final_strategy"],
        "GROWTH",
        "ACCUMULATE GROWTH -> final strategy",
    )
    assert_equal(
        result["adaptive_override"],
        False,
        "ACCUMULATE GROWTH -> no override",
    )
    assert_equal(
        result["final_action"],
        "Increase growth exposure "
        "while maintaining risk controls",
        "ACCUMULATE GROWTH -> final action",
    )


def run_case_maintain_monitor(engine):
    print("=" * 82)
    print("CASE: MAINTAIN + MONITOR")
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

    result = engine.generate(
        base_ai_decision(),
        base_decision_quality(),
        base_reliability(),
        adaptive,
        base_rebalance(),
        base_optimization(),
        base_explainability(),
    )

    print(result)

    assert_equal(
        result["strategy_mode"],
        "MONITOR",
        "MAINTAIN MONITOR -> strategy mode",
    )
    assert_equal(
        result["adaptive_action"],
        "MONITOR_CLOSELY",
        "MAINTAIN MONITOR -> adaptive action",
    )
    assert_equal(
        result["final_strategy"],
        "MONITOR",
        "MAINTAIN MONITOR -> final strategy",
    )
    assert_equal(
        result["adaptive_override"],
        False,
        "MAINTAIN MONITOR -> no override",
    )
    assert_equal(
        result["final_action"],
        "Maintain current allocation "
        "and monitor decision conditions closely",
        "MAINTAIN MONITOR -> final action",
    )


def run_case_maintain_growth(engine):
    print("=" * 82)
    print("CASE: MAINTAIN + GROWTH")
    print("=" * 82)

    adaptive = {
        "strategy": "GROWTH",
        "action": "INCREASE_RISK",
        "confidence": 80,
        "score": 75,
        "direction": "STABLE",
        "stability": "MEDIUM",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "MEDIUM",
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 0.9,
        "adaptive_learning_required": False,
        "summary": "Growth learning signal.",
    }

    result = engine.generate(
        base_ai_decision(),
        base_decision_quality(),
        base_reliability(),
        adaptive,
        base_rebalance(),
        base_optimization(),
        base_explainability(),
    )

    print(result)

    assert_equal(
        result["strategy_mode"],
        "GROWTH",
        "MAINTAIN GROWTH -> strategy mode",
    )
    assert_equal(
        result["final_strategy"],
        "GROWTH",
        "MAINTAIN GROWTH -> final strategy",
    )
    assert_equal(
        result["adaptive_override"],
        False,
        "MAINTAIN GROWTH -> no override",
    )
    assert_equal(
        result["final_action"],
        "Gradually increase growth exposure "
        "while monitoring market conditions",
        "MAINTAIN GROWTH -> final action",
    )


def run_case_learning_propagation(engine):
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

    result = engine.generate(
        base_ai_decision(),
        base_decision_quality(),
        base_reliability(),
        adaptive,
        base_rebalance(),
        base_optimization(),
        base_explainability(),
    )

    print(result)

    assert_equal(
        result["outcome_learning_signal"],
        "NEGATIVE",
        "LEARNING -> signal propagation",
    )
    assert_equal(
        result["outcome_learning_signal_strength"],
        0.9,
        "LEARNING -> signal strength propagation",
    )
    assert_equal(
        result["adaptive_learning_required"],
        True,
        "LEARNING -> adaptive requirement propagation",
    )


def run_case_missing_adaptive_strategy(engine):
    print("=" * 82)
    print("CASE: MISSING_ADAPTIVE_STRATEGY -> DEFAULT")
    print("=" * 82)

    result = engine.generate(
        base_ai_decision(),
        base_decision_quality(),
        base_reliability(),
        {},
        base_rebalance(),
        base_optimization(),
        base_explainability(),
    )

    print(result)

    assert_equal(
        result["strategy_mode"],
        "BALANCED",
        "MISSING adaptive -> default strategy",
    )
    assert_equal(
        result["adaptive_action"],
        "MONITOR_CLOSELY",
        "MISSING adaptive -> default action",
    )
    assert_equal(
        result["final_strategy"],
        "BALANCED",
        "MISSING adaptive -> final strategy",
    )


def main():
    print("=" * 82)
    print("PHASE 7-10-18-I")
    print("ADAPTIVE STRATEGY")
    print("-> PORTFOLIO DECISION INTELLIGENCE")
    print("BOUNDARY CONTRACT TEST V2")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    engine = PortfolioDecisionIntelligence()

    run_case_defensive_override(engine)
    run_case_cautious_override(engine)
    run_case_accumulate_growth(engine)
    run_case_maintain_monitor(engine)
    run_case_maintain_growth(engine)
    run_case_learning_propagation(engine)
    run_case_missing_adaptive_strategy(engine)

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
    print("Actual Outcome data exists only in memory test dictionaries.")

    print("")
    print("=" * 82)
    print("===== PHASE 7-10-18-I CONTRACT TEST V2 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()
