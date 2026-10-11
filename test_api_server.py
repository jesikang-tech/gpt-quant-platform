import pytest
from price_test_support import isolated_price_db, synthetic_ranking_db, phase8_test_scope


def run_api_server_test(client):
    print("=" * 50)
    print("GPT Quant Platform API Test")
    print("=" * 50)

    print()
    print("===== Root API Test =====")

    response = client.get("/")

    print(
        "Status Code :",
        response.status_code
    )

    assert response.status_code == 200
    assert "text/html" in response.headers.get("Content-Type", "")
    assert "GPT Quant ETF Dashboard" in response.text

    print(
        "Root API Status : PASS"
    )

    print()
    print("===== Ranking API Test =====")

    response = client.get("/api/ranking")

    print(
        "Status Code :",
        response.status_code
    )

    assert response.status_code == 200

    data = response.get_json()

    print(
        data
    )

    print()
    print("===== Validation =====")

    if data["success"]:
        print(
            "API Status : PASS"
        )
    else:
        print(
            "API Status : FAIL"
        )

    assert data["success"] is True

    print("=" * 50)


@pytest.fixture(autouse=True)
def _protected_flask_state(isolated_price_db, monkeypatch):
    with phase8_test_scope(isolated_price_db) as scope:
        api = scope.api
        config_before = dict(api.app.config)
        auth_path_before = api.AUTH_CONFIG_PATH
        try:
            yield scope
        finally:
            api.app.config.clear()
            api.app.config.update(config_before)
            api.AUTH_CONFIG_PATH = auth_path_before


def test_api_server_contract(synthetic_ranking_db, _protected_flask_state):
    from testing_helpers import authenticated_client

    client = authenticated_client(_protected_flask_state.api.app)
    run_api_server_test(client)


if __name__ == "__main__":
    raise SystemExit("Run this isolated contract with pytest; direct server HTTP tests are disabled.")
