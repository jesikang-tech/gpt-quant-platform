import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="phase8_6_e_",
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

        evaluation_date = "2026-08-21"

        print("=" * 60)
        print(
            "Phase8-6-E Runtime Evaluation Idempotency Boundary"
        )
        print("=" * 60)

        print("")
        print("CASE 1 FIRST REAL EVALUATION")

        first = repository.evaluate_ai_decision_portfolio_snapshot(
            history_id=history_id,
            evaluation_date=evaluation_date,
        )

        print(
            "first:",
            first
        )

        assert first["evaluation_status"] == "EVALUATED"
        assert first["outcome_status"] == "EVALUATED"
        assert first["portfolio_return"] == 1.25

        print(
            "CASE 1 FIRST EVALUATION: PASS | "
            f"status={first['evaluation_status']} | "
            f"return={first['portfolio_return']}"
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

        first_state = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE outcome_history_id = ?
              AND event_type = 'OUTCOME_EVALUATED'
            """,
            (history_id,),
        )

        first_evaluated_audit_count = cursor.fetchone()[0]

        print(
            "first_state:",
            first_state
        )
        print(
            "first_evaluated_audit_count:",
            first_evaluated_audit_count
        )

        assert first_state == (
            "EVALUATED",
            1.25,
            "2026-08-21",
        )
        assert first_evaluated_audit_count == 1

        print(
            "CASE 2 FIRST PERSISTENCE: PASS | "
            f"state={first_state} | "
            f"evaluated_audit={first_evaluated_audit_count}"
        )

        conn.close()

        print("")
        print("CASE 3 SAME-DATE SECOND REAL EVALUATION")

        second = repository.evaluate_ai_decision_portfolio_snapshot(
            history_id=history_id,
            evaluation_date=evaluation_date,
        )

        print(
            "second:",
            second
        )

        assert second["evaluation_status"] == "EVALUATED"
        assert second["outcome_status"] == "EVALUATED"
        assert second["portfolio_return"] == 1.25
        assert second["evaluation_date"] == evaluation_date

        print(
            "CASE 3 SECOND EVALUATION: PASS | "
            f"status={second['evaluation_status']} | "
            f"return={second['portfolio_return']}"
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

        second_state = cursor.fetchone()

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

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE outcome_history_id = ?
              AND event_type = 'OUTCOME_EVALUATED'
            """,
            (history_id,),
        )

        second_evaluated_audit_count = cursor.fetchone()[0]

        print(
            "second_state:",
            second_state
        )
        print(
            "audit_events:",
            audit_events
        )
        print(
            "second_evaluated_audit_count:",
            second_evaluated_audit_count
        )

        assert second_state == first_state
        assert second_evaluated_audit_count == 1
        assert len(audit_events) == 2
        assert second["positions"] == []

        print(
            "CASE 4 SAME-DATE STATE STABILITY: PASS | "
            f"state={second_state}"
        )

        print(
            "CASE 5 SAME-DATE IDEMPOTENCY: PASS | "
            "OUTCOME_EVALUATED audit remains single"
        )

        conn.close()

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
