import json
import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import api_server


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i27_",
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
                "2026-08-31T09:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                501,
                "outcome:501",
                '{"actual_outcome_gate": true}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-31T09:02:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                501,
                "outcome:501",
                '{"portfolio_return": 0.05}',
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "2026-08-31T09:03:00+09:00",
                "outcome_intelligence",
                "AVAILABLE",
                501,
                "outcome:501",
                '{"learning_signal": "POSITIVE"}',
            ),
            (
                "REASSESSMENT_REQUIRED",
                "2026-08-31T09:04:00+09:00",
                "outcome_intelligence",
                "REQUIRED",
                501,
                "outcome:501",
                "not-valid-json",
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-31T09:05:00+09:00",
                "adaptive_strategy",
                "GENERATED",
                501,
                "outcome:501",
                "",
            ),
            (
                "OUTCOME_EVALUATION_STARTED",
                "2026-08-31T09:06:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                501,
                "outcome:501",
                '"scalar"',
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

        cursor.execute(
            """
            SELECT
                audit_event_id,
                details
            FROM audit_event
            WHERE outcome_history_id = 501
            ORDER BY event_time ASC, id ASC
            """
        )

        before_details = cursor.fetchall()
        conn.close()

        client = api_server.app.test_client()

        print("=" * 60)
        print("Step6-10-I-27 Audit Timeline Details API Projection Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 API RESPONSE SUCCESS")

        response = client.get(
            "/api/ai-decision/audit-lifecycle/timeline"
            "?outcome_history_id=501"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["outcome_history_id"] == 501
        assert len(payload["timeline"]) == 6

        print("CASE 1: PASS")

        print("")
        print("CASE 2 VALID JSON OBJECT PRESERVED")

        assert payload["timeline"][0]["details"] == {
            "actual_outcome_gate": True
        }
        assert payload["timeline"][1]["details"] == {
            "portfolio_return": 0.05
        }

        print("CASE 2: PASS")

        print("")
        print("CASE 3 VALID JSON SCALAR PRESERVED")

        assert payload["timeline"][5]["details"] == "scalar"

        print("CASE 3: PASS")

        print("")
        print("CASE 4 MALFORMED JSON FALLBACK")

        assert payload["timeline"][3]["details"] == {}

        print("CASE 4: PASS")

        print("")
        print("CASE 5 EMPTY STRING FALLBACK")

        assert payload["timeline"][4]["details"] == {}

        print("CASE 5: PASS")

        print("")
        print("CASE 6 NO SYNTHETIC DETAIL TRANSFORMATION")

        assert payload["timeline"][3]["details"] == {}
        assert payload["timeline"][4]["details"] == {}
        assert payload["timeline"][5]["details"] == "scalar"

        print("CASE 6: PASS")

        print("")
        print("CASE 7 READ-ONLY AUDIT SOURCE")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                audit_event_id,
                details
            FROM audit_event
            WHERE outcome_history_id = 501
            ORDER BY event_time ASC, id ASC
            """
        )

        after_details = cursor.fetchall()
        conn.close()

        assert before_details == after_details

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
