"""Synthetic isolated API contract; no source database copy or import-time execution."""
from contextlib import ExitStack, closing
from price_test_support import (isolated_price_db, isolated_evaluation_api,
                                synthetic_ranking_db, synthetic_ready_api)


def test_decision_intelligence_get_read_only(synthetic_ready_api):
    client = synthetic_ready_api.client
    with ExitStack() as stack:

        conn = stack.enter_context(closing(synthetic_ready_api.db.connect()))
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_outcome_history"
        )
        history_before = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
        )
        snapshot_before = cursor.fetchone()[0]

        conn.close()

        before_bytes = synthetic_ready_api.db.path.read_bytes()
        response_1 = client.get(
            "/api/portfolio/decision-intelligence"
        )

        assert response_1.status_code == 200
        assert response_1.is_json

        conn = stack.enter_context(closing(synthetic_ready_api.db.connect()))
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_outcome_history"
        )
        history_after_first = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
        )
        snapshot_after_first = cursor.fetchone()[0]

        conn.close()

        response_2 = client.get(
            "/api/portfolio/decision-intelligence"
        )

        assert response_2.status_code == 200
        assert response_2.is_json

        conn = stack.enter_context(closing(synthetic_ready_api.db.connect()))
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_outcome_history"
        )
        history_after_second = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
        )
        snapshot_after_second = cursor.fetchone()[0]

        conn.close()

        assert history_after_first == history_before, (
            "GET must not create Outcome History"
        )

        assert snapshot_after_first == snapshot_before, (
            "GET must not create Portfolio Snapshot"
        )

        assert history_after_second == history_before, (
            "Repeated GET must not create Outcome History"
        )

        assert snapshot_after_second == snapshot_before, (
            "Repeated GET must not create Portfolio Snapshot"
        )

        assert synthetic_ready_api.db.path.read_bytes() == before_bytes

        print("CASE 1 FIRST GET HISTORY: PASS")
        print("CASE 2 FIRST GET SNAPSHOT: PASS")
        print("CASE 3 SECOND GET HISTORY: PASS")
        print("CASE 4 SECOND GET SNAPSHOT: PASS")
        print("")
        print("OVERALL RESULT: PASS")



def test_temporary_connection_closes_on_exception(synthetic_ready_api):
    import sqlite3
    import pytest

    with pytest.raises(RuntimeError, match="synthetic failure"):
        with ExitStack() as stack:
            conn = stack.enter_context(closing(synthetic_ready_api.db.connect()))
            raise RuntimeError("synthetic failure")
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        conn.execute("SELECT 1")
def test_empty_ranking_get_and_post(isolated_price_db):
    """Empty ranking must fail safely before portfolio calculation."""
    from unittest.mock import patch
    from price_test_support import phase8_test_scope
    from testing_helpers import authenticated_client

    with phase8_test_scope(isolated_price_db) as scope:
        api = scope.api
        client = authenticated_client(api.app)

        with patch.object(
            api,
            "get_dashboard_api_data",
            return_value={"success": True, "data": []},
        ):
            with patch.object(
                api,
                "optimize_portfolio_weight",
                side_effect=AssertionError(
                    "Portfolio calculation must not run"
                ),
            ) as optimizer:
                for method in ("GET", "POST"):
                    response = client.open(
                        "/api/portfolio/decision-intelligence",
                        method=method,
                    )
                    payload = response.get_json()

                    assert response.status_code == 422, (
                        method,
                        response.status_code,
                        payload,
                    )
                    assert payload["success"] is False
                    assert "ranking data is empty" in payload["message"]

                optimizer.assert_not_called()
