import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import api_server


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i30_",
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

        for index in range(101):
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
                    f"DEFAULT_LIMIT:{index}",
                    "OUTCOME_EVALUATED",
                    f"2026-08-31T12:{index // 60:02d}:{index % 60:02d}+09:00",
                    "portfolio_outcome_evaluation",
                    "EVALUATED",
                    501,
                    "outcome:501",
                    f'{{"sequence": {index}}}',
                ),
            )

        conn.commit()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE outcome_history_id = 501
            """
        )
        assert cursor.fetchone()[0] == 101

        conn.close()

        client = api_server.app.test_client()

        print("=" * 60)
        print("Step6-10-I-30 Audit Timeline Default Limit Projection Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 DEFAULT LIMIT APPLIED")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/timeline"
            "?outcome_history_id=501"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert len(payload["timeline"]) == 100

        print("CASE 1: PASS")

        print("")
        print("CASE 2 FIRST HUNDRED EVENTS PRESERVED")

        timeline = payload["timeline"]

        assert [
            event["details"]["sequence"]
            for event in timeline
        ] == list(range(100))

        print("CASE 2: PASS")

        print("")
        print("CASE 3 POSTFIX EVENT EXCLUDED")

        assert all(
            event["details"]["sequence"] < 100
            for event in timeline
        )

        assert not any(
            event["details"]["sequence"] == 100
            for event in timeline
        )

        print("CASE 3: PASS")

        print("")
        print("CASE 4 CHRONOLOGICAL ORDER PRESERVED")

        event_times = [
            event["event_time"]
            for event in timeline
        ]

        assert event_times == sorted(event_times)

        print("CASE 4: PASS")

        print("")
        print("CASE 5 PAYLOAD PRESERVATION")

        assert timeline[0]["details"] == {"sequence": 0}
        assert timeline[99]["details"] == {"sequence": 99}

        print("CASE 5: PASS")

        print("")
        print("CASE 6 READ-ONLY AUDIT SOURCE")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*),
                MIN(details),
                MAX(details)
            FROM audit_event
            WHERE outcome_history_id = 501
            """
        )

        before = cursor.fetchone()
        conn.close()

        client.get(
            "/api/ai-decision/audit-lifecycle/timeline"
            "?outcome_history_id=501"
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*),
                MIN(details),
                MAX(details)
            FROM audit_event
            WHERE outcome_history_id = 501
            """
        )

        after = cursor.fetchone()
        conn.close()

        assert before == after

        print("CASE 6: PASS")

        print("")
        print("CASE 7 NO SYNTHETIC EVENTS")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE outcome_history_id = 501
            """
        )

        assert cursor.fetchone()[0] == 101

        conn.close()

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
