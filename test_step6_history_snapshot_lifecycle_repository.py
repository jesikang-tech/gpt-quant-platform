import sqlite3
import repository


class TestConnection:
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


CASES = [
    (
        "CASE 1 PENDING WITH SNAPSHOT",
        "PENDING",
        True,
        "ACTIVE_OUTCOME_TRACKING",
    ),
    (
        "CASE 2 PENDING WITHOUT SNAPSHOT",
        "PENDING",
        False,
        "LEGACY_ORPHAN_CANDIDATE",
    ),
    (
        "CASE 3 EVALUATED WITH SNAPSHOT",
        "EVALUATED",
        True,
        "COMPLETED",
    ),
    (
        "CASE 4 EVALUATED WITHOUT SNAPSHOT",
        "EVALUATED",
        False,
        "LEGACY_EVALUATED_CANDIDATE",
    ),
    (
        "CASE 5 UNKNOWN STATUS",
        "UNKNOWN_STATUS",
        False,
        "UNKNOWN",
    ),
]


print("=" * 60)
print(
    "Production Hardening - History Snapshot "
    "Lifecycle Repository Regression"
)
print("=" * 60)


original_get_connection = repository.get_connection

try:
    for (
        name,
        outcome_status,
        create_snapshot,
        expected_classification,
    ) in CASES:
        raw_conn = build_db()
        cursor = raw_conn.cursor()

        cursor.execute(
            """
            INSERT INTO ai_decision_outcome_history
            (
                outcome_status
            )
            VALUES (?)
            """,
            (outcome_status,),
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

        repository.get_connection = lambda: TestConnection(
            raw_conn
        )

        try:
            rows = (
                repository
                .get_ai_decision_history_snapshot_lifecycle()
            )

            assert len(rows) == 1

            row = rows[0]

            assert row["history_id"] == history_id
            assert row["outcome_status"] == outcome_status
            assert row["snapshot_count"] == (
                1 if create_snapshot else 0
            )
            assert row["classification"] == expected_classification

            print(
                f"{name}: PASS | "
                f"{outcome_status} | "
                f"snapshot_count={row['snapshot_count']} | "
                f"{row['classification']}"
            )

        finally:
            raw_conn.close()

finally:
    repository.get_connection = original_get_connection


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
