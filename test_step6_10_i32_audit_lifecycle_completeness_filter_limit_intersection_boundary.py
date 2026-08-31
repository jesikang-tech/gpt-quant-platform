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
        prefix="step6_10_i32_",
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
                "2026-08-31T14:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                501,
                "outcome:501",
                '{"outcome": 501, "step": 1}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-31T14:02:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                501,
                "outcome:501",
                '{"outcome": 501, "step": 2}',
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "2026-08-31T14:03:00+09:00",
                "outcome_intelligence",
                "AVAILABLE",
                501,
                "outcome:501",
                '{"outcome": 501, "step": 3}',
            ),
            (
                "REASSESSMENT_REQUIRED",
                "2026-08-31T14:04:00+09:00",
                "outcome_intelligence",
                "REQUIRED",
                501,
                "outcome:501",
                '{"outcome": 501, "step": 4}',
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-31T14:05:00+09:00",
                "adaptive_strategy",
                "GENERATED",
                501,
                "outcome:501",
                '{"outcome": 501, "step": 5}',
            ),
            (
                "OUTCOME_EVALUATION_STARTED",
                "2026-08-31T14:06:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                502,
                "outcome:502",
                '{"outcome": 502, "step": 1}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-31T14:07:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                502,
                "outcome:502",
                '{"outcome": 502, "step": 2}',
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
        print("Step6-10-I-32 Audit Lifecycle Completeness Filter-Limit Intersection Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 FILTER AND LIMIT INTERSECTION")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            correlation_key="outcome:501",
            limit=3,
        )

        assert result["lifecycle_status"] == "PARTIAL"
        assert result["event_count"] == 3
        assert result["outcome_history_id"] == 501
        assert result["correlation_key"] == "outcome:501"
        assert result["present_event_types"] == EXPECTED_LIFECYCLE[:3]
        assert result["missing_event_types"] == EXPECTED_LIFECYCLE[3:]

        print("CASE 1: PASS")

        print("")
        print("CASE 2 FILTERED FULL LIMIT REMAINS COMPLETE")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            correlation_key="outcome:501",
            limit=5,
        )

        assert result["lifecycle_status"] == "COMPLETE"
        assert result["event_count"] == 5
        assert result["present_event_types"] == EXPECTED_LIFECYCLE
        assert result["missing_event_types"] == []

        print("CASE 2: PASS")

        print("")
        print("CASE 3 NO CROSS-OUTCOME CONTAMINATION")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501,
            correlation_key="outcome:501",
            limit=3,
        )

        assert result["event_count"] == 3
        assert result["outcome_history_id"] == 501
        assert result["correlation_key"] == "outcome:501"
        assert all(
            event_type in EXPECTED_LIFECYCLE[:3]
            for event_type in result["present_event_types"]
        )

        print("CASE 3: PASS")

        print("")
        print("CASE 4 CONFLICTING FILTERS REMAIN EMPTY")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            outcome_history_id=501,
            correlation_key="outcome:502",
            limit=5,
        )

        assert result["lifecycle_status"] == "EMPTY"
        assert result["event_count"] == 0
        assert result["present_event_types"] == []
        assert result["missing_event_types"] == EXPECTED_LIFECYCLE

        print("CASE 4: PASS")

        print("")
        print("CASE 5 LIMIT DOES NOT REORDER FILTERED EVENTS")

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
            correlation_key="outcome:501",
            limit=3,
        )

        assert [
            event["event_type"]
            for event in timeline
        ] == EXPECTED_LIFECYCLE[:3]

        assert all(
            event["correlation_key"] == "outcome:501"
            for event in timeline
        )

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
                outcome_history_id,
                correlation_key,
                details
            FROM audit_event
            ORDER BY event_time ASC, id ASC
            """
        )

        before = cursor.fetchall()
        conn.close()

        repository.get_ai_decision_audit_lifecycle_completeness(
            correlation_key="outcome:501",
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
        print("CASE 7 NO SYNTHETIC EVENT INFERENCE")

        result = repository.get_ai_decision_audit_lifecycle_completeness(
            correlation_key="outcome:501",
            limit=3,
        )

        assert "REASSESSMENT_REQUIRED" not in result["present_event_types"]
        assert "ADAPTIVE_STRATEGY_GENERATED" not in result["present_event_types"]
        assert result["missing_event_types"] == [
            "REASSESSMENT_REQUIRED",
            "ADAPTIVE_STRATEGY_GENERATED",
        ]

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
