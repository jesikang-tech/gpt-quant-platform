import os
import shutil
import sqlite3
import tempfile
from pathlib import Path

import config
import database


def run_contract():
    source_db = Path(r".\database\g7_10_18_integration_test.db")

    fd, db_path = tempfile.mkstemp(
        prefix="phase8_7_runtime_closed_loop_contract_",
        suffix=".db",
    )
    os.close(fd)

    shutil.copy2(source_db, db_path)

    original_config_path = config.DATABASE_PATH
    original_database_path = database.DATABASE_PATH

    try:
        test_db_path = Path(db_path)

        config.DATABASE_PATH = test_db_path
        database.DATABASE_PATH = test_db_path

        import api_server
        from testing_helpers import authenticated_client

        client = authenticated_client(api_server.app)

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        created_at = "2026-07-27T15:30:00+09:00"

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
                "069500",
                100.0,
                107513.0,
                created_at,
                "2026-07-27",
            ),
        )

        conn.commit()
        conn.close()

        evaluation_response = client.get(
            f"/api/ai-decision/portfolio-snapshot/"
            f"{history_id}/evaluate"
            f"?evaluation_date=2026-07-28"
        )

        assert evaluation_response.status_code == 200

        evaluation_payload = evaluation_response.get_json()

        evaluation = evaluation_payload["evaluation"]
        outcome_evaluation = evaluation_payload["outcome_evaluation"]

        print("EVALUATION STATUS :", evaluation["evaluation_status"])
        print("PORTFOLIO RETURN  :", evaluation["portfolio_return"])
        print("LEARNING SIGNAL   :", outcome_evaluation["learning_signal"])
        print(
            "ADAPTIVE REQUIRED :",
            outcome_evaluation["adaptive_learning_required"],
        )

        conn = sqlite3.connect(test_db_path)

        audit_before = conn.execute(
            "SELECT COUNT(*) FROM audit_event"
        ).fetchone()[0]

        adaptive_before = conn.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE event_type = 'ADAPTIVE_STRATEGY_GENERATED'
              AND outcome_history_id = ?
            """,
            (history_id,),
        ).fetchone()[0]

        conn.close()

        response = client.get(
            "/api/portfolio/decision-intelligence"
        )

        payload = (
            response.get_json()
            if response.is_json
            else None
        )

        conn = sqlite3.connect(test_db_path)

        audit_after = conn.execute(
            "SELECT COUNT(*) FROM audit_event"
        ).fetchone()[0]

        adaptive_after = conn.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            WHERE event_type = 'ADAPTIVE_STRATEGY_GENERATED'
              AND outcome_history_id = ?
            """,
            (history_id,),
        ).fetchone()[0]

        conn.close()

        # --------------------------------
        # Phase 8-7 Runtime Closed Loop Contract
        # --------------------------------

        assert evaluation["evaluation_status"] == "EVALUATED"
        assert evaluation["outcome_status"] == "EVALUATED"
        assert evaluation["portfolio_return"] == -11.1903

        assert outcome_evaluation["learning_signal"] == "NEGATIVE"
        assert (
            outcome_evaluation["adaptive_learning_required"]
            is True
        )
        assert (
            outcome_evaluation["reassessment_required"]
            is True
        )

        assert response.status_code == 200
        assert isinstance(payload, dict)
        assert payload["success"] is True

        intelligence = payload["intelligence"]
        final_decision = payload["final_decision"]

        assert (
            intelligence["outcome_learning_signal"]
            == "NEGATIVE"
        )
        assert intelligence["adaptive_learning_required"] is True
        assert intelligence["strategy_mode"] == "DEFENSIVE"
        assert intelligence["adaptive_action"] == "REDUCE_RISK"
        assert intelligence["adaptive_override"] is True
        assert intelligence["final_strategy"] == "DEFENSIVE"

        assert final_decision["strategy"] == "DEFENSIVE"
        assert final_decision["adaptive_action"] == "REDUCE_RISK"

        assert audit_after == audit_before
        assert adaptive_after == adaptive_before

        print("DECISION HTTP     :", response.status_code)
        print("DECISION SUCCESS  :", (
            payload.get("success")
            if isinstance(payload, dict)
            else None
        ))

        print(
            "RUNTIME SIGNAL    :",
            intelligence.get("outcome_learning_signal"),
        )
        print(
            "STRATEGY MODE     :",
            intelligence.get("strategy_mode"),
        )
        print(
            "ADAPTIVE ACTION   :",
            intelligence.get("adaptive_action"),
        )
        print(
            "ADAPTIVE OVERRIDE :",
            intelligence.get("adaptive_override"),
        )
        print(
            "FINAL STRATEGY    :",
            intelligence.get("final_strategy"),
        )
        print(
            "FINAL DEC STRATEGY:",
            final_decision.get("strategy"),
        )
        print(
            "FINAL DEC ADAPTIVE:",
            final_decision.get("adaptive_action"),
        )

        print("AUDIT BEFORE      :", audit_before)
        print("AUDIT AFTER       :", audit_after)
        print("AUDIT DELTA       :", audit_after - audit_before)
        print("ADAPTIVE BEFORE   :", adaptive_before)
        print("ADAPTIVE AFTER    :", adaptive_after)
        print(
            "ADAPTIVE DELTA    :",
            adaptive_after - adaptive_before,
        )

    finally:
        config.DATABASE_PATH = original_config_path
        database.DATABASE_PATH = original_database_path

        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass


run_contract()
