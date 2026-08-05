"""
GPT Quant Platform
AI Portfolio Advisor

Step5-3-37
"""


from core.market_regime import analyze_market_regime

from core.market_strategy import (
    generate_market_strategy
)

def generate_portfolio(
    ranking,
    market_regime=None
):
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

    market = analyze_market_regime()

    regime = market["regime"]


    if regime == "BULLISH":

        weights = [
            50,
            30,
            15
        ]

        cash_weight = 5


    elif regime == "BEARISH":

        weights = [
            30,
            25,
            20
        ]

        cash_weight = 25


    else:

        if market_regime is None:

            market_regime = analyze_market_regime()


        market_strategy = generate_market_strategy(
            market_regime
        )


        portfolio_mode = (
            market_strategy.get(
                "portfolio_mode",
                "balanced"
            )
        )


        if portfolio_mode == "aggressive":

            weights = [
                50,
                30,
                15
            ]

            cash_weight = 5


        elif portfolio_mode == "conservative":

            weights = [
                35,
                25,
                20
            ]

            cash_weight = 20


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
            "weight": cash_weight,
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


    market = analyze_market_regime()

    regime = market["regime"]
    strength = market["market_strength"]
    confidence = market["confidence"]


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
            "diversification": diversification,

            "market_regime": regime,
            "market_strength": strength,
            "market_confidence": confidence
        },


        "opinion":
            f"""
현재 Portfolio는 평균 Score {avg_score}점 수준의
{risk_level} 전략입니다.

현재 시장 국면은 {regime} 상태이며,
시장 강도는 {strength},
AI 판단 Confidence는 {confidence}% 입니다.

상위 ETF {top_etf['ticker']}의 Momentum이 가장 강하며,
현금 {cash}%를 유지하여 Risk Buffer를 확보하고 있습니다.

분산 수준은 {diversification}으로 평가됩니다.
"""
    }



def analyze_portfolio_health(portfolio):
    """
    Portfolio Intelligence Analysis
    """


    if not portfolio:

        return {
            "health_score": 0,
            "risk_level": "Unknown",
            "confidence": "LOW",
            "allocation": {},
            "cash_weight": 0,
            "rebalance": "No portfolio data"
        }


    market = analyze_market_regime()

    regime = market["regime"]

    strength = market["market_strength"]


    etfs = [
        item
        for item in portfolio
        if item["ticker"] != "CASH"
    ]


    cash = next(
        (
            item["weight"]
            for item in portfolio
            if item["ticker"] == "CASH"
        ),
        0
    )


    avg_score = round(
        sum(
            item.get("score", 0)
            for item in etfs
        )
        /
        len(etfs),
        1
    )


    health_score = round(
        avg_score * 0.8
        +
        (100 - cash) * 0.2,
        1
    )


    if health_score >= 90:

        risk_level = "Low Risk"

        confidence = "HIGH"


    elif health_score >= 80:

        risk_level = "Balanced"

        confidence = "MEDIUM"


    else:

        risk_level = "High Risk"

        confidence = "LOW"



    allocation = {}

    for item in etfs:

        allocation[item["ticker"]] = item["weight"]



    top_etf = max(
        etfs,
        key=lambda x: x.get("score", 0)
    )


    if regime == "BULLISH":

        rebalance = (
            f"{top_etf['ticker']} 중심 공격적 전략 유지 권장. "
            f"현재 시장은 {regime} 상태이며 "
            f"강도는 {strength}입니다. "
            "우수 ETF 비중 확대 전략이 유효합니다."
        )


    elif regime == "BEARISH":

        rebalance = (
            f"{top_etf['ticker']} 중심 방어 전략 필요. "
            f"현재 시장은 {regime} 상태이며 "
            f"강도는 {strength}입니다. "
            "현금 비중 확대와 위험 관리가 필요합니다."
        )


    else:

        rebalance = (
            f"{top_etf['ticker']} 중심 균형 전략 유지 권장. "
            f"현재 시장은 {regime} 상태이며 "
            f"강도는 {strength}입니다. "
            "급격한 변경보다 현재 Portfolio 유지가 적합합니다."
        )


    return {

        "health_score": health_score,

        "risk_level": risk_level,

        "confidence": confidence,

        "allocation": allocation,

        "cash_weight": cash,

        "rebalance": rebalance

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



def analyze_market_condition(ranking):
    """
    AI Market Condition Analyzer
    Step5-3-43
    """

    if not ranking:
        return {
            "market": "UNKNOWN",
            "recommended_mode": "balanced",
            "confidence": "LOW"
        }


    scores = [
        item.get("score", 0)
        for item in ranking
    ]


    avg_score = round(
        sum(scores) / len(scores),
        1
    )


    trend_count = len(
        [
            item
            for item in ranking
            if item.get("trend", 0) > 0
        ]
    )


    trend_ratio = (
        trend_count / len(ranking)
    )


    if avg_score >= 90 and trend_ratio >= 0.6:

        return {
            "market": "BULLISH",
            "recommended_mode": "aggressive",
            "confidence": "HIGH",
            "average_score": avg_score
        }


    elif avg_score >= 80:

        return {
            "market": "NEUTRAL",
            "recommended_mode": "balanced",
            "confidence": "MEDIUM",
            "average_score": avg_score
        }


    else:

        return {
            "market": "BEARISH",
            "recommended_mode": "conservative",
            "confidence": "HIGH",
            "average_score": avg_score
        }