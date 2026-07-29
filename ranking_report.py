from repository import get_top_scores
from score_report import print_score_report



def print_ranking_report(
    limit=10
):
    """
    GPT ETF Ranking Report
    """


    ranking = get_top_scores()



    print("=" * 40)
    print("GPT ETF TOP RANKING REPORT")
    print("=" * 40)

    print()



    for index, item in enumerate(
        ranking[:limit],
        1
    ):

        print(
            f"{index}. {item[0]}  Score : {item[1]}"
        )


    print()


    print("=" * 40)
    print("TOP ETF DETAIL")
    print("=" * 40)


    if ranking:

        top_ticker = ranking[0][0]


        print_score_report(
            top_ticker
        )



if __name__ == "__main__":

    print_ranking_report()