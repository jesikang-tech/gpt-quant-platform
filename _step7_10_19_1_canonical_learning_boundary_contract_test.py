"""
PHASE 7-10-19-1
OUTCOME SCORE
-> CANONICAL LEARNING SIGNAL
BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_decision_outcome_evaluation import (
    AIDecisionOutcomeEvaluation,
)


engine = AIDecisionOutcomeEvaluation()


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def run_case(score, expected_signal, expected_strength):
    print("=" * 82)
    print(f"CASE: SCORE {score}")
    print("=" * 82)

    signal = engine.canonical_learning_signal(score)
    strength = engine.canonical_learning_signal_strength(score)

    print("score:", score)
    print("learning_signal:", signal)
    print("learning_signal_strength:", strength)

    assert_equal(
        signal,
        expected_signal,
        f"SCORE {score} -> learning signal",
    )

    assert_equal(
        strength,
        expected_strength,
        f"SCORE {score} -> learning strength",
    )


run_case(100.0, "POSITIVE", 100.0)
run_case(80.0, "POSITIVE", 60.0)
run_case(79.9, "STABLE", 59.8)
run_case(60.0, "STABLE", 20.0)
run_case(59.9, "NEGATIVE", 19.8)
run_case(0.0, "NEGATIVE", 100.0)

print("")
print("=" * 82)
print("===== PHASE 7-10-19-1 CANONICAL LEARNING BOUNDARY COMPLETE =====")
print("=" * 82)
