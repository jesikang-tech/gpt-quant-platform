import sqlite3
from contextlib import closing
from datetime import date, timedelta

import pytest

import config
import current_analysis
import database


@pytest.fixture
def replay_db(tmp_path, monkeypatch):
    path = tmp_path / "replay # test.db"
    days = []
    day = date(2026, 1, 1)
    while len(days) < 60:
        if day.weekday() < 5:
            days.append(day.isoformat())
        day += timedelta(days=1)
    with closing(sqlite3.connect(path)) as conn:
        conn.executescript(
            "CREATE TABLE etf_info (ticker TEXT PRIMARY KEY, name TEXT);"
            "CREATE TABLE etf_prices (ticker TEXT, date TEXT, close_price REAL,"
            " PRIMARY KEY (ticker, date));"
        )
        for ticker, step in [("AAA", 1.0), ("BBB", 0.1), ("CCC", -0.1)]:
            conn.execute("INSERT INTO etf_info VALUES (?, ?)", (ticker, ticker))
            conn.executemany(
                "INSERT INTO etf_prices VALUES (?, ?, ?)",
                [(ticker, day, 100 + index * step) for index, day in enumerate(days)],
            )
        conn.commit()
    monkeypatch.setattr(config, "DATABASE_PATH", path)

    def reject_shared_connection():
        pytest.fail("Replay must not use the writable database connection")

    monkeypatch.setattr(database, "get_connection", reject_shared_connection)
    return path, days[-1]


@pytest.mark.parametrize("statement", [
    "INSERT INTO etf_info VALUES ('WRITE', 'WRITE')",
    "UPDATE etf_prices SET close_price = 1",
    "DELETE FROM etf_prices",
    "CREATE TABLE replay_results (score REAL)",
])
def test_replay_boundary_rejects_writes(replay_db, statement):
    path, _ = replay_db
    before = path.read_bytes()
    with closing(current_analysis._get_replay_connection()) as conn:
        assert conn.execute("SELECT COUNT(*) FROM etf_prices").fetchone()[0] == 180
        with pytest.raises(sqlite3.OperationalError, match="readonly"):
            conn.execute(statement)
    assert path.read_bytes() == before


def test_replay_boundary_does_not_create_missing_database(tmp_path, monkeypatch):
    path = tmp_path / "missing.db"
    monkeypatch.setattr(config, "DATABASE_PATH", path)
    with pytest.raises(sqlite3.OperationalError):
        current_analysis._get_replay_connection()
    assert not path.exists()


@pytest.mark.parametrize("period", ["1m", "2m", "3m"])
def test_replay_historical_ranking_is_unchanged_by_future_prices(replay_db, period):
    path, analysis_date = replay_db
    original = path.read_bytes()
    before = current_analysis.get_current_analysis_data(analysis_date=analysis_date, period=period)
    assert path.read_bytes() == original
    assert [row["ticker"] for row in before["current_score_top"]] == ["AAA", "BBB", "CCC"]
    assert before["db_write"] is False
    future_date = (date.fromisoformat(analysis_date) + timedelta(days=5)).isoformat()
    with closing(sqlite3.connect(path)) as conn:
        conn.executemany("INSERT INTO etf_prices VALUES (?, ?, ?)", [
            ("AAA", future_date, 1.0),
            ("BBB", future_date, 100000.0),
            ("CCC", future_date, 200000.0),
        ])
        conn.commit()
    updated = path.read_bytes()
    after = current_analysis.get_current_analysis_data(analysis_date=analysis_date, period=period)
    assert path.read_bytes() == updated

    def historical_rows(rows):
        return [{key: value for key, value in row.items()
                 if key not in ("future_performance", "future_performance_days", "reality_test")}
                for row in rows]

    assert historical_rows(before["current_score_top"]) == historical_rows(after["current_score_top"])
    assert historical_rows(before["selection"]["top"]) == historical_rows(after["selection"]["top"])
    assert before["selection"]["count"] == after["selection"]["count"]
    assert before["current_score_top"][0]["future_performance"] is None
    assert after["current_score_top"][0]["future_performance"] is not None


@pytest.mark.parametrize("future_prices, expected", [
    ([], (159.0, None, 0)),
    ([150.0, 140.0], (159.0, -5.66, 2)),
    ([180.0, 200.0, 170.0], (159.0, 25.79, 3)),
    ([160.0] * 40 + [10000.0], (159.0, 0.63, 40)),
])
def test_replay_exact_baseline_and_future_window(replay_db, future_prices, expected):
    path, analysis_date = replay_db
    day = date.fromisoformat(analysis_date)
    rows = []
    for price in future_prices:
        day += timedelta(days=1)
        while day.weekday() >= 5:
            day += timedelta(days=1)
        rows.append(("AAA", day.isoformat(), price))
    with closing(sqlite3.connect(path)) as conn:
        conn.executemany("INSERT INTO etf_prices VALUES (?, ?, ?)", rows)
        conn.commit()
    before = path.read_bytes()
    assert current_analysis._get_future_performance("AAA", analysis_date) == expected
    assert path.read_bytes() == before


@pytest.mark.parametrize("baseline", [None, 0.0, -10.0])
def test_replay_missing_or_nonpositive_baseline_has_no_result(replay_db, baseline):
    path, analysis_date = replay_db
    future_date = (date.fromisoformat(analysis_date) + timedelta(days=5)).isoformat()
    with closing(sqlite3.connect(path)) as conn:
        if baseline is None:
            conn.execute("DELETE FROM etf_prices WHERE ticker = ? AND date = ?",
                         ("AAA", analysis_date))
        else:
            conn.execute("UPDATE etf_prices SET close_price = ? WHERE ticker = ? AND date = ?",
                         (baseline, "AAA", analysis_date))
        conn.execute("INSERT INTO etf_prices VALUES (?, ?, ?)",
                     ("AAA", future_date, 9999.0))
        conn.commit()
    before = path.read_bytes()
    assert current_analysis._get_future_performance("AAA", analysis_date) == (None, None, 0)

    # Exercise the real API path: enough older prices still allow scoring,
    # but a future price must never be exposed as the historical price.
    import api_server
    response = api_server.app.test_client().get(
        f"/api/historical-replay?date={analysis_date}&period=1m"
    )
    assert response.status_code == 200
    result = response.get_json()
    row = next(row for row in result["current_score_top"] if row["ticker"] == "AAA")
    assert row["price"] is None
    assert row["future_performance"] is None
    assert row["future_performance_days"] == 0
    assert result["db_write"] is False
    assert path.read_bytes() == before
