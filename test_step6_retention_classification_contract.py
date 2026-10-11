"""Real retention policy, including the exact seven-day review boundary."""
from price_test_support import isolated_price_db, synthetic_snapshot_db


def test_retention_classification(synthetic_snapshot_db):
    from repository import get_ai_decision_history_snapshot_retention
    before = synthetic_snapshot_db.db.path.read_bytes()
    rows = get_ai_decision_history_snapshot_retention()
    assert len(rows) == len(synthetic_snapshot_db.expected)
    for row in rows:
        lifecycle, retention, _ = synthetic_snapshot_db.expected[row["history_id"]]
        assert row["lifecycle"] == lifecycle
        assert row["retention"] == retention
    assert synthetic_snapshot_db.db.path.read_bytes() == before


def test_seven_day_boundary_and_patch_restoration(isolated_price_db, monkeypatch):
    from datetime import datetime, timedelta, timezone
    import repository
    now = datetime(2026, 1, 15, tzinfo=timezone.utc)
    original = repository.datetime

    class FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return now if tz is None else now.astimezone(tz)

    conn = isolated_price_db.connect()
    try:
        with conn:
            conn.executemany("INSERT INTO ai_decision_outcome_history(outcome_status, created_at) VALUES ('PENDING', ?)",
                [((now-timedelta(days=age)).isoformat(),) for age in (6.999, 7, 7.001)])
    finally:
        conn.close()
    with monkeypatch.context() as patches:
        patches.setattr(repository, "datetime", FixedDateTime)
        rows = repository.get_ai_decision_history_snapshot_retention()
        by_age = sorted(rows, key=lambda row: row["age_days"])
        assert [row["retention"] for row in by_age] == ["RETAIN", "REVIEW_REQUIRED", "REVIEW_REQUIRED"]
    assert repository.datetime is original
