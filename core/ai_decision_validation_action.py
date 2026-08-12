"""
GPT Quant Platform

AI Decision Validation Action Engine

Step5-3-86
"""


class AIDecisionValidationAction:

    def decide(
        self,
        validation,
        confidence=None,
        assessment=None,
        recommendation=None
    ):
        """
        Determine the final executable action
        from AI decision validation intelligence.
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
            confidence.get(
                "confidence_score",
                validation.get(
                    "confidence_score",
                    0
                )
            )
        )

        confidence_level = confidence.get(
            "confidence_level",
            validation.get(
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

        recommendation_status = recommendation.get(
            "recommendation",
            validation.get(
                "recommendation",
                "REVIEW"
            )
        )

        action = self._determine_action(
            validation_status,
            validation_score,
            confidence_score,
            recommendation_status,
            adaptive_action,
            decision
        )

        execution_status = self._determine_execution_status(
            action,
            validation_status
        )

        monitoring = self._determine_monitoring(
            action,
            validation_status,
            confidence_score
        )

        risk_level = self._determine_risk_level(
            validation_status,
            validation_score,
            confidence_score,
            decision_alignment,
            decision_consistency
        )

        action_reason = self._build_reason(
            action,
            validation_status,
            validation_score,
            confidence_score,
            recommendation_status
        )

        summary = self._build_summary(
            action,
            execution_status,
            monitoring,
            risk_level,
            decision
        )

        return {
            "action": action,
            "execution_status": execution_status,
            "monitoring": monitoring,
            "risk_level": risk_level,
            "validation_status": validation_status,
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
            "recommendation": recommendation_status,
            "action_reason": action_reason,
            "summary": summary
        }

    @staticmethod
    def _determine_action(
        validation_status,
        validation_score,
        confidence_score,
        recommendation,
        adaptive_action,
        decision
    ):

        if validation_status == "INVALID":
            return "BLOCK_EXECUTION"

        if validation_status == "REVIEW_REQUIRED":

            if (
                confidence_score >= 80
                and validation_score >= 70
            ):
                return "PROCEED_WITH_MONITORING"

            return "REVIEW_REQUIRED"

        if (
            validation_status == "VALID"
            and validation_score >= 90
            and confidence_score >= 90
        ):
            if recommendation == "PROCEED":
                return "PROCEED"

            if recommendation == "PROCEED_WITH_MONITORING":
                return "PROCEED_WITH_MONITORING"

            if adaptive_action:
                return adaptive_action

            if decision:
                return decision

        if confidence_score >= 80:
            return "PROCEED_WITH_MONITORING"

        return "REVIEW_REQUIRED"

    @staticmethod
    def _determine_execution_status(
        action,
        validation_status
    ):

        if action == "PROCEED":
            return "AUTHORIZED"

        if action == "PROCEED_WITH_MONITORING":
            return "AUTHORIZED_WITH_MONITORING"

        if action == "BLOCK_EXECUTION":
            return "BLOCKED"

        if action == "REVIEW_REQUIRED":
            return "PENDING_REVIEW"

        return "UNDETERMINED"

    @staticmethod
    def _determine_monitoring(
        action,
        validation_status,
        confidence_score
    ):

        if action == "PROCEED":
            return "STANDARD"

        if action == "PROCEED_WITH_MONITORING":
            return "ELEVATED"

        if action == "REVIEW_REQUIRED":
            return "HIGH"

        if action == "BLOCK_EXECUTION":
            return "CRITICAL"

        if validation_status == "VALID":
            return "STANDARD"

        if confidence_score >= 80:
            return "ELEVATED"

        return "HIGH"

    @staticmethod
    def _determine_risk_level(
        validation_status,
        validation_score,
        confidence_score,
        decision_alignment,
        decision_consistency
    ):

        if validation_status == "INVALID":
            return "CRITICAL"

        if (
            validation_status == "REVIEW_REQUIRED"
            and (
                decision_alignment == "CONFLICT"
                or decision_consistency == "CONFLICT"
            )
        ):
            return "HIGH"

        if validation_score < 70:
            return "HIGH"

        if confidence_score < 70:
            return "HIGH"

        if validation_score < 90:
            return "MEDIUM"

        if confidence_score < 90:
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _build_reason(
        action,
        validation_status,
        validation_score,
        confidence_score,
        recommendation
    ):

        if action == "PROCEED":

            return (
                "AI decision validation is strong enough "
                "to authorize execution. Validation score is "
                f"{validation_score}/100 and confidence is "
                f"{confidence_score}/100."
            )

        if action == "PROCEED_WITH_MONITORING":

            return (
                "AI decision validation supports execution "
                "with increased monitoring. Validation score is "
                f"{validation_score}/100 and confidence is "
                f"{confidence_score}/100."
            )

        if action == "REVIEW_REQUIRED":

            return (
                "AI decision validation requires additional "
                "review before execution. Validation status is "
                f"{validation_status} and confidence is "
                f"{confidence_score}/100."
            )

        if action == "BLOCK_EXECUTION":

            return (
                "AI decision execution is blocked because "
                "validation identified critical conflicts or "
                "insufficient supporting intelligence."
            )

        return (
            "AI decision action could not be determined "
            f"from the current validation status {validation_status}."
        )

    @staticmethod
    def _build_summary(
        action,
        execution_status,
        monitoring,
        risk_level,
        decision
    ):

        return (
            f"AI decision {decision} resulted in action "
            f"{action}. Execution status is {execution_status}, "
            f"monitoring level is {monitoring}, and risk level "
            f"is {risk_level}."
        )

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