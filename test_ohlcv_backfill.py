import importlib
import sqlite3
from contextlib import closing

import pandas as pd
import pytest

import config
import database
import collector.ohlcv_backfill as module


class FakeProvider:
    def __init__(self):
        self.calls = []
        self.responses = {}

    def get_price(self, ticker, start, end):
        self.calls.append((ticker, start, end))
        response = self.responses[ticker]
        if isinstance(response, Exception):
            raise response
        return response


def frame(days, **values):
    return pd.DataFrame(values, index=pd.to_datetime(days))


@pytest.fixture
def setup(tmp_path, monkeypatch):
    path = tmp_path / "backfill.db"
    monkeypatch.setattr(config, "DATABASE_PATH", path)
    monkeypatch.setattr(database, "DATABASE_PATH", path)
    database.init_database()
    with closing(sqlite3.connect(path)) as conn:
        conn.executemany("INSERT INTO etf_prices VALUES (?, ?, ?)", [
            ("A", "2026-01-02", 100), ("A", "2026-01-05", 101),
            ("B", "2026-02-02", 200), ("B", "2026-02-03", 201),
        ])
        conn.execute("INSERT INTO etf_info(ticker) VALUES ('INFO_ONLY')")
        conn.commit()
    provider = FakeProvider()
    provider.responses = {
        "A": frame(["2026-01-02", "2026-01-05"], Open=[99, 100], High=[110, 111],
                   Low=[98, 99], Close=[102, 103], Volume=[10, 20]),
        "B": frame(["2026-02-02"], Close=[202]),
    }
    return path, provider, module.OHLCVBackfill(path, provider)


def snapshot(path):
    with closing(sqlite3.connect(path)) as conn:
        return (
            conn.execute("SELECT sql FROM sqlite_master WHERE name='etf_prices'").fetchone(),
            conn.execute("SELECT * FROM etf_prices ORDER BY ticker,date").fetchall(),
            conn.execute("SELECT * FROM etf_info").fetchall(),
        )


def ohlcv(path):
    with closing(sqlite3.connect(path)) as conn:
        return conn.execute("SELECT * FROM etf_ohlcv_prices ORDER BY ticker,date").fetchall()


def test_targets_ranges_and_legacy_preservation(setup):
    path, provider, service = setup
    before = snapshot(path)
    assert service.get_targets() == [("A", "2026-01-02", "2026-01-05"),
                                     ("B", "2026-02-02", "2026-02-03")]
    result = service.backfill()
    assert result["attempted"] == result["succeeded"] == 2
    assert result["failed"] == result["skipped"] == 0
    assert provider.calls == service.get_targets()
    assert snapshot(path) == before
    assert ohlcv(path)[0] == ("A", "2026-01-02", 99, 110, 98, 102, 10)
    assert ohlcv(path)[-1][3] is None  # Close 202 must not become High.


def test_single_ticker_clips_provider_output_and_skips_unknown(setup):
    path, provider, service = setup
    provider.responses["A"] = frame(["2026-01-01", "2026-01-02", "2026-01-06"], Close=[9, 100, 999])
    result = service.backfill_ticker("A")
    assert result["rows_written"] == 1
    assert result["rows_skipped"] == 2
    assert [row[:2] for row in ohlcv(path)] == [("A", "2026-01-02")]
    assert service.backfill_ticker("INFO_ONLY")["status"] == "SKIPPED"
    assert provider.calls == [("A", "2026-01-02", "2026-01-05")]


def test_in_range_date_requires_exact_ticker_legacy_row(setup):
    path, provider, service = setup
    # The gap exists for another ticker, but must not become a date for A.
    with closing(sqlite3.connect(path)) as conn:
        conn.execute("INSERT INTO etf_prices VALUES ('B', '2026-01-03', 200)")
        conn.commit()
    before = snapshot(path)
    provider.responses["A"] = frame(
        ["2026-01-02", "2026-01-03", "2026-01-05"],
        High=[110, 999, 111], Close=[102, 998, 103],
    )
    for _ in range(2):
        result = service.backfill_ticker("A")
        assert result["status"] == "SUCCEEDED"
        assert result["rows_written"] == 2
        assert result["rows_skipped"] == 1
        assert [row[:2] for row in ohlcv(path)] == [
            ("A", "2026-01-02"), ("A", "2026-01-05")
        ]
        assert snapshot(path) == before
    assert provider.calls == [("A", "2026-01-02", "2026-01-05")] * 2


@pytest.mark.parametrize("missing", [None, float("nan"), pd.NA, "absent"])
def test_rerun_preserves_nonnull_fields_without_duplicates(setup, missing):
    path, provider, service = setup
    service.backfill_ticker("A")
    values = {"Close": [105, 106]}
    if not isinstance(missing, str):
        values["High"] = [missing, missing]
    provider.responses["A"] = frame(["2026-01-02", "2026-01-05"], **values)
    assert service.backfill_ticker("A")["status"] == "SUCCEEDED"
    rows = ohlcv(path)
    assert len(rows) == 2
    assert rows[0][2:] == (99, 110, 98, 105, 10)
    assert rows[1][3] == 111


def test_failure_isolated_and_partial_population_resumes(setup):
    path, provider, service = setup
    provider.responses["A"] = provider.responses["A"].iloc[:1]
    assert service.backfill_ticker("A")["rows_written"] == 1
    provider.responses["A"] = frame(["2026-01-02", "2026-01-05"], High=[None, 120], Close=[102, 103])
    provider.responses["B"] = RuntimeError("provider unavailable")
    result = service.backfill()
    assert result["succeeded"] == result["failed"] == 1
    assert "provider unavailable" in result["results"][1]["error"]
    assert len(ohlcv(path)) == 2
    assert ohlcv(path)[0][3] == 110
    provider.responses["B"] = frame(["2026-02-02"], Close=[202])
    assert service.backfill_ticker("B")["status"] == "SUCCEEDED"
    assert len(ohlcv(path)) == 3


def test_ticker_transaction_rolls_back_on_write_failure(setup):
    path, _, service = setup
    with closing(sqlite3.connect(path)) as conn:
        conn.execute("CREATE TRIGGER reject_second BEFORE INSERT ON etf_ohlcv_prices "
                     "WHEN NEW.date='2026-01-05' BEGIN SELECT RAISE(ABORT, 'test interruption'); END")
        conn.commit()
    assert service.backfill_ticker("A")["status"] == "FAILED"
    assert ohlcv(path) == []
    with closing(sqlite3.connect(path)) as conn:
        conn.execute("DROP TRIGGER reject_second")
        conn.commit()
    assert service.backfill_ticker("A")["rows_written"] == 2


@pytest.mark.parametrize("sql", [
    "INSERT INTO etf_prices VALUES ('X','2026-01-01',1)",
    "UPDATE etf_prices SET close_price=1", "DELETE FROM etf_prices",
    "DROP TABLE etf_prices", "UPDATE etf_info SET name='changed'",
])
def test_connection_denies_non_ohlcv_mutations(setup, sql):
    path, _, service = setup
    before = snapshot(path)
    with closing(service._connection()) as conn:
        with pytest.raises(sqlite3.DatabaseError):
            conn.execute(sql)
    assert snapshot(path) == before


def test_no_initialization_on_import_or_missing_schema(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unexpected database initialization/connection")
    with monkeypatch.context() as patch:
        patch.setattr(database, "init_database", forbidden)
        patch.setattr(sqlite3, "connect", forbidden)
        importlib.reload(module)
        module.OHLCVBackfill(tmp_path / "missing.db", FakeProvider())
    missing = tmp_path / "missing.db"
    service = module.OHLCVBackfill(missing, FakeProvider())
    assert service.backfill_ticker("A")["status"] == "FAILED"
    assert not missing.exists()
    path = tmp_path / "legacy.db"
    with closing(sqlite3.connect(path)) as conn:
        conn.executescript("CREATE TABLE etf_prices(ticker TEXT,date TEXT,close_price REAL);"
                           "INSERT INTO etf_prices VALUES ('A','2026-01-02',100);")
    provider = FakeProvider()
    before = path.read_bytes()
    assert module.OHLCVBackfill(path, provider).backfill_ticker("A")["status"] == "FAILED"
    assert provider.calls == []
    assert path.read_bytes() == before
