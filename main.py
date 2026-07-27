from database import initialize_database
from repository import (
    save_etf_price,
    get_etf_prices,
    save_etf_score,
    get_top_scores,
    remove_duplicate_scores
)

from factor_engine import calculate_return, calculate_trend_score
from core.logger import get_logger
from etf_analyzer import analyze_etf


logger = get_logger()


def main():

    logger.info("GPT Quant Platform Start")

    initialize_database()


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


    # ETF Score 저장
    save_etf_score(
        "069500",
        90,
        100,
        80,
        90,
        "2026-07-27"
    )


    # 중복 제거
    remove_duplicate_scores()


    # Ranking 출력
    ranking = get_top_scores()


    logger.info(
        f"ETF Ranking: {ranking}"
    )


    # ETF 분석 Pipeline 테스트
    analysis = analyze_etf(
        "069500",
        [
            10000,
            10200,
            10400,
            10600,
            10800,
            11000,
            11500
        ]
    )


    logger.info(
        f"ETF Analysis: {analysis}"
    )


if __name__ == "__main__":
    main()