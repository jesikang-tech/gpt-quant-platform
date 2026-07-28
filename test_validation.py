import pandas as pd

from src.factor.factor_engine import FactorEngine

engine = FactorEngine()

df = pd.DataFrame({
    "date": [
        "2026-01-03",
        "2026-01-01",
        "2026-01-02",
    ],
    "close": [
        100,
        98,
        99,
    ],
    "volume": [
        1000,
        900,
        950,
    ]
})

validated = engine.trend.validate(df)

print(validated)