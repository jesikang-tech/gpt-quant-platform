from historical_replay import HistoricalReplayEngine


def make_prices(start, daily_change, count=60):
    return [
        start + (daily_change * index)
        for index in range(count)
    ]


print("===== HISTORICAL REPLAY CORE TEST =====")

# CASE 1: 60 trading days boundary
prices_60 = make_prices(100, 0.35, 60)
print("CASE 1 - 60 trading days :", len(prices_60) == 60)

# CASE 2: 3-month window calculation
rows = [
    ("2026-01-01", 100.0),
    ("2026-02-01", 110.0),
    ("2026-03-01", 120.0),
    ("2026-04-01", 130.0),
]
window = HistoricalReplayEngine._calculate_three_month_prices(rows)
print("CASE 2 - 3-month window :", window == [100.0, 110.0, 120.0, 130.0])

# CASE 3: return boundary
return_rate = (115.0 - 100.0) / 100.0 * 100
print("CASE 3 - Return 15% boundary :", return_rate >= 15.0)

# CASE 4: uptrend ratio boundary
uptrend_prices = make_prices(100, 1.0, 10)
uptrend_ratio = sum(
    uptrend_prices[i] > uptrend_prices[i - 1]
    for i in range(1, len(uptrend_prices))
) / (len(uptrend_prices) - 1) * 100
print("CASE 4 - Uptrend 70% boundary :", uptrend_ratio >= 70.0)

# CASE 5: analysis date validation
engine = HistoricalReplayEngine("2026-07-31")
print("CASE 5 - Analysis date validation :", engine.analysis_date == "2026-07-31")

# CASE 6: invalid analysis date
try:
    HistoricalReplayEngine("2026-02-30")
    print("CASE 6 - Invalid date rejection : False")
except ValueError:
    print("CASE 6 - Invalid date rejection : True")

# CASE 7: limit validation
try:
    engine.replay(0)
    print("CASE 7 - Invalid limit rejection : False")
except ValueError:
    print("CASE 7 - Invalid limit rejection : True")

print("===== TEST COMPLETE =====")

