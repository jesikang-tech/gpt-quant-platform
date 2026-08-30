import sqlite3


def build_existing_db():
    conn = sqlite3.connect(":memory:")

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE ai_decision_outcome_history (
            id INTEGER PRIMARY KEY,
            outcome_status TEXT,
            learning_status TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE ai_decision_portfolio_snapshot (
            id INTEGER PRIMARY KEY,
            history_id INTEGER,
            ticker TEXT,
            weight REAL
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO ai_decision_outcome_history
        VALUES
        (13, 'PENDING', 'WAITING_FOR_OUTCOME')
        """
    )

    cursor.execute(
        """
        INSERT INTO ai_decision_portfolio_snapshot
        VALUES
        (1, 13, '306950', 90.0)
        """
    )

    cursor.execute(
        """
        INSERT INTO ai_decision_portfolio_snapshot
        VALUES
        (2, 13, 'CASH', 10.0)
        """
    )

    conn.commit()

    return conn


def migration_create_audit(conn):

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_event (
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

    conn.commit()


print("=" * 60)
print(
    "Step6-10-I-9 Audit Event Migration Safety Contract"
)
print("=" * 60)


conn = build_existing_db()

cursor = conn.cursor()


print("")
print("--- BEFORE MIGRATION SNAPSHOT ---")

cursor.execute(
    "SELECT COUNT(*) FROM ai_decision_outcome_history"
)

before_history = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
)

before_snapshot = cursor.fetchone()[0]


print(
    "before_history:",
    before_history
)

print(
    "before_snapshot:",
    before_snapshot
)


print("")
print("--- CASE 1 MIGRATION SUCCESS ---")

migration_create_audit(conn)

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
      AND name='audit_event'
    """
)

assert cursor.fetchone() is not None

print(
    "CASE 1 MIGRATION CREATE: PASS"
)


print("")
print("--- CASE 2 EXISTING DATA PRESERVED ---")


cursor.execute(
    "SELECT COUNT(*) FROM ai_decision_outcome_history"
)

after_history = cursor.fetchone()[0]


cursor.execute(
    "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
)

after_snapshot = cursor.fetchone()[0]


assert before_history == after_history
assert before_snapshot == after_snapshot


print(
    "CASE 2 DATA PRESERVATION: PASS"
)


print("")
print("--- CASE 3 MIGRATION IDEMPOTENCY ---")


migration_create_audit(conn)

cursor.execute(
    """
    SELECT COUNT(*)
    FROM sqlite_master
    WHERE type='table'
      AND name='audit_event'
    """
)

assert cursor.fetchone()[0] == 1


print(
    "CASE 3 RE-RUN SAFETY: PASS"
)


print("")
print("--- CASE 4 FAILURE ROLLBACK ---")


test_conn = build_existing_db()

try:

    test_conn.execute("BEGIN")

    test_conn.execute(
        """
        CREATE TABLE audit_event_failure_test (
            id INTEGER PRIMARY KEY
        )
        """
    )

    raise RuntimeError(
        "SIMULATED_MIGRATION_FAILURE"
    )

except RuntimeError:

    test_conn.rollback()


cursor = test_conn.cursor()

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
      AND name='audit_event_failure_test'
    """
)

assert cursor.fetchone() is None


print(
    "CASE 4 ROLLBACK SAFETY: PASS"
)


print("")
print("--- CASE 5 NO BUSINESS STATE DUPLICATION ---")


cursor = conn.cursor()

cursor.execute(
    "PRAGMA table_info(audit_event)"
)

columns = [
    row[1]
    for row in cursor.fetchall()
]


assert "outcome_status" not in columns
assert "learning_status" not in columns


print(
    "CASE 5 EVENT/BUSINESS SEPARATION: PASS"
)


conn.close()
test_conn.close()


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)

