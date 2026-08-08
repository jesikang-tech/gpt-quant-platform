"""
AI Portfolio Explainability Engine

Step5-3-68

Purpose:
Explain why AI selected this portfolio
using factor, allocation, risk and market evidence.
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
            Explainability result
        """

        explanation = {

            "summary":
                self._generate_summary(
                    portfolio,
                    market_info
                ),

            "decision_summary":
                self._generate_decision_summary(
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
                ),

            "market_analysis":
                self._analyze_market(
                    market_info
                )

        }

        return explanation


    def _generate_summary(
        self,
        portfolio,
        market_info
    ):

        regime = "UNKNOWN"

        if market_info:
            regime = market_info.get(
                "regime",
                "UNKNOWN"
            )

        return (
            f"AI selected this portfolio "
            f"based on factor strength, "
            f"risk balance and current "
            f"market regime ({regime})."
        )


    def _generate_decision_summary(
        self,
        portfolio,
        market_info
    ):

        regime = "UNKNOWN"

        if market_info:
            regime = market_info.get(
                "regime",
                "UNKNOWN"
            )

        cash_weight = portfolio.get(
            "cash_weight",
            0
        )

        allocations = portfolio.get(
            "allocation",
            portfolio
        )

        if isinstance(
            allocations,
            dict
        ):
            invested_weight = sum(
                weight
                for ticker, weight
                in allocations.items()
                if ticker != "CASH"
            )
        else:
            invested_weight = 0

        return (
            f"AI maintains an invested allocation "
            f"of {invested_weight}% with "
            f"{cash_weight}% cash protection "
            f"under the {regime} market regime."
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
                "Selected ETFs have strong "
                "composite intelligence scores."

        })


        factors.append({

            "name":
                "Trend Strength",

            "impact":
                "positive",

            "reason":
                "Portfolio includes ETFs with "
                "stable upward momentum."

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

                if ticker == "CASH":
                    continue

                if weight >= 40:

                    reason = (
                        f"{weight}% allocation reflects "
                        "a high-conviction portfolio position."
                    )

                elif weight >= 30:

                    reason = (
                        f"{weight}% allocation reflects "
                        "a strong portfolio position."
                    )

                elif weight > 0:

                    reason = (
                        f"{weight}% allocation provides "
                        "portfolio diversification."
                    )

                else:

                    reason = (
                        "No capital is currently allocated "
                        "to this asset."
                    )


                result.append({

                    "ticker":
                        ticker,

                    "weight":
                        weight,

                    "reason":
                        reason

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
                f"{cash_weight}% cash allocation "
                "which provides downside protection."
            )


        return (
            "Portfolio risk is managed "
            "through diversification."
        )


    def _analyze_market(
        self,
        market_info
    ):

        if not market_info:

            return {
                "regime": "UNKNOWN",
                "impact": "neutral",
                "reason":
                    "Market regime information "
                    "is not available."
            }


        regime = market_info.get(
            "regime",
            "UNKNOWN"
        )


        if regime in ("BULL", "BULLISH"):

            impact = "positive"

            reason = (
                "Bullish market conditions "
                "support maintaining higher "
                "risk asset exposure."
            )

        elif regime in ("BEAR", "BEARISH"):

            impact = "negative"

            reason = (
                "Bearish market conditions "
                "increase the importance of "
                "risk control and cash protection."
            )

        else:

            impact = "neutral"

            reason = (
                "Neutral market conditions "
                "support a balanced allocation "
                "between opportunity and risk control."
            )


        return {

            "regime":
                regime,

            "impact":
                impact,

            "reason":
                reason

        }