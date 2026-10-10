from collector.price_collector import PriceCollector


def main():
    collector = PriceCollector()


    df = collector.collect(
        "069500",
        "2026-01-01",
        "2026-07-28"
    )


    print(df.head())

    print()

    print(f"수집 데이터 개수 : {len(df)}")


if __name__ == "__main__":
    main()
