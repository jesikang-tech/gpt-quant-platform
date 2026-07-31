from ranking_analyzer import (
    get_enhanced_ranking
)


print("=" * 40)
print("Multi ETF Ranking Intelligence Test")
print("=" * 40)


results = get_enhanced_ranking()


print()

print(
    "ETF Count :",
    len(results)
)


for item in results[:10]:

    print()

    print(
        "Ticker :",
        item["ticker"]
    )

    print(
        "Enhanced Score :",
        item["enhanced_score"]
    )

    print(
        "Prediction Bonus :",
        item.get(
            "prediction_bonus",
            0
        )
    )