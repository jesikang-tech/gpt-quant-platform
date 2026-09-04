from repository import (
    get_all_etf_tickers,
    get_etf_prices,
    save_ranking_history
)

from etf_analyzer import analyze_etf


def run_batch_analysis(analysis_date=None):

    if analysis_date is None:
        from datetime import date
        analysis_date = date.today().isoformat()

    tickers = get_all_etf_tickers()


    results = []


    total_count = len(tickers)

    analyzable_count = 0
    skipped_count = 0



    for ticker in tickers:


        prices = get_etf_prices(
            ticker
        )


        close_prices = [
            price[1]
            for price in prices
        ]


        if len(close_prices) < 2:

            skipped_count += 1

            continue



        result = analyze_etf(
            ticker,
            close_prices,
            analysis_date
        )


        if result:

            results.append(
                result
            )

            analyzable_count += 1

        else:

            skipped_count += 1



    print("=" * 40)
    print("ETF Batch Analysis")
    print("=" * 40)

    print(
        f"Total ETF : {total_count}"
    )

    print(
        f"Analyzable ETF : {analyzable_count}"
    )

    print(
        f"Skipped ETF : {skipped_count}"
    )


    print()


    print("=" * 40)
    print("Batch Analysis Result")
    print("=" * 40)



    for result in results:

        print(result)



    print()


    print("=" * 40)
    print("GPT ETF Enhanced Ranking TOP 10")
    print("=" * 40)


    # Batch Analysis 결과 기준 Ranking 생성
    ranking = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )[:10]





    for index, item in enumerate(
        ranking,
        1
    ):

        save_ranking_history(
            item["ticker"],
            index,
            item["score"],
            analysis_date
        )


    for index, item in enumerate(
        ranking,
        1
    ):

        print(
            f"{index}. {item['ticker']} "
            f"Return : {item['return']:.2f}% "
            f"Score : {item['score']}"
        )



if __name__ == "__main__":

    run_batch_analysis()