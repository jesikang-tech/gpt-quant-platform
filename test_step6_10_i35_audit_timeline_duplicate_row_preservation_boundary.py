import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i35_",
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
                "2026-08-31T17:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                501,
                "outcome:501",
                '{"order": 1}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-31T17:02:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                501,
                "outcome:501",
                '{"order": 2}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-31T17:03:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                501,
                "outcome:501",
                '{"duplicate": true, "order": 3}',
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "2026-08-31T17:04:00+09:00",
                "outcome_intelligence",
                "AVAILABLE",
                501,
                "outcome:501",
                '{"order": 4}',
            ),
            (
                "REASSESSMENT_REQUIRED",
                "2026-08-31T17:05:00+09:00",
                "outcome_intelligence",
                "REQUIRED",
                501,
                "outcome:501",
                '{"order": 5}',
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-31T17:06:00+09:00",
                "adaptive_strategy",
                "GENERATED",
                501,
                "outcome:501",
                '{"order": 6}',
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
            WHERE outcome_history_id = 501
            ORDER BY event_time ASC, id ASC
            """
        )

        before = cursor.fetchall()
        conn.close()

        print("=" * 60)
        print("Step6-10-I-35 Audit Timeline Duplicate Row Preservation Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 DUPLICATE ROW PRESERVED")

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501
        )

        assert len(timeline) == 6

        assert [
            event["event_type"]
            for event in timeline
        ] == [
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
            "OUTCOME_EVALUATED",
            "LEARNING_SIGNAL_GENERATED",
            "REASSESSMENT_REQUIRED",
            "ADAPTIVE_STRATEGY_GENERATED",
        ]

        print("CASE 1: PASS")

        print("")
        print("CASE 2 DUPLICATE EVENT TYPE NOT DEDUPLICATED")

        assert timeline[1]["event_type"] == "OUTCOME_EVALUATED"
        assert timeline[2]["event_type"] == "OUTCOME_EVALUATED"
        assert timeline[1]["id"] != timeline[2]["id"]

        print("CASE 2: PASS")

        print("")
        print("CASE 3 ROW ORDER PRESERVED")

        assert [
            event["event_time"]
            for event in timeline
        ] == [
            row[3]
            for row in before
        ]

        assert [
            event["id"]
            for event in timeline
        ] == [
            row[0]
            for row in before
        ]

        print("CASE 3: PASS")

        print("")
        print("CASE 4 DUPLICATE PAYLOAD PRESERVED")

        assert timeline[1]["details"] == {
            "order": 2
        }

        assert timeline[2]["details"] == {
            "duplicate": True,
            "order": 3
        }

        print("CASE 4: PASS")

        print("")
        print("CASE 5 NO SYNTHETIC DEDUPLICATION")

        assert len(timeline) == len(before)
        assert timeline[1]["id"] != timeline[2]["id"]

        print("CASE 5: PASS")

        print("")
        print("CASE 6 FILTERED DUPLICATE ROWS PRESERVED")

        filtered = repository.get_ai_decision_audit_lifecycle_timeline(
            correlation_key="outcome:501"
        )

        assert len(filtered) == 6

        assert [
            event["event_type"]
            for event in filtered
        ][1:3] == [
            "OUTCOME_EVALUATED",
            "OUTCOME_EVALUATED",
        ]

        print("CASE 6: PASS")

        print("")
        print("CASE 7 READ-ONLY AUDIT SOURCE")

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

        print("CASE 7: PASS")

        print("")
        print("CASE 8 COMPLETENESS REMAINS DEDUPLICATED")

        completeness = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501
        )

        assert completeness["event_count"] == 6
        assert completeness["present_event_types"] == [
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
            "LEARNING_SIGNAL_GENERATED",
            "REASSESSMENT_REQUIRED",
            "ADAPTIVE_STRATEGY_GENERATED",
        ]
        assert completeness["lifecycle_status"] == "COMPLETE"

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
