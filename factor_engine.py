def calculate_return(
    start_price,
    end_price
):
    """
    기간 수익률 계산
    """

    if start_price == 0:
        return 0

    return (
        (end_price - start_price)
        / start_price
    ) * 100


def calculate_trend_score(
    prices
):
    """
    단순 상승 추세 점수 계산

    prices:
    [10000, 10200, 10500, 11000]
    """

    if len(prices) < 2:
        return 0

    if prices[-1] > prices[0]:
        return 100

    return 0