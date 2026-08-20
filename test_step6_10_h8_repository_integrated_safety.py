from repository import (
    get_ai_decision_history_snapshot_lifecycle,
    get_ai_decision_history_snapshot_retention,
    get_ai_decision_history_snapshot_cleanup_candidates,
)


lifecycle_rows = (
    get_ai_decision_history_snapshot_lifecycle()
)

retention_rows = (
    get_ai_decision_history_snapshot_retention()
)

cleanup_rows = (
    get_ai_decision_history_snapshot_cleanup_candidates()
)


assert len(lifecycle_rows) == len(retention_rows)
assert len(retention_rows) == len(cleanup_rows)


lifecycle_map = {
    row["history_id"]: row
    for row in lifecycle_rows
}

retention_map = {
    row["history_id"]: row
    for row in retention_rows
}

cleanup_map = {
    row["history_id"]: row
    for row in cleanup_rows
}


assert set(lifecycle_map) == set(retention_map)
assert set(retention_map) == set(cleanup_map)


print("=" * 60)
print(
    "Step6-10-H-8 Repository Integrated Safety Regression"
)
print("=" * 60)


for history_id in sorted(lifecycle_map):
    lifecycle = lifecycle_map[history_id]
    retention = retention_map[history_id]
    cleanup = cleanup_map[history_id]

    assert (
        lifecycle["classification"]
        == retention["lifecycle"]
    )

    assert (
        retention["retention"]
        == cleanup["retention"]
    )

    assert (
        cleanup["cleanup_candidate"]
        is False
        or cleanup["retention"]
        == "REVIEW_REQUIRED"
    )

    assert cleanup["auto_delete"] is False

    if lifecycle["classification"] == (
        "ACTIVE_OUTCOME_TRACKING"
    ):
        assert retention["retention"] == "PROTECTED"
        assert cleanup["cleanup_candidate"] is False

    if lifecycle["classification"] == "COMPLETED":
        assert (
            retention["retention"]
            == "RETAIN_LONG_TERM"
        )
        assert cleanup["cleanup_candidate"] is False

    print(
        f"HISTORY {history_id}: PASS | "
        f"{lifecycle['classification']} | "
        f"{retention['retention']} | "
        f"candidate={cleanup['cleanup_candidate']} | "
        f"auto_delete={cleanup['auto_delete']}"
    )


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
