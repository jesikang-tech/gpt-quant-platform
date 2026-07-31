from repository import get_etf_score_detail
from datetime import datetime


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


    report_date = datetime.now().strftime(
    "%Y-%m-%d"
    )


    print(
        f"Score Created : {created_at}"
    )


    print(
        f"Report Date   : {report_date}"
    )


    print("=" * 40)



if __name__ == "__main__":

    print_score_report(
        "365040"
    )