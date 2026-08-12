"""
GPT Quant Platform

AI Decision Confidence Recommendation Engine

Step5-3-83
"""


class DecisionConfidenceRecommendation:

    def recommend(
        self,
        assessment,
        decision
    ):
        """
        Convert AI Decision Confidence Assessment
        into an actionable recommendation.
        """

        assessment = assessment or {}
        decision = decision or {}

        confidence_score = self._normalize(
            assessment.get(
                "confidence_score",
                0
            )
        )

        assessment_level = (
            assessment.get(
                "assessment",
                "NEEDS_ATTENTION"
            )
        )

        attention_signals = (
            assessment.get(
                "attention_signals",
                []
            )
            or []
        )

        decision_action = (
            decision.get(
                "adaptive_action",
                decision.get(
                    "rebalance_action",
                    "REVIEW"
                )
            )
        )

        recommendation = (
            self._determine_recommendation(
                confidence_score,
                assessment_level,
                attention_signals
            )
        )

        monitoring = (
            self._determine_monitoring(
                recommendation,
                attention_signals
            )
        )

        action = (
            self._determine_action(
                recommendation,
                decision_action
            )
        )

        summary = (
            self._build_summary(
                recommendation,
                action,
                monitoring,
                confidence_score,
                assessment_level
            )
        )

        return {
            "recommendation":
                recommendation,

            "action":
                action,

            "monitoring":
                monitoring,

            "recommendation_score":
                confidence_score,

            "assessment":
                assessment_level,

            "summary":
                summary
        }

    @staticmethod
    def _normalize(value):

        try:
            value = float(value or 0)

        except (
            TypeError,
            ValueError
        ):
            value = 0

        return round(
            max(
                0,
                min(
                    100,
                    value
                )
            ),
            1
        )

    @staticmethod
    def _determine_recommendation(
        confidence_score,
        assessment,
        attention_signals
    ):

        if (
            assessment == "VERY_STRONG"
            and confidence_score >= 90
            and not attention_signals
        ):
            return "PROCEED"

        if (
            assessment == "STRONG"
            and confidence_score >= 80
            and not attention_signals
        ):
            return "PROCEED_WITH_MONITORING"

        if (
            assessment == "MODERATE"
            or confidence_score >= 70
        ):
            return "MONITOR"

        return "REVIEW"

    @staticmethod
    def _determine_monitoring(
        recommendation,
        attention_signals
    ):

        if attention_signals:
            return "HIGH"

        if recommendation == "PROCEED":
            return "STANDARD"

        if recommendation == "PROCEED_WITH_MONITORING":
            return "ELEVATED"

        if recommendation == "MONITOR":
            return "ELEVATED"

        return "HIGH"

    @staticmethod
    def _determine_action(
        recommendation,
        decision_action
    ):

        if recommendation == "PROCEED":
            return decision_action

        if recommendation == "PROCEED_WITH_MONITORING":
            return decision_action

        if recommendation == "MONITOR":
            return "MONITOR_ALLOCATION"

        return "REVIEW_ALLOCATION"

    @staticmethod
    def _build_summary(
        recommendation,
        action,
        monitoring,
        confidence_score,
        assessment
    ):

        if recommendation == "PROCEED":

            base = (
                "Decision confidence supports proceeding "
                "with the current AI portfolio action."
            )

        elif recommendation == "PROCEED_WITH_MONITORING":

            base = (
                "Decision confidence supports the current "
                "AI portfolio action with increased monitoring."
            )

        elif recommendation == "MONITOR":

            base = (
                "Decision confidence is moderate and "
                "the portfolio action should be monitored."
            )

        else:

            base = (
                "Decision confidence requires review "
                "before proceeding with the portfolio action."
            )

        return (
            f"{base} Assessment is {assessment} with "
            f"confidence score {confidence_score}/100. "
            f"Recommended action is {action} with "
            f"{monitoring.lower()} monitoring."
        )