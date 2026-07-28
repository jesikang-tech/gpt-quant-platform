import pandas as pd

from src.factor.factor_engine import FactorEngine

engine = FactorEngine()

prices = []

price = 100

for _ in range(60):
    prices.append(price)
    price += 0.35

df = pd.DataFrame({
    "date": pd.date_range("2026-01-01", periods=60),
    "close": prices,
    "volume": [1000] * 60
})

score = engine.trend.return_score(df)

print("Return Score :", score)