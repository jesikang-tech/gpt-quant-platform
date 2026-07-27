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