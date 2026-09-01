import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository
import api_server


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="phase8_6_f_",
        suffix=".db"
    )
    os.close(fd)

    original_config_path = config.DATABASE_PATH
    original_database_path = database.DATABASE_PATH

    try:
        test_db_path = Path(db_path)

        config.DATABASE_PATH = test_db_path
        database.DATABASE_PATH = test_db_path

        database.init_database()

        conn = database.get_connection()
        cursor = conn.cursor()

        created_at = "2026-08-20T13:00:02+09:00"

        cursor.execute(
            """
            INSERT INTO ai_decision_outcome_history
            (
                decision,
                action,
                strategy,
                confidence_score,
                intelligence_score,
                outcome_status,
                snapshot_status,
                snapshot_purpose,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "MAINTAIN",
                "PROCEED",
                "MAINTAIN",
                93.2,
                89.6,
                "PENDING",
                "COLLECTED",
                "FUTURE_OUTCOME_EVALUATION",
                created_at,
            ),
        )

        history_id = cursor.lastrowid
        correlation_key = f"outcome:{history_id}"

        cursor.execute(
            """
            INSERT INTO ai_decision_portfolio_snapshot
            (
                history_id,
                ticker,
                weight,
                reference_price,
                created_at,
                reference_price_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                history_id,
                "306950",
                100.0,
                67560.0,
                created_at,
                "2026-08-20",
            ),
        )

        cursor.execute(
            """
            INSERT INTO etf_prices
            (
                ticker,
                date,
                close_price
            )
            VALUES (?, ?, ?)
            """,
            (
                "306950",
                "2026-08-21",
                68404.5,
            ),
        )

        conn.commit()
        conn.close()

        evaluation_date = "2026-08-21"

        print("=" * 60)
        print("Phase8-6-F Runtime Evaluation Read-Back Contract")
        print("=" * 60)

        print("")
        print("CASE 1 REAL EVALUATION")
        evaluation = repository.evaluate_ai_decision_portfolio_snapshot(
            history_id=history_id,
            evaluation_date=evaluation_date,
        )

        assert evaluation["evaluation_status"] == "EVALUATED"
        assert evaluation["outcome_status"] == "EVALUATED"
        assert evaluation["portfolio_return"] == 1.25
        assert evaluation["evaluation_date"] == evaluation_date

        print(
            "CASE 1: PASS | "
            f"status={evaluation['evaluation_status']} | "
            f"return={evaluation['portfolio_return']}"
        )

        client = api_server.app.test_client()

        print("")
        print("CASE 2 OUTCOME HISTORY API READ-BACK")
        response = client.get("/api/ai-decision/outcome-history")

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True

        matching = [
            item
            for item in payload["history"]
            if item["id"] == history_id
        ]

        assert len(matching) == 1

        history = matching[0]

        assert history["outcome_status"] == "EVALUATED"
        assert history["portfolio_return"] == 1.25
        assert history["portfolio_evaluation_date"] == evaluation_date
        assert history["decision"] == "MAINTAIN"
        assert history["action"] == "PROCEED"
        assert history["strategy"] == "MAINTAIN"

        print(
            "CASE 2: PASS | "
            f"status={history['outcome_status']} | "
            f"return={history['portfolio_return']} | "
            f"date={history['portfolio_evaluation_date']}"
        )

        print("")
        print("CASE 3 AUDIT EVENTS API READ-BACK")
        response = client.get(
            f"/api/ai-decision/audit-events"
            f"?outcome_history_id={history_id}"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["outcome_history_id"] == history_id

        events = payload["events"]

        assert len(events) == 2
        assert events[0]["event_type"] == "OUTCOME_EVALUATION_STARTED"
        assert events[0]["status"] == "STARTED"
        assert events[1]["event_type"] == "OUTCOME_EVALUATED"
        assert events[1]["status"] == "EVALUATED"

        assert all(
            event["outcome_history_id"] == history_id
            for event in events
        )

        assert all(
            event["correlation_key"] == correlation_key
            for event in events
        )

        print(
            "CASE 3: PASS | "
            f"events={len(events)} | "
            f"correlation={correlation_key}"
        )

        print("")
        print("CASE 4 AUDIT LIFECYCLE TIMELINE READ-BACK")
        response = client.get(
            f"/api/ai-decision/audit-lifecycle/"
            f"timeline?outcome_history_id={history_id}"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["outcome_history_id"] == history_id

        timeline = payload["timeline"]

        assert len(timeline) == 2
        assert [
            event["event_type"]
            for event in timeline
        ] == [
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
        ]

        print(
            "CASE 4: PASS | "
            f"timeline_events={len(timeline)}"
        )

        print("")
        print("CASE 5 LIFECYCLE COMPLETENESS READ-BACK")
        response = client.get(
            f"/api/ai-decision/audit-lifecycle/"
            f"completeness?outcome_history_id={history_id}"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True

        completeness = payload["completeness"]

        assert completeness["outcome_history_id"] == history_id
        assert completeness["correlation_key"] == correlation_key
        assert completeness["event_count"] == 2
        assert completeness["lifecycle_status"] == "PARTIAL"

        assert "LEARNING_SIGNAL_GENERATED" in (
            completeness["missing_event_types"]
        )

        assert "ADAPTIVE_STRATEGY_GENERATED" in (
            completeness["missing_event_types"]
        )

        assert "REASSESSMENT_REQUIRED" in (
            completeness["missing_event_types"]
        )

        print(
            "CASE 5: PASS | "
            f"status={completeness['lifecycle_status']} | "
            f"events={completeness['event_count']}"
        )

        print("")
        print("CASE 6 READ-BACK DOES NOT MUTATE BUSINESS STATE")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                outcome_status,
                portfolio_return,
                portfolio_evaluation_date
            FROM ai_decision_outcome_history
            WHERE id = ?
            """,
            (history_id,),
        )

        before = cursor.fetchone()
        conn.close()

        client.get(
            f"/api/ai-decision/audit-lifecycle/"
            f"completeness?outcome_history_id={history_id}"
        )

        client.get(
            f"/api/ai-decision/audit-lifecycle/"
            f"timeline?outcome_history_id={history_id}"
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                outcome_status,
                portfolio_return,
                portfolio_evaluation_date
            FROM ai_decision_outcome_history
            WHERE id = ?
            """,
            (history_id,),
        )

        after = cursor.fetchone()

        conn.close()

        assert after == before

        print(
            "CASE 6: PASS | "
            f"state={after}"
        )

        print("")
        print("CASE 7 SAME-DATE IDEMPOTENT READ-BACK")

        second = repository.evaluate_ai_decision_portfolio_snapshot(
            history_id=history_id,
            evaluation_date=evaluation_date,
        )

        assert second["evaluation_status"] == "EVALUATED"
        assert second["portfolio_return"] == 1.25
        assert second["positions"] == []

        response = client.get(
            f"/api/ai-decision/audit-events"
            f"?outcome_history_id={history_id}"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert len(payload["events"]) == 2

        evaluated_events = [
            event
            for event in payload["events"]
            if event["event_type"] == "OUTCOME_EVALUATED"
        ]

        assert len(evaluated_events) == 1

        print(
            "CASE 7: PASS | "
            "same-date re-evaluation preserved read-back state"
        )

        print("")
        print("=" * 60)
        print("OVERALL RESULT: PASS")
        print("=" * 60)

    finally:
        config.DATABASE_PATH = original_config_path
        database.DATABASE_PATH = original_database_path

        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass


run_test()
