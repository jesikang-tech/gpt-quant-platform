import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i15_",
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

        history_id = 401
        correlation_key = f"outcome:{history_id}"

        events = [
            (
                "OUTCOME_EVALUATION_STARTED",
                "STARTED",
                "portfolio_outcome_evaluation",
                {"actual_outcome_gate": True},
            ),
            (
                "OUTCOME_EVALUATED",
                "EVALUATED",
                "portfolio_outcome_evaluation",
                {"portfolio_return": 1.25},
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "AVAILABLE",
                "outcome_intelligence",
                {
                    "learning_signal": "POSITIVE",
                    "learning_signal_strength": 0.8,
                },
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "GENERATED",
                "adaptive_strategy",
                {
                    "strategy": "GROWTH",
                    "action": "INCREASE_RISK",
                },
            ),
            (
                "REASSESSMENT_REQUIRED",
                "REQUIRED",
                "reassessment",
                {
                    "reassessment_required": True,
                    "reassessment_status":
                        "CRITICAL_REASSESSMENT",
                },
            ),
        ]

        for index, (
            event_type,
            status,
            source,
            details,
        ) in enumerate(events, start=1):

            repository.save_ai_decision_audit_event(
                event_type=event_type,
                event_time=(
                    f"2026-08-30T15:00:0{index}+09:00"
                ),
                source=source,
                status=status,
                outcome_history_id=history_id,
                correlation_key=correlation_key,
                details=details,
            )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                event_type,
                status,
                source,
                outcome_history_id,
                correlation_key
            FROM audit_event
            WHERE correlation_key = ?
            ORDER BY id ASC
            """,
            (correlation_key,),
        )

        rows = cursor.fetchall()

        assert len(rows) == 5

        expected_sequence = [
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
            "LEARNING_SIGNAL_GENERATED",
            "ADAPTIVE_STRATEGY_GENERATED",
            "REASSESSMENT_REQUIRED",
        ]

        actual_sequence = [
            row[0]
            for row in rows
        ]

        assert actual_sequence == expected_sequence

        for row in rows:
            assert row[3] == history_id
            assert row[4] == correlation_key

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE correlation_key = ?
              AND outcome_history_id = ?
            """,
            (
                correlation_key,
                history_id,
            ),
        )

        correlated_count = cursor.fetchone()[0]

        assert correlated_count == 5

        cursor.execute(
            """
            SELECT COUNT(DISTINCT event_type)
            FROM audit_event
            WHERE correlation_key = ?
            """,
            (correlation_key,),
        )

        distinct_event_types = cursor.fetchone()[0]

        assert distinct_event_types == 5

        print(
            "CASE 1 FULL LIFECYCLE: PASS | "
            f"events={len(rows)}"
        )

        print(
            "CASE 2 EVENT ORDER: PASS | "
            "evaluation -> learning -> adaptive -> reassessment"
        )

        print(
            "CASE 3 COMMON CORRELATION: PASS | "
            f"correlation={correlation_key}"
        )

        print(
            "CASE 4 OUTCOME HISTORY LINK: PASS | "
            f"history={history_id}"
        )

        print(
            "CASE 5 NO DUPLICATE EVENT TYPES: PASS | "
            f"types={distinct_event_types}"
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
    "Step6-10-I-15 End-to-End Audit Lifecycle Persistence"
)
print("=" * 60)

run_test()
