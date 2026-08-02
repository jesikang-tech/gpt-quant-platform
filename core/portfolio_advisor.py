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


    etf_count = len(
        [
            item
            for item in portfolio
            if item["ticker"] != "CASH"
        ]
    )


    cash = next(
        (
            item["weight"]
            for item in portfolio
            if item["ticker"] == "CASH"
        ),
        0
    )


    return {

        "summary":
            f"High Score ETF {etf_count}개 중심의 "
            "균형형 포트폴리오입니다.",


        "opinion":
            "상위 Ranking ETF의 비중을 확대하고 "
            f"{cash}% 현금 비중으로 Risk Buffer를 유지하는 "
            "안정형 AI Portfolio 전략입니다."

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