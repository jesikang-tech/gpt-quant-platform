import sqlite3
from contextlib import closing
from datetime import date, timedelta

import pytest

import config
import current_analysis


@pytest.fixture
def close_market(tmp_path, monkeypatch):
    db = tmp_path / "close_only_reality.db"
    monkeypatch.setattr(config, "DATABASE_PATH", db)

    def seed(closes, baseline=100):
        start = date(2026, 1, 1)
        days = []
        while len(days) < 61 + len(closes):
            if start.weekday() < 5:
                days.append(start.isoformat())
            start += timedelta(days=1)

        analysis_date = days[60]

        with closing(sqlite3.connect(db)) as conn:
            conn.execute(
                "CREATE TABLE etf_prices("
                "ticker TEXT, date TEXT, close_price REAL, "
                "PRIMARY KEY(ticker, date))"
            )
            conn.executemany(
                "INSERT INTO etf_prices VALUES ('TEST', ?, 100)",
                [(day,) for day in days[:60]],
            )
            if baseline is not None:
                conn.execute(
                    "INSERT INTO etf_prices VALUES ('TEST', ?, ?)",
                    (analysis_date, baseline),
                )
            conn.executemany(
                "INSERT INTO etf_prices VALUES ('TEST', ?, ?)",
                list(zip(days[61:], closes)),
            )
            conn.commit()

        return analysis_date

    return db, seed


@pytest.mark.parametrize(
    "period,window,target",
    [("1m", 20, 5), ("2m", 40, 10), ("3m", 60, 15)],
)
def test_close_only_complete_window(close_market, period, window, target):
    db, seed = close_market
    closes = [100] * window
    closes[4] = 100 + target
    analysis_date = seed(closes)
    before = db.read_bytes()

    result = current_analysis._get_close_only_reality_test(
        "TEST", analysis_date, period
    )

    assert result["available"] is True
    assert result["window_days"] == window
    assert result["target_return_pct"] == target
    assert result["observed_days"] == window
    assert result["close_status"] == "PASS"
    assert result["close_first_hit_day"] == 5
    assert result["max_close_return_pct"] == target
    assert result["endpoint_close_return_pct"] == 0
    assert db.read_bytes() == before


@pytest.mark.parametrize("baseline", [None, 0, -1])
def test_close_only_invalid_baseline(close_market, baseline):
    db, seed = close_market
    analysis_date = seed([110, 120], baseline=baseline)
    before = db.read_bytes()

    result = current_analysis._get_close_only_reality_test(
        "TEST", analysis_date, "1m"
    )

    assert result["available"] is False
    assert result["unavailable_reason"] == (
        "MISSING_BASELINE" if baseline is None else "INVALID_BASELINE"
    )
    assert result["close_status"] is None
    assert db.read_bytes() == before


def test_close_only_partial_window_remains_pending(close_market):
    db, seed = close_market
    analysis_date = seed([101, 102, 103])
    before = db.read_bytes()

    result = current_analysis._get_close_only_reality_test(
        "TEST", analysis_date, "1m"
    )

    assert result["available"] is True
    assert result["observed_days"] == 3
    assert result["close_status"] == "PENDING"
    assert result["endpoint_close_return_pct"] is None
    assert db.read_bytes() == before
def test_close_only_missing_market_day_never_false_fails(
    close_market,
):
    db, seed = close_market
    analysis_date = seed([100] * 21)

    with closing(sqlite3.connect(db)) as conn:
        dates = [
            row[0] for row in conn.execute(
                "SELECT date FROM etf_prices "
                "WHERE ticker = 'TEST' AND date > ? "
                "ORDER BY date",
                (analysis_date,),
            )
        ]
        missing_date = dates[5]

        conn.execute(
            "DELETE FROM etf_prices "
            "WHERE ticker = 'TEST' AND date = ?",
            (missing_date,),
        )

        conn.execute(
            "INSERT INTO etf_prices VALUES ('OTHER', ?, 100)",
            (missing_date,),
        )
        conn.commit()

    before = db.read_bytes()

    result = current_analysis._get_close_only_reality_test(
        "TEST", analysis_date, "1m"
    )

    assert result["close_status"] != "FAIL"
    assert result["endpoint_close_return_pct"] is None
    assert db.read_bytes() == before
def test_close_only_hit_day_uses_market_day_number(close_market):
    db, seed = close_market
    closes = [100] * 20
    closes[6] = 106
    analysis_date = seed(closes)

    with closing(sqlite3.connect(db)) as conn:
        missing_date = conn.execute(
            "SELECT date FROM etf_prices "
            "WHERE ticker = 'TEST' AND date > ? "
            "ORDER BY date LIMIT 1 OFFSET 2",
            (analysis_date,),
        ).fetchone()[0]

        conn.execute(
            "DELETE FROM etf_prices "
            "WHERE ticker = 'TEST' AND date = ?",
            (missing_date,),
        )
        conn.execute(
            "INSERT INTO etf_prices VALUES ('OTHER', ?, 100)",
            (missing_date,),
        )
        conn.commit()

    before = db.read_bytes()

    result = current_analysis._get_close_only_reality_test(
        "TEST", analysis_date, "1m"
    )

    assert result["close_status"] == "PASS"
    assert result["close_first_hit_day"] == 7
    assert db.read_bytes() == before
def test_close_only_result_attached_after_ranking():
    from pathlib import Path

    source = Path("current_analysis.py").read_text(encoding="utf-8")

    ranking = source.index("current_score_top = all_scores[:limit]")
    attachment = source.index(
        'row["reality_test"] = _get_reality_test('
    )

    expected = (
        'row["close_only_reality_test"] = '
        '_get_close_only_reality_test('
    )

    assert expected in source
    assert source.index(expected) > ranking
    assert source.index(expected) > attachment
