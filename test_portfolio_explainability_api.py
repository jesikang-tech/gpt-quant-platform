"""
Step5-3-66
AI Portfolio Explainability API Test
"""


from price_test_support import isolated_price_db, synthetic_portfolio_db, isolated_portfolio_api


def test_portfolio_explainability_api(isolated_portfolio_api):
    client = isolated_portfolio_api.client

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

    assert result["strategy"] == "Balanced"
    data = isolated_portfolio_api.data
    allocations = explanation["allocation_reason"]
    assert [(item["ticker"], item["weight"]) for item in allocations] == list(zip(data.factors, (40, 30, 20)))
    assert all(item["reason"] for item in allocations)
    assert explanation["risk_analysis"]["cash_weight"] == 10
    assert explanation["market_analysis"]["regime"] == "BULLISH"
    assert explanation["market_analysis"]["impact"] == "positive"
    assert isolated_portfolio_api.data.db.accesses
    assert all(path == isolated_portfolio_api.data.db.path for path in isolated_portfolio_api.data.db.accesses)
