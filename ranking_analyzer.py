import json
from database import get_connection
from repository import get_etf_score_detail



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
        "previous_rank": None,
        "current_rank": None,
        "rank_change": 0,
        "previous_score": 0,
        "current_score": 0
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


    # current_score가 없는 테스트/초기 데이터 제외
    results = [
        item
        for item in results
        if item.get("current_score", 0) > 0
    ]    


    return results



def get_all_intelligence_universe(analysis_date=None):

    if analysis_date is None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT MAX(created_at) FROM etf_scores"
        )
        analysis_date = cursor.fetchone()[0]
        conn.close()

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        '''
        SELECT ticker
        FROM etf_scores
        WHERE created_at = ?
        ORDER BY final_score DESC
        ''',
        (analysis_date,)
    )


    rows = cursor.fetchall()


    conn.close()


    return [
        row[0]
        for row in rows
    ]



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
            item.get("current_score", 0)
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
                "base_score": item.get("current_score", 0),
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



def get_universe_enhanced_ranking(analysis_date=None):

    tickers = get_all_intelligence_universe(
        analysis_date
    )


    results = []


    for ticker in tickers:

        score_detail = get_etf_score_detail(
            ticker
        )

        if not score_detail:
            continue


        analytics = get_ranking_analytics(
            ticker
        )


        if "current_score" not in analytics:

            current_score = score_detail[4]

            grade = "N/A"

            stability = {
                "stability_score": 0
            }

            prediction = {
                "prediction": "UNCERTAIN"
            }

            prediction_bonus = 0

            enhanced_score = current_score

        else:

            current_score = analytics["current_score"]

            grade = calculate_analytics_grade(
                ticker
            )


            stability = get_stability_analytics(
                ticker
            )


            prediction = generate_ranking_prediction(
                ticker
            )


            grade_bonus = calculate_grade_bonus(
                ticker
            )


            prediction_bonus = calculate_prediction_bonus(
                ticker
            )


            enhanced_score = (
                current_score
                +
                grade_bonus
                +
                stability["stability_score"]
                +
                prediction_bonus
            )


            if enhanced_score > 100:
                enhanced_score = 100


        results.append(
            {
                "ticker": ticker,
                "base_score": current_score,
                "return_score":
                    score_detail[1],

                "trend_score":
                    score_detail[2],

                "slope_score":
                    score_detail[3],

                "final_score":
                    score_detail[4],
                "grade": grade,
                "stability_score": stability["stability_score"],
                "prediction": prediction["prediction"],
                "prediction_bonus": prediction_bonus,
                "enhanced_score": enhanced_score
            }
        )


    results.sort(
        key=lambda x:x["enhanced_score"],
        reverse=True
    )



    return results


def get_intelligence_dashboard_data(
    limit=10
):

    results = get_universe_enhanced_ranking()


    dashboard = []


    for index, item in enumerate(
        results[:limit],
        1
    ):

        dashboard.append(
            {
                "rank": index,
                "ticker": item["ticker"],
                "score": item["base_score"],
                "return_score":
                    item.get("return_score", 0),

                "trend_score":
                    item.get("trend_score", 0),

                "slope_score":
                    item.get("slope_score", 0),

                "final_score":
                    item.get("final_score", 0),

                "enhanced_score": item["enhanced_score"],
                "grade": item["grade"],
                "stability": item["stability_score"],
                "prediction": item["prediction"],
                "prediction_bonus": item["prediction_bonus"]
            }
        )


    return dashboard



def get_intelligence_dashboard_json(
    limit=10
):

    data = get_intelligence_dashboard_data(
        limit
    )


    return json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )



def get_dashboard_api_data(
    limit=10
):

    data = get_intelligence_dashboard_data(
        limit
    )

    return {
        "success": True,
        "count": len(data),
        "data": data
    }



def get_etf_detail(ticker):

    raw_history = get_ranking_history(ticker)


    history = []


    for item in raw_history:

        history.append(
            {
                "date": item[3],
                "rank": item[1],
                "score": item[2]
            }
        )

    ranking = get_dashboard_api_data()


    detail = None


    for item in ranking["data"]:

        if item["ticker"] == ticker:
            detail = item
            break


    if detail is None:

        return {
            "success": False,
            "message": "ETF not found"
        }


    return {

        "success": True,

        "ticker": ticker,

        "score":
            detail["score"],

        "enhanced_score":
            detail["enhanced_score"],

        "return_score":
            detail.get("return_score", 0),

        "trend_score":
            detail.get("trend_score", 0),

        "slope_score":
            detail.get("slope_score", 0),

        "final_score":
            detail.get("final_score", 0),

        "grade":
            detail["grade"],

        "prediction":
            detail["prediction"],

        "stability":
            detail["stability"],

        
        "analysis":
            generate_ai_insight(ticker),

            "history":
                history,

    }



def get_dashboard_intelligence_summary():

    ranking = get_dashboard_api_data()

    if not ranking["data"]:
        return {
            "success": False,
            "message": "No ETF data"
        }


    top = ranking["data"][0]

    ticker = top["ticker"]


    insight = generate_ai_insight(
        ticker
    )


    return {

        "success": True,

        "ticker": ticker,

        "score":
            top["score"],

        "enhanced_score":
            top["enhanced_score"],

        "grade":
            top["grade"],

        "prediction":
            top["prediction"],

        "stability":
            top["stability"],

        "trend":
            insight["trend"],

        "risk":
            insight["risk"],

        "opinion":
            insight["opinion"]

    }



def generate_ai_insight(ticker):


    analytics = get_ranking_analytics(
        ticker
    )


    stability = get_stability_analytics(
        ticker
    )


    prediction = generate_ranking_prediction(
        ticker
    )


    rank_direction = analytics.get(
        "rank_direction",
        "UNKNOWN"
    )


    score_change = analytics.get(
        "score_change",
        0
    )


    stability_grade = stability.get(
        "stability_grade",
        "LOW"
    )


    # Trend 판단

    if rank_direction == "RISING":

        trend = (
            "Ranking 상승 흐름 유지"
        )

    elif rank_direction == "FALLING":

        trend = (
            "Ranking 하락 위험 감지"
        )

    else:

        trend = (
            "Ranking 안정 구간 유지"
        )



    # Risk 판단

    if stability_grade == "HIGH":

        risk = (
            "Ranking 변동성이 낮아 안정적"
        )

    elif stability_grade == "MEDIUM":

        risk = (
            "일부 변동성 존재"
        )

    else:

        risk = (
            "변동성 증가 구간"
        )



    # Opinion 판단

    if (
        prediction["prediction"]
        == "UPTREND"
    ):

        opinion = (
            "상승 모멘텀이 강화되어 "
            "적극적인 관심이 필요합니다."
        )


    elif (
        prediction["prediction"]
        == "MAINTAIN"
    ):

        opinion = (
            "Score와 Ranking 안정성이 "
            "확인되어 보유 전략이 적합합니다."
        )


    elif (
        prediction["prediction"]
        == "DOWNRISK"
    ):

        opinion = (
            "Ranking 약화 가능성이 있어 "
            "주의가 필요합니다."
        )


    else:

        opinion = (
            "추가 데이터 확인이 필요합니다."
        )



    return {

        "trend":
            trend,

        "risk":
            risk,

        "opinion":
            opinion,

        "score_change":
            score_change,

        "prediction":
            prediction["prediction"]

    }


def generate_ai_recommendation(ticker):

    insight = generate_ai_insight(ticker)

    detail = get_etf_detail(ticker)

    score = detail.get("enhanced_score", 0)
    prediction = insight.get("prediction", "UNKNOWN")
    risk = insight.get("risk", "")

    if (
        score >= 95
        and prediction == "UPTREND"
    ):

        recommendation = "STRONG BUY"
        confidence = "HIGH"

    elif (
        score >= 90
        and prediction in ["UPTREND", "MAINTAIN"]
    ):

        recommendation = "BUY"
        confidence = "HIGH"

    elif score >= 80:

        recommendation = "HOLD"
        confidence = "MEDIUM"

    elif prediction == "DOWNRISK":

        recommendation = "WATCH"
        confidence = "MEDIUM"

    else:

        recommendation = "AVOID"
        confidence = "LOW"

    reasons = []

    if score >= 90:
        reasons.append("Enhanced Score 우수")

    if prediction == "UPTREND":
        reasons.append("상승 모멘텀 유지")

    elif prediction == "MAINTAIN":
        reasons.append("안정적인 Ranking 유지")

    if "안정" in risk:
        reasons.append("Ranking 안정성 우수")

    return {

        "recommendation": recommendation,
        "confidence": confidence,
        "reasons": reasons

    }        


if __name__ == "__main__":

    results = get_universe_enhanced_ranking()


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



def generate_portfolio_ai_insight(portfolio):
    """
    Portfolio AI Insight 생성
    """

    if not portfolio:
        return {
            "risk": "Unknown",
            "diversification": "Poor",
            "expected_return": 0,
            "confidence": "Low",
            "comment": "Portfolio 데이터가 없습니다."
        }

    etfs = [p for p in portfolio if p["ticker"] != "CASH"]

    if len(etfs) >= 4:
        diversification = "Excellent"
    elif len(etfs) == 3:
        diversification = "Good"
    else:
        diversification = "Low"

    avg_score = sum(e["score"] for e in etfs) / len(etfs)

    expected_return = round(avg_score * 0.22, 1)

    if avg_score >= 90:
        risk = "Balanced"
        confidence = "High"

    elif avg_score >= 80:
        risk = "Moderate"
        confidence = "Medium"

    else:
        risk = "Aggressive"
        confidence = "Low"

    comment = (
        f"현재 포트폴리오는 {risk} 성향이며 "
        f"분산투자 수준은 {diversification}입니다. "
        f"예상 수익률은 약 {expected_return}% 수준으로 분석됩니다."
    )

    return {
        "risk": risk,
        "diversification": diversification,
        "expected_return": expected_return,
        "confidence": confidence,
        "comment": comment
    }




