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


def build_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE ai_decision_outcome_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision TEXT,
            action TEXT,
            strategy TEXT
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
        [
            ("306950", "2026-08-20", 67560.0),
        ],
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

    conn.commit()
    return conn


def valid_portfolio():
    return [
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
    ]


def run_case(
    name,
    history_id,
    create_history,
    expected_success,
    expected_error,
):
    raw_conn = build_db()
    cursor = raw_conn.cursor()

    if create_history:
        cursor.execute(
            """
            INSERT INTO ai_decision_outcome_history
            (
                decision,
                action,
                strategy
            )
            VALUES (?, ?, ?)
            """,
            (
                "MAINTAIN",
                "PROCEED",
                "MAINTAIN",
            ),
        )
        raw_conn.commit()

    original_get_connection = repository.get_connection

    repository.get_connection = lambda: _TestConnection(
        raw_conn
    )

    try:
        try:
            result = repository.save_ai_decision_portfolio_snapshot(
                history_id=history_id,
                portfolio=valid_portfolio(),
                created_at="2026-08-20T14:30:00+09:00",
            )

            if not expected_success:
                raise AssertionError(
                    f"Expected rejection: {expected_error}"
                )

            assert result == 2

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ai_decision_portfolio_snapshot
                WHERE history_id = ?
                """,
                (history_id,),
            )

            snapshot_count = cursor.fetchone()[0]

            assert snapshot_count == 2

            print(
                f"{name}: PASS | "
                f"snapshot_count={snapshot_count}"
            )

        except ValueError as exc:
            if expected_success:
                raise

            assert str(exc) == expected_error

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ai_decision_portfolio_snapshot
                """
            )

            snapshot_count = cursor.fetchone()[0]

            assert snapshot_count == 0

            print(
                f"{name}: PASS | "
                f"rejected={expected_error} | "
                f"snapshot_count=0"
            )

    finally:
        repository.get_connection = (
            original_get_connection
        )
        raw_conn.close()


print("=" * 60)
print(
    "Production Hardening - History Snapshot "
    "Referential Integrity Contract"
)
print("=" * 60)

run_case(
    "CASE 1 EXISTING HISTORY",
    history_id=1,
    create_history=True,
    expected_success=True,
    expected_error=None,
)

run_case(
    "CASE 2 MISSING HISTORY",
    history_id=999,
    create_history=False,
    expected_success=False,
    expected_error="HISTORY_NOT_FOUND",
)

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
