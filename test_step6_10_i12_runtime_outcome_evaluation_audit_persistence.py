import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i12_",
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
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "MAINTAIN",
                "PROCEED",
                "BALANCED",
                90.0,
                90.0,
                "PENDING",
                "COLLECTED",
                "FUTURE_OUTCOME_EVALUATION",
                "2026-08-20T15:00:00+09:00",
            ),
        )

        history_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO ai_decision_portfolio_snapshot
            (
                history_id,
                ticker,
                weight,
                reference_price,
                created_at,
                reference_price_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                history_id,
                "TEST",
                100.0,
                100.0,
                "2026-08-20T15:00:00+09:00",
                "2026-08-20",
            ),
        )

        cursor.execute(
            """
            INSERT INTO etf_prices
            (
                ticker,
                date,
                close_price
            )
            VALUES (?, ?, ?)
            """,
            (
                "TEST",
                "2026-08-21",
                101.0,
            ),
        )

        conn.commit()
        conn.close()

        result = repository.evaluate_ai_decision_portfolio_snapshot(
            history_id=history_id,
            evaluation_date="2026-08-21",
        )

        assert result["evaluation_status"] == "EVALUATED"
        assert result["outcome_status"] == "EVALUATED"
        assert result["portfolio_return"] == 1.0

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                event_type,
                status,
                outcome_history_id,
                correlation_key
            FROM audit_event
            WHERE event_type = ?
            ORDER BY id ASC
            """,
            (
                "OUTCOME_EVALUATION_STARTED",
            ),
        )

        started_events = cursor.fetchall()

        assert len(started_events) == 1

        event = started_events[0]

        assert event[0] == "OUTCOME_EVALUATION_STARTED"
        assert event[1] == "STARTED"
        assert event[2] == history_id
        assert event[3] == f"outcome:{history_id}"

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE event_type = ?
              AND outcome_history_id = ?
            """,
            (
                "OUTCOME_EVALUATED",
                history_id,
            ),
        )

        evaluated_count = cursor.fetchone()[0]

        assert evaluated_count == 1

        print(
            "CASE 1 REAL EVALUATION: PASS | "
            f"history={history_id} | "
            f"return={result['portfolio_return']}"
        )

        print(
            "CASE 2 START AUDIT PERSISTED: PASS | "
            f"events={len(started_events)}"
        )

        print(
            "CASE 3 CORRELATION: PASS | "
            f"correlation={event[3]}"
        )

        print(
            "CASE 4 EVALUATED AUDIT PRESERVED: PASS | "
            f"events={evaluated_count}"
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
    "Step6-10-I-12 Runtime Outcome Evaluation Audit Persistence"
)
print("=" * 60)

run_test()
