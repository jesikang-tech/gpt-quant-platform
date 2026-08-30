import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import api_server


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i22_",
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
        print("Step6-10-I-22 Audit Read API Input Validation Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 MISSING QUERY BOUNDARY")

        response = client.get(
            "/api/ai-decision/audit-events"
        )

        assert response.status_code == 400

        print("CASE 1: PASS")

        print("")
        print("CASE 2 INVALID LIMIT AUDIT EVENTS")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=501&limit=abc"
        )

        assert response.status_code == 400
        assert response.get_json()["success"] is False

        print("CASE 2: PASS")

        print("")
        print("CASE 3 INVALID LIMIT TIMELINE")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/timeline"
            "?outcome_history_id=501&limit=abc"
        )

        assert response.status_code == 400
        assert response.get_json()["success"] is False

        print("CASE 3: PASS")

        print("")
        print("CASE 4 INVALID LIMIT COMPLETENESS")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/completeness"
            "?outcome_history_id=501&limit=abc"
        )

        assert response.status_code == 400
        assert response.get_json()["success"] is False

        print("CASE 4: PASS")

        print("")
        print("CASE 5 ZERO AND NEGATIVE LIMIT")

        for endpoint in [
            "/api/ai-decision/audit-events",
            "/api/ai-decision/audit-lifecycle/timeline",
            "/api/ai-decision/audit-lifecycle/completeness",
        ]:
            for value in ["0", "-1"]:
                response = client.get(
                    f"{endpoint}"
                    f"?outcome_history_id=501&limit={value}"
                )
                assert response.status_code == 400

        print("CASE 5: PASS")

        print("")
        print("CASE 6 VALID LIMIT PRESERVED")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=501&limit=2"
        )

        assert response.status_code == 200
        assert len(response.get_json()["events"]) == 2

        print("CASE 6: PASS")

        print("")
        print("CASE 7 ERROR RESPONSE CONTRACT")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=501&limit=abc"
        )

        payload = response.get_json()

        assert response.status_code == 400
        assert payload["success"] is False
        assert payload["error"] == "limit must be an integer"

        print("CASE 7: PASS")

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
