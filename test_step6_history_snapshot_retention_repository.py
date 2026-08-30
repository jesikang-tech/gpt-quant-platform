from repository import (
    get_ai_decision_history_snapshot_retention,
)


EXPECTED = {
    1: "RETAIN",
    2: "RETAIN",
    3: "RETAIN",
    4: "RETAIN",
    5: "RETAIN",
    6: "PROTECTED",
    7: "PROTECTED",
    8: "PROTECTED",
    9: "PROTECTED",
    10: "PROTECTED",
    11: "PROTECTED",
    12: "PROTECTED",
    16: "PROTECTED",
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
