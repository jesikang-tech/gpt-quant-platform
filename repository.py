from datetime import datetime
import json
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

def enrich_portfolio_reference_prices(
    portfolio
):
    """
    Enrich portfolio positions with missing reference
    price/date values from the latest available ETF price.

    Contract:
    - Preserve ticker and weight.
    - Preserve existing reference price/date.
    - CASH does not require reference price/date.
    - Resolve only missing values from etf_prices.
    - Do not write to the database.
    """

    if not isinstance(portfolio, list):
        raise ValueError("PORTFOLIO_NOT_LIST")

    enriched_portfolio = []

    conn = get_connection()
    cursor = conn.cursor()

    try:
        for item in portfolio:

            if not isinstance(item, dict):
                raise ValueError("INVALID_POSITION")

            enriched_item = item.copy()

            ticker = enriched_item.get("ticker")

            if not ticker:
                raise ValueError("MISSING_TICKER")

            if ticker == "CASH":
                enriched_portfolio.append(
                    enriched_item
                )
                continue

            reference_price = (
                enriched_item.get("reference_price")
            )

            reference_price_date = (
                enriched_item.get("reference_price_date")
            )

            if (
                reference_price is None
                or reference_price_date is None
            ):

                price_row = cursor.execute(
                    """
                    SELECT date, close_price
                    FROM etf_prices
                    WHERE ticker = ?
                    ORDER BY date DESC
                    LIMIT 1
                    """,
                    (ticker,),
                ).fetchone()

                if price_row:

                    if reference_price is None:
                        reference_price = (
                            price_row[1]
                        )

                    if reference_price_date is None:
                        reference_price_date = (
                            price_row[0]
                        )

            if reference_price is not None:
                enriched_item[
                    "reference_price"
                ] = reference_price

            if reference_price_date is not None:
                enriched_item[
                    "reference_price_date"
                ] = reference_price_date

            enriched_portfolio.append(
                enriched_item
            )

        return enriched_portfolio

    finally:
        conn.close()


def validate_portfolio_snapshot_input(
    portfolio
):
    """
    Validate Portfolio Snapshot input before persistence.

    Production Hardening:
    - portfolio must be a non-empty list
    - weights must be numeric and non-negative
    - total weight must equal 100
    - tickers must be unique
    - non-CASH positions require reference price/date
    - CASH does not require reference price/date
    """

    if not isinstance(portfolio, list):
        raise ValueError("PORTFOLIO_NOT_LIST")

    if not portfolio:
        raise ValueError("EMPTY_PORTFOLIO")

    tickers = set()
    total_weight = 0.0

    for item in portfolio:
        if not isinstance(item, dict):
            raise ValueError("INVALID_POSITION")

        ticker = item.get("ticker")

        if not ticker:
            raise ValueError("MISSING_TICKER")

        if ticker in tickers:
            raise ValueError("DUPLICATE_TICKER")

        tickers.add(ticker)

        weight = item.get("weight")

        if weight is None:
            raise ValueError("MISSING_WEIGHT")

        try:
            weight = float(weight)
        except (TypeError, ValueError):
            raise ValueError("INVALID_WEIGHT")

        if weight < 0:
            raise ValueError("NEGATIVE_WEIGHT")

        total_weight += weight

        if ticker != "CASH":
            if (
                item.get("reference_price") is None
                or item.get("reference_price_date") is None
            ):
                raise ValueError(
                    "MISSING_REFERENCE_PRICE"
                )

    if abs(total_weight - 100.0) > 0.0001:
        raise ValueError(
            "INVALID_TOTAL_WEIGHT"
        )

    return True


def save_ai_decision_audit_event(
    event_type,
    event_time,
    source,
    status=None,
    decision_history_id=None,
    outcome_history_id=None,
    correlation_key=None,
    details=None,
    cursor=None,
):
    """
    Persist one AI Decision Audit Event.

    The caller may provide an existing cursor so the event is
    persisted inside the caller's transaction boundary.
    """

    if cursor is None:
        conn = get_connection()
        cursor = conn.cursor()
        owns_connection = True
    else:
        conn = None
        owns_connection = False

    try:
        if not event_type:
            raise ValueError("event_type is required")
        if not event_time:
            raise ValueError("event_time is required")
        if not source:
            raise ValueError("source is required")

        if outcome_history_id is not None:
            default_correlation_key = f"outcome:{outcome_history_id}"
        elif decision_history_id is not None:
            default_correlation_key = f"decision:{decision_history_id}"
        else:
            default_correlation_key = f"{event_type}:unbound"

        correlation_key = correlation_key or default_correlation_key

        audit_event_id = (
            f"{event_type}:{correlation_key}:{event_time}"
        )

        cursor.execute(
            """
            INSERT INTO audit_event
            (
                audit_event_id,
                event_type,
                event_time,
                source,
                status,
                decision_history_id,
                outcome_history_id,
                correlation_key,
                details
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                audit_event_id,
                event_type,
                event_time,
                source,
                status,
                decision_history_id,
                outcome_history_id,
                correlation_key,
                json.dumps(
                    details or {},
                    ensure_ascii=False,
                    sort_keys=True,
                ),
            ),
        )

        if owns_connection:
            conn.commit()

        return {
            "audit_event_id": audit_event_id,
            "event_type": event_type,
            "event_time": event_time,
            "source": source,
            "status": status,
            "decision_history_id": decision_history_id,
            "outcome_history_id": outcome_history_id,
            "correlation_key": correlation_key,
        }

    except Exception:
        if owns_connection:
            conn.rollback()
        raise

    finally:
        if owns_connection:
            conn.close()


def save_ai_decision_outcome_with_portfolio_transaction(
    history_kwargs,
    portfolio,
    created_at
):
    """
    Atomically persist AI Decision Outcome History and
    Portfolio Snapshot.

    Production Hardening:
    History INSERT and Portfolio Snapshot INSERT are
    committed as one transaction. Any failure rolls back
    the full creation transaction.
    """

    portfolio = enrich_portfolio_reference_prices(
        portfolio
    )

    validate_portfolio_snapshot_input(
        portfolio
    )

    conn = get_connection()
    cursor = conn.cursor()

    try:
        history_columns = [
            "decision",
            "action",
            "strategy",
            "confidence_score",
            "intelligence_score",
            "validation_score",
            "governance_score",
            "execution_score",
            "lifecycle_score",
            "operational_score",
            "orchestration_score",
            "integrated_score",
            "market_view",
            "risk_level",
            "outcome_status",
            "snapshot_status",
            "snapshot_purpose",
            "outcome_score",
            "outcome_grade",
            "decision_effectiveness",
            "strategy_effectiveness",
            "market_response",
            "portfolio_response",
            "learning_status",
            "feedback_state",
            "adaptive_learning_required",
            "reassessment_required",
            "reassessment_status",
            "created_at",
            "execution_status",
            "execution_authorization",
            "execution_readiness",
            "certification_status",
            "monitoring_status",
            "feedback_status",
        ]

        history_values = [
            history_kwargs.get(column)
            for column in history_columns
        ]

        columns_sql = ", ".join(history_columns)
        placeholders = ", ".join(
            "?" for _ in history_columns
        )

        cursor.execute(
            f"""
            INSERT INTO ai_decision_outcome_history
            ({columns_sql})
            VALUES ({placeholders})
            """,
            tuple(history_values),
        )

        history_id = cursor.lastrowid
        saved_count = 0

        for item in portfolio:
            ticker = item.get("ticker")

            if not ticker:
                continue

            weight = item.get("weight", 0)
            reference_price = item.get("reference_price")
            reference_price_date = item.get(
                "reference_price_date"
            )

            if reference_price is None:
                price_row = cursor.execute(
                    """
                    SELECT date, close_price
                    FROM etf_prices
                    WHERE ticker = ?
                    ORDER BY date DESC
                    LIMIT 1
                    """,
                    (ticker,),
                ).fetchone()

                if price_row:
                    reference_price_date = price_row[0]
                    reference_price = price_row[1]

            elif reference_price_date is None:
                price_row = cursor.execute(
                    """
                    SELECT date
                    FROM etf_prices
                    WHERE ticker = ?
                      AND close_price = ?
                    ORDER BY date DESC
                    LIMIT 1
                    """,
                    (
                        ticker,
                        reference_price,
                    ),
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
                    reference_price_date,
                ),
            )

            saved_count += 1

        save_ai_decision_audit_event(
            event_type="SNAPSHOT_PERSISTED",
            event_time=created_at,
            source="outcome_persistence",
            status="SUCCESS",
            outcome_history_id=history_id,
            correlation_key=f"outcome:{history_id}",
            details={
                "snapshot_count": saved_count,
                "snapshot_status": history_kwargs.get(
                    "snapshot_status",
                    "COLLECTED",
                ),
                "snapshot_purpose": history_kwargs.get(
                    "snapshot_purpose",
                    "FUTURE_OUTCOME_EVALUATION",
                ),
            },
            cursor=cursor,
        )

        save_ai_decision_audit_event(
            event_type="OUTCOME_PERSISTED",
            event_time=created_at,
            source="outcome_persistence",
            status=history_kwargs.get(
                "outcome_status",
                "PENDING",
            ),
            outcome_history_id=history_id,
            correlation_key=f"outcome:{history_id}",
            details={
                "decision": history_kwargs.get(
                    "decision",
                    "UNKNOWN",
                ),
                "action": history_kwargs.get(
                    "action",
                    "REVIEW",
                ),
                "strategy": history_kwargs.get(
                    "strategy",
                    "UNKNOWN",
                ),
                "snapshot_status": history_kwargs.get(
                    "snapshot_status",
                    "COLLECTED",
                ),
                "snapshot_purpose": history_kwargs.get(
                    "snapshot_purpose",
                    "FUTURE_OUTCOME_EVALUATION",
                ),
            },
            cursor=cursor,
        )

        conn.commit()

        return {
            "history_id": history_id,
            "snapshot_count": saved_count,
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

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
    created_at,
    execution_status,
    execution_authorization,
    execution_readiness,
    certification_status,
    monitoring_status,
    feedback_status
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
            created_at,
            execution_status,
            execution_authorization,
            execution_readiness,
            certification_status,
            monitoring_status,
            feedback_status
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?
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
            created_at,
            execution_status,
            execution_authorization,
            execution_readiness,
            certification_status,
            monitoring_status,
            feedback_status
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


def get_ai_decision_outcome_history_by_id(history_id):
    """
    Retrieve one AI Decision Outcome History record by ID.

    Step6-10-F-4
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
            created_at,
            portfolio_return,
            portfolio_evaluation_date,
            execution_status,
            execution_authorization,
            execution_readiness,
            certification_status,
            monitoring_status,
            feedback_status
        FROM ai_decision_outcome_history
        WHERE id = ?
        LIMIT 1
        """,
        (
            history_id,
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row



def get_ai_decision_audit_events(
    outcome_history_id=None,
    correlation_key=None,
    limit=50,
):
    """
    Retrieve AI Decision Audit Events.

    Step6-10-I-17

    Read-only audit event boundary.
    Events are returned in chronological order.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if outcome_history_id is None and correlation_key is None:
            raise ValueError(
                "outcome_history_id or correlation_key is required"
            )

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            raise ValueError("limit must be an integer")

        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        where_clauses = []
        params = []

        if outcome_history_id is not None:
            where_clauses.append(
                "outcome_history_id = ?"
            )
            params.append(outcome_history_id)

        if correlation_key is not None:
            where_clauses.append(
                "correlation_key = ?"
            )
            params.append(correlation_key)

        cursor.execute(
            f"""
            SELECT
                id,
                audit_event_id,
                event_type,
                event_time,
                source,
                status,
                outcome_history_id,
                correlation_key,
                details
            FROM audit_event
            WHERE {" AND ".join(where_clauses)}
            ORDER BY event_time ASC, id ASC
            LIMIT ?
            """,
            (
                *params,
                limit,
            ),
        )

        return cursor.fetchall()

    finally:
        conn.close()

def get_ai_decision_audit_lifecycle_timeline(
    outcome_history_id=None,
    correlation_key=None,
    limit=100,
):
    """
    Project persisted AI Decision Audit Events into a
    lifecycle timeline.

    Step6-10-I-18

    Read-only projection boundary.
    No business state or audit event is created or modified.
    """

    rows = get_ai_decision_audit_events(
        outcome_history_id=outcome_history_id,
        correlation_key=correlation_key,
        limit=limit,
    )

    timeline = []

    for row in rows:
        details = row[8]

        if isinstance(details, str):
            try:
                details = json.loads(details)
            except (TypeError, ValueError):
                details = {}

        timeline.append(
            {
                "id": row[0],
                "audit_event_id": row[1],
                "event_type": row[2],
                "event_time": row[3],
                "source": row[4],
                "status": row[5],
                "outcome_history_id": row[6],
                "correlation_key": row[7],
                "details": details,
            }
        )

    return timeline

def get_ai_decision_audit_lifecycle_completeness(
    outcome_history_id=None,
    correlation_key=None,
    limit=100,
):
    """
    Assess persisted AI Decision Audit lifecycle completeness.

    Step6-10-I-20

    Read-only projection boundary.
    Completeness is determined only from persisted audit events.
    No synthetic event inference or business-state mutation occurs.
    """

    expected_event_types = [
        "OUTCOME_EVALUATION_STARTED",
        "OUTCOME_EVALUATED",
        "LEARNING_SIGNAL_GENERATED",
        "REASSESSMENT_REQUIRED",
        "ADAPTIVE_STRATEGY_GENERATED",
    ]

    timeline = get_ai_decision_audit_lifecycle_timeline(
        outcome_history_id=outcome_history_id,
        correlation_key=correlation_key,
        limit=limit,
    )

    present_event_types = []
    for event in timeline:
        event_type = event.get("event_type")
        if (
            event_type in expected_event_types
            and event_type not in present_event_types
        ):
            present_event_types.append(event_type)

    missing_event_types = [
        event_type
        for event_type in expected_event_types
        if event_type not in present_event_types
    ]

    if not present_event_types:
        lifecycle_status = "EMPTY"
    elif not missing_event_types:
        lifecycle_status = "COMPLETE"
    else:
        lifecycle_status = "PARTIAL"

    resolved_outcome_history_id = outcome_history_id
    resolved_correlation_key = correlation_key

    if timeline:
        if resolved_outcome_history_id is None:
            resolved_outcome_history_id = timeline[0].get(
                "outcome_history_id"
            )
        if resolved_correlation_key is None:
            resolved_correlation_key = timeline[0].get(
                "correlation_key"
            )

    return {
        "outcome_history_id":
            resolved_outcome_history_id,
        "correlation_key":
            resolved_correlation_key,
        "lifecycle_status":
            lifecycle_status,
        "expected_event_types":
            expected_event_types,
        "present_event_types":
            present_event_types,
        "missing_event_types":
            missing_event_types,
        "event_count":
            len(timeline),
    }

def get_ai_decision_outcome_learning_summary():
    """
    Aggregate AI Decision Outcome Learning status.

    Step6-10-F-11-D

    Pending outcomes are excluded from outcome-score
    and portfolio-return averages.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM ai_decision_outcome_history
        """
    )
    total_outcomes = cursor.fetchone()[0] or 0

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM ai_decision_outcome_history
        WHERE outcome_status = 'EVALUATED'
        """
    )
    evaluated_outcomes = cursor.fetchone()[0] or 0

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM ai_decision_outcome_history
        WHERE outcome_status = 'PENDING'
        """
    )
    pending_outcomes = cursor.fetchone()[0] or 0

    cursor.execute(
        """
        SELECT AVG(outcome_score)
        FROM ai_decision_outcome_history
        WHERE outcome_status = 'EVALUATED'
          AND outcome_score IS NOT NULL
        """
    )
    average_outcome_score = cursor.fetchone()[0]

    if average_outcome_score is not None:
        average_outcome_score = round(
            average_outcome_score,
            2
        )

    cursor.execute(
        """
        SELECT AVG(portfolio_return)
        FROM ai_decision_outcome_history
        WHERE outcome_status = 'EVALUATED'
          AND portfolio_return IS NOT NULL
        """
    )
    average_portfolio_return = cursor.fetchone()[0]

    if average_portfolio_return is not None:
        average_portfolio_return = round(
            average_portfolio_return,
            4
        )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM ai_decision_outcome_history
        WHERE outcome_status = 'EVALUATED'
          AND portfolio_return IS NOT NULL
          AND portfolio_return > 0
        """
    )
    positive_outcomes = cursor.fetchone()[0] or 0

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM ai_decision_outcome_history
        WHERE outcome_status = 'EVALUATED'
          AND portfolio_return IS NOT NULL
          AND portfolio_return < 0
        """
    )
    negative_outcomes = cursor.fetchone()[0] or 0

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM ai_decision_outcome_history
        WHERE adaptive_learning_required = 1
        """
    )
    adaptive_learning_required = cursor.fetchone()[0] or 0

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM ai_decision_outcome_history
        WHERE reassessment_required = 1
        """
    )
    reassessment_required = cursor.fetchone()[0] or 0

    cursor.execute(
        """
        SELECT learning_status, COUNT(*)
        FROM ai_decision_outcome_history
        GROUP BY learning_status
        ORDER BY COUNT(*) DESC
        """
    )

    learning_status_distribution = {
        row[0] if row[0] is not None else "UNKNOWN": row[1]
        for row in cursor.fetchall()
    }

    cursor.execute(
        """
        SELECT feedback_state, COUNT(*)
        FROM ai_decision_outcome_history
        GROUP BY feedback_state
        ORDER BY COUNT(*) DESC
        """
    )

    feedback_state_distribution = {
        row[0] if row[0] is not None else "UNKNOWN": row[1]
        for row in cursor.fetchall()
    }

    cursor.execute(
        """
        SELECT outcome_grade, COUNT(*)
        FROM ai_decision_outcome_history
        WHERE outcome_status = 'EVALUATED'
        GROUP BY outcome_grade
        ORDER BY COUNT(*) DESC
        """
    )

    outcome_grade_distribution = {
        row[0] if row[0] is not None else "UNKNOWN": row[1]
        for row in cursor.fetchall()
    }

    conn.close()

    return {
        "total_outcomes": total_outcomes,
        "evaluated_outcomes": evaluated_outcomes,
        "pending_outcomes": pending_outcomes,
        "average_outcome_score": average_outcome_score,
        "average_portfolio_return": average_portfolio_return,
        "positive_outcomes": positive_outcomes,
        "negative_outcomes": negative_outcomes,
        "adaptive_learning_required": adaptive_learning_required,
        "reassessment_required": reassessment_required,
        "learning_status_distribution":
            learning_status_distribution,
        "feedback_state_distribution":
            feedback_state_distribution,
        "outcome_grade_distribution":
            outcome_grade_distribution
    }


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
            created_at,
            portfolio_return,
            portfolio_evaluation_date,
            execution_status,
            execution_authorization,
            execution_readiness,
            certification_status,
            monitoring_status,
            feedback_status
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

def get_ai_decision_history_snapshot_lifecycle():
    """
    Read-only classification of AI Decision Outcome History
    and Portfolio Snapshot lifecycle state.

    Production Hardening:
    No database mutation is performed.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            h.id,
            h.outcome_status,
            COUNT(s.id) AS snapshot_count
        FROM ai_decision_outcome_history h
        LEFT JOIN ai_decision_portfolio_snapshot s
            ON s.history_id = h.id
        GROUP BY
            h.id,
            h.outcome_status
        ORDER BY h.id
        """
    )

    rows = cursor.fetchall()

    result = []

    for row in rows:
        history_id = row[0]
        outcome_status = row[1]
        snapshot_count = int(row[2] or 0)

        if outcome_status == "PENDING":
            if snapshot_count > 0:
                classification = (
                    "ACTIVE_OUTCOME_TRACKING"
                )
            else:
                classification = (
                    "LEGACY_ORPHAN_CANDIDATE"
                )

        elif outcome_status == "EVALUATED":
            if snapshot_count > 0:
                classification = "COMPLETED"
            else:
                classification = (
                    "LEGACY_EVALUATED_CANDIDATE"
                )

        else:
            classification = "UNKNOWN"

        result.append(
            {
                "history_id": history_id,
                "outcome_status": outcome_status,
                "snapshot_count": snapshot_count,
                "classification": classification,
            }
        )

    conn.close()

    return result


def get_ai_decision_history_snapshot_retention():
    """
    Read-only retention classification for AI Decision
    Outcome History and Portfolio Snapshot lifecycle.

    Production Hardening:
    No database mutation is performed.
    """

    REVIEW_DAYS = 7

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            h.id,
            h.created_at,
            h.outcome_status,
            COUNT(s.id) AS snapshot_count
        FROM ai_decision_outcome_history h
        LEFT JOIN ai_decision_portfolio_snapshot s
            ON s.history_id = h.id
        GROUP BY
            h.id,
            h.created_at,
            h.outcome_status
        ORDER BY h.created_at ASC
        """
    )

    rows = cursor.fetchall()

    now = datetime.now().astimezone()
    result = []

    for row in rows:
        history_id = row[0]
        created_at = row[1]
        outcome_status = row[2]
        snapshot_count = int(row[3] or 0)

        if outcome_status == "PENDING":
            if snapshot_count > 0:
                lifecycle = (
                    "ACTIVE_OUTCOME_TRACKING"
                )
            else:
                lifecycle = (
                    "LEGACY_ORPHAN_CANDIDATE"
                )

        elif outcome_status == "EVALUATED":
            if snapshot_count > 0:
                lifecycle = "COMPLETED"
            else:
                lifecycle = (
                    "LEGACY_EVALUATED_CANDIDATE"
                )

        else:
            lifecycle = "UNKNOWN"

        try:
            created = datetime.fromisoformat(
                created_at
            )

            if created.tzinfo is None:
                created = created.replace(
                    tzinfo=now.tzinfo
                )

            age_days = (
                now - created
            ).total_seconds() / 86400.0

        except Exception:
            age_days = None

        if lifecycle == "ACTIVE_OUTCOME_TRACKING":
            retention = "PROTECTED"

        elif lifecycle == "COMPLETED":
            retention = "RETAIN_LONG_TERM"

        elif lifecycle in (
            "LEGACY_EVALUATED_CANDIDATE",
            "LEGACY_ORPHAN_CANDIDATE",
        ):
            if (
                age_days is not None
                and age_days < REVIEW_DAYS
            ):
                retention = "RETAIN"
            else:
                retention = "REVIEW_REQUIRED"

        else:
            retention = "UNKNOWN"

        result.append(
            {
                "history_id": history_id,
                "created_at": created_at,
                "age_days": (
                    round(age_days, 3)
                    if age_days is not None
                    else None
                ),
                "outcome_status": outcome_status,
                "snapshot_count": snapshot_count,
                "lifecycle": lifecycle,
                "retention": retention,
            }
        )

    conn.close()

    return result


def get_ai_decision_history_snapshot_cleanup_candidates():
    """
    Read-only cleanup candidate classification for AI Decision
    Outcome History and Portfolio Snapshot lifecycle.

    Production Hardening:
    This function never deletes or updates data.
    REVIEW_REQUIRED is a review candidate only.
    """

    retention_rows = (
        get_ai_decision_history_snapshot_retention()
    )

    result = []

    for row in retention_rows:
        retention = row["retention"]

        if retention == "REVIEW_REQUIRED":
            cleanup_candidate = True
            auto_delete = False
            action = "REVIEW_ONLY"

        elif retention in (
            "PROTECTED",
            "RETAIN_LONG_TERM",
            "RETAIN",
        ):
            cleanup_candidate = False
            auto_delete = False
            action = "NO_AUTO_DELETE"

        else:
            cleanup_candidate = False
            auto_delete = False
            action = "NO_ACTION"

        result.append(
            {
                **row,
                "cleanup_candidate": cleanup_candidate,
                "auto_delete": auto_delete,
                "cleanup_action": action,
            }
        )

    return result


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

    cursor.execute(
        """
        SELECT 1
        FROM ai_decision_outcome_history
        WHERE id = ?
        LIMIT 1
        """,
        (history_id,)
    )

    if cursor.fetchone() is None:
        conn.close()
        raise ValueError("HISTORY_NOT_FOUND")

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

def save_ai_decision_portfolio_evaluation_transaction(
    history_id,
    portfolio_return,
    portfolio_evaluation_date,
    event_time,
    evaluated_weight,
    pending_positions,
):
    """
    Atomically persist completed AI Decision Portfolio evaluation
    and its audit event.

    Step6-10-I
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE ai_decision_outcome_history
            SET
                portfolio_return = ?,
                portfolio_evaluation_date = ?,
                outcome_status = ?
            WHERE id = ?
            """,
            (
                portfolio_return,
                portfolio_evaluation_date,
                "EVALUATED",
                history_id,
            ),
        )

        updated_count = cursor.rowcount

        if updated_count != 1:
            raise ValueError("HISTORY_UPDATE_FAILED")

        save_ai_decision_audit_event(
            event_type="OUTCOME_EVALUATED",
            event_time=event_time,
            source="portfolio_outcome_evaluation",
            status="EVALUATED",
            outcome_history_id=history_id,
            correlation_key=f"outcome:{history_id}",
            details={
                "portfolio_return": portfolio_return,
                "portfolio_evaluation_date":
                    portfolio_evaluation_date,
                "evaluated_weight": evaluated_weight,
                "pending_positions": pending_positions,
            },
            cursor=cursor,
        )

        conn.commit()

        return {
            "history_id": history_id,
            "portfolio_return": portfolio_return,
            "portfolio_evaluation_date":
                portfolio_evaluation_date,
            "outcome_status": "EVALUATED",
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


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

    # Phase8-6-E
    # Same-date completed evaluation is idempotent.
    # Do not re-run evaluation or append duplicate audit events.
    if evaluation_date is not None:
        cursor.execute(
            """
            SELECT
                outcome_status,
                portfolio_return,
                portfolio_evaluation_date
            FROM ai_decision_outcome_history
            WHERE id = ?
            LIMIT 1
            """,
            (
                history_id,
            ),
        )

        existing_evaluation = cursor.fetchone()

        if (
            existing_evaluation is not None
            and existing_evaluation[0] == "EVALUATED"
            and existing_evaluation[2] == evaluation_date
        ):
            conn.close()

            return {
                "evaluation_status": "EVALUATED",
                "outcome_status": "EVALUATED",
                "history_id": history_id,
                "evaluation_date": evaluation_date,
                "portfolio_return": existing_evaluation[1],
                "evaluated_weight": 100.0,
                "pending_positions": 0,
                "positions": [],
            }

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

    save_ai_decision_audit_event(
        event_type="OUTCOME_EVALUATION_STARTED",
        event_time=(
            evaluation_date
            or datetime.now().astimezone().isoformat()
        ),
        source="portfolio_outcome_evaluation",
        status="STARTED",
        outcome_history_id=history_id,
        correlation_key=f"outcome:{history_id}",
        details={
            "evaluation_date": evaluation_date,
            "actual_outcome_gate": True,
        },
    )

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

    save_ai_decision_portfolio_evaluation_transaction(
        history_id=history_id,
        portfolio_return=round(weighted_return, 4),
        portfolio_evaluation_date=last_evaluation_date,
        event_time=(
            evaluation_date
            or last_evaluation_date
        ),
        evaluated_weight=round(evaluated_weight, 4),
        pending_positions=0,
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
