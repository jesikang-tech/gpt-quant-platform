import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i28_",
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
                "2026-08-31T10:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                501,
                "outcome:501",
                '{"step": 1}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-31T10:02:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                501,
                "outcome:501",
                '{"step": 2}',
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "2026-08-31T10:03:00+09:00",
                "outcome_intelligence",
                "AVAILABLE",
                501,
                "outcome:501",
                '{"step": 3}',
            ),
            (
                "REASSESSMENT_REQUIRED",
                "2026-08-31T10:04:00+09:00",
                "outcome_intelligence",
                "REQUIRED",
                501,
                "outcome:501",
                '{"step": 4}',
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-31T10:05:00+09:00",
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
        print("Step6-10-I-28 Audit Timeline Limit Prefix Projection Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 LIMIT THREE PREFIX")

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501,
            limit=3,
        )

        assert len(timeline) == 3
        assert [
            event["event_type"]
            for event in timeline
        ] == [
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
            "LEARNING_SIGNAL_GENERATED",
        ]

        print("CASE 1: PASS")

        print("")
        print("CASE 2 LIMIT ONE PREFIX")

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501,
            limit=1,
        )

        assert len(timeline) == 1
        assert timeline[0]["event_type"] == (
            "OUTCOME_EVALUATION_STARTED"
        )

        print("CASE 2: PASS")

        print("")
        print("CASE 3 NO POSTFIX LEAKAGE")

        assert all(
            event["event_type"]
            not in {
                "REASSESSMENT_REQUIRED",
                "ADAPTIVE_STRATEGY_GENERATED",
            }
            for event in timeline
        )

        print("CASE 3: PASS")

        print("")
        print("CASE 4 FILTERED PREFIX")

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
            correlation_key="outcome:501",
            limit=2,
        )

        assert len(timeline) == 2
        assert [
            event["event_type"]
            for event in timeline
        ] == [
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
        ]

        print("CASE 4: PASS")

        print("")
        print("CASE 5 PAYLOAD PRESERVATION")

        assert timeline[0]["details"] == {"step": 1}
        assert timeline[1]["details"] == {"step": 2}

        print("CASE 5: PASS")

        print("")
        print("CASE 6 READ-ONLY SOURCE")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
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

        repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501,
            limit=3,
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
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
        print("CASE 7 NO SYNTHETIC EVENTS")

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501,
            limit=10,
        )

        assert len(timeline) == 5

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
