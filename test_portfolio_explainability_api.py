"""
Step5-3-66
AI Portfolio Explainability API Test
"""


import requests



BASE_URL = (
    "http://127.0.0.1:5000"
)



def test_portfolio_explainability_api():


    print(
        "\nAI Portfolio Explainability API Test\n"
    )


    response = requests.get(
        BASE_URL +
        "/api/portfolio/explain"
    )


    print(
        "Status:",
        response.status_code
    )


    assert response.status_code == 200



    result = response.json()



    assert result["success"] is True



    explanation = (
        result["explanation"]
    )


    print("\nSummary:")

    print(
        explanation["summary"]
    )



    print("\nFactors:")


    for factor in explanation["factor_analysis"]:

        print(
            factor["name"],
            ":",
            factor["impact"]
        )



    print("\nAllocation:")


    for item in explanation["allocation_reason"]:

        print(
            item["ticker"],
            ":",
            item["reason"]
        )



    print("\nRisk:")

    print(
        explanation["risk_analysis"]
    )



    print(
        "\nPASS - AI Portfolio Explainability API"
    )



if __name__ == "__main__":

    test_portfolio_explainability_api()