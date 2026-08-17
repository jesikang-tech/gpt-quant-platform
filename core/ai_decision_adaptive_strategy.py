"""
AI Decision Adaptive Strategy Engine
Step5-3-73

Generate adaptive strategy recommendations
based on AI decision trend, stability,
momentum, grade stability, and consistency.
"""


class AIDecisionAdaptiveStrategy:

    def analyze(
        self,
        trend,
        outcome_intelligence=None
    ):

        if not trend:
            trend = {}

        if outcome_intelligence is None:
            outcome_intelligence = {}

        direction = trend.get(
            "direction",
            "STABLE"
        )

        # --------------------------------
        # Step6-10-F-12
        # Outcome Intelligence → Adaptive Strategy
        # --------------------------------
        outcome_learning_signal = (
            outcome_intelligence.get(
                "outcome_learning_signal",
                "NONE"
            )
        )

        outcome_learning_signal_strength = (
            outcome_intelligence.get(
                "outcome_learning_signal_strength",
                0.0
            )
        )

        adaptive_learning_required = bool(
            outcome_intelligence.get(
                "adaptive_learning_required",
                False
            )
        )

        stability = trend.get(
            "stability",
            "UNKNOWN"
        )

        momentum = trend.get(
            "momentum",
            "NEUTRAL"
        )

        grade_stability = trend.get(
            "grade_stability",
            "UNKNOWN"
        )

        consistency = trend.get(
            "consistency",
            "UNKNOWN"
        )

        score = trend.get(
            "latest_score",
            0
        )

        strategy = self._determine_strategy(
            direction,
            stability,
            momentum,
            grade_stability,
            consistency
        )

        # --------------------------------
        # Outcome learning override
        # --------------------------------
        strategy = self._apply_outcome_learning(
            strategy,
            outcome_learning_signal,
            outcome_learning_signal_strength,
            adaptive_learning_required
        )

        confidence = self._calculate_confidence(
            stability,
            grade_stability,
            consistency
        )

        action = self._determine_action(
            strategy
        )

        summary = self._generate_summary(
            strategy,
            action,
            direction,
            momentum,
            stability
        )

        return {
            "strategy": strategy,
            "action": action,
            "confidence": confidence,
            "score": score,
            "direction": direction,
            "stability": stability,
            "momentum": momentum,
            "grade_stability": grade_stability,
            "consistency": consistency,
            "outcome_learning_signal":
                outcome_learning_signal,
            "outcome_learning_signal_strength":
                outcome_learning_signal_strength,
            "adaptive_learning_required":
                adaptive_learning_required,
            "summary": summary
        }


    def _apply_outcome_learning(
        self,
        strategy,
        learning_signal,
        learning_signal_strength,
        adaptive_learning_required
    ):
        """
        Step6-10-F-12

        Connect evaluated outcome intelligence to
        the existing adaptive strategy engine.

        Negative learning signals can force a
        defensive posture when adaptive learning
        is explicitly required.
        """

        if not adaptive_learning_required:
            return strategy

        if learning_signal == "NEGATIVE":
            return "DEFENSIVE"

        if (
            learning_signal == "POSITIVE"
            and learning_signal_strength >= 0.7
            and strategy == "BALANCED"
        ):
            return "GROWTH"

        return strategy


    def _determine_strategy(
        self,
        direction,
        stability,
        momentum,
        grade_stability,
        consistency
    ):

        if stability == "LOW":
            return "CAUTIOUS"

        if (
            direction == "DOWN"
            and momentum == "NEGATIVE"
        ):
            return "DEFENSIVE"

        if (
            direction == "UP"
            and momentum == "POSITIVE"
            and stability in (
                "HIGH",
                "MEDIUM"
            )
        ):
            return "GROWTH"

        if (
            direction == "STABLE"
            and stability == "HIGH"
            and consistency == "HIGH"
        ):
            return "MAINTAIN"

        if (
            grade_stability == "CHANGING"
            or consistency == "LOW"
        ):
            return "MONITOR"

        return "BALANCED"


    def _calculate_confidence(
        self,
        stability,
        grade_stability,
        consistency
    ):

        confidence = 50

        if stability == "HIGH":
            confidence += 20

        elif stability == "MEDIUM":
            confidence += 10

        if grade_stability == "STABLE":
            confidence += 10

        if consistency == "HIGH":
            confidence += 20

        elif consistency == "MEDIUM":
            confidence += 10

        return min(
            confidence,
            100
        )


    def _determine_action(
        self,
        strategy
    ):

        actions = {
            "GROWTH": "INCREASE_RISK",
            "DEFENSIVE": "REDUCE_RISK",
            "MAINTAIN": "MAINTAIN_ALLOCATION",
            "CAUTIOUS": "LIMIT_EXPOSURE",
            "MONITOR": "MONITOR_CLOSELY",
            "BALANCED": "MAINTAIN_BALANCE"
        }

        return actions.get(
            strategy,
            "MONITOR_CLOSELY"
        )


    def _generate_summary(
        self,
        strategy,
        action,
        direction,
        momentum,
        stability
    ):

        return (
            f"Adaptive strategy is {strategy}. "
            f"Recommended action is {action}. "
            f"AI decision direction is {direction}, "
            f"momentum is {momentum}, "
            f"and stability is {stability.lower()}."
        )


    @staticmethod
    def _empty_result():

        return {
            "strategy": "MONITOR",
            "action": "MONITOR_CLOSELY",
            "confidence": 0,
            "score": 0,
            "direction": "STABLE",
            "stability": "UNKNOWN",
            "momentum": "NEUTRAL",
            "grade_stability": "UNKNOWN",
            "consistency": "UNKNOWN",
            "summary": (
                "AI adaptive strategy data "
                "is unavailable."
            )
        }