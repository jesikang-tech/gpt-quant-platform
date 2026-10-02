"""
Step5-3-67
AI Portfolio Conversational Analyst API Test
"""


def test_portfolio_chat(tmp_path, monkeypatch):
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

    payload = {
        "question": "왜 365040 비중이 높은가?"
    }

    response = client.post(
        "/api/portfolio/chat",
        json=payload,
    )

    assert response.status_code == 200

    result = response.get_json()

    assert result["success"] is True

    response_data = result["response"]

    assert "question_type" in response_data
    assert "answer" in response_data
    assert "reason" in response_data
    assert "recommendation" in response_data
    assert "confidence" in response_data
