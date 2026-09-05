import sqlite3
from datetime import datetime, timedelta

import repository


class _TestConnection:
    def __init__(self, connection):
        self._connection = connection

    def cursor(self):
        return self._connection.cursor()

    def close(self):
        return None


def build_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE ai_decision_outcome_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            outcome_status TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE ai_decision_portfolio_snapshot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            history_id INTEGER NOT NULL
        )
        """
    )

    conn.commit()
    return conn


now = datetime.now().astimezone()

CASES = [
    (
        "CASE 1 PENDING WITH SNAPSHOT",
        "PENDING",
        True,
        1,
        "PROTECTED",
    ),
    (
        "CASE 2 EVALUATED WITH SNAPSHOT",
        "EVALUATED",
        True,
        1,
        "RETAIN_LONG_TERM",
    ),
    (
        "CASE 3 RECENT PENDING ORPHAN",
        "PENDING",
        False,
        1,
        "RETAIN",
    ),
    (
        "CASE 4 RECENT EVALUATED LEGACY",
        "EVALUATED",
        False,
        1,
        "RETAIN",
    ),
    (
        "CASE 5 OLD PENDING ORPHAN",
        "PENDING",
        False,
        8,
        "REVIEW_REQUIRED",
    ),
    (
        "CASE 6 OLD EVALUATED LEGACY",
        "EVALUATED",
        False,
        8,
        "REVIEW_REQUIRED",
    ),
]


print("=" * 60)
print(
    "Production Hardening - History Snapshot "
    "Retention Repository Regression"
)
print("=" * 60)


original_get_connection = repository.get_connection

try:
    for (
        name,
        outcome_status,
        create_snapshot,
        age_days,
        expected_retention,
    ) in CASES:
        raw_conn = build_db()
        cursor = raw_conn.cursor()

        created_at = (
            now - timedelta(days=age_days)
        ).isoformat()

        cursor.execute(
            """
            INSERT INTO ai_decision_outcome_history
            (
                created_at,
                outcome_status
            )
            VALUES (?, ?)
            """,
            (
                created_at,
                outcome_status,
            ),
        )

        history_id = cursor.lastrowid

        if create_snapshot:
            cursor.execute(
                """
                INSERT INTO ai_decision_portfolio_snapshot
                (
                    history_id
                )
                VALUES (?)
                """,
                (history_id,),
            )

        raw_conn.commit()

        repository.get_connection = lambda: _TestConnection(
            raw_conn
        )

        try:
            rows = (
                repository
                .get_ai_decision_history_snapshot_retention()
            )

            assert len(rows) == 1

            row = rows[0]

            assert row["history_id"] == history_id
            assert row["outcome_status"] == outcome_status
            assert row["snapshot_count"] == (
                1 if create_snapshot else 0
            )
            assert row["retention"] == expected_retention

            print(
                f"{name}: PASS | "
                f"{row['lifecycle']} | "
                f"retention={row['retention']}"
            )

        finally:
            raw_conn.close()

finally:
    repository.get_connection = original_get_connection


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
