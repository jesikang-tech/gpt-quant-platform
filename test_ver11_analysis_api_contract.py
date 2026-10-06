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


def test_ver11_analysis_api_exposes_point_in_time_portfolio(monkeypatch):
    import api_server
    from testing_helpers import authenticated_client

    replay_scores = [
        {
            "ticker": "AAA",
            "return_score": 96.0,
            "trend_score": 94.0,
            "slope_score": 93.0,
            "final_score": 94.8,
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

    monkeypatch.setattr(
        "api_server.get_current_analysis_data",
        lambda **kwargs: {
            "success": True,
            "analysis_date": "2026-06-12",
            "market_data_date": "2026-06-12",
            "period": "3m",
            "current_score_top": [
                {
                    "ticker": "DISPLAY_ONLY",
                    "return_score": 10.0,
                    "trend_score": 10.0,
                    "slope_score": 10.0,
                    "final_score": 10.0,
                }
            ],
            "market_regime_scores": replay_scores,
            "db_write": False,
        },
    )

    client = authenticated_client(api_server.app)
    response = client.get(
        "/api/ver11-analysis?date=2026-06-12&period=3m"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["analysis_date"] == "2026-06-12"
    assert data["db_write"] is False
    assert data["market_regime"]["regime"] == "BULLISH"
    assert data["market_strategy"]["portfolio_mode"] == "aggressive"
    assert [item["ticker"] for item in data["portfolio"]] == [
        "AAA",
        "BBB",
        "CCC",
        "CASH",
    ]
    assert [item["weight"] for item in data["portfolio"]] == [
        50,
        30,
        15,
        5,
    ]

def test_ver11_and_historical_replay_share_point_in_time_portfolio_contract(monkeypatch):
    import api_server
    from testing_helpers import authenticated_client

    replay_scores = [
        {
            "ticker": "AAA",
            "name": "AAA",
            "return_score": 96.0,
            "trend_score": 94.0,
            "slope_score": 93.0,
            "final_score": 94.8,
        },
        {
            "ticker": "BBB",
            "name": "BBB",
            "return_score": 93.0,
            "trend_score": 91.0,
            "slope_score": 90.0,
            "final_score": 91.8,
        },
        {
            "ticker": "CCC",
            "name": "CCC",
            "return_score": 91.0,
            "trend_score": 89.0,
            "slope_score": 88.0,
            "final_score": 89.8,
        },
    ]

    def fake_get_current_analysis_data(
        limit=10,
        analysis_date=None,
        period="3m",
        sort_by="final_score",
    ):
        sorted_scores = list(replay_scores)

        if sort_by == "return":
            sorted_scores = list(reversed(sorted_scores))

        return {
            "success": True,
            "analysis_date": "2026-06-12",
            "market_data_date": "2026-06-12",
            "period": period,
            "lookback_trading_days": 60,
            "current_score_top": sorted_scores[:limit],
            "market_regime_scores": replay_scores,
            "db_write": False,
        }

    monkeypatch.setattr(
        "api_server.get_current_analysis_data",
        fake_get_current_analysis_data,
    )

    client = authenticated_client(api_server.app)

    historical_response = client.get(
        "/api/historical-replay?date=2026-06-12&period=3m"
    )
    ver11_response = client.get(
        "/api/ver11-analysis"
        "?date=2026-06-12&period=3m&limit=20&sort=return"
    )

    assert historical_response.status_code == 200
    assert ver11_response.status_code == 200

    historical = historical_response.get_json()
    ver11 = ver11_response.get_json()

    assert historical["analysis_date"] == ver11["analysis_date"]
    assert historical["period"] == ver11["period"]
    assert historical["db_write"] is False
    assert ver11["db_write"] is False

    assert historical["market_regime"] == ver11["market_regime"]
    assert historical["market_strategy"] == ver11["market_strategy"]
    assert historical["portfolio"] == ver11["portfolio"]
    assert (
        historical["point_in_time_explanation"]
        == ver11["point_in_time_explanation"]
    )

def test_ver11_point_in_time_explain_contract(monkeypatch):
    import api_server

    point_in_time_scores = [
        {
            "ticker": "AAA",
            "return_score": 96.0,
            "trend_score": 94.0,
            "slope_score": 93.0,
            "final_score": 94.8,
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

    monkeypatch.setattr(
        "api_server.get_current_analysis_data",
        lambda **kwargs: {
            "success": True,
            "analysis_date": "2026-06-12",
            "market_data_date": "2026-06-12",
            "period": "3m",
            "current_score_top": point_in_time_scores,
            "market_regime_scores": point_in_time_scores,
            "db_write": False,
        },
    )

    client = __import__(
        "testing_helpers",
        fromlist=["authenticated_client"],
    ).authenticated_client(api_server.app)

    response = client.get(
        "/api/ver11-analysis"
        "?date=2026-06-12&period=3m&limit=10&sort=final_score"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "market_regime" in data
    assert "market_strategy" in data
    assert "portfolio" in data
    assert "point_in_time_explanation" in data

    explanation = data["point_in_time_explanation"]

    assert explanation["analysis_date"] == "2026-06-12"
    assert explanation["period"] == "3m"

    assert "market_regime" in explanation
    assert "market_strategy" in explanation
    assert "portfolio" in explanation

    assert explanation["market_regime"]["regime"] == "BULLISH"
    assert explanation["market_strategy"]["portfolio_mode"] == "aggressive"

    assert explanation["portfolio"]["cash_weight"] == 5

    allocations = explanation["portfolio"]["allocations"]

    assert [item["ticker"] for item in allocations] == [
        "AAA",
        "BBB",
        "CCC",
    ]

    assert [item["weight"] for item in allocations] == [
        50,
        30,
        15,
    ]

    assert allocations[0]["return_score"] == 96.0
    assert allocations[0]["trend_score"] == 94.0
    assert allocations[0]["slope_score"] == 93.0
    assert allocations[0]["optimization_score"] == 91.9

    assert explanation["market_regime"]["avg_score"] == 92.13
    assert explanation["market_regime"]["confidence"] == 95
    assert explanation["market_strategy"]["cash_target"] == 5
    assert explanation["market_strategy"]["recommendation"] == "BUY"
    assert explanation["market_strategy"]["rebalance_action"] == "Increase Equity"

    assert data["db_write"] is False


def test_ver11_point_in_time_explain_does_not_read_current_market_or_scores(
    monkeypatch,
):
    import api_server

    replay_scores = [
        {
            "ticker": "AAA",
            "return_score": 96.0,
            "trend_score": 94.0,
            "slope_score": 93.0,
            "final_score": 94.8,
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

    real_analyze_market_regime = api_server.analyze_market_regime

    def reject_current_market_read(*args, **kwargs):
        if kwargs.get("scores") is None:
            raise AssertionError(
                "Ver1.1 Point-in-Time Explain must not read current market data"
            )
        return real_analyze_market_regime(*args, **kwargs)

    def reject_current_score_read(*args, **kwargs):
        raise AssertionError(
            "Ver1.1 Point-in-Time Explain must not read persisted current scores"
        )

    monkeypatch.setattr(
        "api_server.analyze_market_regime",
        reject_current_market_read,
    )

    monkeypatch.setattr(
        "api_server.get_dashboard_api_data",
        reject_current_score_read,
    )

    monkeypatch.setattr(
        "api_server.get_current_analysis_data",
        lambda **kwargs: {
            "success": True,
            "analysis_date": "2026-06-12",
            "market_data_date": "2026-06-12",
            "period": "3m",
            "current_score_top": replay_scores,
            "market_regime_scores": replay_scores,
            "db_write": False,
        },
    )

    from testing_helpers import authenticated_client

    client = authenticated_client(api_server.app)

    response = client.get(
        "/api/ver11-analysis"
        "?date=2026-06-12&period=3m&limit=10&sort=final_score"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["point_in_time_explanation"]["analysis_date"] == "2026-06-12"
    assert data["point_in_time_explanation"]["market_regime"]["regime"] == "BULLISH"
    assert (
        data["point_in_time_explanation"]["market_strategy"]["portfolio_mode"]
        == "aggressive"
    )
    assert data["point_in_time_explanation"]["portfolio"]["cash_weight"] == 5
