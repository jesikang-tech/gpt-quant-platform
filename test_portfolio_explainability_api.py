"""
Step5-3-66
AI Portfolio Explainability API Test
"""


def test_portfolio_explainability_api(tmp_path, monkeypatch):
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

    login_response = client.post(
        "/api/auth/login",
        json={"password": "1234"},
    )
    assert login_response.status_code == 200

    response = client.get("/api/portfolio/explain")

    assert response.status_code == 200

    result = response.get_json()

    assert result["success"] is True

    explanation = result["explanation"]

    assert "summary" in explanation
    assert "factor_analysis" in explanation
    assert "allocation_reason" in explanation
    assert "risk_analysis" in explanation
