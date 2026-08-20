from repository import (
    get_ai_decision_history_snapshot_lifecycle,
)


EXPECTED = {
    1: "LEGACY_ORPHAN_CANDIDATE",
    2: "LEGACY_ORPHAN_CANDIDATE",
    4: "LEGACY_ORPHAN_CANDIDATE",
    5: "LEGACY_ORPHAN_CANDIDATE",
    6: "LEGACY_ORPHAN_CANDIDATE",
    7: "LEGACY_EVALUATED_CANDIDATE",
    8: "LEGACY_ORPHAN_CANDIDATE",
    9: "LEGACY_ORPHAN_CANDIDATE",
    10: "LEGACY_ORPHAN_CANDIDATE",
    11: "LEGACY_ORPHAN_CANDIDATE",
    12: "ACTIVE_OUTCOME_TRACKING",
    13: "ACTIVE_OUTCOME_TRACKING",
}


print("=" * 60)
print(
    "Production Hardening - History Snapshot "
    "Lifecycle Repository Regression"
)
print("=" * 60)


rows = get_ai_decision_history_snapshot_lifecycle()

assert len(rows) == len(EXPECTED)

actual = {
    row["history_id"]: row["classification"]
    for row in rows
}

assert actual == EXPECTED

for row in rows:
    print(
        f"HISTORY {row['history_id']}: PASS | "
        f"{row['outcome_status']} | "
        f"snapshot_count={row['snapshot_count']} | "
        f"{row['classification']}"
    )


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
