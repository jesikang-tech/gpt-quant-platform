from core.portfolio_conversational import (
    PortfolioConversationalAnalyst
)



engine = PortfolioConversationalAnalyst()



portfolio = [

    {
        "ticker":"365040",
        "weight":40,
        "score":93
    },

    {
        "ticker":"306950",
        "weight":30,
        "score":88
    },

    {
        "ticker":"CASH",
        "weight":10,
        "score":0    
    }

]



market = {

    "regime":
        "NEUTRAL"

}



questions = [

    "왜 365040 비중이 높은가?",

    "포트폴리오 위험을 줄이고 싶다"

]



for question in questions:

    result = engine.analyze(
        question,
        portfolio,
        market
    )


    print("\nQuestion:")
    print(result["question"])


    print("\nQuestion Type:")
    print(
        result.get(
            "question_type"
        )
    )


    print("\nAnswer:")
    print(result["answer"])


    print("\nReason:")

    for item in result["reason"]:
        print("-", item)


    print("\nRecommendation:")
    print(result["recommendation"])


    print("\nConfidence:")
    print(result["confidence"])