"""
GPT Quant Platform

AI Final Decision Execution Feedback Intelligence Engine

Step5-3-92
"""


class AIFinalDecisionExecutionFeedback:

    def feedback(
        self,
        final_decision=None,
        governance=None,
        execution_control=None,
        execution_assurance=None,
        execution_monitoring=None
    ):
        """
        Evaluate execution monitoring results and produce
        post-monitoring feedback intelligence.
        """

        final_decision = final_decision or {}
        governance = governance or {}
        execution_control = execution_control or {}
        execution_assurance = execution_assurance or {}
        execution_monitoring = execution_monitoring or {}

        decision = execution_monitoring.get(
            "decision",
            execution_assurance.get(
                "decision",
                execution_control.get(
                    "decision",
                    final_decision.get(
                        "decision",
                        "UNKNOWN"
                    )
                )
            )
        )

        action = execution_monitoring.get(
            "action",
            execution_assurance.get(
                "action",
                execution_control.get(
                    "action",
                    final_decision.get(
                        "action",
                        "UNKNOWN"
                    )
                )
            )
        )

        execution_status = execution_monitoring.get(
            "execution_status",
            execution_assurance.get(
                "execution_status",
                execution_control.get(
                    "execution_status",
                    final_decision.get(
                        "execution_status",
                        "UNDETERMINED"
                    )
                )
            )
        )

        monitoring_status = execution_monitoring.get(
            "monitoring_status",
            "UNKNOWN"
        )

        monitoring_action = execution_monitoring.get(
            "monitoring_action",
            "UNKNOWN"
        )

        monitoring_risk = execution_monitoring.get(
            "monitoring_risk",
            "UNKNOWN"
        )

        monitoring_score = self._normalize(
            execution_monitoring.get(
                "monitoring_score",
                0
            )
        )

        assurance_status = execution_monitoring.get(
            "assurance_status",
            execution_assurance.get(
                "assurance_status",
                "UNKNOWN"
            )
        )

        assurance_risk = execution_monitoring.get(
            "assurance_risk",
            execution_assurance.get(
                "assurance_risk",
                "UNKNOWN"
            )
        )

        assurance_score = self._normalize(
            execution_monitoring.get(
                "assurance_score",
                execution_assurance.get(
                    "assurance_score",
                    0
                )
            )
        )

        control_status = execution_monitoring.get(
            "control_status",
            execution_control.get(
                "control_status",
                "UNKNOWN"
            )
        )

        control_risk = execution_monitoring.get(
            "control_risk",
            execution_control.get(
                "control_risk",
                "UNKNOWN"
            )
        )

        governance_status = execution_monitoring.get(
            "governance_status",
            governance.get(
                "governance_status",
                "UNKNOWN"
            )
        )

        governance_score = self._normalize(
            execution_monitoring.get(
                "governance_score",
                governance.get(
                    "governance_score",
                    0
                )
            )
        )

        validation_status = execution_monitoring.get(
            "validation_status",
            execution_assurance.get(
                "validation_status",
                final_decision.get(
                    "validation_status",
                    "UNKNOWN"
                )
            )
        )

        validation_score = self._normalize(
            execution_monitoring.get(
                "validation_score",
                execution_assurance.get(
                    "validation_score",
                    final_decision.get(
                        "validation_score",
                        0
                    )
                )
            )
        )

        feedback_status = self._determine_feedback_status(
            monitoring_status,
            monitoring_risk,
            assurance_status,
            control_status,
            governance_status,
            validation_status,
            monitoring_score
        )

        feedback_action = self._determine_feedback_action(
            feedback_status,
            monitoring_risk,
            monitoring_action
        )

        feedback_risk = self._determine_feedback_risk(
            feedback_status,
            monitoring_risk,
            assurance_risk,
            control_risk,
            monitoring_score
        )

        feedback_score = self._calculate_feedback_score(
            monitoring_score,
            assurance_score,
            governance_score,
            validation_score,
            feedback_status,
            feedback_risk
        )

        reassessment_required = self._determine_reassessment(
            feedback_status,
            feedback_risk,
            monitoring_score,
            assurance_score,
            validation_score
        )

        feedback_reason = self._build_reason(
            feedback_status,
            feedback_action,
            feedback_risk,
            reassessment_required
        )

        summary = self._build_summary(
            decision,
            action,
            feedback_status,
            feedback_action,
            feedback_risk,
            feedback_score,
            reassessment_required
        )

        return {
            "decision": decision,
            "action": action,
            "execution_status": execution_status,

            "monitoring_status": monitoring_status,
            "monitoring_action": monitoring_action,
            "monitoring_risk": monitoring_risk,
            "monitoring_score": monitoring_score,

            "assurance_status": assurance_status,
            "assurance_risk": assurance_risk,
            "assurance_score": assurance_score,

            "control_status": control_status,
            "control_risk": control_risk,

            "governance_status": governance_status,
            "governance_score": governance_score,

            "validation_status": validation_status,
            "validation_score": validation_score,

            "feedback_status": feedback_status,
            "feedback_action": feedback_action,
            "feedback_risk": feedback_risk,
            "feedback_score": feedback_score,

            "reassessment_required": reassessment_required,

            "feedback_reason": feedback_reason,
            "summary": summary
        }

    @staticmethod
    def _determine_feedback_status(
        monitoring_status,
        monitoring_risk,
        assurance_status,
        control_status,
        governance_status,
        validation_status,
        monitoring_score
    ):

        if monitoring_status == "BLOCKED_MONITORING":
            return "CRITICAL"

        if monitoring_status == "CRITICAL_MONITORING":
            return "CRITICAL"

        if monitoring_risk == "CRITICAL":
            return "CRITICAL"

        if (
            assurance_status == "BLOCKED"
            or control_status == "BLOCKED"
            or governance_status == "REJECTED"
            or validation_status == "INVALID"
        ):
            return "UNSTABLE"

        if monitoring_risk == "HIGH":
            return "REQUIRES_ATTENTION"

        if monitoring_score < 80:
            return "REQUIRES_ATTENTION"

        if monitoring_status == "PRE_EXECUTION_MONITORING":
            return "PENDING"

        if (
            monitoring_status == "STANDARD_MONITORING"
            and monitoring_risk == "LOW"
            and assurance_status == "ASSURED"
            and control_status == "AUTHORIZED"
            and governance_status == "APPROVED"
            and validation_status == "VALID"
            and monitoring_score >= 90
        ):
            return "STABLE"

        return "MONITORED"

    @staticmethod
    def _determine_feedback_action(
        feedback_status,
        monitoring_risk,
        monitoring_action
    ):

        if feedback_status == "CRITICAL":
            return "HALT"

        if feedback_status == "UNSTABLE":
            return "REASSESS"

        if feedback_status == "REQUIRES_ATTENTION":
            return "ENHANCED_REVIEW"

        if feedback_status == "PENDING":
            return "WAIT"

        if feedback_status == "STABLE":
            return "CONTINUE"

        if monitoring_risk == "HIGH":
            return "REASSESS"

        if monitoring_action == "ESCALATE":
            return "ENHANCED_REVIEW"

        return "CONTINUE"

    @staticmethod
    def _determine_feedback_risk(
        feedback_status,
        monitoring_risk,
        assurance_risk,
        control_risk,
        monitoring_score
    ):

        if feedback_status == "CRITICAL":
            return "CRITICAL"

        if (
            monitoring_risk == "CRITICAL"
            or assurance_risk == "CRITICAL"
            or control_risk == "CRITICAL"
        ):
            return "CRITICAL"

        if feedback_status == "UNSTABLE":
            return "HIGH"

        if (
            monitoring_risk == "HIGH"
            or assurance_risk == "HIGH"
            or control_risk == "HIGH"
        ):
            return "HIGH"

        if feedback_status == "REQUIRES_ATTENTION":
            return "MEDIUM"

        if monitoring_score < 80:
            return "MEDIUM"

        if (
            monitoring_risk == "MEDIUM"
            or assurance_risk == "MEDIUM"
            or control_risk == "MEDIUM"
        ):
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _calculate_feedback_score(
        monitoring_score,
        assurance_score,
        governance_score,
        validation_score,
        feedback_status,
        feedback_risk
    ):

        score = (
            monitoring_score * 0.40
            + assurance_score * 0.25
            + governance_score * 0.20
            + validation_score * 0.15
        )

        if feedback_status == "STABLE":
            score += 2

        if feedback_status == "REQUIRES_ATTENTION":
            score -= 5

        if feedback_status == "UNSTABLE":
            score -= 10

        if feedback_status == "CRITICAL":
            score -= 20

        if feedback_risk == "HIGH":
            score -= 5

        if feedback_risk == "CRITICAL":
            score -= 15

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
    def _determine_reassessment(
        feedback_status,
        feedback_risk,
        monitoring_score,
        assurance_score,
        validation_score
    ):

        if feedback_status in (
            "CRITICAL",
            "UNSTABLE",
            "REQUIRES_ATTENTION"
        ):
            return True

        if feedback_risk in (
            "HIGH",
            "CRITICAL"
        ):
            return True

        if (
            monitoring_score < 80
            or assurance_score < 80
            or validation_score < 80
        ):
            return True

        return False

    @staticmethod
    def _build_reason(
        feedback_status,
        feedback_action,
        feedback_risk,
        reassessment_required
    ):

        if feedback_status == "STABLE":
            return (
                "Final AI decision execution feedback is stable "
                "because monitoring is within the expected range, "
                "execution assurance remains valid, and no "
                "reassessment is required."
            )

        if feedback_status == "REQUIRES_ATTENTION":
            return (
                "Final AI decision execution feedback requires "
                "additional attention because monitoring or risk "
                "conditions require enhanced review."
            )

        if feedback_status == "UNSTABLE":
            return (
                "Final AI decision execution feedback is unstable "
                "because execution governance, assurance, control, "
                "or validation conditions require reassessment."
            )

        if feedback_status == "CRITICAL":
            return (
                "Final AI decision execution feedback is critical "
                "and execution should be halted pending reassessment."
            )

        if feedback_status == "PENDING":
            return (
                "Final AI decision execution feedback remains pending "
                "because execution monitoring has not reached a "
                "stable post-execution state."
            )

        return (
            "Final AI decision execution feedback remains monitored "
            "with continued oversight."
        )

    @staticmethod
    def _build_summary(
        decision,
        action,
        feedback_status,
        feedback_action,
        feedback_risk,
        feedback_score,
        reassessment_required
    ):

        return (
            f"Final AI decision {decision} with action {action} "
            f"received execution feedback status "
            f"{feedback_status}. Feedback action is "
            f"{feedback_action}, feedback risk is "
            f"{feedback_risk}, feedback score is "
            f"{feedback_score}/100, and reassessment required is "
            f"{reassessment_required}."
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
