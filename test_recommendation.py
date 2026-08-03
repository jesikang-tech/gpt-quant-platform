from ranking_analyzer import generate_ai_recommendation


print("=" * 60)
print("GPT AI Recommendation Test")
print("=" * 60)


ticker = "365040"


result = generate_ai_recommendation(
    ticker
)


print()

print("Ticker :", ticker)

print(
    "Recommendation :",
    result["recommendation"]
)

print(
    "Confidence :",
    result["confidence"]
)


print()

print("Reasons")

for reason in result["reasons"]:

    print(
        "-",
        reason
    )