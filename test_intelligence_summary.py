from ranking_analyzer import (
    get_dashboard_intelligence_summary
)


print("=" * 60)
print("GPT Dashboard Intelligence Test")
print("=" * 60)


result = get_dashboard_intelligence_summary()


print()


if result["success"]:

    print("Ticker :", result["ticker"])
    print("Score :", result["score"])
    print("Enhanced Score :", result["enhanced_score"])
    print("Grade :", result["grade"])
    print("Prediction :", result["prediction"])
    print("Stability :", result["stability"])

    print()

    print("Trend :")
    print(result["trend"])

    print()

    print("Risk :")
    print(result["risk"])

    print()

    print("Opinion :")
    print(result["opinion"])


else:

    print(
        result["message"]
    )