from repository import get_connection


def classify_history_snapshot_lifecycle(
    outcome_status,
    snapshot_count,
):
    snapshot_count = int(snapshot_count or 0)

    if outcome_status == "PENDING":
        if snapshot_count > 0:
            return "ACTIVE_OUTCOME_TRACKING"

        return "LEGACY_ORPHAN_CANDIDATE"

    if outcome_status == "EVALUATED":
        if snapshot_count > 0:
            return "COMPLETED"

        return "LEGACY_EVALUATED_CANDIDATE"

    return "UNKNOWN"


def run_case(
    name,
    outcome_status,
    snapshot_count,
    expected,
):
    actual = classify_history_snapshot_lifecycle(
        outcome_status,
        snapshot_count,
    )

    assert actual == expected

    print(
        f"{name}: PASS | "
        f"status={outcome_status} | "
        f"snapshot_count={snapshot_count} | "
        f"classification={actual}"
    )


print("=" * 60)
print(
    "Production Hardening - History Snapshot "
    "Lifecycle Classification Contract"
)
print("=" * 60)


run_case(
    "CASE 1 PENDING WITHOUT SNAPSHOT",
    "PENDING",
    0,
    "LEGACY_ORPHAN_CANDIDATE",
)

run_case(
    "CASE 2 PENDING WITH SNAPSHOT",
    "PENDING",
    4,
    "ACTIVE_OUTCOME_TRACKING",
)

run_case(
    "CASE 3 EVALUATED WITH SNAPSHOT",
    "EVALUATED",
    4,
    "COMPLETED",
)

run_case(
    "CASE 4 EVALUATED WITHOUT SNAPSHOT",
    "EVALUATED",
    0,
    "LEGACY_EVALUATED_CANDIDATE",
)

run_case(
    "CASE 5 UNKNOWN STATUS",
    "UNKNOWN",
    0,
    "UNKNOWN",
)


print("")
print("--- CURRENT DATABASE CLASSIFICATION ---")

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        h.id,
        h.outcome_status,
        COUNT(s.id) AS snapshot_count
    FROM ai_decision_outcome_history h
    LEFT JOIN ai_decision_portfolio_snapshot s
        ON s.history_id = h.id
    GROUP BY
        h.id,
        h.outcome_status
    ORDER BY h.id
    """
)

rows = cursor.fetchall()

counts = {}

for row in rows:
    history_id = row[0]
    outcome_status = row[1]
    snapshot_count = row[2]

    classification = (
        classify_history_snapshot_lifecycle(
            outcome_status,
            snapshot_count,
        )
    )

    counts[classification] = (
        counts.get(classification, 0) + 1
    )

    print({
        "history_id": history_id,
        "outcome_status": outcome_status,
        "snapshot_count": snapshot_count,
        "classification": classification,
    })

conn.close()

print("")
print("--- CLASSIFICATION COUNTS ---")

for key in sorted(counts):
    print(
        key,
        ":",
        counts[key]
    )

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
