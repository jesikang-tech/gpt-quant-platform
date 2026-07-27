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

def save_etf_info(
    ticker,
    name,
    market
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO etf_info
        (
            ticker,
            name,
            market
        )
        VALUES (?, ?, ?)
        """,
        (
            ticker,
            name,
            market
        )
    )

    conn.commit()
    conn.close()



def save_etf_score(
    ticker,
    return_score,
    trend_score,
    volume_score,
    final_score,
    created_at
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO etf_scores
        (
            ticker,
            return_score,
            trend_score,
            volume_score,
            final_score,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ticker,
            return_score,
            trend_score,
            volume_score,
            final_score,
            created_at
        )
    )

    conn.commit()
    conn.close()

def get_top_scores(limit=10):
    """
    ETF Score Ranking 조회
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            ticker,
            final_score
        FROM etf_scores
        ORDER BY final_score DESC
        LIMIT ?
        """,
        (limit,)
    )

    results = cursor.fetchall()

    conn.close()

    return results