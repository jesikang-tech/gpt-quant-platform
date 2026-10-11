"""Synthetic isolated API contract; no source database copy or import-time execution."""
from contextlib import ExitStack, closing
from price_test_support import (isolated_price_db, isolated_evaluation_api,
                                synthetic_ranking_db, synthetic_ready_api)


def test_decision_intelligence_post_persistence(synthetic_ready_api):
    client = synthetic_ready_api.client
    with ExitStack() as stack:

        conn = stack.enter_context(closing(synthetic_ready_api.db.connect()))
        cursor = conn.cursor()
        # Every non-cash synthetic constituent has an explicit reference price.
        with conn:
            conn.executemany("INSERT INTO etf_prices VALUES (?, '2026-01-06', ?)",
                             [("222222", 200), ("333333", 300)])

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_outcome_history"
        )
        history_before = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
        )
        snapshot_before = cursor.fetchone()[0]

        conn.close()

        response_1 = client.post(
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


        cursor = stack.enter_context(closing(synthetic_ready_api.db.connect())).cursor()

        cursor.execute(
            """
            SELECT
                id,
                outcome_status,
                snapshot_status,
                snapshot_purpose,
                outcome_score,
                outcome_grade
            FROM ai_decision_outcome_history
            ORDER BY id DESC
            LIMIT 1
            """
        )
        latest_history = cursor.fetchone()
        cursor.connection.close()


        assert latest_history is not None, (
            "POST must create a latest Outcome History row"
        )

        assert latest_history[1] == "PENDING", (
            "New Outcome History must remain PENDING"
        )

        assert latest_history[2] == "COLLECTED", (
            "New Outcome History snapshot status must be COLLECTED"
        )

        assert latest_history[3] == "FUTURE_OUTCOME_EVALUATION", (
            "New Outcome History snapshot purpose must be FUTURE_OUTCOME_EVALUATION"
        )

        assert float(latest_history[4]) == 0.0, (
            "New Outcome History must not fabricate an outcome score"
        )

        assert latest_history[5] == "N/A", (
            "New Outcome History must not fabricate an outcome grade"
        )



        assert history_after_first == history_before + 1, (
            "POST must create exactly one Outcome History"
        )

        assert snapshot_after_first > snapshot_before, (
            "POST must create Portfolio Snapshot"
        )

        print("CASE 3 NEW HISTORY STATUS: PASS")
        print("CASE 4 SNAPSHOT STATUS: PASS")
        print("CASE 5 SNAPSHOT PURPOSE: PASS")
        print("CASE 6 NO FABRICATED OUTCOME SCORE: PASS")
        print("CASE 7 NO FABRICATED OUTCOME GRADE: PASS")
        print("CASE 8 POST OUTCOME PERSISTENCE: PASS")
        print("")
        print("OVERALL RESULT: PASS")
