import api_server


captured = {
    "atomic": None,
    "update": None,
}


def fake_atomic_persistence(**kwargs):
    captured["atomic"] = kwargs.copy()

    return {
        "history_id": 901,
        "snapshot_count": len(
            kwargs.get("portfolio", [])
        ),
    }


def fake_update_history(**kwargs):
    captured["update"] = kwargs.copy()
    return 1


original_atomic = (
    api_server.save_ai_decision_outcome_with_portfolio_transaction
)

original_update_history = (
    api_server.update_ai_decision_outcome_history
)


try:
    api_server.save_ai_decision_outcome_with_portfolio_transaction = (
        fake_atomic_persistence
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

    assert captured["atomic"] is not None
    assert captured["update"] is not None

    atomic = captured["atomic"]
    update = captured["update"]

    history_kwargs = atomic["history_kwargs"]

    assert history_kwargs["outcome_status"] == "PENDING"
    assert history_kwargs["snapshot_status"] == "COLLECTED"

    assert (
        history_kwargs["snapshot_purpose"]
        == "FUTURE_OUTCOME_EVALUATION"
    )

    assert (
        history_kwargs["learning_status"]
        == "WAITING_FOR_OUTCOME"
    )

    assert history_kwargs["feedback_state"] == "COLLECTING"
    assert (
        history_kwargs["adaptive_learning_required"]
        == 0
    )
    assert (
        history_kwargs["reassessment_required"]
        == 0
    )
    assert (
        history_kwargs["reassessment_status"]
        == "NOT_REQUIRED"
    )

    assert atomic["portfolio"] is not None

    portfolio = atomic["portfolio"]

    assert isinstance(portfolio, list)
    assert len(portfolio) > 0

    total_weight = sum(
        float(item.get("weight", 0) or 0)
        for item in portfolio
    )

    assert total_weight > 0

    assert (
        atomic["created_at"] is not None
    )

    assert update["history_id"] == 901
    assert update["outcome_status"] == "PENDING"

    assert (
        update["learning_status"]
        == "WAITING_FOR_OUTCOME"
    )

    assert (
        update["feedback_state"]
        == "COLLECTING"
    )

    assert (
        update["adaptive_learning_required"]
        == 0
    )

    assert update["reassessment_required"] == 0

    assert (
        update["reassessment_status"]
        == "NOT_REQUIRED"
    )

    print("=" * 60)
    print(
        "Step6 Production Atomic Persistence "
        "Integration Regression"
    )
    print("=" * 60)

    print(
        "CASE 1 ATOMIC HISTORY + SNAPSHOT SAVE: PASS"
    )

    print(
        "CASE 2 HISTORY UPDATE: PASS"
    )

    print("")
    print("=" * 60)
    print("OVERALL RESULT: PASS")
    print("=" * 60)

finally:
    api_server.save_ai_decision_outcome_with_portfolio_transaction = (
        original_atomic
    )

    api_server.update_ai_decision_outcome_history = (
        original_update_history
    )
