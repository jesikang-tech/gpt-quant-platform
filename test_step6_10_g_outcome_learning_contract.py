from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence
)


engine = AIDecisionOutcomeIntelligence()


def run_case(
    name,
    signal,
    expected_learning,
    expected_feedback,
    outcome_score,
    outcome_grade,
    market_response,
    portfolio_response,
):
    result = engine.analyze(
        final_decision={
            "decision": "TEST",
            "action": "TEST",
            "strategy": "TEST",
        },
        final_decision_execution_reassessment={
            "reassessment_required": False,
            "reassessment_status": "NOT_REQUIRED",
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
            "outcome_score": outcome_score,
            "outcome_grade": outcome_grade,
            "learning_status": "LEARNING_AVAILABLE",
            "learning_signal": signal,
            "learning_signal_strength": outcome_score,
            "decision_effectiveness": "EFFECTIVE",
            "strategy_effectiveness": "EFFECTIVE",
            "market_response": market_response,
            "portfolio_response": portfolio_response,
        },
    )

    assert result["outcome_status"] == "EVALUATED"
    assert result["outcome_learning_signal"] == signal
    assert result["learning_status"] == expected_learning
    assert result["feedback_state"] == expected_feedback

    print(
        f"{name}: PASS | "
        f"{signal} -> "
        f"{expected_learning} / "
        f"{expected_feedback}"
    )


print("=" * 60)
print(
    "Step6-10-G Outcome Learning Contract Regression Test"
)
print("=" * 60)


run_case(
    "CASE 1 NEGATIVE",
    "NEGATIVE",
    "ADAPTIVE_LEARNING_REQUIRED",
    "ADAPTIVE_LEARNING",
    40.0,
    "F",
    "NEGATIVE",
    "NEGATIVE",
)


run_case(
    "CASE 2 POSITIVE",
    "POSITIVE",
    "LEARNING_AVAILABLE",
    "LEARNING_AVAILABLE",
    87.5,
    "B",
    "POSITIVE",
    "POSITIVE",
)


run_case(
    "CASE 3 STABLE",
    "STABLE",
    "LEARNING_AVAILABLE",
    "LEARNING_AVAILABLE",
    75.0,
    "B",
    "STABLE",
    "STABLE",
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
