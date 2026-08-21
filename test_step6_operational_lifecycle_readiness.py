import api_server
from api_server import app


client = app.test_client()


def fake_portfolio_evaluation(
    history_id,
    evaluation_date=None,
):
    return {
        "evaluation_status": "EVALUATED",
        "outcome_status": "EVALUATED",
        "history_id": history_id,
        "evaluation_date":
            evaluation_date or "2026-08-21",
        "portfolio_return": 5.0,
        "evaluated_weight": 100.0,
        "pending_positions": 0,
        "positions": [],
    }


def fake_history_reader(history_id):
    row = [None] * 37

    row[0] = history_id
    row[1] = "MAINTAIN"
    row[2] = "PROCEED"
    row[3] = "MAINTAIN"
    row[4] = 93.2
    row[5] = 89.6

    return tuple(row)


captured = {}


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
    assert evaluation["outcome_score"] == 75.0
    assert evaluation["outcome_grade"] == "C"
    assert evaluation["learning_signal"] == "STABLE"

    assert (
        intelligence["learning_status"]
        == "LEARNING_AVAILABLE"
    )

    assert (
        intelligence["feedback_state"]
        == "LEARNING_AVAILABLE"
    )

    assert (
        intelligence["adaptive_learning_required"]
        is False
    )

    assert (
        intelligence["reassessment_required"]
        is False
    )

    assert captured["history_id"] == 12
    assert captured["outcome_status"] == "EVALUATED"
    assert captured["outcome_score"] == 75.0
    assert captured["outcome_grade"] == "C"
    assert (
        captured["learning_status"]
        == "LEARNING_AVAILABLE"
    )
    assert (
        captured["feedback_state"]
        == "LEARNING_AVAILABLE"
    )
    assert (
        captured["adaptive_learning_required"]
        == 0
    )
    assert captured["reassessment_required"] == 0
    assert (
        captured["reassessment_status"]
        == "NOT_REQUIRED"
    )

    print("=" * 60)
    print(
        "Step6 Operational Lifecycle Readiness Regression"
    )
    print("=" * 60)
    print("CASE 1 PENDING -> EVALUATED: PASS")
    print("CASE 2 STABLE LEARNING: PASS")
    print("CASE 3 HISTORY UPDATE: PASS")
    print("")
    print("=" * 60)
    print("OVERALL RESULT: PASS")
    print("=" * 60)

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
