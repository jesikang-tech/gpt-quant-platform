"""
GPT Quant Platform

AI Final Decision Governance Engine

Step5-3-88
"""


class AIFinalDecisionGovernance:

    def govern(
        self,
        final_decision,
        intelligence=None,
        intelligence_score=None,
        confidence=None,
        validation=None,
        validation_action=None
    ):
        """
        Evaluate whether the final AI decision
        satisfies governance and execution requirements.
        """

        final_decision = final_decision or {}
        intelligence = intelligence or {}
        intelligence_score = intelligence_score or {}
        confidence = confidence or {}
        validation = validation or {}
        validation_action = validation_action or {}

        decision = final_decision.get(
            "decision",
            "UNKNOWN"
        )

        action = final_decision.get(
            "action",
            "UNKNOWN"
        )

        execution_status = final_decision.get(
            "execution_status",
            "UNKNOWN"
        )

        validation_status = final_decision.get(
            "validation_status",
            validation.get(
                "validation_status",
                validation.get(
                    "validation",
                    "UNKNOWN"
                )
            )
        )

        validation_score = self._normalize(
            final_decision.get(
                "validation_score",
                validation.get(
                    "validation_score",
                    0
                )
            )
        )

        confidence_score = self._normalize(
            final_decision.get(
                "confidence_score",
                confidence.get(
                    "confidence_score",
                    0
                )
            )
        )

        intelligence_score_value = self._extract_intelligence_score(
            final_decision,
            intelligence_score
        )

        decision_alignment = final_decision.get(
            "decision_alignment",
            validation.get(
                "decision_alignment",
                "UNKNOWN"
            )
        )

        decision_consistency = final_decision.get(
            "decision_consistency",
            validation.get(
                "decision_consistency",
                "UNKNOWN"
            )
        )

        reliability = final_decision.get(
            "reliability",
            validation.get(
                "reliability",
                "UNKNOWN"
            )
        )

        optimization_status = final_decision.get(
            "optimization_status",
            validation.get(
                "optimization_status",
                "UNKNOWN"
            )
        )

        adaptive_action = final_decision.get(
            "adaptive_action",
            validation.get(
                "adaptive_action",
                "UNKNOWN"
            )
        )

        recommendation = final_decision.get(
            "recommendation",
            validation_action.get(
                "recommendation",
                "UNKNOWN"
            )
        )

        integrity_status = self._determine_integrity(
            decision,
            action,
            execution_status,
            validation_status,
            validation_score,
            confidence_score,
            decision_alignment,
            decision_consistency
        )

        stability_status = self._determine_stability(
            decision_alignment,
            decision_consistency,
            confidence_score,
            reliability,
            adaptive_action
        )

        execution_readiness = self._determine_execution_readiness(
            integrity_status,
            validation_status,
            action,
            execution_status,
            confidence_score,
            validation_score
        )

        risk_governance = self._determine_risk_governance(
            integrity_status,
            stability_status,
            confidence_score,
            validation_score,
            reliability
        )

        override_status = self._determine_override_status(
            final_decision,
            validation,
            intelligence
        )

        monitoring_policy = self._determine_monitoring_policy(
            execution_readiness,
            risk_governance,
            confidence_score
        )

        governance_score = self._calculate_governance_score(
            integrity_status,
            stability_status,
            execution_readiness,
            risk_governance,
            override_status,
            confidence_score,
            validation_score,
            intelligence_score_value
        )

        governance_status = self._determine_governance_status(
            governance_score,
            execution_readiness,
            risk_governance,
            override_status
        )

        governance_reason = self._build_reason(
            governance_status,
            decision,
            action,
            integrity_status,
            stability_status,
            execution_readiness,
            risk_governance
        )

        summary = self._build_summary(
            decision,
            action,
            governance_status,
            governance_score,
            monitoring_policy
        )

        return {
            "governance_status": governance_status,
            "governance_score": governance_score,
            "decision": decision,
            "action": action,
            "execution_status": execution_status,
            "integrity_status": integrity_status,
            "stability_status": stability_status,
            "execution_readiness": execution_readiness,
            "risk_governance": risk_governance,
            "override_status": override_status,
            "monitoring_policy": monitoring_policy,
            "validation_status": validation_status,
            "validation_score": validation_score,
            "confidence_score": confidence_score,
            "intelligence_score": intelligence_score_value,
            "decision_alignment": decision_alignment,
            "decision_consistency": decision_consistency,
            "reliability": reliability,
            "optimization_status": optimization_status,
            "adaptive_action": adaptive_action,
            "recommendation": recommendation,
            "governance_reason": governance_reason,
            "summary": summary
        }

    @staticmethod
    def _determine_integrity(
        decision,
        action,
        execution_status,
        validation_status,
        validation_score,
        confidence_score,
        decision_alignment,
        decision_consistency
    ):

        if decision == "UNKNOWN":
            return "BROKEN"

        if action == "UNKNOWN":
            return "BROKEN"

        if execution_status == "UNKNOWN":
            return "BROKEN"

        if validation_status == "INVALID":
            return "BROKEN"

        if validation_score < 70:
            return "DEGRADED"

        if confidence_score < 70:
            return "DEGRADED"

        if decision_alignment == "CONFLICT":
            return "DEGRADED"

        if decision_consistency == "CONFLICT":
            return "DEGRADED"

        return "INTACT"

    @staticmethod
    def _determine_stability(
        decision_alignment,
        decision_consistency,
        confidence_score,
        reliability,
        adaptive_action
    ):

        if (
            decision_alignment == "CONFLICT"
            or decision_consistency == "CONFLICT"
        ):
            return "UNSTABLE"

        if confidence_score < 70:
            return "UNSTABLE"

        if reliability == "LOW":
            return "UNSTABLE"

        if adaptive_action in (
            None,
            "",
            "UNKNOWN"
        ):
            return "WATCH"

        if confidence_score < 90:
            return "WATCH"

        return "STABLE"

    @staticmethod
    def _determine_execution_readiness(
        integrity_status,
        validation_status,
        action,
        execution_status,
        confidence_score,
        validation_score
    ):

        if integrity_status == "BROKEN":
            return "NOT_READY"

        if validation_status == "INVALID":
            return "NOT_READY"

        if action == "BLOCK_EXECUTION":
            return "NOT_READY"

        if execution_status == "BLOCKED":
            return "NOT_READY"

        if (
            confidence_score >= 90
            and validation_score >= 90
            and execution_status == "AUTHORIZED"
        ):
            return "READY"

        if (
            confidence_score >= 80
            and validation_score >= 80
        ):
            return "CONDITIONAL"

        return "NOT_READY"

    @staticmethod
    def _determine_risk_governance(
        integrity_status,
        stability_status,
        confidence_score,
        validation_score,
        reliability
    ):

        if integrity_status == "BROKEN":
            return "UNACCEPTABLE"

        if stability_status == "UNSTABLE":
            return "HIGH_ATTENTION"

        if confidence_score < 70:
            return "UNACCEPTABLE"

        if validation_score < 70:
            return "UNACCEPTABLE"

        if reliability == "LOW":
            return "HIGH_ATTENTION"

        if (
            confidence_score < 90
            or validation_score < 90
        ):
            return "MONITORED"

        return "ACCEPTABLE"

    @staticmethod
    def _determine_override_status(
        final_decision,
        validation,
        intelligence
    ):

        final_override = final_decision.get(
            "adaptive_override"
        )

        validation_override = validation.get(
            "adaptive_override"
        )

        intelligence_override = intelligence.get(
            "adaptive_override"
        )

        if (
            final_override is True
            or validation_override is True
            or intelligence_override is True
        ):
            return "OVERRIDE_ACTIVE"

        return "NONE"

    @staticmethod
    def _determine_monitoring_policy(
        execution_readiness,
        risk_governance,
        confidence_score
    ):

        if risk_governance == "UNACCEPTABLE":
            return "CRITICAL"

        if risk_governance == "HIGH_ATTENTION":
            return "ELEVATED"

        if execution_readiness == "CONDITIONAL":
            return "ELEVATED"

        if confidence_score < 90:
            return "ELEVATED"

        return "STANDARD"

    @staticmethod
    def _calculate_governance_score(
        integrity_status,
        stability_status,
        execution_readiness,
        risk_governance,
        override_status,
        confidence_score,
        validation_score,
        intelligence_score
    ):

        score = 0.0

        integrity_points = {
            "INTACT": 100,
            "DEGRADED": 60,
            "BROKEN": 0
        }

        stability_points = {
            "STABLE": 100,
            "WATCH": 70,
            "UNSTABLE": 30
        }

        readiness_points = {
            "READY": 100,
            "CONDITIONAL": 70,
            "NOT_READY": 0
        }

        risk_points = {
            "ACCEPTABLE": 100,
            "MONITORED": 70,
            "HIGH_ATTENTION": 40,
            "UNACCEPTABLE": 0
        }

        override_points = {
            "NONE": 100,
            "OVERRIDE_ACTIVE": 60
        }

        score += integrity_points.get(
            integrity_status,
            0
        ) * 0.20

        score += stability_points.get(
            stability_status,
            0
        ) * 0.15

        score += readiness_points.get(
            execution_readiness,
            0
        ) * 0.20

        score += risk_points.get(
            risk_governance,
            0
        ) * 0.15

        score += override_points.get(
            override_status,
            0
        ) * 0.10

        score += confidence_score * 0.10

        score += validation_score * 0.05

        score += intelligence_score * 0.05

        return round(
            max(
                0,
                min(
                    100,
                    score
                )
            ),
            1
        )

    @staticmethod
    def _determine_governance_status(
        governance_score,
        execution_readiness,
        risk_governance,
        override_status
    ):

        if risk_governance == "UNACCEPTABLE":
            return "BLOCKED"

        if execution_readiness == "NOT_READY":
            return "REVIEW_REQUIRED"

        if governance_score >= 90:
            if override_status == "OVERRIDE_ACTIVE":
                return "APPROVED_WITH_OVERRIDE"

            return "APPROVED"

        if governance_score >= 75:
            return "APPROVED_WITH_MONITORING"

        return "REVIEW_REQUIRED"

    @staticmethod
    def _build_reason(
        governance_status,
        decision,
        action,
        integrity_status,
        stability_status,
        execution_readiness,
        risk_governance
    ):

        return (
            f"Final AI decision {decision} with action {action} "
            f"has governance status {governance_status}. "
            f"Decision integrity is {integrity_status}, "
            f"stability is {stability_status}, "
            f"execution readiness is {execution_readiness}, "
            f"and risk governance is {risk_governance}."
        )

    @staticmethod
    def _build_summary(
        decision,
        action,
        governance_status,
        governance_score,
        monitoring_policy
    ):

        return (
            f"Final AI decision {decision} with action {action} "
            f"received governance status {governance_status} "
            f"with governance score {governance_score}/100. "
            f"Monitoring policy is {monitoring_policy}."
        )

    @staticmethod
    def _extract_intelligence_score(
        final_decision,
        intelligence_score
    ):

        value = final_decision.get(
            "intelligence_score"
        )

        if value is None:
            if isinstance(
                intelligence_score,
                dict
            ):
                value = intelligence_score.get(
                    "intelligence_score",
                    0
                )
            else:
                value = intelligence_score

        return AIFinalDecisionGovernance._normalize(
            value
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