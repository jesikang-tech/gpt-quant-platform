"""Lifecycle, retention and cleanup projections remain consistent and read-only."""
import pytest
from price_test_support import isolated_price_db, synthetic_snapshot_db


def test_repository_integrated_safety(synthetic_snapshot_db):
    from repository import (get_ai_decision_history_snapshot_lifecycle,
        get_ai_decision_history_snapshot_retention, get_ai_decision_history_snapshot_cleanup_candidates)
    before = synthetic_snapshot_db.db.path.read_bytes()
    lifecycle_rows = get_ai_decision_history_snapshot_lifecycle()
    retention_rows = get_ai_decision_history_snapshot_retention()
    cleanup_rows = get_ai_decision_history_snapshot_cleanup_candidates()
    assert_snapshot_rows(lifecycle_rows, retention_rows, cleanup_rows,
                         synthetic_snapshot_db.expected)
    lifecycle = {row["history_id"]: row for row in lifecycle_rows}
    retention = {row["history_id"]: row for row in retention_rows}
    cleanup = {row["history_id"]: row for row in cleanup_rows}
    assert set(lifecycle) == set(retention) == set(cleanup) == set(synthetic_snapshot_db.expected)
    for history_id in lifecycle:
        assert lifecycle[history_id]["classification"] == retention[history_id]["lifecycle"]
        assert retention[history_id]["retention"] == cleanup[history_id]["retention"]
        assert cleanup[history_id]["auto_delete"] is False
        assert cleanup[history_id]["cleanup_candidate"] == (retention[history_id]["retention"] == "REVIEW_REQUIRED")
        if lifecycle[history_id]["classification"] == "ACTIVE_OUTCOME_TRACKING":
            assert retention[history_id]["retention"] == "PROTECTED"
        if lifecycle[history_id]["classification"] == "COMPLETED":
            assert retention[history_id]["retention"] == "RETAIN_LONG_TERM"
    assert synthetic_snapshot_db.db.path.read_bytes() == before



def assert_snapshot_rows(lifecycle_rows, retention_rows, cleanup_rows, expected_ids):
    assert len(lifecycle_rows) == len(retention_rows) == len(cleanup_rows), "row counts differ"
    for rows in (lifecycle_rows, retention_rows, cleanup_rows):
        assert len(rows) == len(expected_ids), "unexpected row count"
        ids = [row["history_id"] for row in rows]
        assert len(ids) == len(set(ids)), "duplicate history_id"
        assert set(ids) == set(expected_ids), "unexpected history_id"


@pytest.mark.parametrize("projection", [0, 1, 2])
@pytest.mark.parametrize("append", [False, True])
def test_duplicate_history_id_is_rejected(projection, append):
    rows = [[{"history_id": 1}, {"history_id": 2}] for _ in range(3)]
    duplicate = {"history_id": 1}
    if append:
        rows[projection].append(duplicate)
    else:
        rows[projection][1] = duplicate
    with pytest.raises(AssertionError, match="row counts differ" if append else "duplicate history_id"):
        assert_snapshot_rows(*rows, {1, 2})
