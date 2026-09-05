import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import repository


class _TestConnection:
    def __init__(self, connection):
        self._connection = connection

    def cursor(self):
        return self._connection.cursor()

    def commit(self):
        return self._connection.commit()

    def rollback(self):
        return self._connection.rollback()

    def close(self):
        # Keep the in-memory connection open for inspection.
        return None


def build_test_db():
    raw_conn = sqlite3.connect(":memory:")
    cursor = raw_conn.cursor()

    cursor.execute(
        """
        CREATE TABLE ai_decision_outcome_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision TEXT,
            action TEXT,
            strategy TEXT,
            confidence_score REAL,
            intelligence_score REAL,
            validation_score REAL,
            governance_score REAL,
            execution_score REAL,
            lifecycle_score REAL,
            operational_score REAL,
            orchestration_score REAL,
            integrated_score REAL,
            market_view TEXT,
            risk_level TEXT,
            outcome_status TEXT,
            snapshot_status TEXT,
            snapshot_purpose TEXT,
            outcome_score REAL,
            outcome_grade TEXT,
            decision_effectiveness TEXT,
            strategy_effectiveness TEXT,
            market_response TEXT,
            portfolio_response TEXT,
            learning_status TEXT,
            feedback_state TEXT,
            adaptive_learning_required INTEGER,
            reassessment_required INTEGER,
            reassessment_status TEXT,
            created_at TEXT,
            execution_status TEXT,
            execution_authorization TEXT,
            execution_readiness TEXT,
            certification_status TEXT,
            monitoring_status TEXT,
            feedback_status TEXT,
            portfolio_return REAL,
            portfolio_evaluation_date TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE ai_decision_portfolio_snapshot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            history_id INTEGER NOT NULL,
            ticker TEXT NOT NULL,
            weight REAL,
            reference_price REAL,
            created_at TEXT,
            reference_price_date TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE audit_event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_event_id TEXT NOT NULL UNIQUE,
            event_type TEXT NOT NULL,
            event_time TEXT NOT NULL,
            source TEXT NOT NULL,
            status TEXT,
            decision_history_id INTEGER,
            outcome_history_id INTEGER,
            correlation_key TEXT NOT NULL,
            details TEXT NOT NULL
        )
        """
    )

    raw_conn.commit()
    return raw_conn


original_get_connection = repository.get_connection


try:
    print("=" * 60)
    print("Phase8-6-B Runtime Evaluation Transaction Rollback")
    print("=" * 60)

    # --------------------------------------------------
    # CASE 1 - EVALUATION TRANSACTION SUCCESS
    # --------------------------------------------------
    print("")
    print("CASE 1 SUCCESS")

    raw_conn = build_test_db()
    test_conn = _TestConnection(raw_conn)
    repository.get_connection = lambda: test_conn

    cursor = raw_conn.cursor()

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
            "2026-08-20T13:00:00+09:00",
        ),
    )

    history_id = cursor.lastrowid
    raw_conn.commit()

    result = repository.save_ai_decision_portfolio_evaluation_transaction(
        history_id=history_id,
        portfolio_return=1.25,
        portfolio_evaluation_date="2026-08-21",
        event_time="2026-08-21T15:00:00+09:00",
        evaluated_weight=100.0,
        pending_positions=0,
    )

    cursor.execute(
        """
        SELECT outcome_status, portfolio_return, portfolio_evaluation_date
        FROM ai_decision_outcome_history
        WHERE id = ?
        """,
        (history_id,),
    )

    state = cursor.fetchone()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM audit_event
        WHERE event_type = 'OUTCOME_EVALUATED'
          AND outcome_history_id = ?
        """,
        (history_id,),
    )

    audit_count = cursor.fetchone()[0]

    assert result["outcome_status"] == "EVALUATED"
    assert state == ("EVALUATED", 1.25, "2026-08-21")
    assert audit_count == 1

    print(
        "CASE 1 SUCCESS: PASS | "
        f"history={history_id} | "
        f"status={state[0]} | "
        f"return={state[1]}"
    )

    raw_conn.close()

    # --------------------------------------------------
    # CASE 2 - FORCE OUTCOME_EVALUATED AUDIT COLLISION
    # --------------------------------------------------
    print("")
    print("CASE 2 FORCED AUDIT COLLISION -> ROLLBACK")

    raw_conn = build_test_db()
    test_conn = _TestConnection(raw_conn)
    repository.get_connection = lambda: test_conn

    cursor = raw_conn.cursor()

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
            "2026-08-20T13:00:00+09:00",
        ),
    )

    history_id = cursor.lastrowid
    event_time = "2026-08-21T15:00:01+09:00"

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
            f"OUTCOME_EVALUATED:outcome:{history_id}:{event_time}",
            "TEST_COLLISION",
            event_time,
            "test",
            "TEST",
            history_id,
            f"outcome:{history_id}",
            "{}",
        ),
    )

    raw_conn.commit()

    try:
        repository.save_ai_decision_portfolio_evaluation_transaction(
            history_id=history_id,
            portfolio_return=2.50,
            portfolio_evaluation_date="2026-08-21",
            event_time=event_time,
            evaluated_weight=100.0,
            pending_positions=0,
        )
    except Exception as exc:
        print(
            "CASE 2 EXCEPTION: PASS | "
            f"type={type(exc).__name__} | "
            f"message={exc}"
        )
    else:
        raise AssertionError(
            "Expected forced audit collision."
        )

    cursor = raw_conn.cursor()

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

    state = cursor.fetchone()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM audit_event
        WHERE outcome_history_id = ?
        """,
        (history_id,),
    )

    audit_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM audit_event
        WHERE audit_event_id = ?
        """,
        (
            f"OUTCOME_EVALUATED:outcome:{history_id}:{event_time}",
        ),
    )

    collision_count = cursor.fetchone()[0]

    print("persisted_state:", state)
    print("audit_count:", audit_count)
    print("collision_count:", collision_count)

    assert state == ("PENDING", None, None)
    assert audit_count == 1
    assert collision_count == 1

    print(
        "CASE 2 ROLLBACK INVARIANT: PASS | "
        "business state remained PENDING"
    )

    print("")
    print("=" * 60)
    print("OVERALL RESULT: PASS")
    print("=" * 60)

finally:
    repository.get_connection = original_get_connection
