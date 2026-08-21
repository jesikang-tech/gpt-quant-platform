def validate_portfolio_snapshot_input(portfolio):
    if not isinstance(portfolio, list):
        return False, "PORTFOLIO_NOT_LIST"

    if not portfolio:
        return False, "EMPTY_PORTFOLIO"

    tickers = []
    total_weight = 0.0

    for item in portfolio:
        if not isinstance(item, dict):
            return False, "INVALID_POSITION"

        ticker = item.get("ticker")

        if not ticker:
            return False, "MISSING_TICKER"

        if ticker in tickers:
            return False, "DUPLICATE_TICKER"

        tickers.append(ticker)

        weight = item.get("weight")

        if weight is None:
            return False, "MISSING_WEIGHT"

        try:
            weight = float(weight)
        except (TypeError, ValueError):
            return False, "INVALID_WEIGHT"

        if weight < 0:
            return False, "NEGATIVE_WEIGHT"

        total_weight += weight

        if ticker != "CASH":
            if (
                item.get("reference_price") is None
                or item.get("reference_price_date") is None
            ):
                return False, "MISSING_REFERENCE_PRICE"

    if abs(total_weight - 100.0) > 0.0001:
        return False, "INVALID_TOTAL_WEIGHT"

    return True, "VALID"


def run_case(name, portfolio, expected_valid, expected_reason):
    valid, reason = validate_portfolio_snapshot_input(
        portfolio
    )

    assert valid is expected_valid
    assert reason == expected_reason

    print(
        f"{name}: PASS | valid={valid} | reason={reason}"
    )


print("=" * 60)
print(
    "Production Hardening - Snapshot Input "
    "Validation Contract"
)
print("=" * 60)


run_case(
    "CASE 1 VALID PORTFOLIO",
    [
        {
            "ticker": "306950",
            "weight": 40,
            "reference_price": 67560,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "365040",
            "weight": 30,
            "reference_price": 33540,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "475720",
            "weight": 20,
            "reference_price": 11730,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "CASH",
            "weight": 10,
        },
    ],
    True,
    "VALID",
)


run_case(
    "CASE 2 EMPTY PORTFOLIO",
    [],
    False,
    "EMPTY_PORTFOLIO",
)


run_case(
    "CASE 3 INVALID TOTAL WEIGHT",
    [
        {
            "ticker": "306950",
            "weight": 40,
            "reference_price": 67560,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "365040",
            "weight": 30,
            "reference_price": 33540,
            "reference_price_date": "2026-08-20",
        },
    ],
    False,
    "INVALID_TOTAL_WEIGHT",
)


run_case(
    "CASE 4 NEGATIVE WEIGHT",
    [
        {
            "ticker": "306950",
            "weight": -10,
            "reference_price": 67560,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "365040",
            "weight": 110,
            "reference_price": 33540,
            "reference_price_date": "2026-08-20",
        },
    ],
    False,
    "NEGATIVE_WEIGHT",
)


run_case(
    "CASE 5 DUPLICATE TICKER",
    [
        {
            "ticker": "306950",
            "weight": 40,
            "reference_price": 67560,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "306950",
            "weight": 50,
            "reference_price": 67560,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "CASH",
            "weight": 10,
        },
    ],
    False,
    "DUPLICATE_TICKER",
)


run_case(
    "CASE 6 MISSING ETF REFERENCE",
    [
        {
            "ticker": "306950",
            "weight": 90,
        },
        {
            "ticker": "CASH",
            "weight": 10,
        },
    ],
    False,
    "MISSING_REFERENCE_PRICE",
)


run_case(
    "CASE 7 CASH WITHOUT REFERENCE",
    [
        {
            "ticker": "306950",
            "weight": 90,
            "reference_price": 67560,
            "reference_price_date": "2026-08-20",
        },
        {
            "ticker": "CASH",
            "weight": 10,
        },
    ],
    True,
    "VALID",
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
