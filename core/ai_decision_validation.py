"""
GPT Quant Platform

AI Decision Validation Engine

Step5-3-84
"""


class AIDecisionValidation:

    def validate(
        self,
        intelligence,
        confidence,
        assessment=None,
        recommendation=None
    ):
        """
        Cross-validate the AI portfolio decision
        against multiple intelligence signals.
        """

        intelligence = intelligence or {}
        confidence = confidence or {}
        assessment = assessment or {}
        recommendation = recommendation or {}

        decision = intelligence.get(
            "decision",
            "UNKNOWN"
        )

        strategy_mode = intelligence.get(
            "strategy_mode",
            "UNKNOWN"
        )

        adaptive_action = intelligence.get(
            "adaptive_action",
            "UNKNOWN"
        )

        decision_alignment = intelligence.get(
            "decision_alignment",
            "UNKNOWN"
        )

        decision_consistency = intelligence.get(
            "decision_consistency",
            "UNKNOWN"
        )

        confidence_score = self._normalize(
            confidence.get(
                "confidence_score",
                intelligence.get(
                    "confidence",
                    0
                )
            )
        )

        confidence_level = confidence.get(
            "confidence_level",
            "UNKNOWN"
        )

        reliability = intelligence.get(
            "reliability",
            "UNKNOWN"
        )

        optimization_status = intelligence.get(
            "optimization_status",
            "UNKNOWN"
        )

        adaptive_override = bool(
            intelligence.get(
                "adaptive_override",
                False
            )
        )

        attention_signals = (
            assessment.get(
                "attention_signals",
                []
            )
            or []
        )

        recommendation_status = recommendation.get(
            "recommendation",
            "UNKNOWN"
        )

        validation_signals = []
        risk_signals = []

        # ---------------------------------
        # Decision Alignment
        # ---------------------------------

        if decision_alignment == "ALIGNED":

            validation_signals.append(
                {
                    "name": "Decision Alignment",
                    "status": "PASS",
                    "value": decision_alignment
                }
            )

        elif decision_alignment == "CONFLICT":

            validation_signals.append(
                {
                    "name": "Decision Alignment",
                    "status": "FAIL",
                    "value": decision_alignment
                }
            )

            risk_signals.append(
                "Decision and adaptive strategy conflict."
            )

        else:

            validation_signals.append(
                {
                    "name": "Decision Alignment",
                    "status": "REVIEW",
                    "value": decision_alignment
                }
            )

        # ---------------------------------
        # Decision Consistency
        # ---------------------------------

        if decision_consistency == "CONSISTENT":

            validation_signals.append(
                {
                    "name": "Decision Consistency",
                    "status": "PASS",
                    "value": decision_consistency
                }
            )

        elif decision_consistency in (
            "CONFLICT",
            "OVERRIDDEN"
        ):

            validation_signals.append(
                {
                    "name": "Decision Consistency",
                    "status": "FAIL",
                    "value": decision_consistency
                }
            )

            risk_signals.append(
                "Decision consistency indicates a conflict or override."
            )

        else:

            validation_signals.append(
                {
                    "name": "Decision Consistency",
                    "status": "REVIEW",
                    "value": decision_consistency
                }
            )

        # ---------------------------------
        # Confidence
        # ---------------------------------

        if confidence_score >= 80:

            validation_signals.append(
                {
                    "name": "Confidence",
                    "status": "PASS",
                    "value": confidence_score
                }
            )

        elif confidence_score >= 60:

            validation_signals.append(
                {
                    "name": "Confidence",
                    "status": "REVIEW",
                    "value": confidence_score
                }
            )

            risk_signals.append(
                "Decision confidence is moderate."
            )

        else:

            validation_signals.append(
                {
                    "name": "Confidence",
                    "status": "FAIL",
                    "value": confidence_score
                }
            )

            risk_signals.append(
                "Decision confidence is low."
            )

        # ---------------------------------
        # Reliability
        # ---------------------------------

        if reliability in (
            "HIGH",
            "VERY_HIGH",
            "Very High"
        ):

            validation_signals.append(
                {
                    "name": "Reliability",
                    "status": "PASS",
                    "value": reliability
                }
            )

        elif reliability in (
            "MEDIUM",
            "MODERATE"
        ):

            validation_signals.append(
                {
                    "name": "Reliability",
                    "status": "REVIEW",
                    "value": reliability
                }
            )

            risk_signals.append(
                "Decision reliability requires monitoring."
            )

        else:

            validation_signals.append(
                {
                    "name": "Reliability",
                    "status": "REVIEW",
                    "value": reliability
                }
            )

        # ---------------------------------
        # Optimization
        # ---------------------------------

        if optimization_status == "COMPLETED":

            validation_signals.append(
                {
                    "name": "Optimization",
                    "status": "PASS",
                    "value": optimization_status
                }
            )

        else:

            validation_signals.append(
                {
                    "name": "Optimization",
                    "status": "REVIEW",
                    "value": optimization_status
                }
            )

            risk_signals.append(
                "Portfolio optimization is not completed."
            )

        # ---------------------------------
        # Adaptive Override
        # ---------------------------------

        if adaptive_override:

            validation_signals.append(
                {
                    "name": "Adaptive Override",
                    "status": "FAIL",
                    "value": True
                }
            )

            risk_signals.append(
                "Adaptive strategy overrode the original AI decision."
            )

        else:

            validation_signals.append(
                {
                    "name": "Adaptive Override",
                    "status": "PASS",
                    "value": False
                }
            )

        # ---------------------------------
        # Confidence Risk
        # ---------------------------------

        if attention_signals:

            validation_signals.append(
                {
                    "name": "Confidence Risk",
                    "status": "REVIEW",
                    "value": len(attention_signals)
                }
            )

            for signal in attention_signals:

                if isinstance(signal, dict):

                    risk_signals.append(
                        signal.get(
                            "name",
                            "Unknown"
                        )
                    )

                else:

                    risk_signals.append(
                        str(signal)
                    )

        else:

            validation_signals.append(
                {
                    "name": "Confidence Risk",
                    "status": "PASS",
                    "value": "NONE"
                }
            )

        # ---------------------------------
        # Final Validation
        # ---------------------------------

        failed = sum(
            1
            for signal in validation_signals
            if signal["status"] == "FAIL"
        )

        review = sum(
            1
            for signal in validation_signals
            if signal["status"] == "REVIEW"
        )

        if failed >= 3:

            validation = "INVALID"

        elif failed >= 1 or review >= 2:

            validation = "REVIEW_REQUIRED"

        else:

            validation = "VALID"

        validation_score = self._calculate_score(
            validation_signals
        )

        summary = self._build_summary(
            validation,
            decision,
            strategy_mode,
            confidence_score
        )

        return {
            "validation": validation,
            "validation_status": validation,
            "validation_score": validation_score,
            "decision": decision,
            "strategy_mode": strategy_mode,
            "adaptive_action": adaptive_action,
            "decision_alignment": decision_alignment,
            "decision_consistency": decision_consistency,
            "confidence_score": confidence_score,
            "confidence_level": confidence_level,
            "reliability": reliability,
            "optimization_status": optimization_status,
            "adaptive_override": adaptive_override,
            "recommendation": recommendation_status,
            "validation_signals": validation_signals,
            "risk_signals": risk_signals,
            "summary": summary
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
    def _calculate_score(signals):

        if not signals:
            return 0

        weights = {
            "PASS": 100,
            "REVIEW": 60,
            "FAIL": 20
        }

        total = sum(
            weights.get(
                signal.get("status"),
                0
            )
            for signal in signals
        )

        return round(
            total / len(signals),
            1
        )

    @staticmethod
    def _build_summary(
        validation,
        decision,
        strategy_mode,
        confidence_score
    ):

        if validation == "VALID":

            return (
                f"AI decision {decision} is validated "
                f"against adaptive strategy {strategy_mode} "
                f"and supporting intelligence signals. "
                f"Confidence is {confidence_score}/100."
            )

        if validation == "REVIEW_REQUIRED":

            return (
                f"AI decision {decision} requires review "
                f"because one or more intelligence signals "
                f"require additional validation. "
                f"Confidence is {confidence_score}/100."
            )

        return (
            f"AI decision {decision} failed validation "
            f"because critical intelligence signals conflict. "
            f"Confidence is {confidence_score}/100."
        )