import sqlite3
from contextlib import closing
from datetime import date, timedelta

import pytest
from testing_helpers import authenticated_client

import config
import current_analysis


@pytest.fixture
def market(tmp_path, monkeypatch):
    path = tmp_path / "reality.db"
    monkeypatch.setattr(config, "DATABASE_PATH", path)

    def seed(closes, highs=None, baseline=100):
        with closing(sqlite3.connect(path)) as conn:
            conn.executescript(
                "CREATE TABLE etf_prices(ticker TEXT, date TEXT, close_price REAL, PRIMARY KEY(ticker,date));"
                "CREATE TABLE etf_info(ticker TEXT, name TEXT);"
                "INSERT INTO etf_info VALUES ('TEST', 'Test ETF');"
            )
            # Historical observations end on day zero; no network or production DB.
            day = date(2026, 1, 1)
            days = []
            while len(days) < 61 + len(closes):
                if day.weekday() < 5:
                    days.append(day.isoformat())
                day += timedelta(days=1)
            analysis_date = days[60]
            conn.executemany("INSERT INTO etf_prices VALUES ('TEST', ?, ?)",
                             [(d, 100) for d in days[:60]])
            if baseline is not None:
                conn.execute("INSERT INTO etf_prices VALUES ('TEST', ?, ?)", (analysis_date, baseline))
            conn.executemany("INSERT INTO etf_prices VALUES ('TEST', ?, ?)", zip(days[61:], closes))
            conn.execute("CREATE TABLE etf_ohlcv_prices(ticker TEXT, date TEXT, close_price REAL, high_price REAL, PRIMARY KEY(ticker,date))")
            if baseline is not None:
                conn.execute("INSERT INTO etf_ohlcv_prices VALUES ('TEST', ?, ?, NULL)", (analysis_date, baseline))
            highs = highs or []
            conn.executemany("INSERT INTO etf_ohlcv_prices VALUES ('TEST', ?, ?, ?)",
                             [(day, close, highs[i] if i < len(highs) else None)
                              for i, (day, close) in enumerate(zip(days[61:], closes))])
            conn.commit()
        return analysis_date

    return path, seed


@pytest.mark.parametrize("period,window,target", [("1m",20,5), ("2m",40,10), ("3m",60,15)])
def test_period_window_endpoint_and_legacy_compatibility(market, period, window, target):
    path, seed = market
    closes = [100] * window + [999]
    closes[0] = 104
    closes[window - 1] = 102
    analysis_date = seed(closes, [100] * window + [999])
    before = path.read_bytes()
    result = current_analysis._get_reality_test("TEST", analysis_date, period)
    assert result["window_days"] == window
    assert result["target_return_pct"] == target
    assert result["observed_days"] == window
    assert result["max_close_return_pct"] == 4
    assert result["endpoint_close_return_pct"] == 2
    assert result["high_status"] == result["close_status"] == "FAIL"
    assert result["high_first_hit_day"] is result["close_first_hit_day"] is None
    # The legacy metric still uses up to 40 observations, independent of period.
    legacy = current_analysis._get_future_performance("TEST", analysis_date)
    assert legacy == (100, 899.0 if window == 20 else 4.0, min(window + 1, 40))
    import api_server
    response = authenticated_client(api_server.app).get(
        f"/api/historical-replay?date={analysis_date}&period={period}"
    )
    assert response.status_code == 200
    row = response.get_json()["current_score_top"][0]
    assert row["reality_test"] == result
    assert (row["price"], row["future_performance"], row["future_performance_days"]) == legacy
    assert path.read_bytes() == before


@pytest.mark.parametrize("baseline", [None, 0, -1])
def test_exact_positive_baseline_required(market, baseline):
    path, seed = market
    analysis_date = seed([200, 300], [250, 350], baseline)
    before = path.read_bytes()
    result = current_analysis._get_reality_test("TEST", analysis_date, "1m")
    assert result["available"] is False
    assert result["unavailable_reason"] == ("MISSING_BASELINE" if baseline is None else "INVALID_BASELINE")
    assert result["max_close_return_pct"] is result["endpoint_close_return_pct"] is None
    assert result["high_status"] is result["close_status"] is None
    assert path.read_bytes() == before


def test_independent_first_hits_and_exact_fifteen_percent(market):
    _, seed = market
    closes, highs = [100] * 60, [100] * 60
    highs[11], closes[11] = 116, 113
    highs[17], closes[17] = 117, 115
    highs[20], closes[20] = 130, 125
    analysis_date = seed(closes, highs)
    result = current_analysis._get_reality_test("TEST", analysis_date, "3m")
    assert result["high_status"] == result["close_status"] == "PASS"
    assert result["high_first_hit_day"] == 12
    assert result["close_first_hit_day"] == 18


@pytest.mark.parametrize("count,high_hit,expected_high,expected_close", [
    (20, True, "PASS", "FAIL"),
    (3, True, "PASS", "PENDING"),
    (3, False, "PENDING", "PENDING"),
    (0, False, "PENDING", "PENDING"),
    (20, False, "FAIL", "FAIL"),
])
def test_complete_and_partial_statuses(market, count, high_hit, expected_high, expected_close):
    _, seed = market
    highs = [104] * count
    if high_hit:
        highs[1] = 105
    analysis_date = seed([101] * count, highs)
    result = current_analysis._get_reality_test("TEST", analysis_date, "1m")
    assert result["high_status"] == expected_high
    assert result["close_status"] == expected_close
    assert result["high_first_hit_day"] == (2 if high_hit else None)
    assert result["observed_days"] == count
    assert result["endpoint_close_return_pct"] == (1 if count == 20 else None)


@pytest.mark.parametrize("highs", [None, [], [None] * 20])
def test_missing_high_never_uses_close_and_replay_still_works(market, highs):
    path, seed = market
    analysis_date = seed([110] * 20, highs)
    before = path.read_bytes()
    data = current_analysis.get_current_analysis_data(analysis_date=analysis_date, period="1m")
    result = data["current_score_top"][0]["reality_test"]
    assert result["close_status"] == "PASS"
    assert result["close_first_hit_day"] == 1
    assert result["high_status"] is None
    assert result["high_unavailable_reason"] == "INCOMPLETE_HIGH_COVERAGE"
    assert result["high_first_hit_day"] is None
    assert result["high_observed_days"] == 0
    assert path.read_bytes() == before


def test_missing_high_does_not_shift_first_hit_day(market):
    _, seed = market
    analysis_date = seed([100, 105, 106], [None, None, 106])
    result = current_analysis._get_reality_test("TEST", analysis_date, "1m")
    assert result["high_first_hit_day"] == 3
    assert result["close_first_hit_day"] == 2
    assert result["high_observed_days"] == 1


def test_period_configuration_is_reused(market, monkeypatch):
    _, seed = market
    analysis_date = seed([101, 102, 999], [101, 102, 999])
    monkeypatch.setattr(current_analysis, "_get_period_config", lambda period: {
        "lookback_trading_days": 2, "return_threshold": 2.0,
    })
    result = current_analysis._get_reality_test("TEST", analysis_date, "1m")
    assert result["window_days"] == 2
    assert result["target_return_pct"] == 2
    assert result["endpoint_close_return_pct"] == 2
    assert result["high_first_hit_day"] == result["close_first_hit_day"] == 2


@pytest.mark.parametrize("period,window", [("1m", 20), ("2m", 40), ("3m", 60)])
@pytest.mark.parametrize("coverage", [0, 1, "all_but_one", "all"])
def test_completed_high_failure_requires_full_coverage(market, period, window, coverage):
    path, seed = market
    count = window if coverage == "all" else window - 1 if coverage == "all_but_one" else coverage
    analysis_date = seed([100] * window, [100] * count + [None] * (window - count))
    before = path.read_bytes()
    result = current_analysis._get_reality_test("TEST", analysis_date, period)
    assert result["high_observed_days"] == count
    assert result["high_status"] == ("FAIL" if count == window else None)
    assert result["high_unavailable_reason"] == (None if count == window else "INCOMPLETE_HIGH_COVERAGE")
    assert result["high_first_hit_day"] is None
    assert result["close_status"] == "FAIL"
    assert result["available"] is True
    assert result["endpoint_close_return_pct"] == 0
    assert path.read_bytes() == before


@pytest.mark.parametrize("count", [3, 20])
def test_observed_high_pass_wins_despite_missing_coverage(market, count):
    _, seed = market
    analysis_date = seed([100] * count, [None, 105] + [None] * (count - 2))
    result = current_analysis._get_reality_test("TEST", analysis_date, "1m")
    assert result["high_status"] == "PASS"
    assert result["high_first_hit_day"] == 2
    assert result["high_observed_days"] == 1
    assert result["high_unavailable_reason"] is None
    assert result["close_status"] == ("FAIL" if count == 20 else "PENDING")


@pytest.mark.parametrize("highs", [None, [None, 100, None]])
def test_incomplete_window_without_high_hit_remains_pending(market, highs):
    _, seed = market
    analysis_date = seed([100] * 3, highs)
    result = current_analysis._get_reality_test("TEST", analysis_date, "1m")
    assert result["high_status"] == "PENDING"
    assert result["high_unavailable_reason"] is None
    assert result["high_observed_days"] == (0 if highs is None else 1)
    assert result["close_status"] == "PENDING"


def test_reality_uses_only_ohlcv_basis_and_observation_dates(market):
    path, seed = market
    analysis_date = seed([100, 104, 110], [101, 106, 112])
    with closing(sqlite3.connect(path)) as conn:
        # OHLCV is on a different price basis from legacy history.
        conn.execute("UPDATE etf_ohlcv_prices SET close_price=close_price*2, high_price=high_price*2")
        # A legacy-only date must not count toward the Reality Test window.
        conn.execute("DELETE FROM etf_ohlcv_prices WHERE date=(SELECT MIN(date) FROM etf_ohlcv_prices WHERE date>?)", (analysis_date,))
        conn.commit()
    before = path.read_bytes()
    result = current_analysis._get_reality_test("TEST", analysis_date, "1m")
    assert result["observed_days"] == 2
    assert result["high_first_hit_day"] == 1
    assert result["close_first_hit_day"] == 2
    assert result["max_close_return_pct"] == 10
    assert result["high_status"] == result["close_status"] == "PASS"
    assert current_analysis._get_future_performance("TEST", analysis_date) == (100, 10, 3)
    assert path.read_bytes() == before
    with closing(sqlite3.connect(path)) as conn:
        conn.execute("UPDATE etf_prices SET close_price=7")
        conn.execute("DELETE FROM etf_prices WHERE date>?", (analysis_date,))
        conn.commit()
    assert current_analysis._get_reality_test("TEST", analysis_date, "1m") == result
    assert current_analysis._get_future_performance("TEST", analysis_date) == (7, None, 0)


@pytest.mark.parametrize("case,reason", [
    ("missing_table", "MISSING_BASELINE"), ("missing_row", "MISSING_BASELINE"),
    ("null", "INVALID_BASELINE"), ("zero", "INVALID_BASELINE"),
    ("negative", "INVALID_BASELINE"),
])
def test_ohlcv_baseline_never_falls_back_to_valid_legacy(market, case, reason):
    path, seed = market
    analysis_date = seed([110], [115])
    with closing(sqlite3.connect(path)) as conn:
        if case == "missing_table":
            conn.execute("DROP TABLE etf_ohlcv_prices")
        elif case == "missing_row":
            conn.execute("DELETE FROM etf_ohlcv_prices WHERE date=?", (analysis_date,))
        else:
            conn.execute("UPDATE etf_ohlcv_prices SET close_price=? WHERE date=?",
                         ({"null": None, "zero": 0, "negative": -1}[case], analysis_date))
        conn.commit()
    before = path.read_bytes()
    data = current_analysis.get_current_analysis_data(analysis_date=analysis_date, period="1m")
    row = data["current_score_top"][0]
    assert row["reality_test"]["available"] is False
    assert row["reality_test"]["unavailable_reason"] == reason
    assert row["reality_test"]["close_status"] is None
    assert row["price"] == 100
    assert row["future_performance"] == 10
    assert path.read_bytes() == before


def test_null_future_ohlcv_close_is_not_replaced_by_legacy(market):
    path, seed = market
    analysis_date = seed([110, 120], [115, 125])
    with closing(sqlite3.connect(path)) as conn:
        conn.execute("UPDATE etf_ohlcv_prices SET close_price=NULL WHERE date>?", (analysis_date,))
        conn.commit()
    result = current_analysis._get_reality_test("TEST", analysis_date, "1m")
    assert result["available"] is True
    assert result["unavailable_reason"] is None
    assert result["close_status"] == "PENDING"
    assert result["close_unavailable_reason"] is None
    assert result["high_status"] == "PASS"
    assert result["observed_days"] == 2
    assert result["max_close_return_pct"] is None
    assert current_analysis._get_future_performance("TEST", analysis_date) == (100, 20, 2)


@pytest.mark.parametrize("invalid", [None, float("inf"), float("-inf"), float("nan")])
@pytest.mark.parametrize("count,hit", [(3, False), (20, False), (3, True), (20, True)])
def test_invalid_close_coverage_preserves_independent_results(market, invalid, count, hit):
    path, seed = market
    closes = [101] * count
    closes[1] = 105 if hit else 102
    analysis_date = seed(closes, [106] * count)
    with closing(sqlite3.connect(path)) as conn:
        conn.execute("UPDATE etf_ohlcv_prices SET close_price=? WHERE date="
                     "(SELECT MIN(date) FROM etf_ohlcv_prices WHERE date>?)",
                     (invalid, analysis_date))
        conn.commit()
    before = path.read_bytes()
    result = current_analysis._get_reality_test("TEST", analysis_date, "1m")
    assert result["available"] is True
    assert result["unavailable_reason"] is None
    assert result["observed_days"] == count
    assert result["high_status"] == "PASS"
    assert result["high_first_hit_day"] == 1
    assert result["close_status"] == ("PASS" if hit else None if count == 20 else "PENDING")
    assert result["close_unavailable_reason"] == (
        "INCOMPLETE_CLOSE_COVERAGE" if count == 20 and not hit else None
    )
    assert result["close_first_hit_day"] == (2 if hit else None)
    assert result["max_close_return_pct"] == (5 if hit else 2)
    assert result["endpoint_close_return_pct"] == (1 if count == 20 else None)
    assert path.read_bytes() == before


def test_invalid_endpoint_is_not_replaced_with_previous_valid_close(market):
    path, seed = market
    analysis_date = seed([102] * 20, [103] * 20)
    with closing(sqlite3.connect(path)) as conn:
        conn.execute("UPDATE etf_ohlcv_prices SET close_price=NULL WHERE date="
                     "(SELECT MAX(date) FROM etf_ohlcv_prices)")
        conn.commit()
    result = current_analysis._get_reality_test("TEST", analysis_date, "1m")
    assert result["observed_days"] == 20
    assert result["close_status"] is None
    assert result["close_unavailable_reason"] == "INCOMPLETE_CLOSE_COVERAGE"
    assert result["endpoint_close_return_pct"] is None
    assert result["max_close_return_pct"] == 2
    assert result["high_status"] == "FAIL"

def test_reality_test_excludes_weekend_rows_from_trading_day_window(market):
    path, seed = market
    analysis_date = seed([101] * 20, [102] * 20)

    with closing(sqlite3.connect(path)) as conn:
        first_future = conn.execute(
            "SELECT MIN(date) FROM etf_ohlcv_prices WHERE date > ?",
            (analysis_date,),
        ).fetchone()[0]

        saturday = (
            date.fromisoformat(first_future)
            + timedelta(days=(5 - date.fromisoformat(first_future).weekday()) % 7)
        ).isoformat()
        sunday = (
            date.fromisoformat(saturday) + timedelta(days=1)
        ).isoformat()

        conn.execute(
            "INSERT OR REPLACE INTO etf_ohlcv_prices "
            "VALUES ('TEST', ?, 999, 999)",
            (saturday,),
        )
        conn.execute(
            "INSERT OR REPLACE INTO etf_ohlcv_prices "
            "VALUES ('TEST', ?, 999, 999)",
            (sunday,),
        )
        conn.commit()

    result = current_analysis._get_reality_test(
        "TEST", analysis_date, "1m"
    )

    assert result["observed_days"] == 20
    assert result["close_first_hit_day"] is None
    assert result["high_first_hit_day"] is None
    assert result["close_status"] == "FAIL"
    assert result["high_status"] == "FAIL"


def test_legacy_future_performance_excludes_weekend_rows(market):
    path, seed = market
    analysis_date = seed([101] * 40, [102] * 40)

    with closing(sqlite3.connect(path)) as conn:
        first_future = conn.execute(
            "SELECT MIN(date) FROM etf_prices WHERE date > ?",
            (analysis_date,),
        ).fetchone()[0]
        first_future_date = date.fromisoformat(first_future)
        saturday = (
            first_future_date
            + timedelta(days=(5 - first_future_date.weekday()) % 7)
        ).isoformat()
        sunday = (
            date.fromisoformat(saturday) + timedelta(days=1)
        ).isoformat()

        conn.execute(
            "INSERT OR REPLACE INTO etf_prices VALUES ('TEST', ?, 999)",
            (saturday,),
        )
        conn.execute(
            "INSERT OR REPLACE INTO etf_prices VALUES ('TEST', ?, 999)",
            (sunday,),
        )
        conn.commit()

    assert current_analysis._get_future_performance(
        "TEST", analysis_date
    ) == (100, 1.0, 40)

def test_replay_price_history_excludes_weekend_rows(market):
    path, seed = market
    analysis_date = seed([101] * 3, [102] * 3)

    with closing(sqlite3.connect(path)) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO etf_prices VALUES ('TEST', ?, 999)",
            ("2026-03-21",),
        )
        conn.execute(
            "INSERT OR REPLACE INTO etf_prices VALUES ('TEST', ?, 999)",
            ("2026-03-22",),
        )
        conn.commit()

    rows = current_analysis.get_etf_prices("TEST", analysis_date)

    assert all(
        date.fromisoformat(row[0]).weekday() < 5
        for row in rows
    )
