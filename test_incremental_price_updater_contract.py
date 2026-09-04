from collector.incremental_price_updater import calculate_update_range


def test_incremental_range_starts_after_latest_date():
    start_date, end_date = calculate_update_range(
        "2026-08-04",
        "2026-09-04",
    )

    assert start_date == "2026-08-05"
    assert end_date == "2026-09-04"


def test_incremental_range_skips_when_already_current():
    start_date, end_date = calculate_update_range(
        "2026-09-04",
        "2026-09-04",
    )

    assert start_date is None
    assert end_date == "2026-09-04"


def test_incremental_range_skips_when_latest_date_is_after_end_date():
    start_date, end_date = calculate_update_range(
        "2026-09-05",
        "2026-09-04",
    )

    assert start_date is None
    assert end_date == "2026-09-04"

def test_incremental_range_uses_initial_start_date_when_no_history_exists():
    start_date, end_date = calculate_update_range(
        None,
        "2026-09-04",
        initial_start_date="2025-01-01",
    )
    assert start_date == "2025-01-01"
    assert end_date == "2026-09-04"
