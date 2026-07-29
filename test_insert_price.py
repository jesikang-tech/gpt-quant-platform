from repository import save_etf_price


ticker = "069500"


prices = [
    10000,
    10200,
    10500,
    10800,
    11000,
    11300,
    11600
]


for i, price in enumerate(prices):

    save_etf_price(
        ticker,
        f"2026-07-{20+i}",
        price
    )


print("Price data inserted")