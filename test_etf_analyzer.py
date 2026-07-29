from etf_analyzer import analyze_etf


def main():

    ticker = "069500"

    prices = [
        10000,
        10200,
        10500,
        10800,
        11000,
        11300,
        11600
    ]


    result = analyze_etf(
        ticker,
        prices
    )


    print("=" * 40)
    print("ETF Analyzer Test")
    print("=" * 40)

    print(result)



if __name__ == "__main__":
    main()