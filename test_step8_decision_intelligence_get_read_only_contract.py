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
