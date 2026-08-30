import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import api_server


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i23_",
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
                '{"learning_signal": "POSITIVE"}',
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
        print("Step6-10-I-23 Audit Lifecycle Read API Response Schema")
        print("=" * 60)

        print("")
        print("CASE 1 AUDIT EVENTS RESPONSE ENVELOPE")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=501"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert set(payload.keys()) == {
            "success",
            "outcome_history_id",
            "correlation_key",
            "events",
        }

        assert isinstance(payload["success"], bool)
        assert payload["success"] is True
        assert payload["outcome_history_id"] == 501
        assert payload["correlation_key"] is None
        assert isinstance(payload["events"], list)

        print("CASE 1: PASS")

        print("")
        print("CASE 2 AUDIT EVENT ITEM SCHEMA")

        event = payload["events"][0]

        assert set(event.keys()) == {
            "id",
            "audit_event_id",
            "event_type",
            "event_time",
            "source",
            "status",
            "outcome_history_id",
            "correlation_key",
            "details",
        }

        assert isinstance(event["id"], int)
        assert isinstance(event["audit_event_id"], str)
        assert isinstance(event["event_type"], str)
        assert isinstance(event["event_time"], str)
        assert isinstance(event["source"], str)
        assert isinstance(event["status"], str)
        assert isinstance(event["outcome_history_id"], int)
        assert isinstance(event["correlation_key"], str)
        assert isinstance(event["details"], str)

        print("CASE 2: PASS")

        print("")
        print("CASE 3 TIMELINE RESPONSE SCHEMA")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/timeline"
            "?outcome_history_id=501"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert set(payload.keys()) == {
            "success",
            "outcome_history_id",
            "correlation_key",
            "timeline",
        }

        assert isinstance(payload["success"], bool)
        assert isinstance(payload["timeline"], list)
        assert len(payload["timeline"]) == 3

        timeline_event = payload["timeline"][0]

        assert set(timeline_event.keys()) == {
            "id",
            "audit_event_id",
            "event_type",
            "event_time",
            "source",
            "status",
            "outcome_history_id",
            "correlation_key",
            "details",
        }

        print("CASE 3: PASS")

        print("")
        print("CASE 4 COMPLETENESS RESPONSE SCHEMA")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/completeness"
            "?outcome_history_id=501"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert set(payload.keys()) == {
            "success",
            "completeness",
        }

        assert isinstance(payload["success"], bool)

        completeness = payload["completeness"]

        assert set(completeness.keys()) == {
            "outcome_history_id",
            "correlation_key",
            "lifecycle_status",
            "expected_event_types",
            "present_event_types",
            "missing_event_types",
            "event_count",
        }

        assert isinstance(
            completeness["lifecycle_status"],
            str,
        )
        assert isinstance(
            completeness["expected_event_types"],
            list,
        )
        assert isinstance(
            completeness["present_event_types"],
            list,
        )
        assert isinstance(
            completeness["missing_event_types"],
            list,
        )
        assert isinstance(
            completeness["event_count"],
            int,
        )

        print("CASE 4: PASS")

        print("")
        print("CASE 5 EMPTY RESPONSE SCHEMA")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=999"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert set(payload.keys()) == {
            "success",
            "outcome_history_id",
            "correlation_key",
            "events",
        }

        assert payload["success"] is True
        assert payload["events"] == []

        print("CASE 5: PASS")

        print("")
        print("CASE 6 EMPTY TIMELINE SCHEMA")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/timeline"
            "?outcome_history_id=999"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert set(payload.keys()) == {
            "success",
            "outcome_history_id",
            "correlation_key",
            "timeline",
        }

        assert payload["success"] is True
        assert payload["timeline"] == []

        print("CASE 6: PASS")

        print("")
        print("CASE 7 EMPTY COMPLETENESS SCHEMA")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/completeness"
            "?outcome_history_id=999"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert set(payload.keys()) == {
            "success",
            "completeness",
        }

        completeness = payload["completeness"]

        assert completeness["lifecycle_status"] == "EMPTY"
        assert completeness["event_count"] == 0

        print("CASE 7: PASS")

        print("")
        print("CASE 8 READ-ONLY RESPONSE CONTRACT")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            """
        )

        before = cursor.fetchone()[0]
        conn.close()

        client.get(
            "/api/ai-decision/audit-lifecycle/completeness"
            "?outcome_history_id=501"
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            """
        )

        after = cursor.fetchone()[0]
        conn.close()

        assert before == after

        print("CASE 8: PASS")

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
