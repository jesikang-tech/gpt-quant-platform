import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="phase8_6_a_",
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
                outcome_status,
                portfolio_return,
                portfolio_evaluation_date
            FROM ai_decision_outcome_history
            WHERE id = ?
            """,
            (history_id,),
        )

        history_row = cursor.fetchone()

        assert history_row is not None
        assert history_row[0] == "EVALUATED"
        assert history_row[1] == 1.0
        assert history_row[2] == "2026-08-21"

        print(
            "CASE 1 BUSINESS STATE PERSISTED: PASS | "
            f"history={history_id} | "
            f"status={history_row[0]} | "
            f"return={history_row[1]} | "
            f"date={history_row[2]}"
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

        audit_rows = cursor.fetchall()

        assert len(audit_rows) == 2
        assert audit_rows[0][0] == "OUTCOME_EVALUATION_STARTED"
        assert audit_rows[0][1] == "STARTED"
        assert audit_rows[1][0] == "OUTCOME_EVALUATED"
        assert audit_rows[1][1] == "EVALUATED"
        assert all(row[2] == history_id for row in audit_rows)
        assert all(
            row[3] == f"outcome:{history_id}"
            for row in audit_rows
        )

        print(
            "CASE 2 AUDIT LIFECYCLE PERSISTED: PASS | "
            f"events={len(audit_rows)}"
        )

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

        persisted_row = cursor.fetchone()

        assert persisted_row == (
            "EVALUATED",
            1.0,
            "2026-08-21",
        )

        print("CASE 3 PERSISTED STATE EXACT: PASS")

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


print("=" * 60)
print(
    "Phase8-6-A Runtime Evaluation Business State Persistence"
)
print("=" * 60)

run_test()
