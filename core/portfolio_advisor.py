"""
GPT Quant Platform
AI Portfolio Advisor

Step5-3-37
"""



def generate_portfolio(ranking):
    """
    Generate AI portfolio recommendation

    Args:
        ranking:
            [
                {
                    "ticker": "069500",
                    "score": 93.0,
                    "trend": 1
                }
            ]

    Returns:
        portfolio list
    """

    if not ranking:
        return []


    # Score 기준 정렬
    sorted_ranking = sorted(
        ranking,
        key=lambda x: x.get("score", 0),
        reverse=True
    )


    weights = [
        40,
        30,
        20
    ]


    portfolio = []


    for index, etf in enumerate(sorted_ranking[:3]):

        portfolio.append(
            {
                "ticker": etf.get("ticker"),
                "weight": weights[index],
                "score": etf.get("score"),
                "reason":
                    "High Score + Strong Trend"
                    if etf.get("trend", 0) > 0
                    else
                    "High Score"
            }
        )


    # 현금 비중 추가

    portfolio.append(
        {
            "ticker": "CASH",
            "weight": 10,
            "score": None,
            "reason":
                "Risk Management"
        }
    )


    return portfolio



def generate_portfolio_insight(portfolio):
    """
    Generate AI Portfolio Insight
    """

    if not portfolio:
        return {
            "summary": "No portfolio available",
            "opinion": ""
        }


    etfs = [
        item
        for item in portfolio
        if item["ticker"] != "CASH"
    ]


    etf_count = len(etfs)


    cash = next(
        (
            item["weight"]
            for item in portfolio
            if item["ticker"] == "CASH"
        ),
        0
    )


    if etfs:

        avg_score = round(
            sum(
                item.get("score", 0)
                for item in etfs
            )
            /
            etf_count,
            1
        )


        top_etf = max(
            etfs,
            key=lambda x: x.get("score",0)
        )


    else:

        avg_score = 0
        top_etf = {
            "ticker":"N/A",
            "score":0
        }


    if avg_score >= 90:

        risk_level = "Low Risk / Strong Trend"

    elif avg_score >= 80:

        risk_level = "Balanced"

    else:

        risk_level = "Growth Focus"


    if etf_count >= 4:

        diversification = "Excellent"

    elif etf_count >= 3:

        diversification = "Good"

    else:

        diversification = "Limited"


    return {

        "summary":
            f"{risk_level} AI Portfolio "
            f"({etf_count} ETF 구성)",


        "analytics":
        {
            "average_score": avg_score,
            "top_etf": top_etf["ticker"],
            "top_score": top_etf["score"],
            "cash_weight": cash,
            "diversification": diversification
        },


        "opinion":
            f"""
현재 Portfolio는 평균 Score {avg_score}점 수준의
{risk_level} 전략입니다.

상위 ETF {top_etf['ticker']}의 Momentum이 가장 강하며,
현금 {cash}%를 유지하여 Risk Buffer를 확보하고 있습니다.

분산 수준은 {diversification}으로 평가됩니다.
"""
    }



def optimize_portfolio_weight(ranking, mode="balanced"):
    """
    AI Portfolio Weight Optimization
    """

    if not ranking:
        return []


    sorted_ranking = sorted(
        ranking,
        key=lambda x: x.get("score", 0),
        reverse=True
    )


    if mode == "conservative":

        weights = [
            35,
            25,
            20
        ]

        cash_weight = 20


    elif mode == "aggressive":

        weights = [
            50,
            30,
            15
        ]

        cash_weight = 5


    else:

        weights = [
            40,
            30,
            20
        ]

        cash_weight = 10



    portfolio = []


    for index, etf in enumerate(sorted_ranking[:3]):

        portfolio.append(
            {
                "ticker": etf.get("ticker"),

                "weight":
                    weights[index],

                "score":
                    etf.get("score"),

                "mode":
                    mode,

                "reason":
                    "AI Optimized Weight"
            }
        )


    portfolio.append(
        {
            "ticker": "CASH",

            "weight":
                cash_weight,

            "score":
                None,

            "mode":
                mode,

            "reason":
                "Risk Management"
        }
    )


    return portfolio