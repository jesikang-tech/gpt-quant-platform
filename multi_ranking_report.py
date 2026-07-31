from ranking_analyzer import (
    get_universe_enhanced_ranking
)

from repository import save_ranking_history


def print_multi_ranking_report(
    limit=10
):

    results = get_universe_enhanced_ranking()


    print("=" * 60)
    print("GPT ETF MULTI INTELLIGENCE RANKING")
    print("=" * 60)


    print()


    for index, item in enumerate(
        results[:limit],
        1
    ):

        print(
            f"{index}. {item['ticker']}"
        )

        print(
            "Enhanced Score :",
            item["enhanced_score"]
        )

        print(
            "Grade           :",
            item["grade"]
        )

        print(
            "Stability       :",
            item["stability_score"]
        )

        print(
            "Prediction Bonus:",
            item["prediction_bonus"]
        )

        save_ranking_history(
            item["ticker"],
            index,
            item["enhanced_score"],
            "2026-07-31"
        )

        print(
            "-" * 40
        )



if __name__ == "__main__":

    print_multi_ranking_report()