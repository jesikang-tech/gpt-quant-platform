from core.market_strategy import generate_market_strategy


market_regime = {

    "regime": "NEUTRAL",

    "confidence": 82,

    "market_strength": "Strong"

}


result = generate_market_strategy(
    market_regime
)


print("=" * 40)
print("AI Market Strategy Test")
print("=" * 40)


for key, value in result.items():

    print(
        f"{key}: {value}"
    )