from repository import get_etf_score_detail


def main():

    ticker = "365040"


    result = get_etf_score_detail(
        ticker
    )


    print("=" * 40)
    print("ETF Score Detail")
    print("=" * 40)


    print(result)



if __name__ == "__main__":

    main()