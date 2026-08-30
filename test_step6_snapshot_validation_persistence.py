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
        return None


def build_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

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

    conn.commit()
    return conn


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
        "created_at": "2026-08-20T14:00:00+09:00",
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
        "Production Hardening - Snapshot Validation "
        "Persistence Regression"
    )
    print("=" * 60)

    valid_portfolio = [
        {
            "ticker": "306950",
            "weight": 40,
            "reference_price": 67560,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "365040",
            "weight": 30,
            "reference_price": 33540,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "475720",
            "weight": 20,
            "reference_price": 11730,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "CASH",
            "weight": 10,
        },
    ]

    invalid_cases = [
        (
            "EMPTY",
            [],
            "EMPTY_PORTFOLIO",
        ),
        (
            "BAD_WEIGHT",
            [
                {
                    "ticker": "306950",
                    "weight": 90,
                    "reference_price": 67560,
                    "reference_price_date": "2026-08-20",
                },
                {
                    "ticker": "CASH",
                    "weight": 5,
                },
            ],
            "INVALID_TOTAL_WEIGHT",
        ),
        (
            "DUPLICATE",
            [
                {
                    "ticker": "306950",
                    "weight": 40,
                    "reference_price": 67560,
                    "reference_price_date": "2026-08-20",
                },
                {
                    "ticker": "306950",
                    "weight": 50,
                    "reference_price": 67560,
                    "reference_price_date": "2026-08-20",
                },
                {
                    "ticker": "CASH",
                    "weight": 10,
                },
            ],
            "DUPLICATE_TICKER",
        ),
        (
            "MISSING_REFERENCE",
            [
                {
                    "ticker": "306950",
                    "weight": 90,
                },
                {
                    "ticker": "CASH",
                    "weight": 10,
                },
            ],
            "MISSING_REFERENCE_PRICE",
        ),
    ]

    raw_conn = build_db()
    test_conn = TestConnection(raw_conn)
    repository.get_connection = lambda: test_conn

    result = (
        repository
        .save_ai_decision_outcome_with_portfolio_transaction(
            history_kwargs=history_payload(),
            portfolio=valid_portfolio,
            created_at="2026-08-20T14:00:00+09:00",
        )
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

    assert result["history_id"] == 1
    assert history_count == 1
    assert snapshot_count == 4

    print("CASE 1 VALID PERSISTENCE: PASS")

    raw_conn.close()

    for name, portfolio, expected_reason in invalid_cases:
        raw_conn = build_db()
        test_conn = TestConnection(raw_conn)
        repository.get_connection = lambda: test_conn

        try:
            repository.save_ai_decision_outcome_with_portfolio_transaction(
                history_kwargs=history_payload(),
                portfolio=portfolio,
                created_at="2026-08-20T14:00:00+09:00",
            )

            raise AssertionError(
                f"Expected {expected_reason}"
            )

        except ValueError as exc:
            assert str(exc) == expected_reason

        cursor = raw_conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_outcome_history"
        )
        history_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
        )
        snapshot_count = cursor.fetchone()[0]

        assert history_count == 0
        assert snapshot_count == 0

        print(
            f"CASE {name} REJECTION: PASS | "
            f"reason={expected_reason}"
        )

        raw_conn.close()

    print("")
    print("=" * 60)
    print("OVERALL RESULT: PASS")
    print("=" * 60)

finally:
    repository.get_connection = original_get_connection
