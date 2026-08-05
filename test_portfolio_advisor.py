from core.portfolio_advisor import (
    generate_portfolio,
    analyze_portfolio_health
)

from core.market_strategy import (
    generate_market_strategy
)

from core.market_regime import (
    analyze_market_regime
)


ranking = [

    {
        "ticker":"069500",
        "score":93,
        "trend":1
    },

    {
        "ticker":"379800",
        "score":88,
        "trend":1
    },

    {
        "ticker":"360750",
        "score":82,
        "trend":1
    }

]



market_regime = analyze_market_regime()


strategy = generate_market_strategy(
    market_regime
)


print()


print("="*40)
print("Forced Aggressive Strategy Test")
print("="*40)


aggressive_regime = {

    "regime": "BULLISH",

    "confidence": 90,

    "market_strength": "Strong"

}


aggressive_strategy = generate_market_strategy(
    aggressive_regime
)


for key, value in aggressive_strategy.items():

    print(
        f"{key}: {value}"
    )


print("="*40)
print("AI Market Strategy Test")
print("="*40)



for key, value in strategy.items():

    print(
        f"{key}: {value}"
    )


result = generate_portfolio(ranking)


print()


print("="*40)
print("Forced Aggressive Portfolio Test")
print("="*40)


aggressive_portfolio = generate_portfolio(
    ranking,
    aggressive_regime
)


for item in aggressive_portfolio:
    print(item)

print()


print("="*40)
print("AI Portfolio Advisor Test")
print("="*40)


for item in result:
    print(item)

print("\n")
print("="*40)
print("Portfolio Health Test")
print("="*40)


health = analyze_portfolio_health(result)


print(health)    