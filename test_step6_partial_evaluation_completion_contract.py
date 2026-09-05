import sqlite3
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
        return None


def build_db(snapshot_rows, price_rows):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

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
        CREATE TABLE ai_decision_outcome_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outcome_status TEXT,
            snapshot_status TEXT,
            portfolio_return REAL,
            portfolio_evaluation_date TEXT
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO ai_decision_outcome_history(
            id,
            outcome_status,
            snapshot_status,
            portfolio_return,
            portfolio_evaluation_date
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            12,
            "PENDING",
            "COLLECTED",
            None,
            None,
        )
    )

    cursor.executemany(
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
        snapshot_rows
    )

    cursor.executemany(
        """
        INSERT INTO etf_prices
        (
            ticker,
            date,
            close_price
        )
        VALUES (?, ?, ?)
        """,
        price_rows
    )

    conn.commit()
    return conn


def run_case(
    name,
    snapshot_rows,
    price_rows,
    expected_status,
    expected_outcome_status,
    expected_weight,
    expected_pending,
    expected_return,
):
    raw_conn = build_db(
        snapshot_rows,
        price_rows
    )

    original_get_connection = (
        repository.get_connection
    )

    repository.get_connection = lambda: (
        _TestConnection(raw_conn)
    )

    try:
        result = (
            repository
            .evaluate_ai_decision_portfolio_snapshot(
                history_id=12,
                evaluation_date="2026-08-21",
            )
        )

        assert (
            result["evaluation_status"]
            == expected_status
        )

        assert (
            result["outcome_status"]
            == expected_outcome_status
        )

        assert (
            result.get("evaluated_weight")
            == expected_weight
        )

        assert (
            result.get("pending_positions")
            == expected_pending
        )

        assert (
            result.get("portfolio_return")
            == expected_return
        )

        cursor = raw_conn.cursor()

        cursor.execute(
            """
            SELECT
                portfolio_return,
                portfolio_evaluation_date
            FROM ai_decision_outcome_history
            WHERE id = 12
            """
        )

        stored = cursor.fetchone()

        if expected_return is None:
            assert stored[0] is None
            assert stored[1] is None
        else:
            assert stored[0] == expected_return
            assert stored[1] == "2026-08-21"

        print(
            f"{name}: PASS | "
            f"status={expected_status} | "
            f"weight={expected_weight} | "
            f"pending={expected_pending} | "
            f"return={expected_return}"
        )

    finally:
        repository.get_connection = (
            original_get_connection
        )
        raw_conn.close()


print("=" * 60)
print(
    "Production Hardening - Partial Evaluation "
    "Completion Contract"
)
print("=" * 60)


run_case(
    "CASE 1 FULL EVALUATION",
    [
        (12, "A", 40.0, 100.0,
         "2026-08-20T00:00:00",
         "2026-08-20"),
        (12, "B", 30.0, 200.0,
         "2026-08-20T00:00:00",
         "2026-08-20"),
        (12, "C", 20.0, 300.0,
         "2026-08-20T00:00:00",
         "2026-08-20"),
        (12, "CASH", 10.0, None,
         "2026-08-20T00:00:00",
         None),
    ],
    [
        ("A", "2026-08-21", 110.0),
        ("B", "2026-08-21", 210.0),
        ("C", "2026-08-21", 315.0),
    ],
    "EVALUATED",
    "EVALUATED",
    100.0,
    0,
    6.5,
)


run_case(
    "CASE 2 PARTIAL EVALUATION",
    [
        (12, "A", 40.0, 100.0,
         "2026-08-20T00:00:00",
         "2026-08-20"),
        (12, "B", 30.0, 200.0,
         "2026-08-20T00:00:00",
         "2026-08-20"),
        (12, "C", 20.0, 300.0,
         "2026-08-20T00:00:00",
         "2026-08-20"),
        (12, "CASH", 10.0, None,
         "2026-08-20T00:00:00",
         None),
    ],
    [
        ("A", "2026-08-21", 110.0),
        ("B", "2026-08-21", 210.0),
    ],
    "WAITING_FOR_OUTCOME",
    "PENDING",
    80.0,
    1,
    None,
)


run_case(
    "CASE 3 HEAVY PARTIAL EVALUATION",
    [
        (12, "A", 40.0, 100.0,
         "2026-08-20T00:00:00",
         "2026-08-20"),
        (12, "B", 30.0, 200.0,
         "2026-08-20T00:00:00",
         "2026-08-20"),
        (12, "C", 20.0, 300.0,
         "2026-08-20T00:00:00",
         "2026-08-20"),
        (12, "CASH", 10.0, None,
         "2026-08-20T00:00:00",
         None),
    ],
    [
        ("A", "2026-08-21", 110.0),
    ],
    "WAITING_FOR_OUTCOME",
    "PENDING",
    50.0,
    2,
    None,
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
