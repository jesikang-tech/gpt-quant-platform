import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i29_",
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
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-31T11:01:00+09:00",
                "adaptive_strategy",
                "GENERATED",
                501,
                "outcome:501",
                '{"order": 3}',
            ),
            (
                "OUTCOME_EVALUATION_STARTED",
                "2026-08-31T11:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                501,
                "outcome:501",
                '{"order": 1}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-31T11:01:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                501,
                "outcome:501",
                '{"order": 2}',
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "2026-08-31T11:02:00+09:00",
                "outcome_intelligence",
                "AVAILABLE",
                501,
                "outcome:501",
                '{"order": 4}',
            ),
        ]

        for index, event in enumerate(events):
            details = event[6] if len(event) > 6 else event[6]
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
                    f"{event[0]}:{event[5]}:{event[1]}:{index}",
                    event[0],
                    event[1],
                    event[2],
                    event[3],
                    event[4],
                    event[5],
                    details,
                ),
            )

        conn.commit()

        cursor.execute(
            """
            SELECT id, event_type, event_time
            FROM audit_event
            WHERE outcome_history_id = 501
            ORDER BY id ASC
            """
        )

        inserted = cursor.fetchall()
        conn.close()

        print("=" * 60)
        print("Step6-10-I-29 Audit Timeline Deterministic Tie-Break Ordering Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 SAME-TIMESTAMP ID ORDER")

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501
        )

        assert [
            event["event_type"]
            for event in timeline
        ] == [
            "ADAPTIVE_STRATEGY_GENERATED",
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
            "LEARNING_SIGNAL_GENERATED",
        ]

        same_time_ids = [
            event["id"]
            for event in timeline[:3]
        ]

        assert same_time_ids == sorted(same_time_ids)

        print("CASE 1: PASS")

        print("")
        print("CASE 2 SAME-TIMESTAMP DETERMINISM")

        timeline_again = (
            repository.get_ai_decision_audit_lifecycle_timeline(
                outcome_history_id=501
            )
        )

        assert timeline_again == timeline

        print("CASE 2: PASS")

        print("")
        print("CASE 3 LIMIT PRESERVES TIE-BREAK PREFIX")

        limited = repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501,
            limit=2,
        )

        assert len(limited) == 2
        assert [
            event["event_type"]
            for event in limited
        ] == [
            "ADAPTIVE_STRATEGY_GENERATED",
            "OUTCOME_EVALUATION_STARTED",
        ]

        assert [
            event["id"]
            for event in limited
        ] == sorted(event["id"] for event in limited)

        print("CASE 3: PASS")

        print("")
        print("CASE 4 FILTER PRESERVES TIE-BREAK ORDER")

        filtered = repository.get_ai_decision_audit_lifecycle_timeline(
            correlation_key="outcome:501",
            limit=3,
        )

        assert [
            event["event_type"]
            for event in filtered
        ] == [
            "ADAPTIVE_STRATEGY_GENERATED",
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
        ]

        assert [
            event["id"]
            for event in filtered
        ] == sorted(event["id"] for event in filtered)

        print("CASE 4: PASS")

        print("")
        print("CASE 5 PAYLOAD PRESERVATION")

        assert filtered[0]["details"] == {"order": 3}
        assert filtered[1]["details"] == {"order": 1}
        assert filtered[2]["details"] == {"order": 2}

        print("CASE 5: PASS")

        print("")
        print("CASE 6 NO SYNTHETIC REORDERING")

        assert len(timeline) == len(inserted)
        assert {
            event["id"]
            for event in timeline
        } == {
            row[0]
            for row in inserted
        }

        print("CASE 6: PASS")

        print("")
        print("CASE 7 READ-ONLY SOURCE")

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
            ORDER BY id ASC
            """
        )

        before = cursor.fetchall()
        conn.close()

        repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501
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
            ORDER BY id ASC
            """
        )

        after = cursor.fetchall()
        conn.close()

        assert before == after

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


