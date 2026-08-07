from core.portfolio_explainability import (
    PortfolioExplainabilityEngine
)



engine = PortfolioExplainabilityEngine()



portfolio = {

    "allocation":{

        "069500":40,
        "365040":30,
        "475720":20

    },

    "cash_weight":10

}



market = {

    "regime":
        "NEUTRAL"

}



result = engine.generate_explanation(
    portfolio,
    market
)



print("\nAI Portfolio Explainability Test\n")

print(result["summary"])

print("\nFactors:")

for factor in result["factor_analysis"]:

    print(
        factor["name"],
        ":",
        factor["impact"]
    )


print("\nRisk:")

print(
    result["risk_analysis"]
)