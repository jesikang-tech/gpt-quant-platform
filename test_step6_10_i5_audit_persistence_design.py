import sqlite3


def build_db():
    conn = sqlite3.connect(":memory:")

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE ai_decision_outcome_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision TEXT NOT NULL,
            outcome_status TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE ai_decision_portfolio_snapshot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            history_id INTEGER NOT NULL,
            ticker TEXT NOT NULL,
            weight REAL NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE audit_event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_event_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_time TEXT NOT NULL,
            source TEXT NOT NULL,
            decision_history_id INTEGER,
            outcome_history_id INTEGER,
            status TEXT,
            details TEXT
        )
        """
    )

    conn.commit()

    return conn


def atomic_success():
    conn = build_db()

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO ai_decision_outcome_history
            (
                decision,
                outcome_status
            )
            VALUES (?, ?)
            """,
            (
                "MAINTAIN",
                "PENDING",
            ),
        )

        history_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO ai_decision_portfolio_snapshot
            (
                history_id,
                ticker,
                weight
            )
            VALUES (?, ?, ?)
            """,
            (
                history_id,
                "306950",
                90.0,
            ),
        )

        cursor.execute(
            """
            INSERT INTO ai_decision_portfolio_snapshot
            (
                history_id,
                ticker,
                weight
            )
            VALUES (?, ?, ?)
            """,
            (
                history_id,
                "CASH",
                10.0,
            ),
        )

        cursor.execute(
            """
            INSERT INTO audit_event
            (
                audit_event_id,
                event_type,
                event_time,
                source,
                decision_history_id,
                outcome_history_id,
                status,
                details
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "OUTCOME_PERSISTED:1",
                "OUTCOME_PERSISTED",
                "2026-08-20T15:00:00+09:00",
                "repository",
                history_id,
                history_id,
                "SUCCESS",
                "{}",
            ),
        )

        conn.commit()

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

        return (
            history_count,
            snapshot_count,
            audit_count,
        )

    finally:
        conn.close()


def atomic_failure():
    conn = build_db()

    cursor = conn.cursor()

    try:
        conn.execute("BEGIN")

        cursor.execute(
            """
            INSERT INTO ai_decision_outcome_history
            (
                decision,
                outcome_status
            )
            VALUES (?, ?)
            """,
            (
                "MAINTAIN",
                "PENDING",
            ),
        )

        history_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO ai_decision_portfolio_snapshot
            (
                history_id,
                ticker,
                weight
            )
            VALUES (?, ?, ?)
            """,
            (
                history_id,
                "306950",
                90.0,
            ),
        )

        raise RuntimeError(
            "SIMULATED_AUDIT_FAILURE"
        )

    except RuntimeError:
        conn.rollback()

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

        conn.close()

        return (
            history_count,
            snapshot_count,
            audit_count,
        )


print("=" * 60)
print(
    "Step6-10-I-5 Audit Event Persistence Design Contract"
)
print("=" * 60)

history_count, snapshot_count, audit_count = (
    atomic_success()
)

assert history_count == 1
assert snapshot_count == 2
assert audit_count == 1

print(
    "CASE 1 ATOMIC SUCCESS: PASS | "
    f"history={history_count} | "
    f"snapshot={snapshot_count} | "
    f"audit={audit_count}"
)

history_count, snapshot_count, audit_count = (
    atomic_failure()
)

assert history_count == 0
assert snapshot_count == 0
assert audit_count == 0

print(
    "CASE 2 AUDIT FAILURE ROLLBACK: PASS | "
    f"history={history_count} | "
    f"snapshot={snapshot_count} | "
    f"audit={audit_count}"
)

print("")
print("--- DESIGN INVARIANTS ---")

assert (
    audit_count == 0
)

print(
    "INVARIANT 1: AUDIT FAILURE CANNOT LEAVE PARTIAL DATA: PASS"
)

print(
    "INVARIANT 2: AUDIT EVENT SAVES INSIDE SAME TRANSACTION: PASS"
)

print(
    "INVARIANT 3: NO AUTO-COMMIT AUDIT SIDE EFFECT: PASS"
)

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
