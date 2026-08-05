from core.portfolio_advisor import (
    generate_portfolio,
    analyze_portfolio_health
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


result = generate_portfolio(ranking)


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