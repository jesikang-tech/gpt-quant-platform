from factor_engine import calculate_slope_score

prices = [
    100,
    102,
    103,
    105,
    107,
    110,
    112,
    115
]

score = calculate_slope_score(prices)

print("=" * 40)
print("Slope Score Test")
print("=" * 40)
print(score)