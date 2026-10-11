"""Lifecycle, retention and cleanup projections remain consistent and read-only."""
from price_test_support import isolated_price_db, synthetic_snapshot_db


def test_repository_integrated_safety(synthetic_snapshot_db):
    from repository import (get_ai_decision_history_snapshot_lifecycle,
        get_ai_decision_history_snapshot_retention, get_ai_decision_history_snapshot_cleanup_candidates)
    before = synthetic_snapshot_db.db.path.read_bytes()
    lifecycle = {row["history_id"]: row for row in get_ai_decision_history_snapshot_lifecycle()}
    retention = {row["history_id"]: row for row in get_ai_decision_history_snapshot_retention()}
    cleanup = {row["history_id"]: row for row in get_ai_decision_history_snapshot_cleanup_candidates()}
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
