from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence,
)
from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


OUTCOME_ENGINE = AIDecisionOutcomeIntelligence()
ADAPTIVE_ENGINE = AIDecisionAdaptiveStrategy()


TREND = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}


CASES = [
    (
        "CASE 1 PENDING",
        {
            "outcome_status": "PENDING",
            "outcome_score": 0.0,
            "learning_signal": "NONE",
            "learning_signal_strength": 0.0,
        },
        "WAITING_FOR_OUTCOME",
        "BLOCKED",
        "BLOCKED",
        "NONE",
        0.0,
        False,
        False,
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
    ),
    (
        "CASE 2 POSITIVE",
        {
            "outcome_status": "EVALUATED",
            "outcome_score": 87.5,
            "learning_signal": "POSITIVE",
            "learning_signal_strength": 0.875,
        },
        "WAITING_FOR_OUTCOME",
        "LEARNING_AVAILABLE",
        "LEARNING_AVAILABLE",
        "POSITIVE",
        0.9,
        False,
        False,
        "MAINTAIN",
        "MAINTAIN_ALLOCATION",
    ),
    (
        "CASE 3 NEGATIVE",
        {
            "outcome_status": "EVALUATED",
            "outcome_score": 20.0,
            "learning_signal": "NEGATIVE",
            "learning_signal_strength": 1.0,
        },
        "WAITING_FOR_OUTCOME",
        "ADAPTIVE_LEARNING_REQUIRED",
        "ADAPTIVE_LEARNING",
        "NEGATIVE",
        1.0,
        True,
        False,
        "DEFENSIVE",
        "REDUCE_RISK",
    ),
]


print("=" * 60)
print("PHASE 7-2-11 OUTCOME-TO-STRATEGY INTEGRATION CONTRACT")
print("=" * 60)


for (
    name,
    outcome_evaluation,
    expected_outcome_learning_status,
    expected_learning_status,
    expected_feedback_state,
    expected_signal,
    expected_signal_strength,
    expected_adaptive,
    expected_reassessment,
    expected_strategy,
    expected_action,
) in CASES:

    intelligence = OUTCOME_ENGINE.analyze(
        outcome_evaluation=outcome_evaluation,
    )

    assert (
        intelligence["outcome_learning_status"]
        == expected_outcome_learning_status
    )

    assert (
        intelligence["learning_status"]
        == expected_learning_status
    )

    assert (
        intelligence["feedback_state"]
        == expected_feedback_state
    )

    assert (
        intelligence["outcome_learning_signal"]
        == expected_signal
    )

    assert (
        intelligence["outcome_learning_signal_strength"]
        == expected_signal_strength
    )

    assert (
        intelligence["adaptive_learning_required"]
        is expected_adaptive
    )

    assert (
        intelligence["reassessment_required"]
        is expected_reassessment
    )

    strategy = ADAPTIVE_ENGINE.analyze(
        trend=TREND,
        outcome_intelligence=intelligence,
    )

    assert (
        strategy["outcome_learning_signal"]
        == expected_signal
    )

    assert (
        strategy["outcome_learning_signal_strength"]
        == expected_signal_strength
    )

    assert (
        strategy["adaptive_learning_required"]
        is expected_adaptive
    )

    assert strategy["strategy"] == expected_strategy
    assert strategy["action"] == expected_action

    print(
        f"{name}: PASS | "
        f"{expected_signal} | "
        f"outcome_learning={expected_outcome_learning_status} | "
        f"learning={expected_learning_status} | "
        f"feedback={expected_feedback_state} | "
        f"adaptive={expected_adaptive} | "
        f"{strategy['strategy']} -> "
        f"{strategy['action']}"
    )


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
