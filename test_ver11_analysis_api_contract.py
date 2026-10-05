def test_ver11_analysis_api_passes_date_period_and_limit(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import (
        configure_flask_auth,
        create_password_hash,
        save_auth_config,
    )

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    captured = {}

    def fake_get_current_analysis_data(
        limit=10,
        analysis_date=None,
        period="3m",
        sort_by="final_score",
    ):
        captured["limit"] = limit
        captured["analysis_date"] = analysis_date
        captured["period"] = period
        captured["sort_by"] = sort_by

        return {
            "success": True,
            "analysis_date": analysis_date,
            "period": period,
            "lookback_trading_days": {
                "1m": 20,
                "2m": 40,
                "3m": 60,
            }[period],
            "current_score_top": [],
        }

    monkeypatch.setattr(
        api_server,
        "get_current_analysis_data",
        fake_get_current_analysis_data,
    )

    client = api_server.app.test_client()

    login_response = client.post(
        "/api/auth/login",
        json={"password": "1234"},
    )
    assert login_response.status_code == 200

    response = client.get(
        "/api/ver11-analysis"
        "?date=2026-09-04"
        "&period=2m"
        "&limit=20"
        "&sort=trend_score"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["analysis_date"] == "2026-09-04"
    assert data["period"] == "2m"
    assert data["lookback_trading_days"] == 40

    assert captured == {
        "limit": 20,
        "analysis_date": "2026-09-04",
        "period": "2m",
        "sort_by": "trend_score",
    }


def test_ver11_analysis_api_defaults_to_3m_and_10(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import (
        configure_flask_auth,
        create_password_hash,
        save_auth_config,
    )

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    captured = {}

    def fake_get_current_analysis_data(
        limit=10,
        analysis_date=None,
        period="3m",
        sort_by="final_score",
    ):
        captured["limit"] = limit
        captured["analysis_date"] = analysis_date
        captured["period"] = period
        captured["sort_by"] = sort_by

        return {
            "success": True,
            "analysis_date": analysis_date,
            "period": period,
        }

    monkeypatch.setattr(
        api_server,
        "get_current_analysis_data",
        fake_get_current_analysis_data,
    )

    client = api_server.app.test_client()

    login_response = client.post(
        "/api/auth/login",
        json={"password": "1234"},
    )
    assert login_response.status_code == 200

    response = client.get(
        "/api/ver11-analysis?date=2026-09-04"
    )

    assert response.status_code == 200

    assert captured == {
        "limit": 10,
        "analysis_date": "2026-09-04",
        "period": "3m",
        "sort_by": "final_score",
    }


def test_ver11_analysis_api_requires_authentication(tmp_path, monkeypatch):
    import api_server
    from core.platform_auth import (
        configure_flask_auth,
        create_password_hash,
        save_auth_config,
    )

    config_path = tmp_path / "platform_auth.json"
    save_auth_config(
        create_password_hash("1234"),
        create_password_hash("1234567", admin=True),
        config_path,
    )

    configure_flask_auth(api_server.app, config_path)
    monkeypatch.setattr(api_server, "AUTH_CONFIG_PATH", config_path)

    client = api_server.app.test_client()

    response = client.get(
        "/api/ver11-analysis?date=2026-09-04"
    )

    assert response.status_code == 401

    data = response.get_json()
    assert data["success"] is False
