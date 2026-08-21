import api_server
from api_server import app


client = app.test_client()


def make_history_row():
    row = [None] * 37

    row[0] = 12
    row[1] = "TEST_PORTFOLIO"
    row[2] = "TEST_ACTION"
    row[3] = "BALANCED"
    row[4] = 100.0
    row[5] = 86.6

    return tuple(row)


def run_case(
    name,
    portfolio_return,
    expected_signal,
    expected_learning,
    expected_feedback,
    expected_adaptive,
    expected_reassessment,
):
    original_evaluator = (
        api_server.evaluate_ai_decision_portfolio_snapshot
    )
    original_history_reader = (
        api_server.get_ai_decision_outcome_history_by_id
    )
    original_history_updater = (
        api_server.update_ai_decision_outcome_history
    )

    captured_update = {}

    try:
        api_server.evaluate_ai_decision_portfolio_snapshot = (
            lambda history_id, evaluation_date=None: {
                "evaluation_status": "EVALUATED",
                "outcome_status": "EVALUATED",
                "history_id": history_id,
                "evaluation_date": "2026-08-20",
                "portfolio_return": portfolio_return,
                "evaluated_weight": 100.0,
                "pending_positions": 0,
                "positions": [],
            }
        )

        api_server.get_ai_decision_outcome_history_by_id = (
            lambda history_id: make_history_row()
        )

        def capture_update(**kwargs):
            captured_update.update(kwargs)
            return 1

        api_server.update_ai_decision_outcome_history = (
            capture_update
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
        assert (
            evaluation["learning_signal"]
            == expected_signal
        )
        assert (
            evaluation["adaptive_learning_required"]
            == expected_adaptive
        )
        assert (
            evaluation["reassessment_required"]
            == expected_reassessment
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

        assert captured_update["outcome_status"] == "EVALUATED"
        assert (
            captured_update["learning_status"]
            == expected_learning
        )
        assert (
            captured_update["feedback_state"]
            == expected_feedback
        )
        assert (
            bool(
                captured_update[
                    "adaptive_learning_required"
                ]
            )
            == expected_adaptive
        )
        assert (
            bool(
                captured_update[
                    "reassessment_required"
                ]
            )
            == expected_reassessment
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
    "Step6-10-G Portfolio Outcome Integration "
    "Semantic Regression Test"
)
print("=" * 60)


run_case(
    "CASE 1 POSITIVE",
    10.0,
    "POSITIVE",
    "LEARNING_AVAILABLE",
    "LEARNING_AVAILABLE",
    False,
    False,
)


run_case(
    "CASE 2 NEGATIVE",
    0.0,
    "NEGATIVE",
    "ADAPTIVE_LEARNING_REQUIRED",
    "ADAPTIVE_LEARNING",
    True,
    True,
)


run_case(
    "CASE 3 STABLE",
    5.0,
    "STABLE",
    "LEARNING_AVAILABLE",
    "LEARNING_AVAILABLE",
    False,
    False,
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
