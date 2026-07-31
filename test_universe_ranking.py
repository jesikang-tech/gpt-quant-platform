from ranking_analyzer import (
    get_universe_enhanced_ranking
)


print("="*40)
print("Universe Enhanced Ranking Test")
print("="*40)


results = get_universe_enhanced_ranking()


print()

print(
    "ETF Count :",
    len(results)
)


for item in results:

    print()

    print(
        item
    )