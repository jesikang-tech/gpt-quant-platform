import time
from datetime import datetime

from collector.bulk_price_collector import BulkPriceCollector


def main():

    start_time = time.time()

    print("=" * 50)
    print("GPT Quant Platform")
    print("ETF Price Collection Start")
    print("=" * 50)

    start_date = "2026-01-01"
    end_date = datetime.today().strftime("%Y-%m-%d")


    print()
    print(f"수집 기간 : {start_date} ~ {end_date}")
    print()


    collector = BulkPriceCollector()


    collector.collect(
        start_date,
        end_date
    )


    elapsed = time.time() - start_time


    print()
    print("=" * 50)
    print("ETF Price Collection Finished")
    print(f"소요 시간 : {elapsed:.2f}초")
    print("=" * 50)


if __name__ == "__main__":
    main()