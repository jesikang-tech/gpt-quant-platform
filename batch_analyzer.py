from repository import (
    get_all_etf_tickers,
    get_etf_prices,
    save_ranking_history
)

from ranking_analyzer import get_enhanced_ranking

from datetime import datetime
from etf_analyzer import analyze_etf
from ranking_analyzer import get_enhanced_ranking



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
    print("GPT ETF Enhanced Ranking TOP 10")
    print("=" * 40)


    ranking = get_enhanced_ranking()



    ranking_date = datetime.now().strftime("%Y-%m-%d")


    for index, item in enumerate(
        ranking,
        1
    ):

        save_ranking_history(
            item["ticker"],
            index,
            item["enhanced_score"],
            ranking_date
        )


    for index, item in enumerate(
        ranking,
        1
    ):

        print(
            f"{index}. {item['ticker']} "
            f"Base : {item['base_score']} "
            f"Trend : {item['trend_score']} "
            f"Momentum : {item['momentum_score']} "
            f"Enhanced : {item['enhanced_score']}"
        )



if __name__ == "__main__":

    run_batch_analysis()