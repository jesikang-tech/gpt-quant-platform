"""
Step5-3-67
AI Portfolio Conversational Analyst API Test
"""


from price_test_support import isolated_price_db, synthetic_portfolio_db, isolated_portfolio_api


def test_portfolio_chat(isolated_portfolio_api):
    client = isolated_portfolio_api.client

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

    assert response_data["question"] == payload["question"]
    assert response_data["question_type"] == "ALLOCATION"
    assert response_data["answer"]
    assert response_data["reason"]
    assert response_data["recommendation"]
    assert response_data["confidence"] == "HIGH"
    assert response_data["portfolio_context"] == {
        "top_ticker": "365040", "top_score": 90.7, "top_weight": 40, "asset_count": 4}
    assert any("BULLISH" in reason for reason in response_data["reason"])
    assert isolated_portfolio_api.data.db.accesses
    assert all(path == isolated_portfolio_api.data.db.path for path in isolated_portfolio_api.data.db.accesses)
