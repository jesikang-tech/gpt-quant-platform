import sqlite3
from contextlib import closing
from datetime import date, timedelta

import pytest

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
            if highs is not None:
                conn.execute("CREATE TABLE etf_ohlcv_prices(ticker TEXT, date TEXT, high_price REAL, PRIMARY KEY(ticker,date))")
                conn.executemany("INSERT INTO etf_ohlcv_prices VALUES ('TEST', ?, ?)", zip(days[61:], highs))
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
    response = api_server.app.test_client().get(
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
