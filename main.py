from database import init_database

from etf_loader import (
    get_csv_etf_list,
    update_etf_database
)

from batch_analyzer import run_batch_analysis

from ranking_report import print_ranking_report

from core.logger import get_logger


logger = get_logger()



def main():

    logger.info(
        "GPT Quant Platform Pipeline Start"
    )


    # --------------------------------
    # Database Initialize
    # --------------------------------

    init_database()



    # --------------------------------
    # Step 1
    # ETF Information Update
    # --------------------------------

    logger.info(
        "[1] ETF Information Update"
    )


    etf_list = get_csv_etf_list()


    update_etf_database(
        etf_list
    )



    # --------------------------------
    # Step 2
    # ETF Price Data Update
    #
    # 현재:
    # price_data.csv 테스트 데이터 사용 안 함
    #
    # 향후:
    # pykrx 실제 데이터 수집 연결 예정
    # --------------------------------

    logger.info(
        "[2] Price Data Update"
    )


    logger.info(
        "Price update skipped (production mode)"
    )



    # --------------------------------
    # Step 3
    # ETF Batch Analysis
    # --------------------------------

    logger.info(
        "[3] ETF Batch Analysis"
    )


    run_batch_analysis()



    # --------------------------------
    # Step 4
    # Ranking Report
    # --------------------------------

    logger.info(
        "[4] GPT ETF Ranking Report"
    )


    print_ranking_report()



    logger.info(
        "GPT Quant Platform Pipeline Completed"
    )



if __name__ == "__main__":

    main()