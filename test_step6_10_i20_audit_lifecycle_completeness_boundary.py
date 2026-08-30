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


def insert_event(
    cursor,
    event_type,
    event_time,
    source,
    status,
    outcome_history_id,
    correlation_key,
    details,
):
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
            f"{event_type}:{correlation_key}:{event_time}",
            event_type,
            event_time,
            source,
            status,
            outcome_history_id,
            correlation_key,
            details,
        ),
    )


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i20_",
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

        lifecycle_events = [
            (
                "OUTCOME_EVALUATION_STARTED",
                "2026-08-30T15:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                '{"actual_outcome_gate": true}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-30T15:02:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                '{"portfolio_return": 0.05}',
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "2026-08-30T15:03:00+09:00",
                "outcome_intelligence",
                "AVAILABLE",
                '{"learning_signal": "POSITIVE"}',
            ),
            (
                "REASSESSMENT_REQUIRED",
                "2026-08-30T15:04:00+09:00",
                "outcome_intelligence",
                "REQUIRED",
                '{"reassessment_required": true}',
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-30T15:05:00+09:00",
                "adaptive_strategy",
                "GENERATED",
                '{"strategy": "GROWTH"}',
            ),
        ]

        for event in lifecycle_events:
            insert_event(
                cursor,
                event[0],
                event[1],
                event[2],
                event[3],
                501,
                "outcome:501",
                event[4],
            )

        insert_event(
            cursor,
            "OUTCOME_EVALUATION_STARTED",
            "2026-08-30T16:01:00+09:00",
            "portfolio_outcome_evaluation",
            "STARTED",
            502,
            "outcome:502",
            '{"actual_outcome_gate": true}',
        )

        conn.commit()
        conn.close()

        print("=" * 60)
        print("Step6-10-I-20 Audit Lifecycle Completeness Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 COMPLETE LIFECYCLE")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501
        )

        assert result["lifecycle_status"] == "COMPLETE"
        assert result["event_count"] == 5
        assert result["present_event_types"] == EXPECTED_LIFECYCLE
        assert result["missing_event_types"] == []

        print(
            "CASE 1: PASS | "
            f"status={result['lifecycle_status']}"
        )

        print("")
        print("CASE 2 PARTIAL LIFECYCLE")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=502
        )

        assert result["lifecycle_status"] == "PARTIAL"
        assert result["event_count"] == 1
        assert result["present_event_types"] == [
            "OUTCOME_EVALUATION_STARTED"
        ]
        assert result["missing_event_types"] == EXPECTED_LIFECYCLE[1:]

        print(
            "CASE 2: PASS | "
            f"status={result['lifecycle_status']}"
        )

        print("")
        print("CASE 3 EMPTY LIFECYCLE")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=999
        )

        assert result["lifecycle_status"] == "EMPTY"
        assert result["event_count"] == 0
        assert result["present_event_types"] == []
        assert result["missing_event_types"] == EXPECTED_LIFECYCLE

        print(
            "CASE 3: PASS | "
            f"status={result['lifecycle_status']}"
        )

        print("")
        print("CASE 4 CORRELATION KEY BOUNDARY")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            correlation_key="outcome:501"
        )

        assert result["lifecycle_status"] == "COMPLETE"
        assert result["correlation_key"] == "outcome:501"
        assert result["outcome_history_id"] == 501

        print("CASE 4: PASS")

        print("")
        print("CASE 5 NO CROSS-OUTCOME CONTAMINATION")

        assert result["event_count"] == 5
        assert 502 not in [
            event["outcome_history_id"]
            for event in repository.get_ai_decision_audit_lifecycle_timeline(
                correlation_key="outcome:501"
            )
        ]

        print("CASE 5: PASS")

        print("")
        print("CASE 6 NO SYNTHETIC EVENT INFERENCE")

        assert result["present_event_types"] == EXPECTED_LIFECYCLE
        assert result["event_count"] == len(EXPECTED_LIFECYCLE)

        print(
            "CASE 6: PASS | "
            "source-based completeness only"
        )

        print("")
        print("CASE 7 READ-ONLY BUSINESS STATE")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE i20_business_state_probe (
                outcome_history_id INTEGER,
                outcome_status TEXT,
                reassessment_required INTEGER,
                reassessment_status TEXT
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO i20_business_state_probe
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
            FROM i20_business_state_probe
            WHERE outcome_history_id = ?
            """,
            (501,),
        )

        before = cursor.fetchone()
        conn.close()

        repository.get_ai_decision_audit_lifecycle_completeness(
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
            FROM i20_business_state_probe
            WHERE outcome_history_id = ?
            """,
            (501,),
        )

        after = cursor.fetchone()
        conn.close()

        assert before == after

        print("CASE 7: PASS")

        print("")
        print("CASE 8 DUPLICATE EVENT TYPE DOES NOT ALTER COMPLETENESS")

        conn = database.get_connection()
        cursor = conn.cursor()

        insert_event(
            cursor,
            "OUTCOME_EVALUATED",
            "2026-08-30T15:06:00+09:00",
            "portfolio_outcome_evaluation",
            "EVALUATED",
            501,
            "outcome:501",
            '{"duplicate": true}',
        )

        conn.commit()
        conn.close()

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501
        )

        assert result["lifecycle_status"] == "COMPLETE"
        assert result["event_count"] == 6
        assert result["present_event_types"] == EXPECTED_LIFECYCLE
        assert result["missing_event_types"] == []

        print(
            "CASE 8: PASS | "
            "duplicate event type ignored for completeness"
        )

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
