"""
GPT Quant Platform

AI Final Decision Execution Monitoring Engine

Step5-3-91
"""


class AIFinalDecisionExecutionMonitoring:

    def monitor(
        self,
        final_decision=None,
        governance=None,
        execution_control=None,
        execution_assurance=None
    ):
        """
        Monitor the final AI decision execution state
        after governance, execution control, and execution assurance.
        """

        final_decision = final_decision or {}
        governance = governance or {}
        execution_control = execution_control or {}
        execution_assurance = execution_assurance or {}

        decision = execution_assurance.get(
            "decision",
            execution_control.get(
                "decision",
                final_decision.get(
                    "decision",
                    "UNKNOWN"
                )
            )
        )

        action = execution_assurance.get(
            "action",
            execution_control.get(
                "action",
                final_decision.get(
                    "action",
                    "UNKNOWN"
                )
            )
        )

        execution_status = execution_assurance.get(
            "execution_status",
            execution_control.get(
                "execution_status",
                final_decision.get(
                    "execution_status",
                    "UNDETERMINED"
                )
            )
        )

        assurance_status = execution_assurance.get(
            "assurance_status",
            "UNKNOWN"
        )

        assurance_level = execution_assurance.get(
            "assurance_level",
            "UNKNOWN"
        )

        assurance_risk = execution_assurance.get(
            "assurance_risk",
            "UNKNOWN"
        )

        assurance_score = self._normalize(
            execution_assurance.get(
                "assurance_score",
                0
            )
        )

        control_action = execution_assurance.get(
            "control_action",
            execution_control.get(
                "control_action",
                "UNKNOWN"
            )
        )

        control_status = execution_assurance.get(
            "control_status",
            execution_control.get(
                "control_status",
                "UNKNOWN"
            )
        )

        control_risk = execution_assurance.get(
            "control_risk",
            execution_control.get(
                "control_risk",
                "UNKNOWN"
            )
        )

        governance_status = execution_assurance.get(
            "governance_status",
            governance.get(
                "governance_status",
                "UNKNOWN"
            )
        )

        governance_score = self._normalize(
            execution_assurance.get(
                "governance_score",
                governance.get(
                    "governance_score",
                    0
                )
            )
        )

        validation_status = execution_assurance.get(
            "validation_status",
            final_decision.get(
                "validation_status",
                "UNKNOWN"
            )
        )

        validation_score = self._normalize(
            execution_assurance.get(
                "validation_score",
                final_decision.get(
                    "validation_score",
                    0
                )
            )
        )

        monitoring_policy = execution_assurance.get(
            "monitoring_policy",
            "STANDARD"
        )

        monitoring_status = self._determine_monitoring_status(
            assurance_status,
            assurance_level,
            assurance_risk,
            control_action,
            control_status,
            control_risk,
            monitoring_policy,
            assurance_score,
            governance_score,
            validation_score
        )

        monitoring_risk = self._determine_monitoring_risk(
            monitoring_status,
            assurance_risk,
            control_risk,
            assurance_score,
            governance_score,
            validation_score
        )

        monitoring_action = self._determine_monitoring_action(
            monitoring_status,
            monitoring_risk,
            control_action
        )

        monitoring_score = self._calculate_monitoring_score(
            assurance_score,
            governance_score,
            validation_score,
            monitoring_status,
            monitoring_risk
        )

        monitoring_reason = self._build_reason(
            monitoring_status,
            monitoring_risk,
            assurance_status,
            control_status,
            governance_status
        )

        summary = self._build_summary(
            decision,
            action,
            monitoring_status,
            monitoring_action,
            monitoring_risk,
            monitoring_score
        )

        return {
            "decision": decision,
            "action": action,
            "execution_status": execution_status,

            "assurance_status": assurance_status,
            "assurance_level": assurance_level,
            "assurance_risk": assurance_risk,
            "assurance_score": assurance_score,

            "control_action": control_action,
            "control_status": control_status,
            "control_risk": control_risk,

            "governance_status": governance_status,
            "governance_score": governance_score,

            "validation_status": validation_status,
            "validation_score": validation_score,

            "monitoring_policy": monitoring_policy,
            "monitoring_status": monitoring_status,
            "monitoring_action": monitoring_action,
            "monitoring_risk": monitoring_risk,
            "monitoring_score": monitoring_score,

            "monitoring_reason": monitoring_reason,
            "summary": summary
        }

    @staticmethod
    def _determine_monitoring_status(
        assurance_status,
        assurance_level,
        assurance_risk,
        control_action,
        control_status,
        control_risk,
        monitoring_policy,
        assurance_score,
        governance_score,
        validation_score
    ):

        if assurance_status == "BLOCKED":
            return "BLOCKED_MONITORING"

        if control_status == "BLOCKED":
            return "BLOCKED_MONITORING"

        if assurance_risk == "CRITICAL":
            return "CRITICAL_MONITORING"

        if control_risk == "HIGH":
            return "ENHANCED_MONITORING"

        if assurance_status == "PENDING":
            return "PRE_EXECUTION_MONITORING"

        if assurance_status == "ASSURED":
            if (
                assurance_level == "HIGH"
                and assurance_risk == "LOW"
                and control_action == "EXECUTE"
                and control_status == "AUTHORIZED"
                and assurance_score >= 90
                and governance_score >= 90
                and validation_score >= 90
            ):
                if monitoring_policy == "STANDARD":
                    return "STANDARD_MONITORING"

                return "ENHANCED_MONITORING"

        return "ENHANCED_MONITORING"

    @staticmethod
    def _determine_monitoring_risk(
        monitoring_status,
        assurance_risk,
        control_risk,
        assurance_score,
        governance_score,
        validation_score
    ):

        if monitoring_status == "BLOCKED_MONITORING":
            return "CRITICAL"

        if monitoring_status == "CRITICAL_MONITORING":
            return "CRITICAL"

        if assurance_risk == "HIGH":
            return "HIGH"

        if control_risk == "HIGH":
            return "HIGH"

        if (
            assurance_score < 80
            or governance_score < 80
            or validation_score < 80
        ):
            return "MEDIUM"

        if assurance_risk == "MEDIUM":
            return "MEDIUM"

        if control_risk == "MEDIUM":
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _determine_monitoring_action(
        monitoring_status,
        monitoring_risk,
        control_action
    ):

        if monitoring_status == "BLOCKED_MONITORING":
            return "HALT"

        if monitoring_status == "CRITICAL_MONITORING":
            return "HALT"

        if monitoring_risk == "HIGH":
            return "ESCALATE"

        if monitoring_risk == "MEDIUM":
            return "ENHANCED_MONITORING"

        if (
            monitoring_status == "STANDARD_MONITORING"
            and control_action == "EXECUTE"
        ):
            return "MONITOR"

        return "MONITOR"

    @staticmethod
    def _calculate_monitoring_score(
        assurance_score,
        governance_score,
        validation_score,
        monitoring_status,
        monitoring_risk
    ):

        score = (
            assurance_score * 0.50
            + governance_score * 0.30
            + validation_score * 0.20
        )

        if monitoring_status == "STANDARD_MONITORING":
            score += 2

        if monitoring_status == "CRITICAL_MONITORING":
            score -= 10

        if monitoring_status == "BLOCKED_MONITORING":
            score -= 20

        if monitoring_risk == "HIGH":
            score -= 5

        if monitoring_risk == "CRITICAL":
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
    def _build_reason(
        monitoring_status,
        monitoring_risk,
        assurance_status,
        control_status,
        governance_status
    ):

        if monitoring_status == "STANDARD_MONITORING":
            return (
                "Final AI decision execution is under standard "
                "monitoring because execution assurance is "
                "ASSURED, execution control is AUTHORIZED, "
                "and governance is APPROVED."
            )

        if monitoring_status == "ENHANCED_MONITORING":
            return (
                "Final AI decision execution remains active "
                "under enhanced monitoring because additional "
                "execution oversight is required."
            )

        if monitoring_status == "PRE_EXECUTION_MONITORING":
            return (
                "Final AI decision execution remains under "
                "pre-execution monitoring because execution "
                "assurance is not yet fully established."
            )

        if monitoring_status == "CRITICAL_MONITORING":
            return (
                "Final AI decision execution requires critical "
                "monitoring because execution risk is critical."
            )

        if monitoring_status == "BLOCKED_MONITORING":
            return (
                "Final AI decision execution monitoring is "
                "blocked because execution control or assurance "
                "conditions are blocked."
            )

        return (
            "Final AI decision execution monitoring requires "
            "additional evaluation."
        )

    @staticmethod
    def _build_summary(
        decision,
        action,
        monitoring_status,
        monitoring_action,
        monitoring_risk,
        monitoring_score
    ):

        return (
            f"Final AI decision {decision} with action {action} "
            f"is under {monitoring_status}. Monitoring action "
            f"is {monitoring_action}, monitoring risk is "
            f"{monitoring_risk}, and monitoring score is "
            f"{monitoring_score}/100."
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
