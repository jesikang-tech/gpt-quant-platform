from repository import (
    get_top_scores,
    save_ranking_history
)

from score_report import print_score_report

from ranking_analyzer import (
    get_enhanced_ranking,
    generate_ranking_assessment
)



def print_ranking_report(
    limit=10
):
    """
    GPT ETF Ranking Analytics Report
    """


    ranking = get_top_scores()

    enhanced = get_enhanced_ranking()


    print("=" * 50)
    print("GPT ETF RANKING ANALYTICS REPORT")
    print("=" * 50)

    print()


    print("===== Enhanced Ranking =====")


    for index, item in enumerate(
        enhanced[:limit],
        1
    ):

        print()

        print(
            f"{index}. {item['ticker']}"
        )

        print(
            "Base Score :",
            item["base_score"]
        )

        print(
            "Trend Score :",
            item["trend_score"]
        )

        print(
            "Momentum Score :",
            item["momentum_score"]
        )

        print(
            "Grade :",
            item["grade"]
        )

        print(
            "Grade Bonus :",
            item["grade_bonus"]
        )

        print(
            "Enhanced Score :",
            item["enhanced_score"]
        )

        assessment = generate_ranking_assessment(
            item["ticker"]
        )

        print(
            "Assessment :",
            assessment["message"]
        )

        print(
            "-" * 40
        )



    print()


    print("=" * 50)
    print("===== Ranking History Save =====")
    print("=" * 50)


    for index, item in enumerate(
        ranking[:limit],
        1
    ):

        save_ranking_history(
            item[0],
            index,
            item[1],
            "2026-07-31"
        )



    print()


    print("=" * 50)
    print("===== TOP ETF DETAIL =====")
    print("=" * 50)


    if ranking:

        top_ticker = ranking[0][0]


        print_score_report(
            top_ticker
        )



if __name__ == "__main__":

    print_ranking_report()