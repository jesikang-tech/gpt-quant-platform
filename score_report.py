from repository import get_etf_score_detail



def print_score_report(
    ticker
):
    """
    ETF Score Report 출력
    """


    result = get_etf_score_detail(
        ticker
    )


    if result is None:

        print(
            "No Score Data"
        )

        return



    (
        ticker,
        return_score,
        trend_score,
        slope_score,
        final_score,
        created_at
    ) = result



    print("=" * 40)
    print("GPT ETF Score Report")
    print("=" * 40)


    print()

    print(
        f"ETF Ticker : {ticker}"
    )


    print()

    print(
        f"Return Score : {return_score}"
    )


    print(
        f"Trend Score  : {trend_score}"
    )


    print(
        f"Slope Score  : {slope_score}"
    )


    print()

    print("-" * 40)


    print(
        f"Final Score : {final_score}"
    )


    print(
        f"Analysis Date : {created_at}"
    )


    print("=" * 40)



if __name__ == "__main__":

    print_score_report(
        "365040"
    )