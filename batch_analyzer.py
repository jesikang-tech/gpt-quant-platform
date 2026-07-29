from repository import (
    get_etf_prices,
    save_or_update_etf_score
)

from etf_analyzer import analyze_etf



def get_price_list(ticker):
    """
    DB 가격 데이터를
    분석용 리스트로 변환
    """

    rows = get_etf_prices(
        ticker
    )

    prices = []

    for row in rows:
        prices.append(
            row[1]
        )

    return prices



def run_batch_analysis(
    tickers
):
    """
    ETF 전체 분석 실행
    """

    results = []


    for ticker in tickers:

        prices = get_price_list(
            ticker
        )


        if len(prices) == 0:
            continue


        result = analyze_etf(
            ticker,
            prices
        )


        if result:

            results.append(
                result
            )


    return results



if __name__ == "__main__":

    test_tickers = [
        "069500"
    ]


    results = run_batch_analysis(
        test_tickers
    )


    print("=" * 40)
    print("Batch Analysis Result")
    print("=" * 40)


    for item in results:
        print(item)