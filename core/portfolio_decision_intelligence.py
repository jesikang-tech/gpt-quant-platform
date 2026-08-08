"""
GPT Quant Platform

AI Portfolio Decision Intelligence

Step5-3-69
"""


class PortfolioDecisionIntelligence:

    def generate(
        self,
        ai_decision,
        decision_quality,
        reliability,
        adaptive_strategy,
        rebalance,
        optimization,
        explainability
    ):
        """Integrate all AI portfolio intelligence into one final decision."""

        ai_decision = ai_decision or {}
        decision_quality = decision_quality or {}
        reliability = reliability or {}
        adaptive_strategy = adaptive_strategy or {}
        rebalance = rebalance or {}
        optimization = optimization or {}
        explainability = explainability or {}

        decision = ai_decision.get(
            "decision",
            "UNKNOWN"
        )

        market_view = ai_decision.get(
            "market_view",
            "UNKNOWN"
        )

        confidence = reliability.get(
            "confidence",
            ai_decision.get(
                "confidence",
                0
            )
        )

        reliability_level = reliability.get(
            "reliability_level",
            "UNKNOWN"
        )

        strategy_mode = adaptive_strategy.get(
            "strategy_mode",
            "balanced"
        )

        rebalance_action = rebalance.get(
            "rebalance_action",
            "HOLD"
        )

        optimization_status = optimization.get(
            "optimization_status",
            "UNKNOWN"
        )

        summary = explainability.get(
            "summary",
            ""
        )

        if decision == "ACCUMULATE":

            final_action = (
                "Increase growth exposure "
                "while maintaining risk controls"
            )

        elif decision == "DEFENSIVE":

            final_action = (
                "Reduce equity exposure "
                "and strengthen defensive allocation"
            )

        elif decision == "MAINTAIN":

            final_action = (
                "Maintain balanced allocation "
                "and monitor market conditions"
            )

        else:

            final_action = (
                "Monitor market conditions "
                "before making allocation changes"
            )

        return {
            "decision": decision,
            "market_view": market_view,
            "confidence": confidence,
            "reliability": reliability_level,
            "strategy_mode": strategy_mode,
            "rebalance_action": rebalance_action,
            "optimization_status": optimization_status,
            "final_action": final_action,
            "summary": summary,
            "quality": decision_quality.get(
                "quality_level",
                "UNKNOWN"
            ),
            "quality_trend": decision_quality.get(
                "recent_trend",
                "UNKNOWN"
            )
        }