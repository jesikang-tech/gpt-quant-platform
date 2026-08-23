"""
GPT Quant Platform

AI Portfolio Decision Intelligence

Step5-3-74
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

        # ---------------------------------
        # Adaptive Strategy
        # ---------------------------------

        strategy_mode = adaptive_strategy.get(
            "strategy",
            adaptive_strategy.get(
                "strategy_mode",
                "BALANCED"
            )
        )

        adaptive_action = adaptive_strategy.get(
            "action",
            "MONITOR_CLOSELY"
        )

        adaptive_confidence = adaptive_strategy.get(
            "confidence",
            0
        )

        adaptive_score = adaptive_strategy.get(
            "score",
            0
        )

        adaptive_direction = adaptive_strategy.get(
            "direction",
            "UNKNOWN"
        )

        adaptive_stability = adaptive_strategy.get(
            "stability",
            "UNKNOWN"
        )

        adaptive_momentum = adaptive_strategy.get(
            "momentum",
            "UNKNOWN"
        )

        adaptive_grade_stability = adaptive_strategy.get(
            "grade_stability",
            "UNKNOWN"
        )

        adaptive_consistency = adaptive_strategy.get(
            "consistency",
            "UNKNOWN"
        )

        adaptive_summary = adaptive_strategy.get(
            "summary",
            ""
        )

        outcome_learning_signal = adaptive_strategy.get(
            "outcome_learning_signal"
        )

        outcome_learning_signal_strength = adaptive_strategy.get(
            "outcome_learning_signal_strength"
        )

        adaptive_learning_required = adaptive_strategy.get(
            "adaptive_learning_required"
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

        # ---------------------------------
        # Adaptive Strategy Decision Integration
        # Step5-3-76
        # ---------------------------------

        if decision == "DEFENSIVE":

            decision_alignment = (
                "ALIGNED"
                if strategy_mode in (
                    "DEFENSIVE",
                    "CAUTIOUS"
                )
                else "CONFLICT"
            )

        elif decision == "ACCUMULATE":

            decision_alignment = (
                "ALIGNED"
                if strategy_mode in (
                    "GROWTH",
                    "BALANCED"
                )
                else "CONFLICT"
            )

        elif decision == "MAINTAIN":

            decision_alignment = (
                "ALIGNED"
                if strategy_mode in (
                    "MAINTAIN",
                    "BALANCED",
                    "MONITOR"
                )
                else "CONFLICT"
            )

        else:

            decision_alignment = "UNKNOWN"


        # Strong defensive adaptive signals
        # take priority over aggressive AI decisions.

        if strategy_mode == "DEFENSIVE":

            final_strategy = "DEFENSIVE"

            adaptive_override = (
                decision != "DEFENSIVE"
            )

            adaptive_override_reason = (
                "Adaptive strategy detected defensive "
                "conditions and prioritized risk reduction."
                if adaptive_override
                else ""
            )

            final_action = (
                "Reduce equity exposure "
                "and strengthen defensive allocation"
            )


        elif strategy_mode == "CAUTIOUS":

            final_strategy = "CAUTIOUS"

            adaptive_override = (
                decision != "DEFENSIVE"
            )

            adaptive_override_reason = (
                "Adaptive strategy detected elevated "
                "risk and recommended limiting exposure."
                if adaptive_override
                else ""
            )

            final_action = (
                "Limit portfolio exposure "
                "and monitor risk conditions closely"
            )


        elif decision == "ACCUMULATE":

            final_strategy = strategy_mode

            adaptive_override = False

            adaptive_override_reason = ""

            if strategy_mode == "GROWTH":

                final_action = (
                    "Increase growth exposure "
                    "while maintaining risk controls"
                )

            else:

                final_action = (
                    "Increase portfolio exposure "
                    "with balanced risk controls"
                )


        elif decision == "DEFENSIVE":

            final_strategy = "DEFENSIVE"

            adaptive_override = False

            adaptive_override_reason = ""

            final_action = (
                "Reduce equity exposure "
                "and strengthen defensive allocation"
            )


        elif decision == "MAINTAIN":

            final_strategy = strategy_mode

            adaptive_override = False

            adaptive_override_reason = ""

            if strategy_mode == "GROWTH":

                final_action = (
                    "Gradually increase growth exposure "
                    "while monitoring market conditions"
                )

            elif strategy_mode == "MONITOR":

                final_action = (
                    "Maintain current allocation "
                    "and monitor decision conditions closely"
                )

            else:

                final_action = (
                    "Maintain balanced allocation "
                    "and monitor market conditions"
                )


        else:

            final_strategy = strategy_mode

            adaptive_override = False

            adaptive_override_reason = ""

            final_action = (
                "Monitor market conditions "
                "before making allocation changes"
            )

        # ---------------------------------
        # Decision Consistency
        # Step5-3-78
        # ---------------------------------

        if adaptive_override:

            decision_consistency = "OVERRIDDEN"

            decision_consistency_score = 60

            decision_consistency_summary = (
                "Adaptive strategy overrode the original "
                "AI decision due to elevated risk conditions."
            )

        elif decision_alignment == "ALIGNED":

            decision_consistency = "CONSISTENT"

            decision_consistency_score = 100

            decision_consistency_summary = (
                "AI decision and adaptive strategy are "
                "fully aligned."
            )

        elif decision_alignment == "CONFLICT":

            decision_consistency = "CONFLICT"

            decision_consistency_score = 40

            decision_consistency_summary = (
                "AI decision and adaptive strategy show "
                "conflicting signals."
            )

        else:

            decision_consistency = "UNKNOWN"

            decision_consistency_score = 0

            decision_consistency_summary = (
                "Decision consistency could not be determined."
            )

        return {
            "decision": decision,
            "market_view": market_view,
            "confidence": confidence,
            "reliability": reliability_level,

            "decision_consistency": decision_consistency,
            "decision_consistency_score": decision_consistency_score,
            "decision_consistency_summary": decision_consistency_summary,

            "strategy_mode": strategy_mode,

            "adaptive_action": adaptive_action,
            "adaptive_confidence": adaptive_confidence,
            "adaptive_score": adaptive_score,
            "adaptive_direction": adaptive_direction,
            "adaptive_stability": adaptive_stability,
            "adaptive_momentum": adaptive_momentum,
            "adaptive_grade_stability": adaptive_grade_stability,
            "adaptive_consistency": adaptive_consistency,
            "adaptive_summary": adaptive_summary,

            "outcome_learning_signal": outcome_learning_signal,
            "outcome_learning_signal_strength": outcome_learning_signal_strength,
            "adaptive_learning_required": adaptive_learning_required,

            "adaptive_override": adaptive_override,
            "adaptive_override_reason": adaptive_override_reason,
            "decision_alignment": decision_alignment,
            "final_strategy": final_strategy,

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
