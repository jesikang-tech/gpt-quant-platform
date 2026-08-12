"""
GPT Quant Platform

AI Decision Confidence Explainability Engine

Step5-3-81
"""


class DecisionConfidenceExplainability:

    def explain(
        self,
        decision_confidence
    ):
        """
        Explain AI Decision Confidence Intelligence.

        The engine converts confidence components
        into human-readable positive, supporting,
        and risk signals.
        """

        decision_confidence = (
            decision_confidence or {}
        )

        confidence_score = self._normalize(
            decision_confidence.get(
                "confidence_score",
                0
            )
        )

        confidence_grade = (
            decision_confidence.get(
                "confidence_grade",
                "-"
            )
        )

        confidence_level = (
            decision_confidence.get(
                "confidence_level",
                "-"
            )
        )

        confidence_status = (
            decision_confidence.get(
                "confidence_status",
                "-"
            )
        )

        components = (
            decision_confidence.get(
                "components",
                {}
            )
            or {}
        )

        positive_signals = []
        supporting_signals = []
        risk_signals = []

        self._classify_signal(
            positive_signals,
            supporting_signals,
            risk_signals,
            "Reliability",
            components.get(
                "reliability",
                0
            )
        )

        self._classify_signal(
            positive_signals,
            supporting_signals,
            risk_signals,
            "Decision Consistency",
            components.get(
                "decision_consistency",
                0
            )
        )

        self._classify_signal(
            positive_signals,
            supporting_signals,
            risk_signals,
            "Adaptive Strategy",
            components.get(
                "adaptive_strategy",
                0
            )
        )

        self._classify_signal(
            positive_signals,
            supporting_signals,
            risk_signals,
            "Decision Quality",
            components.get(
                "decision_quality",
                0
            )
        )

        self._classify_signal(
            positive_signals,
            supporting_signals,
            risk_signals,
            "Rebalance",
            components.get(
                "rebalance",
                0
            )
        )

        self._classify_signal(
            positive_signals,
            supporting_signals,
            risk_signals,
            "Optimization",
            components.get(
                "optimization",
                0
            )
        )

        explanation = self._build_explanation(
            confidence_score,
            confidence_level,
            confidence_status,
            positive_signals,
            supporting_signals,
            risk_signals
        )

        return {
            "confidence_score":
                confidence_score,

            "confidence_grade":
                confidence_grade,

            "confidence_level":
                confidence_level,

            "confidence_status":
                confidence_status,

            "positive_signals":
                positive_signals,

            "supporting_signals":
                supporting_signals,

            "risk_signals":
                risk_signals,

            "explanation":
                explanation
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
    def _classify_signal(
        positive_signals,
        supporting_signals,
        risk_signals,
        name,
        value
    ):

        value = DecisionConfidenceExplainability._normalize(
            value
        )

        signal = {
            "name": name,
            "score": value
        }

        if value >= 90:

            positive_signals.append(
                signal
            )

        elif value >= 80:

            supporting_signals.append(
                signal
            )

        else:

            risk_signals.append(
                signal
            )

    @staticmethod
    def _build_explanation(
        confidence_score,
        confidence_level,
        confidence_status,
        positive_signals,
        supporting_signals,
        risk_signals
    ):

        if confidence_score >= 90:

            base = (
                "Decision confidence is very high "
                "with strong supporting intelligence signals."
            )

        elif confidence_score >= 80:

            base = (
                "Decision confidence is high "
                "with generally supportive intelligence signals."
            )

        elif confidence_score >= 70:

            base = (
                "Decision confidence is moderate "
                "and should be monitored."
            )

        else:

            base = (
                "Decision confidence is limited "
                "and supporting signals require attention."
            )

        return (
            f"{base} "
            f"Current confidence level is "
            f"{confidence_level} with status "
            f"{confidence_status}."
        )