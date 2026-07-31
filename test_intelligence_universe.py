from ranking_analyzer import (
    get_all_intelligence_universe
)


print("=" * 40)
print("ETF Intelligence Universe Test")
print("=" * 40)


tickers = get_all_intelligence_universe()


print()

print(
    "ETF Count :",
    len(tickers)
)


for ticker in tickers[:10]:

    print(
        ticker
    )