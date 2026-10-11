"""Lifecycle classification through the real repository on synthetic snapshots."""
from price_test_support import isolated_price_db, synthetic_snapshot_db


def test_lifecycle_classification(synthetic_snapshot_db):
    from repository import get_ai_decision_history_snapshot_lifecycle
    before = synthetic_snapshot_db.db.path.read_bytes()
    rows = get_ai_decision_history_snapshot_lifecycle()
    assert len(rows) == len(synthetic_snapshot_db.expected)
    for row in rows:
        expected, _, count = synthetic_snapshot_db.expected[row["history_id"]]
        assert row["classification"] == expected
        assert row["snapshot_count"] == count
        if expected in ("ACTIVE_OUTCOME_TRACKING", "COMPLETED"):
            assert row["snapshot_count"] == 4
    assert synthetic_snapshot_db.db.path.read_bytes() == before
