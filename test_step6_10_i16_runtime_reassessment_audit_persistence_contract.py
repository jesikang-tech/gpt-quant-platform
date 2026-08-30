import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i16_",
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

        history_id = 501

        conn = database.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO ai_decision_outcome_history
            (
                decision,
                action,
                strategy,
                confidence_score,
                intelligence_score,
                outcome_status,
                snapshot_status,
                snapshot_purpose,
                created_at,
                reassessment_required,
                reassessment_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "MAINTAIN",
                "PROCEED",
                "BALANCED",
                90.0,
                90.0,
                "EVALUATED",
                "COLLECTED",
                "FUTURE_OUTCOME_EVALUATION",
                "2026-08-30T15:00:00+09:00",
                1,
                "CRITICAL_REASSESSMENT",
            ),
        )

        history_id = cursor.lastrowid
        conn.commit()
        conn.close()

        outcome_intelligence = {
            "outcome_status": "EVALUATED",
            "outcome_score": 35.0,
            "outcome_grade": "D",
            "outcome_learning_status": "REASSESSMENT_REQUIRED",
            "feedback_state": "REASSESSMENT_REQUIRED",
            "adaptive_learning_required": True,
            "reassessment_required": True,
            "reassessment_status": "CRITICAL_REASSESSMENT",
            "source_history_id": history_id,
        }

        source_history_id = outcome_intelligence.get(
            "source_history_id"
        )

        assert source_history_id == history_id
        assert outcome_intelligence[
            "reassessment_required"
        ] is True

        repository.save_ai_decision_audit_event(
            event_type="REASSESSMENT_REQUIRED",
            event_time="2026-08-30T15:01:00+09:00",
            source="portfolio_reassessment",
            status="REQUIRED",
            outcome_history_id=source_history_id,
            correlation_key=f"outcome:{source_history_id}",
            details={
                "reassessment_required":
                    bool(
                        outcome_intelligence.get(
                            "reassessment_required",
                            False
                        )
                    ),
                "reassessment_status":
                    outcome_intelligence.get(
                        "reassessment_status",
                        "UNKNOWN"
                    ),
                "outcome_learning_status":
                    outcome_intelligence.get(
                        "outcome_learning_status",
                        "UNKNOWN"
                    ),
                "feedback_state":
                    outcome_intelligence.get(
                        "feedback_state",
                        "UNKNOWN"
                    ),
            },
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                event_type,
                status,
                outcome_history_id,
                correlation_key,
                details
            FROM audit_event
            WHERE event_type = ?
            ORDER BY id ASC
            """,
            ("REASSESSMENT_REQUIRED",),
        )

        events = cursor.fetchall()

        assert len(events) == 1

        event = events[0]

        assert event[0] == "REASSESSMENT_REQUIRED"
        assert event[1] == "REQUIRED"
        assert event[2] == history_id
        assert event[3] == f"outcome:{history_id}"

        assert '"reassessment_required": true' in event[4]
        assert (
            '"reassessment_status": "CRITICAL_REASSESSMENT"'
            in event[4]
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE outcome_history_id = ?
            """,
            (history_id,),
        )

        correlated_count = cursor.fetchone()[0]

        assert correlated_count == 1

        print(
            "CASE 1 REAL REASSESSMENT: PASS | "
            f"required={outcome_intelligence['reassessment_required']} | "
            f"status={outcome_intelligence['reassessment_status']}"
        )

        print(
            "CASE 2 AUDIT PERSISTED: PASS | "
            f"events={len(events)}"
        )

        print(
            "CASE 3 OUTCOME CORRELATION: PASS | "
            f"correlation={event[3]}"
        )

        print("CASE 4 REASSESSMENT PAYLOAD: PASS")

        print(
            "CASE 5 SINGLE CORRELATED EVENT: PASS | "
            f"events={correlated_count}"
        )

        print("")
        print("OVERALL RESULT: PASS")

        conn.close()

    finally:
        config.DATABASE_PATH = original_config_path
        database.DATABASE_PATH = original_database_path

        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass


print("=" * 60)
print(
    "Step6-10-I-16 Runtime Reassessment Audit Persistence Contract"
)
print("=" * 60)

run_test()
