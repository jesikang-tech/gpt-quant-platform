from config import MIN_RETURN_3M
from repository import get_etf_prices
from decimal import Decimal, localcontext
from fractions import Fraction


DEFAULT_PERIODS = {
    20: 0.05,
    40: 0.10,
    60: MIN_RETURN_3M,
}


def calculate_period_return(prices):
    """Return Decimal for Decimal endpoints, otherwise preserve legacy float.

    Mixed endpoints use Decimal(str(value)) for non-Decimal values. Decimal
    arithmetic inherits the caller's precision/rounding in a local context;
    subtract before division to avoid losing tiny gains by subtracting one.
    Supported prices are finite int/float/Decimal values with positive start.
    Nonpositive starts retain the existing None result. Other invalid-input
    conversion or Decimal arithmetic errors are not suppressed.
    """
    if len(prices) < 2:
        return None

    if isinstance(prices[0], Decimal) or isinstance(prices[-1], Decimal):
        start_price = Decimal(str(prices[0]))
        end_price = Decimal(str(prices[-1]))
        if start_price <= 0:
            return None
        with localcontext():
            return ((end_price - start_price) / start_price) * Decimal(100)

    start_price = float(prices[0])
    end_price = float(prices[-1])

    if start_price <= 0:
        return None

    return ((end_price / start_price) - 1.0) * 100.0


def calculate_period_uptrend_ratio(prices):
    """Keep the legacy float percentage; compare Decimal prices without loss."""
    if len(prices) < 2:
        return None

    changes = len(prices) - 1

    up_days = sum(
        1
        for previous, current in zip(prices, prices[1:])
        if (Decimal(str(current)) > Decimal(str(previous))
            if isinstance(current, Decimal) or isinstance(previous, Decimal)
            else float(current) > float(previous))
    )

    return (up_days / changes) * 100.0


def analyze_period(prices, period_days, threshold):
    """Compare finite numeric inputs exactly, without rounding a shortfall up.

    Threshold display preserves Decimal versus legacy float types. The decision
    uses exact rational arithmetic on decimal text, independent of rounded
    return/display values or Decimal context. For floats, str(value) defines
    the decimal interpretation; prior binary precision loss cannot be recovered.
    Finite negative/zero thresholds remain valid. Nonfinite endpoints or
    thresholds cannot pass the decision or reach Fraction conversion; earlier
    unsupported-input arithmetic errors still propagate. Displayed Decimal
    returns can round to the threshold while the exact decision remains False.
    """
    threshold_percent = threshold * (Decimal(100) if isinstance(threshold, Decimal) else 100.0)
    if len(prices) < period_days:
        return {
            "period_days": period_days,
            "status": "INSUFFICIENT_DATA",
            "required_data": period_days,
            "available_data": len(prices),
            "return_rate": None,
            "uptrend_ratio": None,
            "threshold": threshold_percent,
            "threshold_pass": False,
        }

    period_prices = prices[-period_days:]

    return_rate = calculate_period_return(period_prices)
    uptrend_ratio = calculate_period_uptrend_ratio(period_prices)

    return {
        "period_days": period_days,
        "status": "ANALYZED",
        "required_data": period_days,
        "available_data": len(period_prices),
        "return_rate": return_rate,
        "uptrend_ratio": uptrend_ratio,
        "threshold": threshold_percent,
        "threshold_pass": (
            return_rate is not None
            and all(Decimal(str(value)).is_finite() for value in (
                period_prices[0], period_prices[-1], threshold,
            ))
            and Fraction(str(period_prices[-1])) >= (
                Fraction(str(period_prices[0])) * (1 + Fraction(str(threshold)))
            )
        ),
    }


def analyze_periods(prices, thresholds=None):
    if thresholds is None:
        thresholds = DEFAULT_PERIODS

    results = {}

    for period_days in (20, 40, 60):
        threshold = thresholds.get(
            period_days,
            DEFAULT_PERIODS[period_days]
        )

        results[str(period_days)] = analyze_period(
            prices,
            period_days,
            threshold
        )

    return results



def calculate_trend_state(periods):
    period_20 = periods.get("20", {})
    period_40 = periods.get("40", {})
    period_60 = periods.get("60", {})

    return_20 = period_20.get("return_rate")
    return_40 = period_40.get("return_rate")
    return_60 = period_60.get("return_rate")

    if return_20 is None or return_40 is None or return_60 is None:
        return "DOWNTREND"

    if (
        return_60 >= 15
        and return_40 >= 10
        and return_20 >= 5
    ):
        return "UPTREND"

    if (
        return_60 >= 15
        and return_40 >= 10
        and return_20 >= 0
    ):
        return "SLOWING"

    if (
        return_60 >= 15
        and return_40 >= 0
        and return_20 < 0
    ):
        return "CORRECTION"

    return "DOWNTREND"

def get_period_analysis(ticker, analysis_date=None, thresholds=None):
    rows = get_etf_prices(
        ticker,
        analysis_date
    )

    prices = [
        row[1] if isinstance(row[1], Decimal) else float(row[1])
        for row in rows
    ]

    results = analyze_periods(
        prices,
        thresholds
    )

    return {
        "ticker": ticker,
        "analysis_date": analysis_date,
        "periods": results,
        "trend_state": calculate_trend_state(results),
    }
