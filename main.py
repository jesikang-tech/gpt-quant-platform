from database import init_database

from etf_loader import (
    get_csv_etf_list,
    update_etf_database
)

from price_loader import (
    get_csv_price_data,
    update_price_database
)

from batch_analyzer import run_batch_analysis

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
    # --------------------------------

    logger.info(
        "[2] Price Data Update"
    )

    logger.info(
        "Price update skipped (production mode)"
    )



    # --------------------------------
    # Step 3
    # ETF Analysis
    # --------------------------------

    logger.info(
        "[3] ETF Batch Analysis"
    )


    run_batch_analysis()



    logger.info(
        "GPT Quant Platform Pipeline Completed"
    )



if __name__ == "__main__":

    main()