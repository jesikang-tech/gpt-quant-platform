import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository

from core.ai_final_decision_reassessment import (
    AIFinalDecisionReassessment
)


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i14_",
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

        history_id = 301

        reassessment_engine = (
            AIFinalDecisionReassessment()
        )

        result = reassessment_engine.reassess(
            final_decision={
                "decision": "MAINTAIN",
                "action": "PROCEED",
                "validation_status": "VALID",
                "validation_score": 95
            },
            governance={
                "governance_status": "APPROVED",
                "governance_score": 95
            },
            execution_control={
                "control_status": "AUTHORIZED",
                "control_risk": "LOW"
            },
            execution_assurance={
                "assurance_status": "ASSURED",
                "assurance_risk": "LOW",
                "assurance_score": 95,
                "validation_status": "VALID",
                "validation_score": 95
            },
            execution_feedback={
                "decision": "MAINTAIN",
                "action": "PROCEED",
                "feedback_status": "CRITICAL",
                "feedback_action": "REASSESS",
                "feedback_risk": "HIGH",
                "feedback_score": 40,
                "validation_status": "VALID",
                "validation_score": 95
            },
            execution_monitoring={
                "monitoring_status": "STANDARD_MONITORING",
                "monitoring_risk": "LOW",
                "monitoring_score": 95
            }
        )

        assert result["reassessment_required"] is True
        assert result["reassessment_status"] == (
            "CRITICAL_REASSESSMENT"
        )
        assert result["reassessment_action"] == (
            "HALT_AND_REASSESS"
        )

        event_time = (
            "2026-08-30T15:00:00+09:00"
        )

        repository.save_ai_decision_audit_event(
            event_type="REASSESSMENT_REQUIRED",
            event_time=event_time,
            source="reassessment",
            status="REQUIRED",
            outcome_history_id=history_id,
            correlation_key=(
                f"outcome:{history_id}"
            ),
            details={
                "reassessment_required":
                    result["reassessment_required"],
                "reassessment_status":
                    result["reassessment_status"],
                "reassessment_action":
                    result["reassessment_action"],
                "reassessment_risk":
                    result["reassessment_risk"],
                "reassessment_score":
                    result["reassessment_score"],
                "reassessment_reason":
                    result["reassessment_reason"],
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
            (
                "REASSESSMENT_REQUIRED",
            ),
        )

        events = cursor.fetchall()

        assert len(events) == 1

        event = events[0]

        assert event[0] == "REASSESSMENT_REQUIRED"
        assert event[1] == "REQUIRED"
        assert event[2] == history_id
        assert event[3] == f"outcome:{history_id}"

        assert "reassessment_required" in event[4]
        assert "CRITICAL_REASSESSMENT" in event[4]
        assert "HALT_AND_REASSESS" in event[4]

        print(
            "CASE 1 REAL REASSESSMENT: PASS | "
            f"required={result['reassessment_required']} | "
            f"status={result['reassessment_status']}"
        )

        print(
            "CASE 2 AUDIT PERSISTED: PASS | "
            f"events={len(events)}"
        )

        print(
            "CASE 3 OUTCOME CORRELATION: PASS | "
            f"correlation={event[3]}"
        )

        print(
            "CASE 4 REASSESSMENT PAYLOAD: PASS"
        )

        print(
            "CASE 5 SINGLE CORRELATED EVENT: PASS | "
            f"events={len(events)}"
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
    "Step6-10-I-14 Runtime Reassessment Audit Persistence"
)
print("=" * 60)

run_test()
