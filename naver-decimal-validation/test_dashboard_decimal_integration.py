"""Synthetic metadata handoff only; not operational persistence permission.

Run with the existing isolated dashboard CI source manifest plus the synthetic
Decimal dependencies. The fixture guard is not an OS security boundary.
The legacy dashboard REAL column does not preserve arbitrary Decimal precision;
exact values are verified in the separate synthetic source, not in that column.
"""

from contextlib import closing
from decimal import Decimal
import json
from pathlib import Path

import pytest

from price_test_support import isolated_price_db, synthetic_ranking_db


@pytest.fixture
def decimal_dashboard_source(synthetic_ranking_db):
    from core.naver_decimal_price_pipeline import prepare_naver_decimal_price_pair
    from core.synthetic_decimal_atomic_repository import (
        create_synthetic_decimal_schema,
        insert_synthetic_decimal_batch,
    )

    observations = (
        ("2026-01-07", Decimal("100.00000000000000000001")),
        ("2026-01-08", Decimal("101.00000000000000000001")),
    )
    pairs = tuple(prepare_naver_decimal_price_pair(
        "111111", day,
        {"Open": close, "High": close, "Low": close, "Close": close,
         "Volume": Decimal("1000")},
        adjustment="UNADJUSTED",
    ) for day, close in observations)
    # This fixture API accepts no caller-selected path: it creates :memory: only.
    with closing(synthetic_ranking_db.db.connect_memory()) as source:
        assert source.execute("PRAGMA database_list").fetchall() == [(0, "main", "")]
        create_synthetic_decimal_schema(source)
        insert_synthetic_decimal_batch(source, pairs)
        yield source, observations


def _handoff_validated_prices(source, dashboard_db, calls):
    from core.synthetic_decimal_atomic_repository import read_synthetic_replay_prices

    # Complete validation precedes opening the fixture-owned dashboard DB.
    prices = read_synthetic_replay_prices(
        source, ticker="111111", analysis_date="2026-01-08",
    )
    with closing(dashboard_db.connect()) as target:
        assert target is not source
        assert Path(target.execute("PRAGMA database_list").fetchone()[2]).resolve() == dashboard_db.path
        calls.append(prices)
        with target:
            # Test fixture population only. No production writer/gate is replaced.
            # SQLite REAL affinity may round this text; only metadata is bridged.
            target.executemany(
                "INSERT INTO etf_prices(ticker, date, close_price) VALUES (?, ?, ?)",
                [("111111", day, str(close)) for day, close in prices],
            )
    return prices


def _dashboard_rows(dashboard_db):
    with closing(dashboard_db.connect()) as conn:
        return (
            conn.execute("SELECT * FROM etf_prices ORDER BY ticker, date").fetchall(),
            conn.execute("SELECT * FROM etf_ranking_history ORDER BY ranking_date, ticker").fetchall(),
        )


def test_decimal_handoff_updates_only_dashboard_market_date(
    synthetic_ranking_db, decimal_dashboard_source,
):
    from ranking_analyzer import (
        get_dashboard_api_data,
        get_intelligence_dashboard_json,
    )

    source, observations = decimal_dashboard_source
    before = get_dashboard_api_data(limit=2)
    before_prices, before_ranking = _dashboard_rows(synthetic_ranking_db.db)
    calls = []
    source_changes = source.total_changes
    series = _handoff_validated_prices(source, synthetic_ranking_db.db, calls)
    assert calls == [series]
    assert series == observations
    assert all(type(close) is Decimal for _, close in series)
    assert [close.as_tuple() for _, close in series] == [close.as_tuple() for _, close in observations]
    assert series[0][1] != Decimal(str(float(series[0][1])))

    result = get_dashboard_api_data(limit=2)
    assert result["success"] is True
    assert result["count"] == len(result["data"]) == before["count"] == 2
    assert [row["ticker"] for row in result["data"]] == ["111111", "222222"]
    assert [row["rank"] for row in result["data"]] == [1, 2]
    assert result["data"] == before["data"]
    assert before["metadata"]["market_data_date"] == synthetic_ranking_db.dates[-1]
    assert result["metadata"] == {
        "market_data_date": observations[-1][0],
        "ranking_date": synthetic_ranking_db.dates[-1],
    }
    after_prices, after_ranking = _dashboard_rows(synthetic_ranking_db.db)
    assert len(after_prices) == len(before_prices) + len(observations)
    assert result["metadata"]["market_data_date"] == max(row[1] for row in after_prices)
    assert after_ranking == before_ranking
    assert result["metadata"]["ranking_date"] == max(row[4] for row in after_ranking)
    assert json.loads(json.dumps(result)) == result
    assert json.loads(get_intelligence_dashboard_json(limit=2)) == result["data"]
    assert source.total_changes == source_changes
    assert not source.in_transaction


def test_decimal_close_text_mismatch_prevents_dashboard_handoff(
    monkeypatch, synthetic_ranking_db, decimal_dashboard_source,
):
    from core.synthetic_decimal_atomic_repository import (
        SyntheticDecimalWriteRejected,
        read_synthetic_replay_prices,
    )
    from ranking_analyzer import get_dashboard_api_data

    source, observations = decimal_dashboard_source
    assert read_synthetic_replay_prices(
        source, ticker="111111", analysis_date="2026-01-08",
    ) == observations
    original = str(observations[0][1])
    changed = original + "0"
    assert original != changed and Decimal(original) == Decimal(changed)
    assert str(Decimal(changed)) == changed
    source.execute(
        "UPDATE synthetic_decimal_prices SET close_price = ? WHERE ticker = ? AND date = ?",
        (changed, "111111", observations[0][0]),
    )
    source.commit()
    before = get_dashboard_api_data(limit=2)
    before_rows = _dashboard_rows(synthetic_ranking_db.db)
    handoffs = []
    connections = []

    def forbidden_target_connection():
        connections.append(True)
        raise AssertionError("Rejected source must not open the dashboard target")

    with monkeypatch.context() as patch:
        patch.setattr(synthetic_ranking_db.db, "connect", forbidden_target_connection)
        with pytest.raises(
            SyntheticDecimalWriteRejected, match="^PRICE/OHLCV close TEXT mismatch$",
        ):
            _handoff_validated_prices(source, synthetic_ranking_db.db, handoffs)
    assert handoffs == connections == []
    assert _dashboard_rows(synthetic_ranking_db.db) == before_rows
    assert get_dashboard_api_data(limit=2) == before
    assert not source.in_transaction
