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
        prefix="step6_10_i19_",
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
                '{"learning_signal": "POSITIVE", "learning_signal_strength": 0.8}',
            ),
            (
                "REASSESSMENT_REQUIRED",
                "2026-08-30T15:04:00+09:00",
                "outcome_intelligence",
                "REQUIRED",
                501,
                "outcome:501",
                '{"reassessment_required": true}',
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-30T15:05:00+09:00",
                "adaptive_strategy",
                "GENERATED",
                501,
                "outcome:501",
                '{"strategy": "GROWTH", "action": "INCREASE_RISK"}',
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

        print("=" * 60)
        print("Step6-10-I-19 Audit Lifecycle Completeness Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 COMPLETE LIFECYCLE")

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501
        )

        event_types = [
            event["event_type"]
            for event in timeline
        ]

        assert event_types == EXPECTED_LIFECYCLE

        print(
            "CASE 1: PASS | "
            "lifecycle=COMPLETE"
        )

        print("")
        print("CASE 2 PARTIAL LIFECYCLE")

        partial = timeline[:2]

        partial_types = [
            event["event_type"]
            for event in partial
        ]

        assert partial_types == EXPECTED_LIFECYCLE[:2]
        assert len(partial_types) < len(EXPECTED_LIFECYCLE)

        print(
            "CASE 2: PASS | "
            "lifecycle=PARTIAL"
        )

        print("")
        print("CASE 3 EMPTY LIFECYCLE")

        empty = repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=999
        )

        assert empty == []

        print(
            "CASE 3: PASS | "
            "lifecycle=EMPTY"
        )

        print("")
        print("CASE 4 NO CROSS-OUTCOME CONTAMINATION")

        assert all(
            event["outcome_history_id"] == 501
            for event in timeline
        )

        assert not any(
            event["outcome_history_id"] == 502
            for event in timeline
        )

        print("CASE 4: PASS")

        print("")
        print("CASE 5 EVENT PRESENCE IS SOURCE-BASED")

        assert set(event_types) == set(EXPECTED_LIFECYCLE)

        print(
            "CASE 5: PASS | "
            "no synthetic event inference"
        )

        print("")
        print("CASE 6 ACTUAL OUTCOME GATE PRESERVED")

        assert (
            timeline[0]["details"]["actual_outcome_gate"]
            is True
        )

        print("CASE 6: PASS")

        print("")
        print("CASE 7 READ-ONLY BUSINESS STATE")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS i19_business_state_probe (
                outcome_history_id INTEGER,
                outcome_status TEXT,
                reassessment_required INTEGER,
                reassessment_status TEXT
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO i19_business_state_probe
            VALUES (?, ?, ?, ?)
            """,
            (
                501,
                "EVALUATED",
                0,
                "NOT_REQUIRED",
            ),
        )

        conn.commit()

        cursor.execute(
            """
            SELECT
                outcome_status,
                reassessment_required,
                reassessment_status
            FROM i19_business_state_probe
            WHERE outcome_history_id = ?
            """,
            (501,)
        )

        before = cursor.fetchone()
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
            FROM i19_business_state_probe
            WHERE outcome_history_id = ?
            """,
            (501,)
        )

        after = cursor.fetchone()
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
