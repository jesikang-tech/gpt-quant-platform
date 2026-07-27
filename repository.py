from database import get_connection


def save_etf_price(
    ticker,
    date,
    close_price
):
    """
    ETF 가격 데이터 저장
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO etf_prices
        (
            ticker,
            date,
            close_price
        )
        VALUES (?, ?, ?)
        """,
        (
            ticker,
            date,
            close_price
        )
    )

    conn.commit()
    conn.close()


def get_etf_prices(ticker):
    """
    특정 ETF 가격 조회
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT date, close_price
        FROM etf_prices
        WHERE ticker = ?
        ORDER BY date
        """,
        (ticker,)
    )

    result = cursor.fetchall()

    conn.close()

    return result