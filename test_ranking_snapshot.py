from repository import get_ranking_snapshot



def main():

    ranking_date = "2026-07-30"


    results = get_ranking_snapshot(
        ranking_date
    )


    print("=" * 40)
    print("ETF Ranking Snapshot")
    print("=" * 40)


    for row in results:

        print(
            row
        )



if __name__ == "__main__":

    main()