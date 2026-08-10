"""
AI Decision Explainability Engine
Step5-3-71

Explain why the AI generated the current portfolio decision.
"""


class AIDecisionExplainability:

    def calculate_contributions(
        self,
        market_regime,
        portfolio_health,
        top_etf
    ):
        """
        Calculate AI Decision Score contributions.

        Decision Score:
            Market Confidence : 40%
            Portfolio Health  : 40%
            Top ETF Score     : 20%
        """

        market_confidence = self._normalize(
            market_regime.get("confidence", 0)
        )

        health_score = self._normalize(
            portfolio_health.get("health_score", 0)
        )

        etf_score = self._normalize(
            top_etf.get("score", 0)
        )

        market_contribution = round(
            market_confidence * 0.40,
            1
        )

        portfolio_contribution = round(
            health_score * 0.40,
            1
        )

        etf_contribution = round(
            etf_score * 0.20,
            1
        )

        decision_score = round(
            market_contribution
            + portfolio_contribution
            + etf_contribution,
            1
        )

        return {
            "market_confidence": market_confidence,
            "portfolio_health": health_score,
            "top_etf_score": etf_score,
            "market_contribution": market_contribution,
            "portfolio_contribution": portfolio_contribution,
            "etf_contribution": etf_contribution,
            "decision_score": decision_score
        }

    def generate_market_reason(
        self,
        market_regime,
        contribution
    ):
        regime = market_regime.get(
            "regime",
            "UNKNOWN"
        )

        confidence = contribution.get(
            "market_confidence",
            0
        )

        contribution_score = contribution.get(
            "market_contribution",
            0
        )

        return {
            "regime": regime,
            "confidence": confidence,
            "contribution": contribution_score,
            "reason": (
                f"Market regime is {regime} "
                f"with {confidence:.1f}% confidence. "
                f"This contributes {contribution_score:.1f} "
                f"points to the AI Decision Score."
            )
        }

    def generate_portfolio_reason(
        self,
        portfolio_health,
        contribution
    ):
        health = contribution.get(
            "portfolio_health",
            0
        )

        risk_level = portfolio_health.get(
            "risk_level",
            "Unknown"
        )

        contribution_score = contribution.get(
            "portfolio_contribution",
            0
        )

        return {
            "health_score": health,
            "risk_level": risk_level,
            "contribution": contribution_score,
            "reason": (
                f"Portfolio health is {health:.1f}/100 "
                f"with risk level {risk_level}. "
                f"This contributes {contribution_score:.1f} "
                f"points to the AI Decision Score."
            )
        }

    def generate_etf_reason(
        self,
        top_etf,
        contribution
    ):
        ticker = top_etf.get(
            "ticker",
            "-"
        )

        score = contribution.get(
            "top_etf_score",
            0
        )

        contribution_score = contribution.get(
            "etf_contribution",
            0
        )

        return {
            "ticker": ticker,
            "score": score,
            "contribution": contribution_score,
            "reason": (
                f"Top ETF {ticker} has an AI score of "
                f"{score:.1f}/100. "
                f"This contributes {contribution_score:.1f} "
                f"points to the AI Decision Score."
            )
        }

    def generate_risk_reason(
        self,
        decision,
        portfolio_health,
        market_regime
    ):
        risk_level = portfolio_health.get(
            "risk_level",
            "Unknown"
        )

        regime = market_regime.get(
            "regime",
            "UNKNOWN"
        )

        decision_name = decision.get(
            "decision",
            "UNKNOWN"
        )

        risk_control = decision.get(
            "risk_control",
            "Monitor portfolio risk"
        )

        if risk_level == "High Risk":
            assessment = (
                "High portfolio risk detected. "
                "Risk control should take priority."
            )

        elif regime == "BEARISH":
            assessment = (
                "Bearish market conditions detected. "
                "Defensive positioning is recommended."
            )

        elif risk_level == "Medium Risk":
            assessment = (
                "Moderate portfolio risk detected. "
                "Market conditions should be monitored."
            )

        else:
            assessment = (
                "No critical risk signal detected "
                "from the current market and portfolio state."
            )

        return {
            "risk_level": risk_level,
            "market_regime": regime,
            "decision": decision_name,
            "risk_control": risk_control,
            "assessment": assessment
        }

    def generate_confidence_reason(
        self,
        decision,
        contribution
    ):
        confidence = self._normalize(
            decision.get("confidence", 0)
        )

        decision_score = contribution.get(
            "decision_score",
            0
        )

        if decision_score >= 90:
            level = "Very High"

        elif decision_score >= 80:
            level = "High"

        elif decision_score >= 70:
            level = "Moderate"

        else:
            level = "Low"

        return {
            "confidence": confidence,
            "level": level,
            "decision_score": decision_score,
            "reason": (
                f"AI Decision Score is {decision_score:.1f}/100, "
                f"resulting in {level.lower()} decision confidence."
            )
        }

    def generate_explanation(
        self,
        decision,
        market_regime,
        portfolio_health,
        top_etf
    ):
        """
        Generate complete AI Decision Explainability Report.
        """

        decision = decision or {}
        market_regime = market_regime or {}
        portfolio_health = portfolio_health or {}
        top_etf = top_etf or {}

        contribution = self.calculate_contributions(
            market_regime,
            portfolio_health,
            top_etf
        )

        decision_score = contribution[
            "decision_score"
        ]

        decision_grade = self._get_grade(
            decision_score
        )

        market_reason = self.generate_market_reason(
            market_regime,
            contribution
        )

        portfolio_reason = self.generate_portfolio_reason(
            portfolio_health,
            contribution
        )

        etf_reason = self.generate_etf_reason(
            top_etf,
            contribution
        )

        risk_reason = self.generate_risk_reason(
            decision,
            portfolio_health,
            market_regime
        )

        confidence_reason = self.generate_confidence_reason(
            decision,
            contribution
        )

        recommended_action = decision.get(
            "next_action",
            decision.get(
                "action",
                "Monitor current portfolio"
            )
        )

        return {
            "decision": decision.get(
                "decision",
                "UNKNOWN"
            ),
            "action": decision.get(
                "action",
                "UNKNOWN"
            ),
            "decision_score": decision_score,
            "decision_grade": decision_grade,
            "summary": decision.get(
                "summary",
                ""
            ),
            "explanation": {
                "market": market_reason,
                "portfolio": portfolio_reason,
                "top_etf": etf_reason,
                "risk": risk_reason,
                "confidence": confidence_reason
            },
            "recommended_action": recommended_action,
            "original_reason": decision.get(
                "reason",
                ""
            )
        }

    @staticmethod
    def _normalize(value):
        try:
            value = float(value)
        except (
            TypeError,
            ValueError
        ):
            return 0

        return max(
            0,
            min(
                100,
                value
            )
        )

    @staticmethod
    def _get_grade(score):
        if score >= 90:
            return "A+"

        if score >= 80:
            return "A"

        if score >= 70:
            return "B"

        return "C"
