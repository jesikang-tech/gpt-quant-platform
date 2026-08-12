"""
GPT Quant Platform

AI Decision Validation Explainability Engine

Step5-3-85
"""


class AIDecisionValidationExplainability:

    def explain(
        self,
        validation,
        confidence=None,
        assessment=None,
        recommendation=None
    ):
        """
        Explain why the AI decision validation
        is VALID, REVIEW_REQUIRED, or requires attention.
        """

        validation = validation or {}
        confidence = confidence or {}
        assessment = assessment or {}
        recommendation = recommendation or {}

        validation_status = validation.get(
            "validation",
            validation.get(
                "validation_status",
                "UNKNOWN"
            )
        )

        validation_score = self._normalize(
            validation.get(
                "validation_score",
                0
            )
        )

        decision = validation.get(
            "decision",
            "UNKNOWN"
        )

        strategy_mode = validation.get(
            "strategy_mode",
            "UNKNOWN"
        )

        adaptive_action = validation.get(
            "adaptive_action",
            "UNKNOWN"
        )

        decision_alignment = validation.get(
            "decision_alignment",
            "UNKNOWN"
        )

        decision_consistency = validation.get(
            "decision_consistency",
            "UNKNOWN"
        )

        confidence_score = self._normalize(
            validation.get(
                "confidence_score",
                confidence.get(
                    "confidence_score",
                    0
                )
            )
        )

        confidence_level = validation.get(
            "confidence_level",
            confidence.get(
                "confidence_level",
                "UNKNOWN"
            )
        )

        reliability = validation.get(
            "reliability",
            "UNKNOWN"
        )

        optimization_status = validation.get(
            "optimization_status",
            "UNKNOWN"
        )

        validation_signals = (
            validation.get(
                "validation_signals",
                []
            )
            or []
        )

        risk_signals = (
            validation.get(
                "risk_signals",
                []
            )
            or []
        )

        attention_signals = (
            assessment.get(
                "attention_signals",
                []
            )
            or []
        )

        recommendation_value = recommendation.get(
            "recommendation",
            validation.get(
                "recommendation",
                "UNKNOWN"
            )
        )

        positive_signals = self._extract_positive_signals(
            validation_signals
        )

        explanation = self._build_explanation(
            validation_status,
            decision,
            strategy_mode,
            decision_alignment,
            decision_consistency,
            confidence_score,
            confidence_level,
            reliability,
            optimization_status
        )

        risk_explanation = self._build_risk_explanation(
            validation_status,
            risk_signals,
            attention_signals
        )

        conclusion = self._build_conclusion(
            validation_status,
            decision,
            recommendation_value
        )

        return {
            "validation_status":
                validation_status,

            "validation_score":
                validation_score,

            "decision":
                decision,

            "strategy_mode":
                strategy_mode,

            "adaptive_action":
                adaptive_action,

            "decision_alignment":
                decision_alignment,

            "decision_consistency":
                decision_consistency,

            "confidence_score":
                confidence_score,

            "confidence_level":
                confidence_level,

            "reliability":
                reliability,

            "optimization_status":
                optimization_status,

            "recommendation":
                recommendation_value,

            "positive_signals":
                positive_signals,

            "risk_signals":
                risk_signals,

            "attention_signals":
                attention_signals,

            "explanation":
                explanation,

            "risk_explanation":
                risk_explanation,

            "conclusion":
                conclusion
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
    def _extract_positive_signals(
        validation_signals
    ):

        positive_signals = []

        for signal in validation_signals:

            if not isinstance(
                signal,
                dict
            ):
                continue

            status = signal.get(
                "status",
                ""
            )

            if status == "PASS":

                positive_signals.append(
                    {
                        "name": signal.get(
                            "name",
                            "UNKNOWN"
                        ),
                        "value": signal.get(
                            "value",
                            ""
                        )
                    }
                )

        return positive_signals

    @staticmethod
    def _build_explanation(
        validation_status,
        decision,
        strategy_mode,
        decision_alignment,
        decision_consistency,
        confidence_score,
        confidence_level,
        reliability,
        optimization_status
    ):

        if validation_status == "VALID":

            return (
                f"AI decision {decision} is validated "
                f"against adaptive strategy {strategy_mode}. "
                f"Decision alignment is {decision_alignment}, "
                f"decision consistency is {decision_consistency}, "
                f"confidence is {confidence_level} at "
                f"{confidence_score}/100, reliability is "
                f"{reliability}, and optimization status is "
                f"{optimization_status}."
            )

        if validation_status == "REVIEW_REQUIRED":

            return (
                f"AI decision {decision} requires additional "
                f"validation because one or more supporting "
                f"intelligence signals require review. "
                f"Decision alignment is {decision_alignment}, "
                f"decision consistency is {decision_consistency}, "
                f"confidence is {confidence_level} at "
                f"{confidence_score}/100, reliability is "
                f"{reliability}."
            )

        return (
            f"AI decision {decision} could not be fully "
            f"validated. Current validation status is "
            f"{validation_status}."
        )

    @staticmethod
    def _build_risk_explanation(
        validation_status,
        risk_signals,
        attention_signals
    ):

        risks = list(
            risk_signals
        )

        for signal in attention_signals:

            if isinstance(
                signal,
                dict
            ):

                name = signal.get(
                    "name",
                    "UNKNOWN"
                )

                if name not in risks:
                    risks.append(name)

        if not risks:

            if validation_status == "VALID":
                return "No material validation risks were detected."

            return (
                "Validation requires review even though "
                "no specific risk signal was provided."
            )

        return (
            "Validation risk factors: "
            + "; ".join(
                str(risk)
                for risk in risks
            )
            + "."
        )

    @staticmethod
    def _build_conclusion(
        validation_status,
        decision,
        recommendation
    ):

        if validation_status == "VALID":

            return (
                f"The current AI decision {decision} "
                f"is sufficiently supported by the "
                f"available intelligence signals. "
                f"Current recommendation is "
                f"{recommendation}."
            )

        if validation_status == "REVIEW_REQUIRED":

            return (
                f"The current AI decision {decision} "
                f"should be reviewed before execution. "
                f"Current recommendation is "
                f"{recommendation}."
            )

        return (
            f"The current AI decision {decision} "
            f"requires further validation before "
            f"execution."
        )