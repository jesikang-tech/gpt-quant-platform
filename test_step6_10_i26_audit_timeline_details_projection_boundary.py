import json
import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i26_",
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
                "not-valid-json",
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-30T15:05:00+09:00",
                "adaptive_strategy",
                "GENERATED",
                501,
                "outcome:501",
                "",
            ),
            (
                "OUTCOME_EVALUATION_STARTED",
                "2026-08-30T15:06:00+09:00",
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
            SELECT details
            FROM audit_event
            WHERE outcome_history_id = 501
            ORDER BY event_time ASC, id ASC
            """
        )
        before_details = cursor.fetchall()

        conn.close()

        print("")
        print("CASE 1 MALFORMED JSON FALLBACK")

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501
        )

        assert timeline[3]["details"] == {}

        print("CASE 1: PASS")

        print("")
        print("CASE 2 EMPTY STRING FALLBACK")

        assert timeline[4]["details"] == {}

        print("CASE 2: PASS")

        print("")
        print("CASE 3 VALID JSON OBJECT PRESERVED")

        assert timeline[0]["details"] == {
            "actual_outcome_gate": True
        }
        assert timeline[1]["details"] == {
            "portfolio_return": 0.05
        }

        print("CASE 3: PASS")

        print("")
        print("CASE 4 VALID JSON SCALAR PRESERVED")

        assert timeline[5]["details"] == "scalar"

        print("CASE 4: PASS")

        print("")
        print("CASE 5 NO SYNTHETIC DETAIL INFERENCE")

        assert timeline[3]["details"] == {}
        assert timeline[4]["details"] == {}

        print("CASE 5: PASS")

        print("")
        print("CASE 6 READ-ONLY AUDIT SOURCE")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT details
            FROM audit_event
            WHERE outcome_history_id = 501
            ORDER BY event_time ASC, id ASC
            """
        )
        after_details = cursor.fetchall()

        conn.close()

        assert before_details == after_details

        print("CASE 6: PASS")

        print("")
        print("CASE 7 BUSINESS STATE UNCHANGED")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                outcome_status,
                reassessment_required,
                reassessment_status
            FROM ai_decision_outcome_history
            WHERE id = ?
            """,
            (501,)
        )

        before_state = cursor.fetchone()
        conn.close()

        repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                outcome_status,
                reassessment_required,
                reassessment_status
            FROM ai_decision_outcome_history
            WHERE id = ?
            """,
            (501,)
        )

        after_state = cursor.fetchone()
        conn.close()

        assert before_state == after_state

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


print("=" * 60)
print("Step6-10-I-26 Audit Timeline Details Projection Boundary")
print("=" * 60)

run_test()
