import requests


BASE_URL = "http://127.0.0.1:5000"


def run_api_server_test():
    print("=" * 50)
    print("GPT Quant Platform API Test")
    print("=" * 50)

    print()
    print("===== Root API Test =====")

    response = requests.get(
        BASE_URL + "/",
        timeout=10,
    )

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

    response = requests.get(
        BASE_URL + "/api/ranking",
        timeout=10,
    )

    print(
        "Status Code :",
        response.status_code
    )

    assert response.status_code == 200

    data = response.json()

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


if __name__ == "__main__":
    run_api_server_test()
