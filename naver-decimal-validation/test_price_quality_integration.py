"""Synthetic SQLite integration tests for existing quality summaries.

All databases are created under pytest's temporary directory.
No operational database path, network request, or real market data is used.
"""

import sqlite3

import pytest

from price_quality import (
    summarize_price_quality_by_date,
    summarize_price_quality_overall,
)
from price_quality_decision_adapter import (
    assess_daily_quality_summary,
    assess_overall_quality_summary,
)


DAY = "2026-09-16"


def make_database(tmp_path, prices=(), ohlcv=()):
    path = tmp_path / "synthetic_price_quality.sqlite3"

    with sqlite3.connect(path) as connection:
        connection.executescript(
            """
            CREATE TABLE etf_prices (
                ticker TEXT NOT NULL,
                date TEXT NOT NULL,
                close_price TEXT,
                UNIQUE (ticker, date)
            );

            CREATE TABLE etf_ohlcv_prices (
                ticker TEXT NOT NULL,
                date TEXT NOT NULL,
                close_price TEXT,
                UNIQUE (ticker, date)
            );
            """
        )

        connection.executemany(
            "INSERT INTO etf_prices "
            "(ticker, date, close_price) VALUES (?, ?, ?)",
            prices,
        )

        connection.executemany(
            "INSERT INTO etf_ohlcv_prices "
            "(ticker, date, close_price) VALUES (?, ?, ?)",
            ohlcv,
        )

    return path


def check_both_summaries(path, expected_status, expected_category):
    overall = summarize_price_quality_overall(path)
    daily = summarize_price_quality_by_date(path, DAY)

    for summary in (overall, daily):
        assert summary["price_source_verified"] is False
        assert summary[expected_category] == 1
        assert summary["total"] == 1

    overall_decision = assess_overall_quality_summary(overall)
    daily_decision = assess_daily_quality_summary(daily)

    for decision in (overall_decision, daily_decision):
        assert decision.status == expected_status
        assert decision.analysis_authorized is False
        assert decision.persistence_authorized is False


def test_matching_prices_remain_unverified(tmp_path):
    path = make_database(
        tmp_path,
        prices=[("AAA", DAY, "100.00")],
        ohlcv=[("AAA", DAY, "100.0")],
    )

    check_both_summaries(
        path,
        "CONSISTENT_UNVERIFIED",
        "MATCH",
    )


def test_mismatched_prices_are_blocked(tmp_path):
    path = make_database(
        tmp_path,
        prices=[("AAA", DAY, "100")],
        ohlcv=[("AAA", DAY, "101")],
    )

    check_both_summaries(path, "BLOCKED", "MISMATCH")


@pytest.mark.parametrize("missing_side", ["price", "ohlcv"])
def test_missing_source_is_blocked(tmp_path, missing_side):
    row = ("AAA", DAY, "100")
    prices = [] if missing_side == "price" else [row]
    ohlcv = [] if missing_side == "ohlcv" else [row]

    path = make_database(
        tmp_path,
        prices=prices,
        ohlcv=ohlcv,
    )

    check_both_summaries(path, "BLOCKED", "MISSING_SOURCE")


def test_invalid_price_is_blocked(tmp_path):
    path = make_database(
        tmp_path,
        prices=[("AAA", DAY, "invalid")],
        ohlcv=[("AAA", DAY, "100")],
    )

    check_both_summaries(path, "BLOCKED", "INVALID_PRICE")


def test_empty_database_is_blocked(tmp_path):
    path = make_database(tmp_path)

    overall = summarize_price_quality_overall(path)
    daily = summarize_price_quality_by_date(path, DAY)

    for summary in (overall, daily):
        assert summary["total"] == 0

    for decision in (
        assess_overall_quality_summary(overall),
        assess_daily_quality_summary(daily),
    ):
        assert decision.status == "BLOCKED"
        assert decision.reason == "EMPTY_DATASET"
        assert decision.analysis_authorized is False
        assert decision.persistence_authorized is False


def test_quality_summary_does_not_modify_database(tmp_path):
    path = make_database(
        tmp_path,
        prices=[("AAA", DAY, "100")],
        ohlcv=[("AAA", DAY, "100")],
    )

    before = path.read_bytes()

    summarize_price_quality_overall(path)
    summarize_price_quality_by_date(path, DAY)

    after = path.read_bytes()

    assert before == after


def test_date_scope_excludes_other_dates(tmp_path):
    path = make_database(
        tmp_path,
        prices=[
            ("AAA", DAY, "100"),
            ("BBB", "2026-09-17", "200"),
        ],
        ohlcv=[
            ("AAA", DAY, "100"),
            ("BBB", "2026-09-17", "201"),
        ],
    )

    overall = summarize_price_quality_overall(path)
    daily = summarize_price_quality_by_date(path, DAY)

    assert overall["total"] == 2
    assert overall["MATCH"] == 1
    assert overall["MISMATCH"] == 1
    assert daily["total"] == 1
    assert daily["MATCH"] == 1
    assert daily["MISMATCH"] == 0

    assert assess_overall_quality_summary(overall).status == "BLOCKED"

    daily_decision = assess_daily_quality_summary(daily)
    assert daily_decision.status == "CONSISTENT_UNVERIFIED"
    assert daily_decision.analysis_authorized is False
    assert daily_decision.persistence_authorized is False
