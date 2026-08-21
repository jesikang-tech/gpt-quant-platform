from repository import (
    get_ai_decision_history_snapshot_cleanup_candidates,
)


EXPECTED = {
    1: (False, False, "NO_AUTO_DELETE"),
    2: (False, False, "NO_AUTO_DELETE"),
    3: (False, False, "NO_AUTO_DELETE"),
    4: (False, False, "NO_AUTO_DELETE"),
    5: (False, False, "NO_AUTO_DELETE"),
    6: (False, False, "NO_AUTO_DELETE"),
    7: (False, False, "NO_AUTO_DELETE"),
    8: (False, False, "NO_AUTO_DELETE"),
    9: (False, False, "NO_AUTO_DELETE"),
    10: (False, False, "NO_AUTO_DELETE"),
    11: (False, False, "NO_AUTO_DELETE"),
    12: (False, False, "NO_AUTO_DELETE"),
    16: (False, False, "NO_AUTO_DELETE"),
}


print("=" * 60)
print(
    "Production Hardening - Cleanup Candidate "
    "Repository Regression"
)
print("=" * 60)


rows = (
    get_ai_decision_history_snapshot_cleanup_candidates()
)

assert len(rows) == len(EXPECTED)

actual = {
    row["history_id"]: (
        row["cleanup_candidate"],
        row["auto_delete"],
        row["cleanup_action"],
    )
    for row in rows
}

assert actual == EXPECTED

for row in rows:
    print(
        f"HISTORY {row['history_id']}: PASS | "
        f"{row['lifecycle']} | "
        f"{row['retention']} | "
        f"candidate={row['cleanup_candidate']} | "
        f"auto_delete={row['auto_delete']} | "
        f"{row['cleanup_action']}"
    )


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
