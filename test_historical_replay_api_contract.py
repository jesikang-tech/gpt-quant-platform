import api_server


def test_historical_replay_api_rejects_unsupported_period():
    client = api_server.app.test_client()

    response = client.get(
        "/api/historical-replay?date=2026-09-04&period=6m"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["message"] == "Invalid period. Use 1m, 2m, or 3m."


def test_historical_replay_api_rejects_12m():
    client = api_server.app.test_client()

    response = client.get(
        "/api/historical-replay?date=2026-09-04&period=12m"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["message"] == "Invalid period. Use 1m, 2m, or 3m."


def test_historical_replay_api_passes_supported_period(monkeypatch):
    captured = {}

    def fake_get_current_analysis_data(limit, analysis_date, period):
        captured["limit"] = limit
        captured["analysis_date"] = analysis_date
        captured["period"] = period

        return {
            "success": True,
            "analysis_date": analysis_date,
            "period": period,
            "current_score_top": [],
            "db_write": False,
        }

    monkeypatch.setattr(
        api_server,
        "get_current_analysis_data",
        fake_get_current_analysis_data,
    )

    client = api_server.app.test_client()

    response = client.get(
        "/api/historical-replay?date=2026-09-04&period=2m"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["period"] == "2m"

    assert captured == {
        "limit": 10,
        "analysis_date": "2026-09-04",
        "period": "2m",
    }


def test_historical_replay_api_defaults_to_3m(monkeypatch):
    captured = {}

    def fake_get_current_analysis_data(limit, analysis_date, period):
        captured["limit"] = limit
        captured["analysis_date"] = analysis_date
        captured["period"] = period

        return {
            "success": True,
            "analysis_date": analysis_date,
            "period": period,
            "current_score_top": [],
            "db_write": False,
        }

    monkeypatch.setattr(
        api_server,
        "get_current_analysis_data",
        fake_get_current_analysis_data,
    )

    client = api_server.app.test_client()

    response = client.get(
        "/api/historical-replay?date=2026-09-04"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["period"] == "3m"

    assert captured == {
        "limit": 10,
        "analysis_date": "2026-09-04",
        "period": "3m",
    }


def test_historical_replay_api_response_field_contract(monkeypatch):
    def fake_get_current_analysis_data(limit, analysis_date, period):
        return {
            "success": True,
            "analysis_date": analysis_date,
            "market_data_date": analysis_date,
            "period": period,
            "lookback_trading_days": 60,
            "return_threshold": 15.0,
            "uptrend_threshold": 70.0,
            "total_etf": 1171,
            "enough_data": 1000,
            "selection": {
                "return_threshold": 15.0,
                "uptrend_threshold": 70.0,
                "count": 10,
                "top": [],
            },
            "current_score_top": [
                {
                    "ticker": "230480",
                    "name": "KIWOOM 미국달러선물인버스2X",
                    "return": 20.0,
                    "return_score": 30.0,
                    "trend_score": 25.0,
                    "slope_score": 20.0,
                    "uptrend_ratio": 80.0,
                    "final_score": 88.3,
                    "selection_pass": True,
                    "price": 4835.0,
                    "future_performance": 2.17,
                    "future_performance_days": 12,
                }
            ],
            "db_write": False,
        }

    monkeypatch.setattr(
        api_server,
        "get_current_analysis_data",
        fake_get_current_analysis_data,
    )

    client = api_server.app.test_client()

    response = client.get(
        "/api/historical-replay?date=2026-09-04&period=3m"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["analysis_date"] == "2026-09-04"
    assert data["market_data_date"] == "2026-09-04"
    assert data["period"] == "3m"
    assert data["lookback_trading_days"] == 60
    assert data["db_write"] is False

    row = data["current_score_top"][0]

    assert row["ticker"] == "230480"
    assert row["name"] == "KIWOOM 미국달러선물인버스2X"
    assert row["price"] == 4835.0
    assert row["final_score"] == 88.3
    assert row["future_performance"] == 2.17
    assert row["future_performance_days"] == 12
