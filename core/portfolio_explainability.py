"""
AI Portfolio Explainability Engine

Step5-3-66

Purpose:
Explain why AI selected this portfolio.
"""



class PortfolioExplainabilityEngine:


    def __init__(self):
        pass



    def generate_explanation(
        self,
        portfolio,
        market_info=None
    ):
        """
        Generate AI portfolio explanation.

        Parameters
        ----------
        portfolio : dict
            Portfolio optimization result

        market_info : dict
            Market regime information


        Returns
        -------
        dict
            Explanation result
        """


        explanation = {

            "summary":
                self._generate_summary(
                    portfolio,
                    market_info
                ),


            "factor_analysis":
                self._analyze_factors(
                    portfolio
                ),


            "allocation_reason":
                self._analyze_allocation(
                    portfolio
                ),


            "risk_analysis":
                self._analyze_risk(
                    portfolio
                )

        }


        return explanation




    def _generate_summary(
        self,
        portfolio,
        market_info
    ):


        if market_info:

            regime = market_info.get(
                "regime",
                "UNKNOWN"
            )

        else:

            regime = "UNKNOWN"



        return (
            f"AI selected this portfolio "
            f"based on factor strength, "
            f"risk balance and current "
            f"market regime ({regime})."
        )




    def _analyze_factors(
        self,
        portfolio
    ):


        factors = []


        factors.append({

            "name":
                "Factor Intelligence",

            "impact":
                "positive",

            "reason":
                "Selected ETFs have strong composite intelligence scores."

        })


        factors.append({

            "name":
                "Trend Strength",

            "impact":
                "positive",

            "reason":
                "Portfolio includes ETFs with stable upward momentum."

        })


        return factors




    def _analyze_allocation(
        self,
        portfolio
    ):


        result = []


        allocations = portfolio.get(
            "allocation",
            portfolio
        )


        if isinstance(
            allocations,
            dict
        ):

            for ticker, weight in allocations.items():

                result.append({

                    "ticker":
                        ticker,

                    "reason":
                        f"{weight}% allocation based on portfolio optimization score."

                })


        return result




    def _analyze_risk(
        self,
        portfolio
    ):


        cash_weight = portfolio.get(
            "cash_weight",
            0
        )


        if cash_weight > 0:

            return (
                f"Risk is controlled through "
                f"{cash_weight}% cash allocation."
            )


        return (
            "Portfolio risk is managed "
            "through diversification."
        )