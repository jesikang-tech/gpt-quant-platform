from repository import (
    get_all_etf_tickers,
    get_etf_prices,
    get_top_scores,
    save_ranking_history
)

from datetime import datetime
from etf_analyzer import analyze_etf



def run_batch_analysis():

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
            close_prices
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
    print("GPT ETF Ranking TOP 10")
    print("=" * 40)



    ranking = get_top_scores()



    for index, item in enumerate(
        ranking,
        1
    ):

        save_ranking_history(
            item[0],
            index,
            item[1],
            datetime.now().strftime("%Y-%m-%d")
        )


    for index, item in enumerate(
        ranking,
        1
    ):

        print(
            f"{index}. {item[0]}  Score : {item[1]}"
        )



if __name__ == "__main__":

    run_batch_analysis()