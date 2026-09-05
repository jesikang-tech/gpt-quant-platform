import pandas as pd

from src.factor.factor_engine import FactorEngine

engine = FactorEngine()

dates = pd.date_range("2026-01-01", periods=60)

df = pd.DataFrame({
    "date": dates[::-1],
    "close": [100 + i * 0.35 for i in range(60)],
    "volume": [1000] * 60,
})

validated = engine.trend.validate(df)

assert len(validated) == 60
assert validated["date"].is_monotonic_increasing
assert list(validated.columns) == ["date", "close", "volume"]

print("Validation PASS")
print("Rows :", len(validated))
print("First Date :", validated.iloc[0]["date"])
print("Last Date :", validated.iloc[-1]["date"])
