from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence
)


engine = AIDecisionOutcomeIntelligence()


def run_case(
    name,
    signal,
    score,
    expected_learning,
    expected_feedback,
    expected_adaptive,
    expected_reassessment,
):
    result = engine.analyze(
        final_decision={
            "decision": "TEST",
            "action": "TEST",
            "strategy": "TEST",
        },
        final_decision_execution_reassessment={
            "reassessment_required": expected_reassessment,
            "reassessment_status": (
                "REASSESSMENT_REQUIRED"
                if expected_reassessment
                else "NOT_REQUIRED"
            ),
        },
        intelligence={},
        intelligence_score={
            "intelligence_score": 86.6,
        },
        decision_confidence={
            "confidence_score": 100.0,
        },
        outcome_evaluation={
            "outcome_status": "EVALUATED",
            "outcome_score": score,
            "outcome_grade": "F" if score < 60 else "B",
            "learning_status": "LEARNING_AVAILABLE",
            "learning_signal": signal,
            "learning_signal_strength": score,
            "decision_effectiveness": "EFFECTIVE",
            "strategy_effectiveness": "EFFECTIVE",
            "market_response": (
                "NEGATIVE"
                if signal == "NEGATIVE"
                else "POSITIVE"
            ),
            "portfolio_response": (
                "NEGATIVE"
                if signal == "NEGATIVE"
                else "POSITIVE"
            ),
        },
    )

    assert result["outcome_status"] == "EVALUATED"
    assert result["outcome_learning_signal"] == signal
    assert result["learning_status"] == expected_learning
    assert result["feedback_state"] == expected_feedback
    assert (
        result["adaptive_learning_required"]
        == expected_adaptive
    )
    assert (
        result["reassessment_required"]
        == expected_reassessment
    )

    print(
        f"{name}: PASS | "
        f"{signal} -> "
        f"{expected_learning} / "
        f"{expected_feedback} | "
        f"adaptive={expected_adaptive} | "
        f"reassessment={expected_reassessment}"
    )


print("=" * 60)
print(
    "Step6-10-G Learning/Reassessment Flag Contract Test"
)
print("=" * 60)


run_case(
    "CASE 1 NEGATIVE",
    "NEGATIVE",
    40.0,
    "ADAPTIVE_LEARNING_REQUIRED",
    "ADAPTIVE_LEARNING",
    True,
    True,
)


run_case(
    "CASE 2 POSITIVE",
    "POSITIVE",
    87.5,
    "LEARNING_AVAILABLE",
    "LEARNING_AVAILABLE",
    False,
    False,
)


run_case(
    "CASE 3 STABLE",
    "STABLE",
    75.0,
    "LEARNING_AVAILABLE",
    "LEARNING_AVAILABLE",
    False,
    False,
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
