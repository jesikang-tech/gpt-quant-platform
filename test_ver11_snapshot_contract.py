import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

import config
import database


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    path = tmp_path / "ver11_snapshot.db"
    monkeypatch.setattr(config, "DATABASE_PATH", path)
    monkeypatch.setattr(database, "DATABASE_PATH", path)
    return path


def test_ver11_analysis_snapshot_schema(isolated_db):
    database.init_database()

    with closing(sqlite3.connect(isolated_db)) as conn:
        columns = conn.execute(
            "PRAGMA table_info(ver11_analysis_snapshot)"
        ).fetchall()

    assert [
        (row[1], row[2], row[3], row[5])
        for row in columns
    ] == [
        ("id", "INTEGER", 0, 1),
        ("analysis_date", "TEXT", 1, 0),
        ("period", "TEXT", 1, 0),
        ("sort_by", "TEXT", 1, 0),
        ("display_limit", "INTEGER", 1, 0),
        ("snapshot_version", "TEXT", 1, 0),
        ("snapshot_payload", "TEXT", 1, 0),
        ("created_at", "TEXT", 1, 0),
    ]

def test_ver11_snapshot_save_and_get_round_trip(isolated_db):
    import repository

    database.init_database()

    payload = {
        "analysis_date": "2026-06-12",
        "period": "3m",
        "market_regime": {"regime": "BULLISH", "confidence": 95},
        "market_strategy": {
            "portfolio_mode": "aggressive",
            "cash_target": 5,
        },
        "portfolio": [
            {"ticker": "AAA", "weight": 50},
            {"ticker": "BBB", "weight": 30},
            {"ticker": "CCC", "weight": 15},
            {"ticker": "CASH", "weight": 5},
        ],
    }

    snapshot_id = repository.save_ver11_analysis_snapshot(
        analysis_date="2026-06-12",
        period="3m",
        sort_by="final_score",
        display_limit=10,
        snapshot_payload=payload,
        snapshot_version="VER11-PIT-SNAPSHOT-v1",
    )

    snapshot = repository.get_ver11_analysis_snapshot(snapshot_id)

    assert snapshot["id"] == snapshot_id
    assert snapshot["analysis_date"] == "2026-06-12"
    assert snapshot["period"] == "3m"
    assert snapshot["sort_by"] == "final_score"
    assert snapshot["display_limit"] == 10
    assert snapshot["snapshot_version"] == "VER11-PIT-SNAPSHOT-v1"
    assert snapshot["snapshot_payload"] == payload
    assert snapshot["created_at"]

def test_ver11_snapshot_history_returns_newest_first(isolated_db):
    import repository

    database.init_database()

    first_id = repository.save_ver11_analysis_snapshot(
        analysis_date="2026-06-10",
        period="3m",
        sort_by="final_score",
        display_limit=10,
        snapshot_payload={"marker": "first"},
    )
    second_id = repository.save_ver11_analysis_snapshot(
        analysis_date="2026-06-12",
        period="3m",
        sort_by="return_score",
        display_limit=20,
        snapshot_payload={"marker": "second"},
    )

    history = repository.get_ver11_analysis_snapshot_history(limit=10)

    assert [item["id"] for item in history] == [second_id, first_id]
    assert history[0]["analysis_date"] == "2026-06-12"
    assert history[0]["sort_by"] == "return_score"
    assert history[0]["display_limit"] == 20
    assert history[0]["snapshot_payload"] == {"marker": "second"}
    assert history[1]["snapshot_payload"] == {"marker": "first"}

def test_ver11_snapshot_payload_excludes_future_reality_fields():
    import api_server

    data = {
        "success": True,
        "analysis_date": "2026-06-12",
        "market_data_date": "2026-06-12",
        "period": "3m",
        "lookback_trading_days": 60,
        "current_score_top": [
            {
                "ticker": "AAA",
                "final_score": 94.8,
                "return_score": 96.0,
                "trend_score": 94.0,
                "slope_score": 93.0,
                "price": 12000,
                "future_performance": 8.5,
                "future_performance_days": 20,
                "reality_test": {"status": "PASS"},
            }
        ],
        "market_regime_scores": [
            {
                "ticker": "AAA",
                "final_score": 94.8,
                "return_score": 96.0,
                "trend_score": 94.0,
                "slope_score": 93.0,
            }
        ],
        "market_regime": {"regime": "BULLISH"},
        "market_strategy": {"portfolio_mode": "aggressive"},
        "portfolio": [{"ticker": "AAA", "weight": 50}],
        "point_in_time_explanation": {
            "analysis_date": "2026-06-12",
            "period": "3m",
        },
        "db_write": False,
    }

    payload = api_server._build_ver11_snapshot_payload(data)

    row = payload["current_score_top"][0]

    assert row["ticker"] == "AAA"
    assert row["final_score"] == 94.8
    assert "price" not in row
    assert "future_performance" not in row
    assert "future_performance_days" not in row
    assert "reality_test" not in row

    assert payload["market_regime"]["regime"] == "BULLISH"
    assert payload["market_strategy"]["portfolio_mode"] == "aggressive"
    assert payload["portfolio"] == [{"ticker": "AAA", "weight": 50}]
    assert payload["point_in_time_explanation"]["analysis_date"] == "2026-06-12"
    assert payload["db_write"] is False

def test_ver11_snapshot_api_recomputes_and_saves_point_in_time_result(
    tmp_path,
    monkeypatch,
):
    import api_server
    import config
    import database

    db_path = tmp_path / "ver11_snapshot_api.db"
    monkeypatch.setattr(config, "DATABASE_PATH", db_path)
    monkeypatch.setattr(database, "DATABASE_PATH", db_path)
    database.init_database()

    scores = [
        {
            "ticker": "AAA",
            "return_score": 96.0,
            "trend_score": 94.0,
            "slope_score": 93.0,
            "final_score": 94.8,
            "price": 12000,
            "future_performance": 8.5,
            "future_performance_days": 20,
            "reality_test": {"status": "PASS"},
        },
        {
            "ticker": "BBB",
            "return_score": 93.0,
            "trend_score": 91.0,
            "slope_score": 90.0,
            "final_score": 91.8,
        },
        {
            "ticker": "CCC",
            "return_score": 91.0,
            "trend_score": 89.0,
            "slope_score": 88.0,
            "final_score": 89.8,
        },
    ]

    captured = {}

    def fake_get_current_analysis_data(
        limit=10,
        analysis_date=None,
        period="3m",
        sort_by="final_score",
    ):
        captured.update(
            {
                "limit": limit,
                "analysis_date": analysis_date,
                "period": period,
                "sort_by": sort_by,
            }
        )
        return {
            "success": True,
            "analysis_date": analysis_date,
            "market_data_date": analysis_date,
            "period": period,
            "current_score_top": scores,
            "market_regime_scores": scores,
            "db_write": False,
        }

    monkeypatch.setattr(
        api_server,
        "get_current_analysis_data",
        fake_get_current_analysis_data,
    )

    from testing_helpers import authenticated_client

    client = authenticated_client(api_server.app)

    response = client.post(
        "/api/ver11-analysis/snapshots",
        json={
            "date": "2026-06-12",
            "period": "3m",
            "limit": 20,
            "sort": "return_score",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True
    assert data["snapshot_id"] > 0
    assert data["analysis_date"] == "2026-06-12"
    assert data["period"] == "3m"
    assert data["sort"] == "return_score"
    assert data["limit"] == 20

    assert captured == {
        "limit": 20,
        "analysis_date": "2026-06-12",
        "period": "3m",
        "sort_by": "return_score",
    }

    saved = api_server.get_ver11_analysis_snapshot(data["snapshot_id"])

    assert saved["analysis_date"] == "2026-06-12"
    assert saved["period"] == "3m"
    assert saved["sort_by"] == "return_score"
    assert saved["display_limit"] == 20

    row = saved["snapshot_payload"]["current_score_top"][0]

    assert row["ticker"] == "AAA"
    assert "price" not in row
    assert "future_performance" not in row
    assert "future_performance_days" not in row
    assert "reality_test" not in row
    assert saved["snapshot_payload"]["market_regime"]["regime"] == "BULLISH"

def test_ver11_snapshot_history_and_detail_api(tmp_path, monkeypatch):
    import api_server
    import config
    import database

    db_path = tmp_path / "ver11_snapshot_history_api.db"
    monkeypatch.setattr(config, "DATABASE_PATH", db_path)
    monkeypatch.setattr(database, "DATABASE_PATH", db_path)
    database.init_database()

    first_id = api_server.save_ver11_analysis_snapshot(
        analysis_date="2026-06-10",
        period="3m",
        sort_by="final_score",
        display_limit=10,
        snapshot_payload={
            "analysis_date": "2026-06-10",
            "period": "3m",
            "marker": "first",
        },
    )
    second_id = api_server.save_ver11_analysis_snapshot(
        analysis_date="2026-06-12",
        period="2m",
        sort_by="return_score",
        display_limit=20,
        snapshot_payload={
            "analysis_date": "2026-06-12",
            "period": "2m",
            "marker": "second",
        },
    )

    from testing_helpers import authenticated_client

    client = authenticated_client(api_server.app)

    history_response = client.get(
        "/api/ver11-analysis/snapshots?limit=10"
    )

    assert history_response.status_code == 200

    history_data = history_response.get_json()

    assert history_data["success"] is True
    assert history_data["count"] == 2
    assert [item["id"] for item in history_data["snapshots"]] == [
        second_id,
        first_id,
    ]
    assert history_data["snapshots"][0]["snapshot_payload"]["marker"] == "second"

    detail_response = client.get(
        f"/api/ver11-analysis/snapshots/{first_id}"
    )

    assert detail_response.status_code == 200

    detail_data = detail_response.get_json()

    assert detail_data["success"] is True
    assert detail_data["snapshot"]["id"] == first_id
    assert detail_data["snapshot"]["analysis_date"] == "2026-06-10"
    assert detail_data["snapshot"]["sort_by"] == "final_score"
    assert detail_data["snapshot"]["display_limit"] == 10
    assert detail_data["snapshot"]["snapshot_payload"]["marker"] == "first"

def test_ver11_snapshot_detail_api_returns_404_for_missing_snapshot(
    tmp_path,
    monkeypatch,
):
    import api_server
    import config
    import database

    db_path = tmp_path / "ver11_snapshot_missing_api.db"
    monkeypatch.setattr(config, "DATABASE_PATH", db_path)
    monkeypatch.setattr(database, "DATABASE_PATH", db_path)
    database.init_database()

    from testing_helpers import authenticated_client

    client = authenticated_client(api_server.app)

    response = client.get(
        "/api/ver11-analysis/snapshots/999999"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["success"] is False
    assert data["message"] == "Snapshot not found."

def test_ver11_snapshot_history_api_rejects_invalid_limit(
    tmp_path,
    monkeypatch,
):
    import api_server
    import config
    import database

    db_path = tmp_path / "ver11_snapshot_invalid_limit_api.db"
    monkeypatch.setattr(config, "DATABASE_PATH", db_path)
    monkeypatch.setattr(database, "DATABASE_PATH", db_path)
    database.init_database()

    from testing_helpers import authenticated_client

    client = authenticated_client(api_server.app)

    for invalid_limit in ("abc", "0", "-1"):
        response = client.get(
            f"/api/ver11-analysis/snapshots?limit={invalid_limit}"
        )

        assert response.status_code == 400

        data = response.get_json()

        assert data["success"] is False
        assert data["message"] == "Invalid limit."

def test_ver11_snapshot_payload_recursively_excludes_future_only_fields():
    import api_server

    source = {
        "analysis_date": "2026-06-12",
        "period": "3m",
        "current_score_top": [
            {
                "ticker": "AAA",
                "final_score": 90.0,
                "price": 12345,
                "future_performance": 7.5,
                "future_performance_days": 20,
                "reality_test": {"status": "PASS"},
            }
        ],
        "selection": {
            "top": [
                {
                    "ticker": "AAA",
                    "price": 12345,
                    "future_performance": 7.5,
                    "reality_test": {"status": "PASS"},
                }
            ]
        },
        "market_regime_scores": [
            {
                "ticker": "AAA",
                "final_score": 90.0,
                "future_performance": 7.5,
            }
        ],
        "nested": {
            "rows": [
                {
                    "ticker": "AAA",
                    "future_performance_days": 20,
                    "reality_test": {"status": "PASS"},
                }
            ]
        },
    }

    payload = api_server._build_ver11_snapshot_payload(source)

    forbidden = {
        "price",
        "future_performance",
        "future_performance_days",
        "reality_test",
    }

    def assert_no_forbidden_fields(value):
        if isinstance(value, dict):
            assert forbidden.isdisjoint(value.keys())
            for child in value.values():
                assert_no_forbidden_fields(child)
        elif isinstance(value, list):
            for child in value:
                assert_no_forbidden_fields(child)

    assert_no_forbidden_fields(payload)


def test_api_server_direct_start_initializes_database_before_auth():
    source = Path("api_server.py").read_text(encoding="utf-8")

    assert "from database import init_database" in source

    main_block = source.split('if __name__ == "__main__":', 1)[1]
    assert "init_database()" in main_block
    assert "configure_flask_auth(app)" in main_block
    assert main_block.index("init_database()") < main_block.index(
        "configure_flask_auth(app)"
    )
