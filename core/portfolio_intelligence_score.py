"""
GPT Quant Platform

AI Portfolio Intelligence Score Engine

Step5-3-69
"""


class PortfolioIntelligenceScore:

    def calculate(
        self,
        decision_score,
        decision_quality,
        reliability,
        adaptive_strategy,
        decision_consistency_score,
        rebalance,
        optimization
    ):
        """
        Calculate final AI Portfolio Intelligence Score.

        Components:
            Decision Score        : 30%
            Decision Quality      : 15%
            Reliability           : 15%
            Adaptive Strategy     : 10%
            Decision Consistency  : 10%
            Rebalance             : 10%
            Optimization          : 10%
        """

        decision_score = self._normalize(
            decision_score
        )

        quality_score = self._get_quality_score(
            decision_quality
        )

        reliability_score = self._get_reliability_score(
            reliability
        )

        strategy_score = self._get_strategy_score(
            adaptive_strategy
        )

        consistency_score = self._normalize(
            decision_consistency_score
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

        intelligence_score = (
            decision_score * 0.30
            + quality_score * 0.15
            + reliability_score * 0.15
            + strategy_score * 0.10
            + consistency_score * 0.10
            + rebalance_score * 0.10
            + optimization_score * 0.10
        )

        intelligence_score = round(
            intelligence_score,
            1
        )

        grade = self._get_grade(
            intelligence_score
        )

        level = self._get_level(
            intelligence_score
        )

        return {
            "intelligence_score":
                intelligence_score,

            "grade":
                grade,

            "intelligence_level":
                level,

            "components": {
                "decision_score":
                    decision_score,

                "decision_quality":
                    quality_score,

                "reliability":
                    reliability_score,

                "adaptive_strategy":
                    strategy_score,

                "decision_consistency":
                    consistency_score,

                "rebalance":
                    rebalance_score,

                "optimization":
                    optimization_score
            }
        }

    @staticmethod
    def _normalize(value):
        """
        Convert score to safe 0-100 range.
        """

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
        """
        Convert qualitative decision
        quality into numeric score.
        """

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

    def _get_reliability_score(
        self,
        reliability
    ):
        """
        Reliability score is based
        primarily on confidence.
        """

        return self._normalize(
            reliability.get(
                "confidence",
                reliability.get(
                    "reliability_score",
                    0
                )
            )
        )

    def _get_strategy_score(
        self,
        strategy
    ):
        """
        Adaptive strategy confidence
        is used as the strategy score.
        """

        return self._normalize(
            strategy.get(
                "strategy_score",
                strategy.get(
                    "confidence",
                    0
                )
            )
        )

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
    def _get_level(score):

        if score >= 90:
            return "Excellent"

        elif score >= 80:
            return "Strong"

        elif score >= 70:
            return "Moderate"

        else:
            return "Weak"
