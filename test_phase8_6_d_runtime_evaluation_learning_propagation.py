import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository
import api_server


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="phase8_6_d_",
        suffix=".db"
    )
    os.close(fd)

    original_config_path = config.DATABASE_PATH
    original_database_path = database.DATABASE_PATH
    original_evaluator = (
        api_server.evaluate_ai_decision_portfolio_snapshot
    )

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

        conn.commit()
        conn.close()

        def forced_evaluated(*args, **kwargs):
            return {
                "evaluation_status": "EVALUATED",
                "portfolio_return": 1.25,
                "portfolio_evaluation_date": "2026-08-21",
            }

        api_server.evaluate_ai_decision_portfolio_snapshot = (
            forced_evaluated
        )

        print("=" * 60)
        print(
            "Phase8-6-D Runtime Evaluation -> "
            "Learning Propagation"
        )
        print("=" * 60)

        print("")
        print("CASE 1 ENDPOINT EVALUATION")

        client = api_server.app.test_client()

        response = client.get(
            f"/api/ai-decision/portfolio-snapshot/"
            f"{history_id}/evaluate"
            f"?evaluation_date=2026-08-21"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert payload["evaluation"]["evaluation_status"] == (
            "EVALUATED"
        )
        assert payload["evaluation"]["portfolio_return"] == 1.25

        print(
            "CASE 1 ENDPOINT EVALUATION: PASS | "
            f"status={response.status_code}"
        )

        outcome_evaluation = payload["outcome_evaluation"]
        outcome_intelligence = payload["outcome_intelligence"]

        assert outcome_evaluation is not None
        assert outcome_intelligence is not None

        learning_signal = outcome_evaluation.get(
            "learning_signal"
        )
        learning_signal_strength = outcome_evaluation.get(
            "learning_signal_strength"
        )

        assert learning_signal in {
            "POSITIVE",
            "NEGATIVE",
            "NEUTRAL",
            "NONE",
        }

        assert learning_signal_strength is not None

        print(
            "CASE 2 LEARNING SIGNAL GENERATED: PASS | "
            f"signal={learning_signal} | "
            f"strength={learning_signal_strength}"
        )

        expected_adaptive = (
            learning_signal == "NEGATIVE"
        )
        expected_reassessment = (
            learning_signal == "NEGATIVE"
        )

        assert outcome_evaluation[
            "adaptive_learning_required"
        ] == expected_adaptive

        assert outcome_evaluation[
            "reassessment_required"
        ] == expected_reassessment

        print(
            "CASE 3 LEARNING FLAGS PROPAGATED: PASS | "
            f"adaptive={expected_adaptive} | "
            f"reassessment={expected_reassessment}"
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                outcome_status,
                outcome_score,
                outcome_grade,
                decision_effectiveness,
                strategy_effectiveness,
                learning_status,
                feedback_state,
                adaptive_learning_required,
                reassessment_required,
                reassessment_status
            FROM ai_decision_outcome_history
            WHERE id = ?
            """,
            (history_id,),
        )

        history_state = cursor.fetchone()

        assert history_state[0] == "EVALUATED"
        assert history_state[1] == outcome_evaluation[
            "outcome_score"
        ]
        assert history_state[2] == outcome_evaluation[
            "outcome_grade"
        ]
        assert history_state[3] == outcome_evaluation[
            "decision_effectiveness"
        ]
        assert history_state[4] == outcome_evaluation[
            "strategy_effectiveness"
        ]
        assert history_state[5] == outcome_intelligence[
            "learning_status"
        ]
        assert history_state[6] == outcome_intelligence[
            "feedback_state"
        ]
        assert history_state[7] == int(
            expected_adaptive
        )
        assert history_state[8] == int(
            expected_reassessment
        )
        assert history_state[9] == outcome_evaluation[
            "reassessment_status"
        ]

        print(
            "CASE 4 HISTORY LEARNING PROPAGATION: PASS | "
            f"status={history_state[0]} | "
            f"learning={history_state[5]}"
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

        learning_events = [
            event
            for event in audit_events
            if event[0] == "LEARNING_SIGNAL_GENERATED"
        ]

        assert len(learning_events) == 1

        learning_event = learning_events[0]

        assert learning_event[1] == "GENERATED"
        assert learning_event[2] == history_id
        assert learning_event[3] == (
            f"outcome:{history_id}"
        )

        print(
            "CASE 5 LEARNING AUDIT PROPAGATION: PASS | "
            f"events={len(learning_events)}"
        )

        cursor.execute(
            """
            SELECT
                portfolio_return,
                portfolio_evaluation_date
            FROM ai_decision_outcome_history
            WHERE id = ?
            """,
            (history_id,),
        )

        portfolio_state = cursor.fetchone()

        assert portfolio_state == (
            None,
            None,
        )

        print(
            "CASE 6 PORTFOLIO BUSINESS STATE BOUNDARY: PASS | "
            "evaluation endpoint did not falsely persist "
            "portfolio evaluation fields"
        )

        conn.close()

        print("")
        print("=" * 60)
        print("OVERALL RESULT: PASS")
        print("=" * 60)

    finally:
        api_server.evaluate_ai_decision_portfolio_snapshot = (
            original_evaluator
        )

        config.DATABASE_PATH = original_config_path
        database.DATABASE_PATH = original_database_path

        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass


run_test()
