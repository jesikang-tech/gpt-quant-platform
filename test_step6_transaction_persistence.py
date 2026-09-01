import sqlite3
import repository


class TestConnection:
    def __init__(self, connection):
        self._connection = connection

    def cursor(self):
        return self._connection.cursor()

    def commit(self):
        return self._connection.commit()

    def rollback(self):
        return self._connection.rollback()

    def close(self):
        # Keep the in-memory connection open so the
        # regression test can inspect persisted state.
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
            feedback_status TEXT
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

    cursor.execute(
        """
        CREATE TABLE etf_prices (
            ticker TEXT NOT NULL,
            date TEXT NOT NULL,
            close_price REAL NOT NULL
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO etf_prices(
            ticker,
            date,
            close_price
        )
        VALUES (?, ?, ?)
        """,
        (
            "306950",
            "2026-08-20",
            67560.0,
        ),
    )

    raw_conn.commit()

    return raw_conn


def history_payload():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "strategy": "MAINTAIN",
        "confidence_score": 93.2,
        "intelligence_score": 89.6,
        "validation_score": 100.0,
        "governance_score": 98.8,
        "execution_score": 97.6,
        "lifecycle_score": 99.7,
        "operational_score": 98.3,
        "orchestration_score": 97.6,
        "integrated_score": 97.9,
        "market_view": "NEUTRAL",
        "risk_level": "LOW",
        "outcome_status": "PENDING",
        "snapshot_status": "COLLECTED",
        "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
        "outcome_score": 0.0,
        "outcome_grade": "N/A",
        "decision_effectiveness": "PENDING",
        "strategy_effectiveness": "PENDING",
        "market_response": "PENDING",
        "portfolio_response": "PENDING",
        "learning_status": "WAITING_FOR_OUTCOME",
        "feedback_state": "COLLECTING",
        "adaptive_learning_required": 0,
        "reassessment_required": 0,
        "reassessment_status": "NOT_REQUIRED",
        "created_at": "2026-08-20T13:00:00+09:00",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
        "certification_status": "CERTIFIED",
        "monitoring_status": "STANDARD_MONITORING",
        "feedback_status": "STABLE",
    }


original_get_connection = repository.get_connection


try:
    print("=" * 60)
    print(
        "Step6 Production Transaction Persistence Regression"
    )
    print("=" * 60)

    # --------------------------------------------------
    # CASE 1 - SUCCESS
    # --------------------------------------------------
    print("")
    print("CASE 1 SUCCESS")

    raw_conn = build_test_db()
    test_conn = TestConnection(raw_conn)

    repository.get_connection = (
        lambda: test_conn
    )

    result = (
        repository
        .save_ai_decision_outcome_with_portfolio_transaction(
            history_kwargs=history_payload(),
            portfolio=[
                {
                    "ticker": "306950",
                    "weight": 40.0,
                    "reference_price": 67560.0,
                    "reference_price_date": "2026-08-20",
                },
                {
                    "ticker": "CASH",
                    "weight": 60.0,
                    "reference_price": None,
                    "reference_price_date": None,
                },
            ],
            created_at="2026-08-20T13:00:00+09:00",
        )
    )

    print("result:", result)

    cursor = raw_conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM ai_decision_outcome_history"
    )

    history_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
    )

    snapshot_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM audit_event"
    )

    audit_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT event_type, outcome_history_id, correlation_key
        FROM audit_event
        ORDER BY id
        """
    )

    audit_rows = cursor.fetchall()

    print("history_count:", history_count)
    print("snapshot_count:", snapshot_count)
    print("audit_count:", audit_count)
    print("audit_rows:", audit_rows)

    audit_event_types = {
        row[0]
        for row in audit_rows
    }

    assert result["history_id"] == 1
    assert result["snapshot_count"] == 2
    assert history_count == 1
    assert snapshot_count == 2
    assert audit_count == 2
    assert audit_event_types == {
        "OUTCOME_PERSISTED",
        "SNAPSHOT_PERSISTED",
    }
    assert all(
        row[1] == 1
        and row[2] == "outcome:1"
        for row in audit_rows
    )

    print("RESULT: PASS")

    raw_conn.close()

    # --------------------------------------------------
    # CASE 2 - REAL PRODUCTION TRANSACTION ROLLBACK
    # --------------------------------------------------
    print("")
    print("CASE 2 REAL PRODUCTION TRANSACTION -> ROLLBACK")

    raw_conn = build_test_db()
    test_conn = TestConnection(raw_conn)

    repository.get_connection = (
        lambda: test_conn
    )

    created_at = "2026-08-20T13:00:01+09:00"

    # Force the first audit INSERT inside the real
    # production transaction to fail by occupying the
    # exact UNIQUE audit_event_id it will generate.
    cursor = raw_conn.cursor()

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
            f"SNAPSHOT_PERSISTED:outcome:1:{created_at}",
            "TEST_COLLISION",
            created_at,
            "test",
            "TEST",
            1,
            "outcome:1",
            "{}",
        ),
    )

    raw_conn.commit()

    try:
        repository.save_ai_decision_outcome_with_portfolio_transaction(
            history_kwargs=history_payload(),
            portfolio=[
                {
                    "ticker": "306950",
                    "weight": 90.0,
                    "reference_price": 67560.0,
                    "reference_price_date": "2026-08-20",
                },
                {
                    "ticker": "CASH",
                    "weight": 10.0,
                },
            ],
            created_at=created_at,
        )

        raise AssertionError(
            "Expected UNIQUE audit_event failure."
        )

    except Exception as exc:
        print(
            "exception_type:",
            type(exc).__name__
        )
        print(
            "exception:",
            str(exc)
        )

    cursor = raw_conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM ai_decision_outcome_history"
    )
    history_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
    )
    snapshot_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM audit_event"
    )
    audit_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM audit_event
        WHERE audit_event_id = ?
        """,
        (
            f"SNAPSHOT_PERSISTED:outcome:1:{created_at}",
        ),
    )
    collision_count = cursor.fetchone()[0]

    print("history_count:", history_count)
    print("snapshot_count:", snapshot_count)
    print("audit_count:", audit_count)
    print("collision_count:", collision_count)

    assert history_count == 0
    assert snapshot_count == 0
    assert audit_count == 1
    assert collision_count == 1

    print("RESULT: PASS")

    raw_conn.close()

    print("")
    print("=" * 60)
    print("OVERALL RESULT: PASS")
    print("=" * 60)

finally:
    repository.get_connection = (
        original_get_connection
    )
