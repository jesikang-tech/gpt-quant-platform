from core.portfolio_advisor import optimize_portfolio_weight

print("=" * 40)
print("AI Portfolio Optimization Test")
print("=" * 40)

ranking = [
    {
        "ticker": "365040",
        "score": 90.7
    },
    {
        "ticker": "306950",
        "score": 90.4
    },
    {
        "ticker": "292160",
        "score": 90.1
    }
]

portfolio = optimize_portfolio_weight(
    ranking,
    "aggressive"
)

for item in portfolio:
    print(item)