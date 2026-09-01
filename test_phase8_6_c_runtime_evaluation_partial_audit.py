import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="phase8_6_c_",
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

        created_at = "2026-08-20T13:00:02+09:00"

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
                "MAINTAIN",
                93.2,
                89.6,
                "PENDING",
                "COLLECTED",
                "FUTURE_OUTCOME_EVALUATION",
                created_at,
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
                "306950",
                100.0,
                67560.0,
                created_at,
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
                "306950",
                "2026-08-21",
                68404.5,
            ),
        )

        conn.commit()
        conn.close()

        original_final_transaction = (
            repository
            .save_ai_decision_portfolio_evaluation_transaction
        )

        def forced_failure(*args, **kwargs):
            raise RuntimeError(
                "FORCED_FINAL_EVALUATION_FAILURE"
            )

        repository.save_ai_decision_portfolio_evaluation_transaction = (
            forced_failure
        )

        print("=" * 60)
        print(
            "Phase8-6-C Runtime Evaluation Partial Audit Boundary"
        )
        print("=" * 60)

        print("")
        print("CASE 1 FORCED FINAL EVALUATION FAILURE")

        try:
            repository.evaluate_ai_decision_portfolio_snapshot(
                history_id=history_id,
                evaluation_date="2026-08-21",
            )

            raise AssertionError(
                "Expected forced final evaluation failure."
            )

        except RuntimeError as exc:
            assert str(exc) == (
                "FORCED_FINAL_EVALUATION_FAILURE"
            )

            print(
                "CASE 1 EXCEPTION: PASS | "
                f"type={type(exc).__name__}"
            )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                outcome_status,
                portfolio_return,
                portfolio_evaluation_date
            FROM ai_decision_outcome_history
            WHERE id = ?
            """,
            (history_id,),
        )

        business_state = cursor.fetchone()

        print(
            "business_state:",
            business_state
        )

        assert business_state == (
            "PENDING",
            None,
            None,
        )

        print(
            "CASE 2 BUSINESS STATE: PASS | "
            "PENDING / NULL / NULL"
        )

        cursor.execute(
            """
            SELECT
                event_type,
                status,
                outcome_history_id,
                correlation_key
            FROM audit_event
            WHERE outcome_history_id = ?
            ORDER BY id ASC
            """,
            (history_id,),
        )

        audit_events = cursor.fetchall()

        print(
            "audit_events:",
            audit_events
        )

        assert len(audit_events) == 1

        started_event = audit_events[0]

        assert started_event[0] == (
            "OUTCOME_EVALUATION_STARTED"
        )
        assert started_event[1] == "STARTED"
        assert started_event[2] == history_id
        assert started_event[3] == (
            f"outcome:{history_id}"
        )

        print(
            "CASE 3 START AUDIT PRESERVED: PASS | "
            "STARTED=1"
        )

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

        assert evaluated_count == 0

        print(
            "CASE 4 NO FALSE EVALUATED AUDIT: PASS | "
            f"count={evaluated_count}"
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM ai_decision_portfolio_snapshot
            WHERE history_id = ?
            """,
            (history_id,),
        )

        snapshot_count = cursor.fetchone()[0]

        assert snapshot_count == 1

        print(
            "CASE 5 SNAPSHOT PRESERVED: PASS | "
            f"count={snapshot_count}"
        )

        conn.close()

        print("")
        print("=" * 60)
        print("OVERALL RESULT: PASS")
        print("=" * 60)

    finally:
        repository.save_ai_decision_portfolio_evaluation_transaction = (
            original_final_transaction
            if "original_final_transaction" in locals()
            else repository
            .save_ai_decision_portfolio_evaluation_transaction
        )

        config.DATABASE_PATH = original_config_path
        database.DATABASE_PATH = original_database_path

        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass


run_test()
