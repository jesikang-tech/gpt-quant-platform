import requests


BASE_URL = "http://127.0.0.1:5000"



print("=" * 50)
print("GPT Quant Platform API Test")
print("=" * 50)



print()


print("===== Root API Test =====")


response = requests.get(
    BASE_URL + "/"
)


print(
    "Status Code :",
    response.status_code
)


print(
    response.json()
)



print()


print("===== Ranking API Test =====")


response = requests.get(
    BASE_URL + "/api/ranking"
)


print(
    "Status Code :",
    response.status_code
)


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


print("=" * 50)