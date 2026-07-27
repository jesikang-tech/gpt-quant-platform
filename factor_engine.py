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



def calculate_return_score(
    return_rate
):
    """
    수익률 기반 Score 계산
    """

    if return_rate >= 20:
        return 100

    elif return_rate >= 15:
        return 90

    elif return_rate >= 10:
        return 70

    elif return_rate > 0:
        return 50

    else:
        return 0



def calculate_trend_score(
    prices
):
    """
    지속 상승 추세 Score 계산
    """

    if len(prices) < 2:
        return 0


    increase_count = 0

    for i in range(
        1,
        len(prices)
    ):
        if prices[i] > prices[i-1]:
            increase_count += 1


    ratio = (
        increase_count
        /
        (len(prices)-1)
    )


    return round(
        ratio * 100
    )



def calculate_final_score(
    return_score,
    trend_score
):
    """
    최종 ETF Score 계산
    """

    return round(
        (
            return_score * 0.5
            +
            trend_score * 0.5
        ),
        2
    )

def calculate_3month_return(
    prices
):
    """
    3개월 수익률 계산

    prices:
    [10000, 10100, ..., 11500]
    """

    if len(prices) < 2:
        return 0

    start_price = prices[0]
    end_price = prices[-1]

    return calculate_return(
        start_price,
        end_price
    )



def calculate_uptrend_ratio(
    prices
):
    """
    상승 유지 비율 계산
    """

    if len(prices) < 2:
        return 0


    up_count = 0

    for i in range(1, len(prices)):

        if prices[i] > prices[i-1]:
            up_count += 1


    return round(
        (
            up_count /
            (len(prices)-1)
        ) * 100,
        2
    )



def check_etf_condition(
    prices
):
    """
    GPT ETF Score 대상 조건

    조건:
    3개월 상승률 >= 15%
    상승 유지율 >= 70%
    """

    return_rate = calculate_3month_return(
        prices
    )

    uptrend_ratio = calculate_uptrend_ratio(
        prices
    )


    if (
        return_rate >= 15
        and
        uptrend_ratio >= 70
    ):
        return True


    return False