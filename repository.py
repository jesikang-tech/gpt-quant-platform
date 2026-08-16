from database import get_connection


def save_etf_price(
    ticker,
    date,
    close_price
):
    """
    ETF 媛寃??곗씠?????
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
    ?뱀젙 ETF 媛寃?議고쉶
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
    ?꾩껜 媛寃??곗씠??議고쉶
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
    ?꾩껜 ETF ?뺣낫 議고쉶
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
    ETF Score ????먮뒗 ?낅뜲?댄듃
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
    ETF Score Ranking 議고쉶
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
    ETF Score ?곸꽭 議고쉶
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
    ETF Score 以묐났 ?쒓굅
    理쒖떊 ?곗씠?곕쭔 ?좎?
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
    ETF 紐⑸줉 ?꾩껜 ???
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
    ?대떦 ETF 媛寃??곗씠??議댁옱 ?щ? ?뺤씤
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
    ??λ맂 ETF ticker ?꾩껜 議고쉶
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
    ETF Score History ???
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
    ETF Ranking History ????먮뒗 ?낅뜲?댄듃
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
    ?뱀젙 ?좎쭨 Ranking 議고쉶
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
    ETF??Ranking History 議고쉶
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
    Portfolio Advisor History ???
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
    Portfolio History 議고쉶
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
    AI Decision History 議고쉶
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




def get_ai_decision_summary():
    """
    AI Decision Summary Analytics
    """

    conn = get_connection()
    cursor = conn.cursor()


    # ?꾩껜 ?먮떒 ?잛닔
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM ai_decision_history
        """
    )

    total_decisions = cursor.fetchone()[0]


    # ?됯퇏 Decision Score
    cursor.execute(
        """
        SELECT AVG(decision_score)
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        """
    )

    avg_score_row = cursor.fetchone()

    avg_score = (
        round(avg_score_row[0], 1)
        if avg_score_row[0]
        else 0
    )


    # 理쒓렐 Decision ?뺣낫
    cursor.execute(
        """
        SELECT
            decision,
            grade,
            market_view,
            top_etf
        FROM ai_decision_history
        ORDER BY id DESC
        LIMIT 1
        """
    )


    latest = cursor.fetchone()


    conn.close()


    if latest:

        latest_decision = latest[0]
        latest_grade = latest[1]
        latest_market = latest[2]
        latest_etf = latest[3]

    else:

        latest_decision = None
        latest_grade = None
        latest_market = None
        latest_etf = None



    return {

        "total_decisions":
            total_decisions,

        "average_score":
            avg_score,

        "latest_decision":
            latest_decision,

        "latest_grade":
            latest_grade,

        "market_view":
            latest_market,

        "top_etf":
            latest_etf

    }



def get_ai_decision_quality():
    """
    AI Decision Quality Analysis
    """

    conn = get_connection()
    cursor = conn.cursor()


    # 理쒓렐 Decision Score 5媛?議고쉶
    cursor.execute(
        """
        SELECT
            decision_score
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        ORDER BY id DESC
        LIMIT 5
        """
    )


    scores = [
        row[0]
        for row in cursor.fetchall()
    ]


    conn.close()


    if not scores:

        return {

            "quality_level": "UNKNOWN",
            "score_stability": "UNKNOWN",
            "recent_trend": "UNKNOWN",
            "evaluation": "No decision data"

        }


    # ?됯퇏 ?먯닔
    average_score = sum(scores) / len(scores)


    # 理쒓렐 蹂??遺꾩꽍
    if len(scores) >= 2:

        latest_score = scores[0]
        previous_score = scores[1]


        if latest_score > previous_score:

            trend = "Improving"

        elif latest_score < previous_score:

            trend = "Declining"

        else:

            trend = "Stable"

    else:

        trend = "Stable"



    # ?먯닔 ?덉젙??
    score_range = max(scores) - min(scores)


    if score_range <= 5:

        stability = "Stable"

    else:

        stability = "Variable"



    # Quality ?됯?

    if average_score >= 90:

        quality = "Excellent"

    elif average_score >= 80:

        quality = "Good"

    else:

        quality = "Needs Review"



    return {

        "quality_level":
            quality,

        "score_stability":
            stability,

        "recent_trend":
            trend,

        "evaluation":
            f"AI decision quality is {quality.lower()} with {stability.lower()} score behavior"

    }



def get_ai_decision_trend():
    """
    AI Decision Trend Analysis
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            decision_score
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        ORDER BY id DESC
        LIMIT 10
        """
    )


    scores = [
        row[0]
        for row in cursor.fetchall()
    ]


    conn.close()


    if len(scores) < 2:

        return {

            "trend": "UNKNOWN",

            "average_change": 0,

            "latest_score": (
                scores[0]
                if scores
                else None
            ),

            "previous_score": None

        }


    latest = scores[0]

    previous = scores[1]

    change = round(
        latest - previous,
        1
    )


    if change > 0:

        trend = "Improving"

    elif change < 0:

        trend = "Declining"

    else:

        trend = "Stable"


    return {

        "trend":
            trend,

        "average_change":
            change,

        "latest_score":
            latest,

        "previous_score":
            previous

    }



def get_ai_decision_chart_data(limit=20):
    """
    AI Decision Score Chart Data
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            created_at,
            decision_score
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        ORDER BY id ASC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    labels = []
    scores = []

    for created_at, score in rows:

        labels.append(created_at)

        scores.append(score)

    return {
        "labels": labels,
        "scores": scores
    }


def get_ai_decision_statistics():
    """
    AI Decision Statistics
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            MAX(decision_score),
            MIN(decision_score),
            AVG(decision_score)
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        """
    )

    result = cursor.fetchone()

    max_score = round(result[0], 1) if result[0] else 0
    min_score = round(result[1], 1) if result[1] else 0
    average_score = round(result[2], 1) if result[2] else 0

    cursor.execute(
        """
        SELECT
            AVG(decision_score)
        FROM
        (
            SELECT decision_score
            FROM ai_decision_history
            WHERE decision_score IS NOT NULL
            ORDER BY id DESC
            LIMIT 5
        )
        """
    )

    recent_average = cursor.fetchone()[0]

    recent_average = (
        round(recent_average, 1)
        if recent_average
        else 0
    )

    conn.close()

    return {

        "highest_score": max_score,

        "lowest_score": min_score,

        "average_score": average_score,

        "recent_average": recent_average,

        "score_spread": round(
            max_score - min_score,
            1
        )

    }



def get_ai_decision_performance():
    """
    AI Decision Performance Analysis
    """

    conn = get_connection()
    cursor = conn.cursor()


    # ?꾩껜 Decision 媛쒖닔
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        """
    )

    total_decisions = cursor.fetchone()[0]


    # ?됯퇏 Score
    cursor.execute(
        """
        SELECT AVG(decision_score)
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        """
    )

    average_score = cursor.fetchone()[0]


    # 理쒓퀬 / 理쒖? Score
    cursor.execute(
        """
        SELECT
            MAX(decision_score),
            MIN(decision_score)
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        """
    )

    score_range = cursor.fetchone()


    highest_score = score_range[0]

    lowest_score = score_range[1]


    # 理쒓렐 Score
    cursor.execute(
        """
        SELECT decision_score
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
        """
    )

    latest_row = cursor.fetchone()

    latest_score = latest_row[0] if latest_row else 0

    conn.close()


    if average_score:

        average_score = round(
            average_score,
            1
        )

    else:

        average_score = 0



    if highest_score:

        highest_score = round(
            highest_score,
            1
        )

    else:

        highest_score = 0



    if lowest_score:

        lowest_score = round(
            lowest_score,
            1
        )

    else:

        lowest_score = 0



    if latest_score:

        latest_score = round(
            latest_score,
            1
        )

    else:

        latest_score = 0



    # Reliability ?먮떒

    if average_score >= 85:

        reliability = "HIGH"

    elif average_score >= 70:

        reliability = "MEDIUM"

    else:

        reliability = "LOW"



    return {

        "total_decisions":
            total_decisions,

        "average_score":
            average_score,

        "highest_score":
            highest_score,

        "lowest_score":
            lowest_score,

        "latest_score":
            latest_score,

        "reliability":
            reliability

    }



def get_ai_decision_reliability():
    """
    AI Decision Reliability Analysis
    """

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT AVG(decision_score)
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        """
    )

    average_score = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT decision_score
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        ORDER BY id DESC
        LIMIT 5
        """
    )

    scores = [
        row[0]
        for row in cursor.fetchall()
    ]


    conn.close()


    if average_score is None:
        average_score = 0


    average_score = round(
        average_score,
        1
    )


    if len(scores) > 1:
        score_change = max(scores) - min(scores)

    else:
        score_change = 0


    score_change = round(
        score_change,
        1
    )


    if (
        average_score >= 85
        and score_change <= 5
    ):

        reliability_level = "HIGH"
        stability = "Excellent"
        confidence = 95


    elif average_score >= 70:

        reliability_level = "MEDIUM"
        stability = "Stable"
        confidence = 80


    else:

        reliability_level = "LOW"
        stability = "Unstable"
        confidence = 60


    return {

        "reliability_level":
            reliability_level,

        "confidence":
            confidence,

        "stability":
            stability,

        "average_score":
            average_score,

        "score_change":
            score_change,

        "message":
            "AI decision model is operating consistently"
            if reliability_level == "HIGH"
            else
            "AI decision model requires monitoring"

    }



def get_ai_adaptive_strategy():
    """
    AI Adaptive Strategy Engine

    Decision Reliability,
    Market View,
    Portfolio Condition
    湲곕컲 ?꾨왂 議곗젙
    """

    conn = get_connection()
    cursor = conn.cursor()


    # 理쒖떊 AI Decision
    cursor.execute(
        """
        SELECT
            decision_score,
            market_view,
            recommended_mode
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
        """
    )

    decision = cursor.fetchone()


    conn.close()


    if decision:

        score = decision[0]

        market_view = decision[1]

        current_mode = decision[2]


    else:

        score = 0

        market_view = "UNKNOWN"

        current_mode = "balanced"



    # 湲곕낯媛?

    strategy_mode = current_mode.upper()

    adjustment = "MAINTAIN"

    risk_control = "NORMAL"



    # Adaptive Logic


    if score >= 85:

        if market_view == "BULLISH":

            strategy_mode = "AGGRESSIVE"

            adjustment = "INCREASE_GROWTH"

            risk_control = "ACTIVE"


        elif market_view == "BEARISH":

            strategy_mode = "DEFENSIVE"

            adjustment = "REDUCE_RISK"

            risk_control = "HIGH"


        else:

            strategy_mode = "BALANCED"

            adjustment = "MAINTAIN"

            risk_control = "NORMAL"


    elif score >= 70:

        strategy_mode = "BALANCED"

        adjustment = "MONITOR"

        risk_control = "NORMAL"


    else:

        strategy_mode = "DEFENSIVE"

        adjustment = "REDUCE_RISK"

        risk_control = "HIGH"



    return {

        "strategy_mode":
            strategy_mode,

        "adjustment":
            adjustment,

        "confidence":
            score,

        "risk_control":
            risk_control,

        "market_view":
            market_view,

        "message":
            "Current strategy is optimized for market condition"

    }



def get_ai_rebalance_recommendation():
    """
    AI Portfolio Auto Rebalance Recommendation Engine
    """

    conn = get_connection()
    cursor = conn.cursor()


    # 理쒖떊 Adaptive Strategy 議고쉶

    cursor.execute(
        """
        SELECT
            decision_score,
            market_view,
            recommended_mode,
            top_etf
        FROM ai_decision_history
        WHERE decision_score IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
        """
    )


    decision = cursor.fetchone()


    conn.close()


    if decision:

        score = decision[0]

        market_view = decision[1]

        mode = decision[2]

        top_etf = decision[3]


    else:

        score = 0

        market_view = "UNKNOWN"

        mode = "balanced"

        top_etf = None



    changes = []


    rebalance_action = "HOLD"


    confidence = score



    # Rebalance Logic


    if score >= 85:


        if market_view == "BULLISH":

            rebalance_action = "ADJUST"


            changes.append(
                {
                    "ticker": top_etf,
                    "action": "INCREASE_WEIGHT",
                    "reason":
                    "Strong market condition and high AI confidence"
                }
            )


        elif market_view == "BEARISH":

            rebalance_action = "ADJUST"


            changes.append(
                {
                    "ticker": "CASH",
                    "action": "INCREASE_WEIGHT",
                    "reason":
                    "Risk reduction based on market weakness"
                }
            )


        else:

            rebalance_action = "MAINTAIN"


            changes.append(
                {
                    "ticker": top_etf,
                    "action": "KEEP_WEIGHT",
                    "reason":
                    "Balanced market condition"
                }
            )


    else:


        rebalance_action = "REDUCE_RISK"


        changes.append(
            {
                "ticker": "CASH",
                "action": "INCREASE_WEIGHT",
                "reason":
                "AI confidence below optimal level"
            }
        )



    return {

        "rebalance_action":
            rebalance_action,

        "confidence":
            confidence,

         "rebalance_score":
            confidence,

        "market_view":
            market_view,

        "recommended_mode":
            mode,

        "changes":
            changes,

        "message":
            "AI portfolio allocation recommendation generated"

    }


def get_ai_portfolio_optimization():
    """
    AI Portfolio Self Optimization Engine

    Current allocation 遺꾩꽍 ??
    Target allocation ?쒖븞
    """

    conn = get_connection()
    cursor = conn.cursor()


    # 理쒓렐 Portfolio History 議고쉶

    cursor.execute(
        """
        SELECT
            ticker,
            weight
        FROM portfolio_history
        WHERE id IN
        (
            SELECT MAX(id)
            FROM portfolio_history
            GROUP BY ticker
        )
        ORDER BY weight DESC
        """
    )


    portfolio = cursor.fetchall()


    conn.close()


    optimized_allocation = []


    if portfolio:


        total_weight = sum(
            item[1]
            for item in portfolio
        )


        for ticker, weight in portfolio:


            current = weight


            target = weight


            # AI Optimization Rule

            if weight >= 40:

                target = weight - 5


            elif weight <= 10:

                target = weight + 5



            optimized_allocation.append(
                {
                    "ticker": ticker,

                    "current_weight":
                        current,

                    "target_weight":
                        target
                }
            )


    optimization_score = 0

    if optimized_allocation:

        optimization_score = 100

        changed = any(
            item["current_weight"]
            != item["target_weight"]
            for item in optimized_allocation
        )

        if not changed:
            optimization_score = 80



    return {

        "optimization_status":
            "COMPLETED",

        "optimization_score":
            optimization_score,    

        "optimized_allocation":
            optimized_allocation,

        "message":
            "AI portfolio optimization completed"

    }


def get_portfolio_analytics():
    """
    Portfolio Analytics Data 議고쉶
    """

    conn = get_connection()
    cursor = conn.cursor()


    # ?꾩껜 History 媛쒖닔
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM portfolio_history
        """
    )

    total_history = cursor.fetchone()[0]


    # 理쒓렐 Portfolio Mode
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


    # Mode蹂??ъ슜 ?잛닔
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


    # ETF蹂??됯퇏 鍮꾩쨷
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



def get_latest_etf_scores(limit=30):
    """
    理쒖떊 ETF Score 議고쉶
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            ticker,
            final_score,
            return_score,
            trend_score,
            slope_score
        FROM etf_scores
        ORDER BY final_score DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows



def get_etf_score(ticker):
    """
    ?뱀젙 ETF Score 議고쉶
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            ticker,
            final_score,
            return_score,
            trend_score,
            slope_score
        FROM etf_scores
        WHERE ticker=?
        """,
        (ticker,)
    )

    row = cursor.fetchone()

    conn.close()

    return row


# ==============================
# Step6-3 AI Decision Outcome History
# ==============================

def save_ai_decision_outcome_history(
    decision,
    action,
    strategy,
    confidence_score,
    intelligence_score,
    validation_score,
    governance_score,
    execution_score,
    lifecycle_score,
    operational_score,
    orchestration_score,
    integrated_score,
    market_view,
    risk_level,
    outcome_status,
    snapshot_status,
    snapshot_purpose,
    outcome_score,
    outcome_grade,
    decision_effectiveness,
    strategy_effectiveness,
    market_response,
    portfolio_response,
    learning_status,
    feedback_state,
    adaptive_learning_required,
    reassessment_required,
    reassessment_status,
    created_at
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ai_decision_outcome_history
        (
            decision,
            action,
            strategy,
            confidence_score,
            intelligence_score,
            validation_score,
            governance_score,
            execution_score,
            lifecycle_score,
            operational_score,
            orchestration_score,
            integrated_score,
            market_view,
            risk_level,
            outcome_status,
            snapshot_status,
            snapshot_purpose,
            outcome_score,
            outcome_grade,
            decision_effectiveness,
            strategy_effectiveness,
            market_response,
            portfolio_response,
            learning_status,
            feedback_state,
            adaptive_learning_required,
            reassessment_required,
            reassessment_status,
            created_at
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            decision,
            action,
            strategy,
            confidence_score,
            intelligence_score,
            validation_score,
            governance_score,
            execution_score,
            lifecycle_score,
            operational_score,
            orchestration_score,
            integrated_score,
            market_view,
            risk_level,
            outcome_status,
            snapshot_status,
            snapshot_purpose,
            outcome_score,
            outcome_grade,
            decision_effectiveness,
            strategy_effectiveness,
            market_response,
            portfolio_response,
            learning_status,
            feedback_state,
            adaptive_learning_required,
            reassessment_required,
            reassessment_status,
            created_at
        )
    )

    conn.commit()

    history_id = cursor.lastrowid

    conn.close()

    return history_id


def update_ai_decision_outcome_history(
    history_id,
    outcome_status,
    outcome_score,
    outcome_grade,
    decision_effectiveness,
    strategy_effectiveness,
    market_response,
    portfolio_response,
    learning_status,
    feedback_state,
    adaptive_learning_required,
    reassessment_required,
    reassessment_status
):
    """
    Update AI Decision Outcome History evaluation result.
    Step6-4
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE ai_decision_outcome_history
        SET
            outcome_status = ?,
            outcome_score = ?,
            outcome_grade = ?,
            decision_effectiveness = ?,
            strategy_effectiveness = ?,
            market_response = ?,
            portfolio_response = ?,
            learning_status = ?,
            feedback_state = ?,
            adaptive_learning_required = ?,
            reassessment_required = ?,
            reassessment_status = ?
        WHERE id = ?
        """,
        (
            outcome_status,
            outcome_score,
            outcome_grade,
            decision_effectiveness,
            strategy_effectiveness,
            market_response,
            portfolio_response,
            learning_status,
            feedback_state,
            adaptive_learning_required,
            reassessment_required,
            reassessment_status,
            history_id
        )
    )

    conn.commit()

    updated_count = cursor.rowcount

    conn.close()

    return updated_count


def get_ai_decision_outcome_history(limit=10):
    """
    AI Decision Outcome History 議고쉶
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            decision,
            action,
            strategy,
            confidence_score,
            intelligence_score,
            validation_score,
            governance_score,
            execution_score,
            lifecycle_score,
            operational_score,
            orchestration_score,
            integrated_score,
            market_view,
            risk_level,
            outcome_status,
            snapshot_status,
            snapshot_purpose,
            outcome_score,
            outcome_grade,
            decision_effectiveness,
            strategy_effectiveness,
            market_response,
            portfolio_response,
            learning_status,
            feedback_state,
            adaptive_learning_required,
            reassessment_required,
            reassessment_status,
            created_at
        FROM ai_decision_outcome_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==============================
# AI Decision Portfolio Snapshot
# Phase 6
# Step6-9-B
# ==============================

def save_ai_decision_portfolio_snapshot(
    history_id,
    portfolio,
    created_at
):
    """
    Save the portfolio snapshot associated with an AI decision outcome.

    Step6-10-A
    """

    conn = get_connection()
    cursor = conn.cursor()

    saved_count = 0

    for item in portfolio:

        ticker = item.get("ticker")

        if not ticker:
            continue

        weight = item.get(
            "weight",
            0
        )

        reference_price = item.get(
            "reference_price"
        )

        reference_price_date = item.get(
            "reference_price_date"
        )

        price_row = None

        if reference_price is None:
            price_row = cursor.execute(
                """
                SELECT
                    date,
                    close_price
                FROM etf_prices
                WHERE ticker = ?
                ORDER BY date DESC
                LIMIT 1
                """,
                (
                    ticker,
                )
            ).fetchone()

            if price_row:
                reference_price_date = price_row[0]
                reference_price = price_row[1]

        elif reference_price_date is None:
            price_row = cursor.execute(
                """
                SELECT
                    date
                FROM etf_prices
                WHERE ticker = ?
                  AND close_price = ?
                ORDER BY date DESC
                LIMIT 1
                """,
                (
                    ticker,
                    reference_price
                )
            ).fetchone()

            if price_row:
                reference_price_date = price_row[0]

        cursor.execute(
            """
            INSERT INTO ai_decision_portfolio_snapshot
            (
                history_id,
                ticker,
                weight,
                reference_price,
                created_at,
                reference_price_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                history_id,
                ticker,
                weight,
                reference_price,
                created_at,
                reference_price_date
            )
        )

        saved_count += 1

    conn.commit()
    conn.close()

    return saved_count


def get_ai_decision_portfolio_snapshot(
    history_id
):
    """
    Retrieve the portfolio snapshot associated
    with an AI decision outcome.

    Step6-10-B
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            history_id,
            ticker,
            weight,
            reference_price,
            created_at,
            reference_price_date
        FROM ai_decision_portfolio_snapshot
        WHERE history_id = ?
        ORDER BY id ASC
        """,
        (
            history_id,
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

def mark_ai_decision_portfolio_outcome_evaluated(
    history_id
):
    """
    Mark AI Decision Outcome History
    as EVALUATED after portfolio outcome evaluation.

    Step6-10-E
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE ai_decision_outcome_history
        SET
            outcome_status = ?
        WHERE id = ?
        """,
        (
            "EVALUATED",
            history_id
        )
    )

    conn.commit()

    updated_count = cursor.rowcount

    conn.close()

    return updated_count

def update_ai_decision_portfolio_evaluation(
    history_id,
    portfolio_return,
    portfolio_evaluation_date
):
    """
    Save evaluated portfolio performance
    into AI Decision Outcome History.

    Step6-10-D
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE ai_decision_outcome_history
        SET
            portfolio_return = ?,
            portfolio_evaluation_date = ?
        WHERE id = ?
        """,
        (
            portfolio_return,
            portfolio_evaluation_date,
            history_id
        )
    )

    conn.commit()

    updated_count = cursor.rowcount

    conn.close()

    return updated_count

# ==============================
# AI Decision Portfolio Outcome Evaluation
# Phase 6
# Step6-10-C
# ==============================

def evaluate_ai_decision_portfolio_snapshot(
    history_id,
    evaluation_date=None
):
    """
    Evaluate a stored AI decision portfolio snapshot
    against a later ETF price.

    Step6-10-C

    No future performance is invented.
    If no price exists after the snapshot reference date,
    the evaluation remains in a waiting state.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            ticker,
            weight,
            reference_price,
            reference_price_date
        FROM ai_decision_portfolio_snapshot
        WHERE history_id = ?
        ORDER BY id ASC
        """,
        (
            history_id,
        )
    )

    snapshot_rows = cursor.fetchall()

    if not snapshot_rows:
        conn.close()

        return {
            "evaluation_status": "WAITING_FOR_SNAPSHOT",
            "outcome_status": "PENDING",
            "history_id": history_id,
            "evaluation_date": evaluation_date,
            "portfolio_return": None,
            "positions": []
        }

    positions = []
    weighted_return = 0.0
    evaluated_weight = 0.0
    pending_positions = 0
    last_evaluation_date = evaluation_date

    for row in snapshot_rows:

        ticker = row[0]
        weight = float(row[1] or 0.0)
        reference_price = row[2]
        reference_price_date = row[3]

        if ticker == "CASH":
            positions.append({
                "ticker": ticker,
                "weight": weight,
                "reference_price": reference_price,
                "reference_price_date": reference_price_date,
                "evaluation_price": None,
                "evaluation_date": evaluation_date,
                "return_pct": 0.0,
                "status": "EVALUATED"
            })

            evaluated_weight += weight
            continue

        if reference_price is None or reference_price_date is None:
            pending_positions += 1

            positions.append({
                "ticker": ticker,
                "weight": weight,
                "reference_price": reference_price,
                "reference_price_date": reference_price_date,
                "evaluation_price": None,
                "evaluation_date": evaluation_date,
                "return_pct": None,
                "status": "WAITING_FOR_REFERENCE_PRICE"
            })

            continue

        if evaluation_date is None:
            price_row = cursor.execute(
                """
                SELECT
                    date,
                    close_price
                FROM etf_prices
                WHERE ticker = ?
                  AND date > ?
                ORDER BY date ASC
                LIMIT 1
                """,
                (
                    ticker,
                    reference_price_date
                )
            ).fetchone()
        else:
            price_row = cursor.execute(
                """
                SELECT
                    date,
                    close_price
                FROM etf_prices
                WHERE ticker = ?
                  AND date > ?
                  AND date <= ?
                ORDER BY date DESC
                LIMIT 1
                """,
                (
                    ticker,
                    reference_price_date,
                    evaluation_date
                )
            ).fetchone()

        if not price_row:
            pending_positions += 1

            positions.append({
                "ticker": ticker,
                "weight": weight,
                "reference_price": reference_price,
                "reference_price_date": reference_price_date,
                "evaluation_price": None,
                "evaluation_date": evaluation_date,
                "return_pct": None,
                "status": "WAITING_FOR_OUTCOME"
            })

            continue

        actual_date = price_row[0]
        evaluation_price = float(price_row[1])
        if last_evaluation_date is None:
            last_evaluation_date = actual_date

        return_pct = (
            (evaluation_price - float(reference_price))
            / float(reference_price)
        ) * 100.0

        weighted_return += (
            return_pct * (weight / 100.0)
        )

        evaluated_weight += weight

        positions.append({
            "ticker": ticker,
            "weight": weight,
            "reference_price": float(reference_price),
            "reference_price_date": reference_price_date,
            "evaluation_price": evaluation_price,
            "evaluation_date": actual_date,
            "return_pct": round(return_pct, 4),
            "status": "EVALUATED"
        })

    conn.close()

    if pending_positions > 0:
        return {
            "evaluation_status": "WAITING_FOR_OUTCOME",
            "outcome_status": "PENDING",
            "history_id": history_id,
            "evaluation_date": evaluation_date,
            "portfolio_return": None,
            "evaluated_weight": round(evaluated_weight, 4),
            "pending_positions": pending_positions,
            "positions": positions
        }

    update_ai_decision_portfolio_evaluation(
        history_id=history_id,
        portfolio_return=round(weighted_return, 4),
        portfolio_evaluation_date=last_evaluation_date
    )
    mark_ai_decision_portfolio_outcome_evaluated(
        history_id=history_id
    )

    return {
        "evaluation_status": "EVALUATED",
        "outcome_status": "EVALUATED",
        "history_id": history_id,
        "evaluation_date": evaluation_date,
        "portfolio_return": round(weighted_return, 4),
        "evaluated_weight": round(evaluated_weight, 4),
        "pending_positions": 0,
        "positions": positions
    }
