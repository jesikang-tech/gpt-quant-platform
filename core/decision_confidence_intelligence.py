"""
GPT Quant Platform

AI Decision Confidence Intelligence

Step5-3-80
"""


class DecisionConfidenceIntelligence:

    def calculate(
        self,
        decision_quality,
        reliability,
        adaptive_strategy,
        decision_consistency_score,
        rebalance,
        optimization
    ):
        """
        Calculate independent AI Decision Confidence Intelligence.

        Components:
            Reliability           : 25%
            Decision Consistency  : 25%
            Adaptive Strategy     : 15%
            Decision Quality      : 15%
            Rebalance             : 10%
            Optimization          : 10%
        """

        decision_quality = decision_quality or {}
        reliability = reliability or {}
        adaptive_strategy = adaptive_strategy or {}
        rebalance = rebalance or {}
        optimization = optimization or {}

        reliability_score = self._normalize(
            reliability.get(
                "confidence",
                reliability.get(
                    "reliability_score",
                    0
                )
            )
        )

        consistency_score = self._normalize(
            decision_consistency_score
        )

        adaptive_score = self._normalize(
            adaptive_strategy.get(
                "strategy_score",
                adaptive_strategy.get(
                    "confidence",
                    0
                )
            )
        )

        quality_score = self._get_quality_score(
            decision_quality
        )

        rebalance_score = self._normalize(
            rebalance.get(
                "rebalance_score",
                rebalance.get(
                    "confidence",
                    0
                )
            )
        )

        optimization_score = self._normalize(
            optimization.get(
                "optimization_score",
                0
            )
        )

        confidence_score = (
            reliability_score * 0.25
            + consistency_score * 0.25
            + adaptive_score * 0.15
            + quality_score * 0.15
            + rebalance_score * 0.10
            + optimization_score * 0.10
        )

        confidence_score = round(
            confidence_score,
            1
        )

        confidence_level = self._get_level(
            confidence_score
        )

        confidence_grade = self._get_grade(
            confidence_score
        )

        confidence_status = self._get_status(
            confidence_score
        )

        confidence_summary = self._get_summary(
            confidence_score,
            confidence_status
        )

        return {
            "confidence_score":
                confidence_score,

            "confidence_level":
                confidence_level,

            "confidence_grade":
                confidence_grade,

            "confidence_status":
                confidence_status,

            "confidence_summary":
                confidence_summary,

            "components": {
                "reliability":
                    reliability_score,

                "decision_consistency":
                    consistency_score,

                "adaptive_strategy":
                    adaptive_score,

                "decision_quality":
                    quality_score,

                "rebalance":
                    rebalance_score,

                "optimization":
                    optimization_score
            }
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

        return max(
            0,
            min(
                100,
                value
            )
        )

    def _get_quality_score(
        self,
        quality
    ):

        if "quality_score" in quality:

            return self._normalize(
                quality["quality_score"]
            )

        quality_level = str(
            quality.get(
                "quality_level",
                ""
            )
        ).upper()

        mapping = {
            "EXCELLENT": 95,
            "GOOD": 85,
            "NEEDS REVIEW": 60,
            "UNKNOWN": 0
        }

        return mapping.get(
            quality_level,
            0
        )

    @staticmethod
    def _get_level(score):

        if score >= 90:
            return "Very High"

        elif score >= 80:
            return "High"

        elif score >= 70:
            return "Moderate"

        elif score >= 60:
            return "Low"

        else:
            return "Very Low"

    @staticmethod
    def _get_grade(score):

        if score >= 90:
            return "A+"

        elif score >= 80:
            return "A"

        elif score >= 70:
            return "B"

        elif score >= 60:
            return "C"

        else:
            return "D"

    @staticmethod
    def _get_status(score):

        if score >= 90:
            return "STRONG"

        elif score >= 80:
            return "STABLE"

        elif score >= 70:
            return "MODERATE"

        elif score >= 60:
            return "CAUTION"

        else:
            return "WEAK"

    @staticmethod
    def _get_summary(
        score,
        status
    ):

        if status == "STRONG":

            return (
                "Decision confidence is strong "
                "across reliability, consistency "
                "and portfolio intelligence signals."
            )

        elif status == "STABLE":

            return (
                "Decision confidence is stable "
                "with generally supportive "
                "portfolio intelligence signals."
            )

        elif status == "MODERATE":

            return (
                "Decision confidence is moderate "
                "and should be monitored for "
                "changes in supporting signals."
            )

        elif status == "CAUTION":

            return (
                "Decision confidence is limited "
                "and portfolio conditions should "
                "be monitored closely."
            )

        return (
            "Decision confidence is weak "
            "because supporting intelligence "
            "signals are insufficient."
        )