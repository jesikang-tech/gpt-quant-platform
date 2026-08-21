import api_server
from api_server import app


client = app.test_client()


def run_case(
    name,
    evaluation_date,
    portfolio_return,
    expected_score,
    expected_grade,
    expected_signal,
):
    captured = {}

    def fake_portfolio_evaluation(
        history_id,
        evaluation_date=None,
    ):
        captured["evaluation_date"] = evaluation_date

        return {
            "evaluation_status": "EVALUATED",
            "outcome_status": "EVALUATED",
            "history_id": history_id,
            "evaluation_date": evaluation_date,
            "portfolio_return": portfolio_return,
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

    def fake_update_history(**kwargs):
        captured["update"] = kwargs.copy()
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
            f"/api/ai-decision/portfolio-snapshot/12/evaluate"
            f"?evaluation_date={evaluation_date}"
        )

        data = response.get_json()

        assert response.status_code == 200
        assert data["success"] is True

        evaluation = data["outcome_evaluation"]

        assert evaluation["outcome_status"] == "EVALUATED"
        assert evaluation["outcome_score"] == expected_score
        assert evaluation["outcome_grade"] == expected_grade
        assert evaluation["learning_signal"] == expected_signal

        assert (
            captured["evaluation_date"]
            == evaluation_date
        )

        assert (
            data["evaluation"]["evaluation_date"]
            == evaluation_date
        )

        assert (
            data["evaluation"]["portfolio_return"]
            == portfolio_return
        )

        assert captured["update"]["history_id"] == 12

        assert (
            captured["update"]["outcome_status"]
            == "EVALUATED"
        )

        assert (
            captured["update"]["outcome_score"]
            == expected_score
        )

        assert (
            captured["update"]["outcome_grade"]
            == expected_grade
        )

        print(
            f"{name}: PASS | "
            f"date={evaluation_date} | "
            f"return={portfolio_return} | "
            f"score={expected_score} | "
            f"grade={expected_grade} | "
            f"signal={expected_signal}"
        )

        return evaluation

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
    "Production Hardening - Same-Date Evaluation "
    "Idempotency Regression"
)
print("=" * 60)


first = run_case(
    "CASE 1 FIRST EVALUATION",
    "2026-08-21",
    5.0,
    75.0,
    "C",
    "STABLE",
)


second = run_case(
    "CASE 2 SAME-DATE RE-EVALUATION",
    "2026-08-21",
    5.0,
    75.0,
    "C",
    "STABLE",
)


assert first == second

print(
    "CASE 3 SAME-DATE RESULT STABILITY: PASS"
)


third = run_case(
    "CASE 4 NEXT-DATE RE-EVALUATION",
    "2026-08-22",
    8.0,
    90.0,
    "A",
    "POSITIVE",
)


assert third["outcome_score"] != first["outcome_score"]
assert third["outcome_grade"] != first["outcome_grade"]
assert third["learning_signal"] != first["learning_signal"]

print(
    "CASE 5 NEXT-DATE RE-EVALUATION ALLOWED: PASS"
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
