import sqlite3


def build_db():
    conn = sqlite3.connect(":memory:")

    cursor = conn.cursor()

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

    conn.commit()
    return conn


def insert_event(
    conn,
    audit_event_id,
    event_type,
    event_time,
    source,
    status,
    decision_history_id,
    outcome_history_id,
    correlation_key,
    details,
):
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO audit_event
        (
            audit_event_id,
            event_type,
            event_time,
            source,
            status,
            decision_history_id,
            outcome_history_id,
            correlation_key,
            details
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            audit_event_id,
            event_type,
            event_time,
            source,
            status,
            decision_history_id,
            outcome_history_id,
            correlation_key,
            details,
        ),
    )

    conn.commit()


print("=" * 60)
print(
    "Step6-10-I-8 Audit Event Table Design Validation"
)
print("=" * 60)

conn = build_db()
cursor = conn.cursor()

print("")
print("--- CASE 1 TABLE CREATED ---")

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
      AND name = 'audit_event'
    """
)

assert cursor.fetchone() is not None

print("CASE 1 TABLE CREATION: PASS")

print("")
print("--- CASE 2 SCHEMA ---")

cursor.execute(
    "PRAGMA table_info(audit_event)"
)

columns = cursor.fetchall()

column_names = [
    row[1]
    for row in columns
]

expected_columns = [
    "id",
    "audit_event_id",
    "event_type",
    "event_time",
    "source",
    "status",
    "decision_history_id",
    "outcome_history_id",
    "correlation_key",
    "details",
]

assert column_names == expected_columns

print(
    "CASE 2 SCHEMA: PASS | "
    f"columns={len(column_names)}"
)

print("")
print("--- CASE 3 NORMAL EVENT ---")

insert_event(
    conn,
    "OUTCOME_EVALUATED:outcome:201:1",
    "OUTCOME_EVALUATED",
    "2026-08-20T15:00:00+09:00",
    "outcome_evaluation",
    "EVALUATED",
    None,
    201,
    "outcome:201",
    '{"portfolio_return":5.0}',
)

cursor.execute(
    "SELECT COUNT(*) FROM audit_event"
)

assert cursor.fetchone()[0] == 1

print("CASE 3 NORMAL EVENT: PASS")

print("")
print("--- CASE 4 NULLABLE REFERENCES ---")

insert_event(
    conn,
    "DECISION_CREATED:decision:101:1",
    "DECISION_CREATED",
    "2026-08-20T15:01:00+09:00",
    "ai_decision_engine",
    "CREATED",
    101,
    None,
    "decision:101",
    "{}",
)

cursor.execute(
    """
    SELECT
        decision_history_id,
        outcome_history_id
    FROM audit_event
    WHERE audit_event_id = ?
    """,
    (
        "DECISION_CREATED:decision:101:1",
    ),
)

row = cursor.fetchone()

assert row[0] == 101
assert row[1] is None

print("CASE 4 NULLABLE REFERENCES: PASS")

print("")
print("--- CASE 5 FAILURE EVENT ---")

insert_event(
    conn,
    "PERSISTENCE_FAILED:outcome:201:1",
    "PERSISTENCE_FAILED",
    "2026-08-20T15:02:00+09:00",
    "repository",
    "FAILED",
    None,
    201,
    "outcome:201",
    '{"error_code":"SIMULATED_FAILURE"}',
)

cursor.execute(
    """
    SELECT
        event_type,
        status,
        correlation_key,
        details
    FROM audit_event
    WHERE audit_event_id = ?
    """,
    (
        "PERSISTENCE_FAILED:outcome:201:1",
    ),
)

row = cursor.fetchone()

assert row[0] == "PERSISTENCE_FAILED"
assert row[1] == "FAILED"
assert row[2] == "outcome:201"
assert "SIMULATED_FAILURE" in row[3]

print("CASE 5 FAILURE EVENT: PASS")

print("")
print("--- CASE 6 UNIQUE EVENT ID ---")

try:
    insert_event(
        conn,
        "OUTCOME_EVALUATED:outcome:201:1",
        "OUTCOME_EVALUATED",
        "2026-08-20T15:03:00+09:00",
        "test",
        "EVALUATED",
        None,
        201,
        "outcome:201",
        "{}",
    )

    duplicate_rejected = False

except sqlite3.IntegrityError:
    duplicate_rejected = True

assert duplicate_rejected is True

print("CASE 6 UNIQUE EVENT ID: PASS")

print("")
print("--- CASE 7 MULTI-EVENT CORRELATION ---")

cursor.execute(
    """
    SELECT COUNT(*)
    FROM audit_event
    WHERE correlation_key = ?
    """,
    ("outcome:201",),
)

count = cursor.fetchone()[0]

assert count == 2

print(
    "CASE 7 MULTI-EVENT CORRELATION: PASS | "
    f"events={count}"
)

print("")
print("--- CASE 8 READBACK ---")

cursor.execute(
    """
    SELECT
        audit_event_id,
        event_type,
        event_time,
        source,
        status,
        decision_history_id,
        outcome_history_id,
        correlation_key,
        details
    FROM audit_event
    ORDER BY id
    """
)

rows = cursor.fetchall()

assert len(rows) == 3

for row in rows:
    print({
        "audit_event_id": row[0],
        "event_type": row[1],
        "source": row[3],
        "status": row[4],
        "decision_history_id": row[5],
        "outcome_history_id": row[6],
        "correlation_key": row[7],
    })

print("CASE 8 READBACK: PASS")

conn.close()

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
