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
        INSERT OR REPLACE INTO etf_prices
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

def get_all_price_data():
    """
    전체 가격 데이터 조회
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            ticker,
            date,
            close_price
        FROM etf_prices
        ORDER BY ticker, date
        """
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



def get_all_etf_info():
    """
    전체 ETF 정보 조회
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            ticker,
            name,
            market
        FROM etf_info
        ORDER BY ticker
        """
    )


    result = cursor.fetchall()


    conn.close()

    return result


def save_etf_score(
    ticker,
    return_score,
    trend_score,
    slope_score,
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
            slope_score,
            final_score,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ticker,
            return_score,
            trend_score,
            slope_score,
            final_score,
            created_at
        )
    )

    conn.commit()
    conn.close()


def save_or_update_etf_score(
    ticker,
    return_score,
    trend_score,
    slope_score,
    final_score,
    created_at
):
    """
    ETF Score 저장 또는 업데이트
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ticker
        FROM etf_scores
        WHERE ticker = ?
        """,
        (ticker,)
    )

    exists = cursor.fetchone()


    if exists:

        cursor.execute(
            """
            UPDATE etf_scores
            SET
                return_score = ?,
                trend_score = ?,
                slope_score = ?,
                final_score = ?,
                created_at = ?
            WHERE ticker = ?
            """,
            (
                return_score,
                trend_score,
                slope_score,
                final_score,
                created_at,
                ticker
            )
        )

    else:

        cursor.execute(
            """
            INSERT INTO etf_scores
            (
                ticker,
                return_score,
                trend_score,
                slope_score,
                final_score,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                ticker,
                return_score,
                trend_score,
                slope_score,
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


def get_etf_score_detail(
    ticker
):
    """
    ETF Score 상세 조회
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            ticker,
            return_score,
            trend_score,
            slope_score,
            final_score,
            created_at
        FROM etf_scores
        WHERE ticker = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            ticker,
        )
    )


    result = cursor.fetchone()


    conn.close()


    return result

def remove_duplicate_scores():
    """
    ETF Score 중복 제거
    최신 데이터만 유지
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM etf_scores
        WHERE rowid NOT IN
        (
            SELECT MAX(rowid)
            FROM etf_scores
            GROUP BY ticker
        )
        """
    )

    conn.commit()
    conn.close()


def save_etf_list(df):
    """
    ETF 목록 전체 저장
    """

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():

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
                row["Symbol"],
                row["Name"],
                "ETF"
            )
        )

    conn.commit()
    conn.close()   


def has_price_data(ticker):
    """
    해당 ETF 가격 데이터 존재 여부 확인
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM etf_prices
        WHERE ticker = ?
        """,
        (ticker,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0


def get_all_etf_tickers():
    """
    저장된 ETF ticker 전체 조회
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ticker
        FROM etf_info
        ORDER BY ticker
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        row[0]
        for row in rows
    ]


def save_score_history(
    ticker,
    return_score,
    trend_score,
    slope_score,
    final_score,
    analysis_date
):
    """
    ETF Score History 저장
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO etf_score_history
        (
            ticker,
            return_score,
            trend_score,
            slope_score,
            final_score,
            analysis_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ticker,
            return_score,
            trend_score,
            slope_score,
            final_score,
            analysis_date
        )
    )


    conn.commit()
    conn.close()


def save_ranking_history(
    ticker,
    rank,
    final_score,
    ranking_date
):
    """
    ETF Ranking History 저장 또는 업데이트
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT id
        FROM etf_ranking_history
        WHERE ticker = ?
        AND ranking_date = ?
        """,
        (
            ticker,
            ranking_date
        )
    )


    exists = cursor.fetchone()


    if exists:

        cursor.execute(
            """
            UPDATE etf_ranking_history
            SET
                rank = ?,
                final_score = ?
            WHERE ticker = ?
            AND ranking_date = ?
            """,
            (
                rank,
                final_score,
                ticker,
                ranking_date
            )
        )


    else:

        cursor.execute(
            """
            INSERT INTO etf_ranking_history
            (
                ticker,
                rank,
                final_score,
                ranking_date
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                ticker,
                rank,
                final_score,
                ranking_date
            )
        )


    conn.commit()
    conn.close()


def get_ranking_snapshot(
    ranking_date
):
    """
    특정 날짜 Ranking 조회
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            ticker,
            rank,
            final_score
        FROM etf_ranking_history
        WHERE ranking_date = ?
        ORDER BY rank
        """,
        (
            ranking_date,
        )
    )


    result = cursor.fetchall()


    conn.close()


    return result    



def get_ranking_history(ticker):
    """
    ETF의 Ranking History 조회
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            rank,
            final_score,
            ranking_date
        FROM etf_ranking_history
        WHERE ticker = ?
        ORDER BY ranking_date DESC
    """, (ticker,))

    rows = cursor.fetchall()

    conn.close()

    return rows    


def save_portfolio_history(
    mode,
    ticker,
    weight,
    score,
    reason,
    created_at,
    health_score=None,
    confidence=None,
    market_condition=None
):
    """
    Portfolio Advisor History 저장
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO portfolio_history
        (
            mode,
            ticker,
            weight,
            score,
            reason,
            created_at,
            health_score,
            confidence,
            market_condition
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            mode,
            ticker,
            weight,
            score,
            reason,
            created_at,
            health_score,
            confidence,
            market_condition
        )
    )

    conn.commit()
    conn.close()


def get_portfolio_history(limit=50):
    """
    Portfolio History 조회
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
         SELECT
            mode,
            ticker,
            weight,
            score,
            reason,
            created_at,
            health_score,
            confidence,
            market_condition
        FROM portfolio_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    result = cursor.fetchall()

    conn.close()

    return result   



def save_ai_decision_history(
        decision,
        action,
        decision_score,
        grade,
        market_view,
        recommended_mode,
        top_etf,
        reason,
        summary,
        created_at
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO ai_decision_history
        (
            decision,
            action,
            decision_score,
            grade,
            market_view,
            recommended_mode,
            top_etf,
            reason,
            summary,
            created_at
        )

        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        """,
        (
            decision,
            action,
            decision_score,
            grade,
            market_view,
            recommended_mode,
            top_etf,
            reason,
            summary,
            created_at
        )
    )


    conn.commit()
    conn.close()




# ==============================
# Step5-3-56 AI Decision History
# ==============================

def get_ai_decision_history(limit=10):
    """
    AI Decision History 조회
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            decision,
            action,
            decision_score,
            grade,
            market_view,
            recommended_mode,
            top_etf,
            reason,
            summary,
            created_at
        FROM ai_decision_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )


    history = cursor.fetchall()


    conn.close()


    return history




def get_portfolio_analytics():
    """
    Portfolio Analytics Data 조회
    """

    conn = get_connection()
    cursor = conn.cursor()


    # 전체 History 개수
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM portfolio_history
        """
    )

    total_history = cursor.fetchone()[0]


    # 최근 Portfolio Mode
    cursor.execute(
        """
        SELECT mode
        FROM portfolio_history
        ORDER BY id DESC
        LIMIT 1
        """
    )

    latest_mode_row = cursor.fetchone()

    latest_mode = (
        latest_mode_row[0]
        if latest_mode_row
        else None
    )


    # Mode별 사용 횟수
    cursor.execute(
        """
        SELECT
            mode,
            COUNT(*)
        FROM portfolio_history
        GROUP BY mode
        ORDER BY COUNT(*) DESC
        """
    )

    mode_analysis = cursor.fetchall()


    # ETF별 평균 비중
    cursor.execute(
        """
        SELECT
            ticker,
            AVG(weight)
        FROM portfolio_history
        GROUP BY ticker
        ORDER BY AVG(weight) DESC
        """
    )

    weight_analysis = cursor.fetchall()


    conn.close()


    return {
        "total_history": total_history,
        "latest_mode": latest_mode,
        "mode_analysis": mode_analysis,
        "weight_analysis": weight_analysis
    }