import api_server
from api_server import app


client = app.test_client()


def fake_history_reader(history_id):
    row = [None] * 37

    row[0] = history_id
    row[1] = "MAINTAIN"
    row[2] = "PROCEED"
    row[3] = "MAINTAIN"
    row[4] = 93.2
    row[5] = 89.6

    return tuple(row)


def run_case(
    name,
    portfolio_return,
    expected_score,
    expected_grade,
    expected_signal,
    expected_learning,
    expected_feedback,
    expected_adaptive,
    expected_reassessment,
    expected_reassessment_status,
):
    captured = {}

    def fake_portfolio_evaluation(
        history_id,
        evaluation_date=None,
    ):
        return {
            "evaluation_status": "EVALUATED",
            "outcome_status": "EVALUATED",
            "history_id": history_id,
            "evaluation_date":
                evaluation_date or "2026-08-20",
            "portfolio_return": portfolio_return,
            "evaluated_weight": 100.0,
            "pending_positions": 0,
            "positions": [],
        }

    def fake_update_history(**kwargs):
        captured.update(kwargs)
        return 1

    original_evaluator = (
        api_server.evaluate_ai_decision_portfolio_snapshot
    )
    original_history_reader = (
        api_server.get_ai_decision_outcome_history_by_id
    )
    original_history_updater = (
        api_server.update_ai_decision_outcome_history
    )

    try:
        api_server.evaluate_ai_decision_portfolio_snapshot = (
            fake_portfolio_evaluation
        )

        api_server.get_ai_decision_outcome_history_by_id = (
            fake_history_reader
        )

        api_server.update_ai_decision_outcome_history = (
            fake_update_history
        )

        response = client.get(
            "/api/ai-decision/portfolio-snapshot/12/evaluate"
        )

        data = response.get_json()

        assert response.status_code == 200
        assert data["success"] is True

        evaluation = data["outcome_evaluation"]
        intelligence = data["outcome_intelligence"]

        assert evaluation["outcome_status"] == "EVALUATED"
        assert evaluation["outcome_score"] == expected_score
        assert evaluation["outcome_grade"] == expected_grade
        assert (
            evaluation["learning_signal"]
            == expected_signal
        )

        assert (
            intelligence["learning_status"]
            == expected_learning
        )

        assert (
            intelligence["feedback_state"]
            == expected_feedback
        )

        assert (
            intelligence["adaptive_learning_required"]
            == expected_adaptive
        )

        assert (
            intelligence["reassessment_required"]
            == expected_reassessment
        )

        assert (
            intelligence["reassessment_status"]
            == expected_reassessment_status
        )

        assert captured["history_id"] == 12
        assert captured["outcome_status"] == "EVALUATED"
        assert (
            captured["outcome_score"]
            == expected_score
        )
        assert (
            captured["outcome_grade"]
            == expected_grade
        )

        assert (
            captured["learning_status"]
            == expected_learning
        )

        assert (
            captured["feedback_state"]
            == expected_feedback
        )

        assert (
            captured["adaptive_learning_required"]
            == int(expected_adaptive)
        )

        assert (
            captured["reassessment_required"]
            == int(expected_reassessment)
        )

        assert (
            captured["reassessment_status"]
            == expected_reassessment_status
        )

        print(
            f"{name}: PASS | "
            f"return={portfolio_return} | "
            f"signal={expected_signal} | "
            f"adaptive={expected_adaptive} | "
            f"reassessment={expected_reassessment}"
        )

    finally:
        api_server.evaluate_ai_decision_portfolio_snapshot = (
            original_evaluator
        )

        api_server.get_ai_decision_outcome_history_by_id = (
            original_history_reader
        )

        api_server.update_ai_decision_outcome_history = (
            original_history_updater
        )


print("=" * 60)
print(
    "Step6-10-G Outcome Lifecycle Regression Test"
)
print("=" * 60)


run_case(
    "CASE 1 POSITIVE",
    10.0,
    100.0,
    "A",
    "POSITIVE",
    "LEARNING_AVAILABLE",
    "LEARNING_AVAILABLE",
    False,
    False,
    "NOT_REQUIRED",
)


run_case(
    "CASE 2 NEGATIVE",
    -10.0,
    0.0,
    "F",
    "NEGATIVE",
    "ADAPTIVE_LEARNING_REQUIRED",
    "ADAPTIVE_LEARNING",
    True,
    True,
    "REASSESSMENT_REQUIRED",
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
