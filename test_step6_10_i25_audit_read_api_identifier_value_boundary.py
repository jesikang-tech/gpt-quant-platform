import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import api_server


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i25_",
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
                '{"strategy": "GROWTH"}',
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
        print("Step6-10-I-25 Audit Read API Identifier Value Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 ZERO OUTCOME HISTORY ID")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=0"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["outcome_history_id"] == 0
        assert payload["events"] == []

        print("CASE 1: PASS")

        print("")
        print("CASE 2 NEGATIVE OUTCOME HISTORY ID")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=-1"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["outcome_history_id"] == -1
        assert payload["events"] == []

        print("CASE 2: PASS")

        print("")
        print("CASE 3 NON-INTEGER OUTCOME HISTORY ID")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=abc"
        )

        assert response.status_code == 400

        payload = response.get_json()

        assert payload["success"] is False
        assert payload["error"] == (
            "outcome_history_id or correlation_key is required"
        )

        print("CASE 3: PASS")

        print("")
        print("CASE 4 EMPTY CORRELATION KEY")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?correlation_key="
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["correlation_key"] == ""
        assert payload["events"] == []

        print("CASE 4: PASS")

        print("")
        print("CASE 5 WHITESPACE CORRELATION KEY")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?correlation_key=%20"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["correlation_key"] == " "
        assert payload["events"] == []

        print("CASE 5: PASS")

        print("")
        print("CASE 6 TRAILING WHITESPACE PRESERVED")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?correlation_key=outcome%3A501%20"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["correlation_key"] == "outcome:501 "
        assert payload["events"] == []

        print("CASE 6: PASS")

        print("")
        print("CASE 7 INVALID FILTER INTERSECTION")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=0"
            "&correlation_key=outcome%3A501"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["outcome_history_id"] == 0
        assert payload["correlation_key"] == "outcome:501"
        assert payload["events"] == []

        print("CASE 7: PASS")

        print("")
        print("CASE 8 READ-ONLY IDENTIFIER QUERY")

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
            "/api/ai-decision/audit-events"
            "?outcome_history_id=-1"
        )

        client.get(
            "/api/ai-decision/audit-events"
            "?correlation_key=%20"
        )

        client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=0"
            "&correlation_key=outcome%3A501"
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
