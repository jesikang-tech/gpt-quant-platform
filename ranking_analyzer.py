from database import get_connection



def get_ranking_history(ticker):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            ticker,
            rank,
            final_score,
            ranking_date
        FROM etf_ranking_history
        WHERE ticker = ?
        ORDER BY ranking_date ASC
        """,
        (
            ticker,
        )
    )


    rows = cursor.fetchall()

    conn.close()


    return rows



def analyze_ranking_trend(ticker):

    history = get_ranking_history(
        ticker
    )


    if len(history) < 2:

        return {
            "ticker": ticker,
            "message": "Not enough history"
        }


    previous = history[-2]
    current = history[-1]


    rank_change = (
        previous[1]
        -
        current[1]
    )


    return {
        "ticker": ticker,
        "previous_rank": previous[1],
        "current_rank": current[1],
        "rank_change": rank_change,
        "previous_score": previous[2],
        "current_score": current[2]
    }



def calculate_ranking_trend_score(ticker):

    trend = analyze_ranking_trend(
        ticker
    )


    if "rank_change" not in trend:

        return 0


    return trend["rank_change"]



def calculate_score_momentum(ticker):

    trend = analyze_ranking_trend(
        ticker
    )


    if "current_score" not in trend:

        return 0


    score_change = (
        trend["current_score"]
        -
        trend["previous_score"]
    )


    return score_change



def get_ranking_trend_all():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT DISTINCT ticker
        FROM etf_ranking_history
        """
    )


    tickers = cursor.fetchall()


    conn.close()


    results = []


    for ticker in tickers:

        trend = analyze_ranking_trend(
            ticker[0]
        )

        results.append(
            trend
        )


    return results



def calculate_rank_direction(ticker):

    history = get_ranking_history(ticker)

    if len(history) < 2:
        return "UNKNOWN"


    ranks = []

    for row in history:
        ranks.append(row[1])


    if ranks[-1] < ranks[0]:
        return "RISING"

    elif ranks[-1] > ranks[0]:
        return "FALLING"

    else:
        return "STABLE"



def get_ranking_analytics(ticker):

    history = get_ranking_history(ticker)

    if len(history) == 0:
        return {
            "ticker": ticker,
            "message": "No ranking history"
        }


    ranks = []

    scores = []


    for row in history:
        ranks.append(row[1])
        scores.append(row[2])


    trend = analyze_ranking_trend(ticker)


    return {
        "ticker": ticker,

        "current_rank": ranks[-1],
        "best_rank": min(ranks),
        "worst_rank": max(ranks),

        "rank_change": trend.get(
            "rank_change",
            0
        ),

        "current_score": scores[-1],

        "score_change":
            scores[-1] - scores[0],

        "rank_direction":
            calculate_rank_direction(ticker)
    }



def calculate_analytics_grade(ticker):

    analytics = get_ranking_analytics(ticker)

    direction = analytics.get(
        "rank_direction"
    )

    score_change = analytics.get(
        "score_change",
        0
    )

    if direction == "RISING" and score_change >= 0:
        return "A"

    elif direction == "STABLE" and score_change >= 0:
        return "B"

    elif direction == "FALLING":
        return "C"

    else:
        return "D"



def calculate_grade_bonus(ticker):

    grade = calculate_analytics_grade(ticker)

    bonus_table = {
        "A": 5,
        "B": 2,
        "C": 0,
        "D": -5
    }

    return bonus_table.get(
        grade,
        0
    )



def get_enhanced_ranking():

    trends = get_ranking_trend_all()

    results = []


    for item in trends:

        trend_score = calculate_ranking_trend_score(
            item["ticker"]
        )


        momentum_score = calculate_score_momentum(
            item["ticker"]
        )


        grade = calculate_analytics_grade(
            item["ticker"]
        )


        grade_bonus = calculate_grade_bonus(
            item["ticker"]
        )


        enhanced_score = (
            item["current_score"]
            +
            trend_score
            +
            momentum_score
            +
            grade_bonus
        )


        results.append(
            {
                "ticker": item["ticker"],
                "base_score": item["current_score"],
                "trend_score": trend_score,
                "momentum_score": momentum_score,
                "grade": grade,
                "grade_bonus": grade_bonus,
                "enhanced_score": enhanced_score
            }
        )


    results.sort(
        key=lambda x: x["enhanced_score"],
        reverse=True
    )


    return results



if __name__ == "__main__":

    results = get_enhanced_ranking()


    for result in results:

        print(result)

        print(
            "Trend Score :",
            result["trend_score"]
        )

        print(
            "Momentum Score :",
            result["momentum_score"]
        )

        print(
            "Grade :",
            result["grade"]
        )

        print(
            "Grade Bonus :",
            result["grade_bonus"]
        )

        print(
            "Enhanced Score :",
            result["enhanced_score"]
        )



def calculate_analytics_grade(ticker):

    analytics = get_ranking_analytics(ticker)

    direction = analytics.get(
        "rank_direction"
    )

    score_change = analytics.get(
        "score_change",
        0
    )

    rank_change = analytics.get(
        "rank_change",
        0
    )


