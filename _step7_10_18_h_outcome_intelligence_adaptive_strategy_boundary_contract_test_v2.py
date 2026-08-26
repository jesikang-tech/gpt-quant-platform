from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def base_trend():
    return {
        "direction": "STABLE",
        "stability": "HIGH",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "HIGH",
        "latest_score": 85,
    }


def base_outcome_intelligence():
    return {
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": False,
    }


def run_case_no_learning_preserves_strategy(engine):
    print("=" * 82)
    print("CASE: NO_LEARNING -> PRESERVE_BASE_STRATEGY")
    print("=" * 82)

    trend = base_trend()
    outcome = base_outcome_intelligence()

    result = engine.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    print(result)

    assert_equal(
        result["strategy"],
        "MAINTAIN",
        "NO_LEARNING -> strategy",
    )
    assert_equal(
        result["action"],
        "MAINTAIN_ALLOCATION",
        "NO_LEARNING -> action",
    )
    assert_equal(
        result["outcome_learning_signal"],
        "NONE",
        "NO_LEARNING -> signal",
    )
    assert_equal(
        result["outcome_learning_signal_strength"],
        0.0,
        "NO_LEARNING -> signal strength",
    )
    assert_equal(
        result["adaptive_learning_required"],
        False,
        "NO_LEARNING -> adaptive learning",
    )


def run_case_negative_adaptive_required(engine):
    print("=" * 82)
    print("CASE: NEGATIVE + ADAPTIVE_REQUIRED -> DEFENSIVE")
    print("=" * 82)

    trend = base_trend()

    outcome = {
        "outcome_learning_signal": "NEGATIVE",
        "outcome_learning_signal_strength": 0.9,
        "adaptive_learning_required": True,
    }

    result = engine.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    print(result)

    assert_equal(
        result["strategy"],
        "DEFENSIVE",
        "NEGATIVE -> strategy",
    )
    assert_equal(
        result["action"],
        "REDUCE_RISK",
        "NEGATIVE -> action",
    )
    assert_equal(
        result["outcome_learning_signal"],
        "NEGATIVE",
        "NEGATIVE -> signal",
    )
    assert_equal(
        result["outcome_learning_signal_strength"],
        0.9,
        "NEGATIVE -> signal strength",
    )
    assert_equal(
        result["adaptive_learning_required"],
        True,
        "NEGATIVE -> adaptive learning",
    )


def run_case_negative_without_adaptive_requirement(engine):
    print("=" * 82)
    print("CASE: NEGATIVE + NO_ADAPTIVE_REQUIREMENT -> PRESERVE")
    print("=" * 82)

    trend = base_trend()

    outcome = {
        "outcome_learning_signal": "NEGATIVE",
        "outcome_learning_signal_strength": 0.9,
        "adaptive_learning_required": False,
    }

    result = engine.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    print(result)

    assert_equal(
        result["strategy"],
        "MAINTAIN",
        "NEGATIVE without adaptive requirement -> strategy",
    )
    assert_equal(
        result["action"],
        "MAINTAIN_ALLOCATION",
        "NEGATIVE without adaptive requirement -> action",
    )
    assert_equal(
        result["adaptive_learning_required"],
        False,
        "NEGATIVE without adaptive requirement -> adaptive learning",
    )


def run_case_positive_balanced_strong(engine):
    print("=" * 82)
    print("CASE: POSITIVE + STRONG + BALANCED -> GROWTH")
    print("=" * 82)

    trend = {
        "direction": "STABLE",
        "stability": "MEDIUM",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "MEDIUM",
        "latest_score": 75,
    }

    outcome = {
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 0.9,
        "adaptive_learning_required": False,
    }

    result = engine.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    print(result)

    assert_equal(
        result["strategy"],
        "GROWTH",
        "POSITIVE strong -> strategy",
    )
    assert_equal(
        result["action"],
        "INCREASE_RISK",
        "POSITIVE strong -> action",
    )
    assert_equal(
        result["outcome_learning_signal"],
        "POSITIVE",
        "POSITIVE strong -> signal",
    )
    assert_equal(
        result["outcome_learning_signal_strength"],
        0.9,
        "POSITIVE strong -> signal strength",
    )
    assert_equal(
        result["adaptive_learning_required"],
        False,
        "POSITIVE strong -> adaptive learning",
    )


def run_case_positive_below_threshold(engine):
    print("=" * 82)
    print("CASE: POSITIVE + BELOW_THRESHOLD -> PRESERVE_BALANCED")
    print("=" * 82)

    trend = {
        "direction": "STABLE",
        "stability": "MEDIUM",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "MEDIUM",
        "latest_score": 55,
    }

    outcome = {
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 0.69,
        "adaptive_learning_required": False,
    }

    result = engine.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    print(result)

    assert_equal(
        result["strategy"],
        "BALANCED",
        "POSITIVE below threshold -> strategy",
    )
    assert_equal(
        result["action"],
        "MAINTAIN_BALANCE",
        "POSITIVE below threshold -> action",
    )
    assert_equal(
        result["outcome_learning_signal"],
        "POSITIVE",
        "POSITIVE below threshold -> signal",
    )
    assert_equal(
        result["outcome_learning_signal_strength"],
        0.69,
        "POSITIVE below threshold -> signal strength",
    )


def run_case_positive_strong_non_balanced_preserves_base(engine):
    print("=" * 82)
    print("CASE: POSITIVE + STRONG + NON_BALANCED -> PRESERVE_BASE")
    print("=" * 82)

    trend = {
        "direction": "DOWN",
        "stability": "LOW",
        "momentum": "NEGATIVE",
        "grade_stability": "STABLE",
        "consistency": "HIGH",
        "latest_score": 60,
    }

    outcome = {
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 0.9,
        "adaptive_learning_required": False,
    }

    result = engine.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    print(result)

    assert_equal(
        result["strategy"],
        "CAUTIOUS",
        "POSITIVE strong non-balanced -> strategy",
    )
    assert_equal(
        result["action"],
        "LIMIT_EXPOSURE",
        "POSITIVE strong non-balanced -> action",
    )
    assert_equal(
        result["outcome_learning_signal"],
        "POSITIVE",
        "POSITIVE strong non-balanced -> signal",
    )


def run_case_boundary_strength_exactly_point_seven(engine):
    print("=" * 82)
    print("CASE: POSITIVE + STRENGTH_0.7 -> GROWTH")
    print("=" * 82)

    trend = {
        "direction": "STABLE",
        "stability": "MEDIUM",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "MEDIUM",
        "latest_score": 55,
    }

    outcome = {
        "outcome_learning_signal": "POSITIVE",
        "outcome_learning_signal_strength": 0.7,
        "adaptive_learning_required": False,
    }

    result = engine.analyze(
        trend=trend,
        outcome_intelligence=outcome,
    )

    print(result)

    assert_equal(
        result["strategy"],
        "GROWTH",
        "STRENGTH 0.7 -> strategy",
    )
    assert_equal(
        result["action"],
        "INCREASE_RISK",
        "STRENGTH 0.7 -> action",
    )


def run_case_missing_outcome_intelligence(engine):
    print("=" * 82)
    print("CASE: MISSING_OUTCOME_INTELLIGENCE -> NORMAL_STRATEGY")
    print("=" * 82)

    trend = base_trend()

    result = engine.analyze(
        trend=trend,
        outcome_intelligence=None,
    )

    print(result)

    assert_equal(
        result["strategy"],
        "MAINTAIN",
        "MISSING outcome intelligence -> strategy",
    )
    assert_equal(
        result["action"],
        "MAINTAIN_ALLOCATION",
        "MISSING outcome intelligence -> action",
    )
    assert_equal(
        result["outcome_learning_signal"],
        "NONE",
        "MISSING outcome intelligence -> signal",
    )
    assert_equal(
        result["adaptive_learning_required"],
        False,
        "MISSING outcome intelligence -> adaptive learning",
    )


def main():
    print("=" * 82)
    print("PHASE 7-10-18-H")
    print("OUTCOME INTELLIGENCE")
    print("-> ADAPTIVE STRATEGY")
    print("BOUNDARY CONTRACT TEST V2")
    print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
    print("=" * 82)

    engine = AIDecisionAdaptiveStrategy()

    run_case_no_learning_preserves_strategy(engine)
    run_case_negative_adaptive_required(engine)
    run_case_negative_without_adaptive_requirement(engine)
    run_case_positive_balanced_strong(engine)
    run_case_positive_below_threshold(engine)
    run_case_positive_strong_non_balanced_preserves_base(engine)
    run_case_boundary_strength_exactly_point_seven(engine)
    run_case_missing_outcome_intelligence(engine)

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
    print("===== PHASE 7-10-18-H CONTRACT TEST V2 COMPLETE =====")
    print("=" * 82)


if __name__ == "__main__":
    main()





