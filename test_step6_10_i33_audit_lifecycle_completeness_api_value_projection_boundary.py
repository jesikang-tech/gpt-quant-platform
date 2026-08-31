import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import api_server


EXPECTED_LIFECYCLE = [
    "OUTCOME_EVALUATION_STARTED",
    "OUTCOME_EVALUATED",
    "LEARNING_SIGNAL_GENERATED",
    "REASSESSMENT_REQUIRED",
    "ADAPTIVE_STRATEGY_GENERATED",
]


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i33_",
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
                "2026-08-31T15:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                501,
                "outcome:501",
                '{"step": 1}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-31T15:02:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                501,
                "outcome:501",
                '{"step": 2}',
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "2026-08-31T15:03:00+09:00",
                "outcome_intelligence",
                "AVAILABLE",
                501,
                "outcome:501",
                '{"step": 3}',
            ),
            (
                "REASSESSMENT_REQUIRED",
                "2026-08-31T15:04:00+09:00",
                "outcome_intelligence",
                "REQUIRED",
                501,
                "outcome:501",
                '{"step": 4}',
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-31T15:05:00+09:00",
                "adaptive_strategy",
                "GENERATED",
                501,
                "outcome:501",
                '{"step": 5}',
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
        print("Step6-10-I-33 Audit Lifecycle Completeness API Value Projection Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 COMPLETE VALUE PROJECTION")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/completeness"
            "?outcome_history_id=501&limit=5"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True

        completeness = payload["completeness"]

        assert completeness["outcome_history_id"] == 501
        assert completeness["correlation_key"] == "outcome:501"
        assert completeness["lifecycle_status"] == "COMPLETE"
        assert completeness["expected_event_types"] == EXPECTED_LIFECYCLE
        assert completeness["present_event_types"] == EXPECTED_LIFECYCLE
        assert completeness["missing_event_types"] == []
        assert completeness["event_count"] == 5

        print("CASE 1: PASS")

        print("")
        print("CASE 2 PARTIAL VALUE PROJECTION")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/completeness"
            "?outcome_history_id=501&limit=3"
        )

        assert response.status_code == 200

        payload = response.get_json()
        completeness = payload["completeness"]

        assert completeness["outcome_history_id"] == 501
        assert completeness["correlation_key"] == "outcome:501"
        assert completeness["lifecycle_status"] == "PARTIAL"
        assert completeness["expected_event_types"] == EXPECTED_LIFECYCLE
        assert completeness["present_event_types"] == EXPECTED_LIFECYCLE[:3]
        assert completeness["missing_event_types"] == EXPECTED_LIFECYCLE[3:]
        assert completeness["event_count"] == 3

        print("CASE 2: PASS")

        print("")
        print("CASE 3 CORRELATION FILTER VALUE PROJECTION")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/completeness"
            "?correlation_key=outcome:501&limit=2"
        )

        assert response.status_code == 200

        payload = response.get_json()
        completeness = payload["completeness"]

        assert completeness["outcome_history_id"] == 501
        assert completeness["correlation_key"] == "outcome:501"
        assert completeness["lifecycle_status"] == "PARTIAL"
        assert completeness["present_event_types"] == EXPECTED_LIFECYCLE[:2]
        assert completeness["missing_event_types"] == EXPECTED_LIFECYCLE[2:]
        assert completeness["event_count"] == 2

        print("CASE 3: PASS")

        print("")
        print("CASE 4 EMPTY VALUE PROJECTION")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/completeness"
            "?outcome_history_id=999"
        )

        assert response.status_code == 200

        payload = response.get_json()
        completeness = payload["completeness"]

        assert completeness["outcome_history_id"] == 999
        assert completeness["correlation_key"] is None
        assert completeness["lifecycle_status"] == "EMPTY"
        assert completeness["expected_event_types"] == EXPECTED_LIFECYCLE
        assert completeness["present_event_types"] == []
        assert completeness["missing_event_types"] == EXPECTED_LIFECYCLE
        assert completeness["event_count"] == 0

        print("CASE 4: PASS")

        print("")
        print("CASE 5 NO SYNTHETIC VALUE TRANSFORMATION")

        assert completeness["present_event_types"] == []
        assert completeness["missing_event_types"] == EXPECTED_LIFECYCLE
        assert completeness["event_count"] == 0

        print("CASE 5: PASS")

        print("")
        print("CASE 6 READ-ONLY AUDIT SOURCE")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                audit_event_id,
                event_type,
                event_time,
                source,
                status,
                outcome_history_id,
                correlation_key,
                details
            FROM audit_event
            ORDER BY event_time ASC, id ASC
            """
        )

        before = cursor.fetchall()
        conn.close()

        client.get(
            "/api/ai-decision/audit-lifecycle/completeness"
            "?outcome_history_id=501&limit=3"
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                audit_event_id,
                event_type,
                event_time,
                source,
                status,
                outcome_history_id,
                correlation_key,
                details
            FROM audit_event
            ORDER BY event_time ASC, id ASC
            """
        )

        after = cursor.fetchall()
        conn.close()

        assert before == after

        print("CASE 6: PASS")

        print("")
        print("CASE 7 NO SYNTHETIC EVENT CREATION")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            """
        )

        before_count = cursor.fetchone()[0]
        conn.close()

        client.get(
            "/api/ai-decision/audit-lifecycle/completeness"
            "?outcome_history_id=501&limit=3"
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            """
        )

        after_count = cursor.fetchone()[0]
        conn.close()

        assert before_count == after_count

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
