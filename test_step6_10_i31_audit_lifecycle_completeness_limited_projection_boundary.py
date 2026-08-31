import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


EXPECTED_LIFECYCLE = [
    "OUTCOME_EVALUATION_STARTED",
    "OUTCOME_EVALUATED",
    "LEARNING_SIGNAL_GENERATED",
    "REASSESSMENT_REQUIRED",
    "ADAPTIVE_STRATEGY_GENERATED",
]


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i31_",
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
                "2026-08-31T13:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                501,
                "outcome:501",
                '{"step": 1}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-31T13:02:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                501,
                "outcome:501",
                '{"step": 2}',
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "2026-08-31T13:03:00+09:00",
                "outcome_intelligence",
                "AVAILABLE",
                501,
                "outcome:501",
                '{"step": 3}',
            ),
            (
                "REASSESSMENT_REQUIRED",
                "2026-08-31T13:04:00+09:00",
                "outcome_intelligence",
                "REQUIRED",
                501,
                "outcome:501",
                '{"step": 4}',
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-31T13:05:00+09:00",
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

        print("=" * 60)
        print("Step6-10-I-31 Audit Lifecycle Completeness Limited Projection Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 FULL LIMIT REMAINS COMPLETE")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501,
            limit=5,
        )

        assert result["lifecycle_status"] == "COMPLETE"
        assert result["event_count"] == 5
        assert result["present_event_types"] == EXPECTED_LIFECYCLE
        assert result["missing_event_types"] == []

        print("CASE 1: PASS")

        print("")
        print("CASE 2 LIMITED PROJECTION BECOMES PARTIAL")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501,
            limit=3,
        )

        assert result["lifecycle_status"] == "PARTIAL"
        assert result["event_count"] == 3
        assert result["present_event_types"] == EXPECTED_LIFECYCLE[:3]
        assert result["missing_event_types"] == EXPECTED_LIFECYCLE[3:]

        print("CASE 2: PASS")

        print("")
        print("CASE 3 SINGLE EVENT PROJECTION")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501,
            limit=1,
        )

        assert result["lifecycle_status"] == "PARTIAL"
        assert result["event_count"] == 1
        assert result["present_event_types"] == [
            EXPECTED_LIFECYCLE[0]
        ]
        assert result["missing_event_types"] == EXPECTED_LIFECYCLE[1:]

        print("CASE 3: PASS")

        print("")
        print("CASE 4 LIMITED PROJECTION IS NOT SYNTHETIC")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501,
            limit=3,
        )

        assert result["present_event_types"] == [
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
            "LEARNING_SIGNAL_GENERATED",
        ]

        assert "REASSESSMENT_REQUIRED" not in result["present_event_types"]
        assert "ADAPTIVE_STRATEGY_GENERATED" not in result["present_event_types"]

        print("CASE 4: PASS")

        print("")
        print("CASE 5 CORRELATION FILTER PRESERVED")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            correlation_key="outcome:501",
            limit=3,
        )

        assert result["lifecycle_status"] == "PARTIAL"
        assert result["event_count"] == 3
        assert result["outcome_history_id"] == 501
        assert result["correlation_key"] == "outcome:501"

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
                details
            FROM audit_event
            WHERE outcome_history_id = 501
            ORDER BY event_time ASC, id ASC
            """
        )

        before = cursor.fetchall()
        conn.close()

        repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501,
            limit=3,
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
                details
            FROM audit_event
            WHERE outcome_history_id = 501
            ORDER BY event_time ASC, id ASC
            """
        )

        after = cursor.fetchall()
        conn.close()

        assert before == after

        print("CASE 6: PASS")

        print("")
        print("CASE 7 BUSINESS STATE UNCHANGED")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM ai_decision_outcome_history
            """
        )

        before_count = cursor.fetchone()[0]
        conn.close()

        repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501,
            limit=3,
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM ai_decision_outcome_history
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
