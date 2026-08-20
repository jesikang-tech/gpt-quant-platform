from repository import (
    get_ai_decision_history_snapshot_retention,
)


EXPECTED = {
    1: "RETAIN",
    2: "RETAIN",
    4: "RETAIN",
    5: "RETAIN",
    6: "RETAIN",
    7: "RETAIN",
    8: "RETAIN",
    9: "RETAIN",
    10: "RETAIN",
    11: "RETAIN",
    12: "PROTECTED",
    13: "PROTECTED",
}


print("=" * 60)
print(
    "Production Hardening - History Snapshot "
    "Retention Repository Regression"
)
print("=" * 60)


rows = get_ai_decision_history_snapshot_retention()

assert len(rows) == len(EXPECTED)

actual = {
    row["history_id"]: row["retention"]
    for row in rows
}

assert actual == EXPECTED

for row in rows:
    print(
        f"HISTORY {row['history_id']}: PASS | "
        f"{row['lifecycle']} | "
        f"retention={row['retention']}"
    )

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
