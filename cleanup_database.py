from database import get_connection


def main():

    conn = get_connection()
    cursor = conn.cursor()

    print("=" * 60)
    print("GPT Quant Platform")
    print("Database Clean-up")
    print("=" * 60)


    # -----------------------------------------
    # etf_info 에 없는 ticker 삭제
    # -----------------------------------------

    cursor.execute(
        """
        DELETE
        FROM etf_prices
        WHERE ticker NOT IN
        (
            SELECT ticker
            FROM etf_info
        )
        """
    )

    print(
        f"삭제(미등록 ETF) : {cursor.rowcount}"
    )


    # -----------------------------------------
    # 숫자 6자리 아닌 ticker 삭제
    # -----------------------------------------

    cursor.execute(
        """
        DELETE
        FROM etf_prices
        WHERE
            LENGTH(ticker) <> 6
            OR ticker GLOB '*[^0-9]*'
        """
    )

    print(
        f"삭제(비정상 코드) : {cursor.rowcount}"
    )


    conn.commit()

    conn.close()


    print()
    print("Clean-up 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()