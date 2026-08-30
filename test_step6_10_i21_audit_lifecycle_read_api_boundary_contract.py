import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import api_server


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i21_",
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

        events = [
            (
                "OUTCOME_EVALUATION_STARTED",
                "2026-08-30T15:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                501,
                "outcome:501",
                '{"actual_outcome_gate": true}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-30T15:02:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                501,
                "outcome:501",
                '{"portfolio_return": 0.05}',
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "2026-08-30T15:03:00+09:00",
                "outcome_intelligence",
                "AVAILABLE",
                501,
                "outcome:501",
                '{"learning_signal": "POSITIVE", "learning_signal_strength": 0.8}',
            ),
            (
                "REASSESSMENT_REQUIRED",
                "2026-08-30T15:04:00+09:00",
                "outcome_intelligence",
                "REQUIRED",
                501,
                "outcome:501",
                '{"reassessment_required": false}',
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-30T15:05:00+09:00",
                "adaptive_strategy",
                "GENERATED",
                501,
                "outcome:501",
                '{"strategy": "GROWTH", "action": "INCREASE_RISK"}',
            ),
            (
                "OUTCOME_EVALUATION_STARTED",
                "2026-08-30T16:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                502,
                "outcome:502",
                '{"actual_outcome_gate": true}',
            ),
        ]

        for event in events:
            cursor.execute(
                """
                INSERT INTO audit_event
                (
                    audit_event_id,
                    event_type,
                    event_time,
                    source,
                    status,
                    outcome_history_id,
                    correlation_key,
                    details
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"{event[0]}:{event[5]}:{event[1]}",
                    event[0],
                    event[1],
                    event[2],
                    event[3],
                    event[4],
                    event[5],
                    event[6],
                ),
            )

        conn.commit()
        conn.close()

        client = api_server.app.test_client()

        print("=" * 60)
        print("Step6-10-I-21 Audit Lifecycle Read API Boundary Contract")
        print("=" * 60)

        print("")
        print("CASE 1 API MODULE LOAD")
        assert api_server.app is not None
        print("CASE 1: PASS")

        print("")
        print("CASE 2 AUDIT EVENTS API")
        response = client.get(
            "/api/ai-decision/audit-events?outcome_history_id=501"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["outcome_history_id"] == 501
        assert len(payload["events"]) == 5
        assert all(
            event["outcome_history_id"] == 501
            for event in payload["events"]
        )

        print(
            "CASE 2: PASS | "
            f"events={len(payload['events'])}"
        )

        print("")
        print("CASE 3 LIFECYCLE TIMELINE API")
        response = client.get(
            "/api/ai-decision/audit-lifecycle/"
            "timeline?outcome_history_id=501"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["outcome_history_id"] == 501
        assert [
            event["event_type"]
            for event in payload["timeline"]
        ] == [
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
            "LEARNING_SIGNAL_GENERATED",
            "REASSESSMENT_REQUIRED",
            "ADAPTIVE_STRATEGY_GENERATED",
        ]

        print(
            "CASE 3: PASS | "
            f"events={len(payload['timeline'])}"
        )

        print("")
        print("CASE 4 LIFECYCLE COMPLETENESS API")
        response = client.get(
            "/api/ai-decision/audit-lifecycle/"
            "completeness?outcome_history_id=501"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["completeness"]["outcome_history_id"] == 501
        assert (
            payload["completeness"]["lifecycle_status"]
            == "COMPLETE"
        )
        assert payload["completeness"]["event_count"] == 5
        assert payload["completeness"]["missing_event_types"] == []

        print(
            "CASE 4: PASS | "
            f"status={payload['completeness']['lifecycle_status']}"
        )

        print("")
        print("CASE 5 CORRELATION KEY BOUNDARY")
        response = client.get(
            "/api/ai-decision/audit-lifecycle/"
            "timeline?correlation_key=outcome%3A501"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["correlation_key"] == "outcome:501"
        assert len(payload["timeline"]) == 5
        assert all(
            event["correlation_key"] == "outcome:501"
            for event in payload["timeline"]
        )

        print("CASE 5: PASS")

        print("")
        print("CASE 6 NO CROSS-OUTCOME CONTAMINATION")
        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=501"
        )

        payload = response.get_json()

        assert not any(
            event["outcome_history_id"] == 502
            for event in payload["events"]
        )

        print("CASE 6: PASS")

        print("")
        print("CASE 7 READ-ONLY BUSINESS STATE")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*)
            FROM ai_decision_outcome_history
            """
        )

        before = cursor.fetchone()[0]

        conn.close()

        client.get(
            "/api/ai-decision/audit-lifecycle/"
            "completeness?outcome_history_id=501"
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*)
            FROM ai_decision_outcome_history
            """
        )

        after = cursor.fetchone()[0]

        conn.close()

        assert before == after

        print("CASE 7: PASS")

        print("")
        print("CASE 8 NO SYNTHETIC EVENT INFERENCE")
        response = client.get(
            "/api/ai-decision/audit-lifecycle/"
            "completeness?outcome_history_id=999"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["completeness"]["lifecycle_status"] == "EMPTY"
        assert payload["completeness"]["event_count"] == 0

        print(
            "CASE 8: PASS | "
            "no synthetic events"
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
