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



def generate_ranking_prediction(ticker):

    analytics = get_ranking_analytics(ticker)

    stability = get_stability_analytics(ticker)

    direction = analytics.get(
        "rank_direction"
    )

    stability_grade = stability.get(
        "stability_grade"
    )


    if (
        direction == "RISING"
        and
        stability_grade == "HIGH"
    ):

        return {
            "ticker": ticker,
            "prediction": "UPTREND",
            "confidence": 90,
            "message":
                "Ranking trend is improving."
        }


    elif (
        direction == "STABLE"
        and
        stability_grade == "HIGH"
    ):

        return {
            "ticker": ticker,
            "prediction": "MAINTAIN",
            "confidence": 85,
            "message":
                "Ranking likely to remain stable."
        }


    elif direction == "FALLING":

        return {
            "ticker": ticker,
            "prediction": "DOWNRISK",
            "confidence": 80,
            "message":
                "Ranking deterioration risk detected."
        }


    else:

        return {
            "ticker": ticker,
            "prediction": "UNCERTAIN",
            "confidence": 50,
            "message":
                "Insufficient ranking signal."
        }



def calculate_stability_score(ticker):

    history = get_ranking_history(
        ticker
    )


    if len(history) < 2:

        return 0


    ranks = []

    for row in history:
        ranks.append(
            row[1]
        )


    changes = []

    for i in range(1, len(ranks)):

        changes.append(
            abs(
                ranks[i]
                -
                ranks[i-1]
            )
        )


    average_change = (
        sum(changes)
        /
        len(changes)
    )


    if average_change == 0:

        return 5


    elif average_change <= 2:

        return 3


    elif average_change <= 5:

        return 1


    else:

        return -3



def get_stability_analytics(ticker):

    history = get_ranking_history(
        ticker
    )


    if len(history) < 2:

        return {
            "ticker": ticker,
            "history_count": len(history),
            "average_rank_change": 0,
            "stability_score": 0,
            "stability_grade": "LOW"
        }


    ranks = []


    for row in history:
        ranks.append(
            row[1]
        )


    changes = []


    for i in range(1, len(ranks)):

        changes.append(
            abs(
                ranks[i]
                -
                ranks[i-1]
            )
        )


    average_change = (
        sum(changes)
        /
        len(changes)
    )


    stability_score = calculate_stability_score(
        ticker
    )


    if stability_score >= 5:

        grade = "HIGH"

    elif stability_score >= 2:

        grade = "MEDIUM"

    else:

        grade = "LOW"



    return {
        "ticker": ticker,
        "history_count": len(history),
        "average_rank_change": average_change,
        "stability_score": stability_score,
        "stability_grade": grade
    }



def generate_ranking_assessment(ticker):

    analytics = get_ranking_analytics(
        ticker
    )


    stability = get_stability_analytics(
        ticker
    )


    grade = analytics.get(
        "rank_direction",
        "UNKNOWN"
    )


    stability_grade = stability.get(
        "stability_grade",
        "LOW"
    )


    score_change = analytics.get(
        "score_change",
        0
    )


    if stability_grade == "HIGH":

        if grade == "RISING":

            message = (
                "Ranking improving with high stability."
            )

        elif grade == "STABLE":

            message = (
                "Ranking stable with high consistency."
            )

        else:

            message = (
                "High stability but ranking weakening."
            )


    elif stability_grade == "MEDIUM":

        message = (
            "Ranking shows moderate stability."
        )


    else:

        message = (
            "Ranking volatility detected. Need caution."
        )


    return {
        "ticker": ticker,
        "grade": calculate_analytics_grade(ticker),
        "direction": grade,
        "stability_grade": stability_grade,
        "score_change": score_change,
        "message": message
    }



def calculate_prediction_bonus(ticker):

    prediction = generate_ranking_prediction(
        ticker
    )


    bonus_table = {
        "UPTREND": 5,
        "MAINTAIN": 3,
        "DOWNRISK": -5,
        "UNCERTAIN": 0
    }


    return bonus_table.get(
        prediction["prediction"],
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


        stability_score = calculate_stability_score(
            item["ticker"]
        )


        prediction_bonus = calculate_prediction_bonus(
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
            +
            stability_score
        )


        results.append(
            {
                "ticker": item["ticker"],
                "base_score": item["current_score"],
                "trend_score": trend_score,
                "momentum_score": momentum_score,
                "grade": grade,
                "grade_bonus": grade_bonus,
                "stability_score": stability_score,
                "prediction_bonus": prediction_bonus,
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



