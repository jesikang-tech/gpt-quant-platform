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
