from repository import (
    get_etf_prices,
    get_all_etf_tickers,
    has_price_data,
    get_top_scores
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



def get_analyzable_tickers(
    tickers
):
    """
    가격 데이터가 존재하는
    ETF만 필터링
    """

    result = []


    for ticker in tickers:

        if has_price_data(
            ticker
        ):
            result.append(
                ticker
            )


    return result



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

    all_tickers = get_all_etf_tickers()

    tickers = get_analyzable_tickers(
        all_tickers
    )


    print("=" * 40)
    print("ETF Batch Analysis")
    print("=" * 40)


    print(
        f"Total ETF : {len(all_tickers)}"
    )

    print(
        f"Analyzable ETF : {len(tickers)}"
    )

    print(
        f"Skipped ETF : {len(all_tickers)-len(tickers)}"
    )


    results = run_batch_analysis(
        tickers
    )


    print()
    print("=" * 40)
    print("Batch Analysis Result")
    print("=" * 40)


    for item in results:
        print(item)


    print()

    print("=" * 40)
    print("GPT ETF Ranking TOP 10")
    print("=" * 40)


    ranking = get_top_scores(
        10
    )


    for index, item in enumerate(
        ranking,
        start=1
    ):

        print(
            f"{index}. {item[0]}  Score : {item[1]}"
        )    