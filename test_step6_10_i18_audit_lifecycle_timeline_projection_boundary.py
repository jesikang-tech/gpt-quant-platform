import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i18_",
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
                '{"evaluation_date": null, "actual_outcome_gate": true}',
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
                '{"evaluation_date": null, "actual_outcome_gate": true}',
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

        print("")
        print("CASE 1 LIFECYCLE TIMELINE")

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
            outcome_history_id=501
        )

        assert len(timeline) == 5
        assert all(
            event["outcome_history_id"] == 501
            for event in timeline
        )

        print(
            "CASE 1: PASS | "
            f"events={len(timeline)}"
        )

        print("")
        print("CASE 2 CHRONOLOGICAL ORDER")

        assert [
            event["event_type"]
            for event in timeline
        ] == [
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
            "LEARNING_SIGNAL_GENERATED",
            "REASSESSMENT_REQUIRED",
            "ADAPTIVE_STRATEGY_GENERATED",
        ]

        print("CASE 2: PASS")

        print("")
        print("CASE 3 COMMON CORRELATION")

        assert all(
            event["correlation_key"] == "outcome:501"
            for event in timeline
        )

        print("CASE 3: PASS")

        print("")
        print("CASE 4 SOURCE EVENT PRESERVATION")

        assert timeline[0]["source"] == (
            "portfolio_outcome_evaluation"
        )
        assert timeline[1]["status"] == "EVALUATED"
        assert timeline[2]["details"] == {
            "learning_signal": "POSITIVE",
            "learning_signal_strength": 0.8,
        }
        assert timeline[3]["details"] == {
            "reassessment_required": True,
        }
        assert timeline[4]["details"] == {
            "strategy": "GROWTH",
            "action": "INCREASE_RISK",
        }

        print("CASE 4: PASS")

        print("")
        print("CASE 5 NO CROSS-OUTCOME CONTAMINATION")

        assert not any(
            event["outcome_history_id"] == 502
            for event in timeline
        )

        print("CASE 5: PASS")

        print("")
        print("CASE 6 NO SYNTHETIC EVENTS")

        assert len(timeline) == 5

        print(
            "CASE 6: PASS | "
            "no synthetic lifecycle events"
        )

        print("")
        print("CASE 7 READ-ONLY BUSINESS STATE")

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

        before = cursor.fetchone()
        conn.close()

        timeline = repository.get_ai_decision_audit_lifecycle_timeline(
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

        after = cursor.fetchone()
        conn.close()

        assert before == after

        print("CASE 7: PASS")

        print("")
        print("CASE 8 ACTUAL OUTCOME GATE PRESERVED")

        assert timeline[0]["details"]["actual_outcome_gate"] is True
        assert "actual_outcome_gate" not in timeline[1]["details"]

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


print("=" * 60)
print("Step6-10-I-18 Audit Lifecycle Timeline Projection Boundary")
print("=" * 60)

run_test()
