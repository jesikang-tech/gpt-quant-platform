from database import initialize_database
from repository import save_etf_price, get_etf_prices
from factor_engine import calculate_return, calculate_trend_score
from core.logger import get_logger
from repository import save_etf_score, get_top_scores


logger = get_logger()


def main():

    logger.info("GPT Quant Platform Start")

    # database 초기화
    initialize_database()

    # 테스트 데이터 저장
    save_etf_price(
        "TEST_ETF",
        "2026-04-01",
        10000
    )

    save_etf_price(
        "TEST_ETF",
        "2026-07-01",
        12000
    )

    prices = get_etf_prices(
        "TEST_ETF"
    )

    close_prices = [
        price[1]
        for price in prices
    ]

    result = calculate_return(
        close_prices[0],
        close_prices[-1]
    )

    score = calculate_trend_score(
        close_prices
    )

    logger.info(
        f"Return: {result:.2f}%"
    )

    logger.info(
        f"Trend Score: {score}"
    )

if __name__ == "__main__":
    main()

    save_etf_score(
    "069500",
    90,
    100,
    80,
    90,
    "2026-07-27"
)


ranking = get_top_scores()

logger.info(
    f"ETF Ranking: {ranking}"
)