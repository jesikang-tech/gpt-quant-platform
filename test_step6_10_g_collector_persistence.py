import api_server


captured = {
    "history": None,
    "snapshot": None,
    "update": None,
}


def fake_save_history(**kwargs):
    captured["history"] = kwargs.copy()
    return 901


def fake_save_snapshot(**kwargs):
    captured["snapshot"] = kwargs.copy()
    return len(kwargs.get("portfolio", []))


def fake_update_history(**kwargs):
    captured["update"] = kwargs.copy()
    return 1


original_save_history = (
    api_server.save_ai_decision_outcome_history
)
original_save_snapshot = (
    api_server.save_ai_decision_portfolio_snapshot
)
original_update_history = (
    api_server.update_ai_decision_outcome_history
)


try:
    api_server.save_ai_decision_outcome_history = (
        fake_save_history
    )

    api_server.save_ai_decision_portfolio_snapshot = (
        fake_save_snapshot
    )

    api_server.update_ai_decision_outcome_history = (
        fake_update_history
    )

    with api_server.app.test_request_context(
        "/api/portfolio/decision-intelligence"
    ):
        response = (
            api_server.portfolio_decision_intelligence_api()
        )

    assert captured["history"] is not None
    assert captured["snapshot"] is not None
    assert captured["update"] is not None

    history = captured["history"]
    snapshot = captured["snapshot"]
    update = captured["update"]

    assert history["outcome_status"] == "PENDING"
    assert history["snapshot_status"] == "COLLECTED"
    assert (
        history["snapshot_purpose"]
        == "FUTURE_OUTCOME_EVALUATION"
    )
    assert (
        history["learning_status"]
        == "WAITING_FOR_OUTCOME"
    )
    assert history["feedback_state"] == "COLLECTING"
    assert history["adaptive_learning_required"] == 0
    assert history["reassessment_required"] == 0
    assert (
        history["reassessment_status"]
        == "NOT_REQUIRED"
    )

    assert snapshot["history_id"] == 901

    portfolio = snapshot["portfolio"]

    assert isinstance(portfolio, list)
    assert len(portfolio) > 0

    total_weight = sum(
        float(item.get("weight", 0) or 0)
        for item in portfolio
    )

    assert total_weight > 0

    assert update["history_id"] == 901
    assert update["outcome_status"] == "PENDING"
    assert (
        update["learning_status"]
        == "WAITING_FOR_OUTCOME"
    )
    assert update["feedback_state"] == "COLLECTING"
    assert (
        update["adaptive_learning_required"] == 0
    )
    assert update["reassessment_required"] == 0
    assert (
        update["reassessment_status"]
        == "NOT_REQUIRED"
    )

    print("=" * 60)
    print(
        "Step6-10-G Collector-to-Persistence "
        "Regression Test"
    )
    print("=" * 60)
    print("CASE 1 HISTORY SAVE: PASS")
    print("CASE 2 SNAPSHOT SAVE: PASS")
    print("CASE 3 HISTORY UPDATE: PASS")
    print("")
    print("=" * 60)
    print("OVERALL RESULT: PASS")
    print("=" * 60)

finally:
    api_server.save_ai_decision_outcome_history = (
        original_save_history
    )

    api_server.save_ai_decision_portfolio_snapshot = (
        original_save_snapshot
    )

    api_server.update_ai_decision_outcome_history = (
        original_update_history
    )
