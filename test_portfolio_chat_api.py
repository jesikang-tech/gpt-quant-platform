"""
Step5-3-67
AI Portfolio Conversational Analyst API Test
"""


import requests



BASE_URL = (
    "http://127.0.0.1:5000"
)



def test_portfolio_chat():


    print(
        "\nAI Portfolio Conversational API Test\n"
    )


    payload = {

        "question":
            "왜 365040 비중이 높은가?"

    }



    response = requests.post(

        BASE_URL +
        "/api/portfolio/chat",

        json=payload

    )


    print(
        "Status:",
        response.status_code
    )


    assert response.status_code == 200



    result = response.json()



    assert result["success"] is True



    print("\nQuestion:")

    print(
        payload["question"]
    )



    response_data = result["response"]


    print("\nQuestion Type:")

    print(
        response_data["question_type"]
    )


    print("\nAnswer:")

    print(
        response_data["answer"]
    )



    print("\nReason:")


    for item in response_data["reason"]:

        print(
            "-",
            item
        )



    print("\nRecommendation:")

    print(
        response_data["recommendation"]
    )



    print("\nConfidence:")

    print(
        response_data["confidence"]
    )



    print(
        "\nPASS - AI Portfolio Conversational API"
    )



if __name__ == "__main__":

    test_portfolio_chat()