"""
GPT Quant Platform

AI Final Decision Execution Control Engine

Step5-3-89
"""


class AIFinalDecisionExecutionControl:

    def control(
        self,
        final_decision=None,
        governance=None
    ):
        """
        Determine the final execution control state
        from the governed AI final decision.
        """

        final_decision = final_decision or {}
        governance = governance or {}

        decision = final_decision.get(
            "decision",
            governance.get(
                "decision",
                "UNKNOWN"
            )
        )

        action = final_decision.get(
            "action",
            governance.get(
                "action",
                "UNKNOWN"
            )
        )

        execution_status = final_decision.get(
            "execution_status",
            governance.get(
                "execution_status",
                "UNDETERMINED"
            )
        )

        governance_status = governance.get(
            "governance_status",
            "UNKNOWN"
        )

        governance_score = self._normalize(
            governance.get(
                "governance_score",
                0
            )
        )

        integrity_status = governance.get(
            "integrity_status",
            "UNKNOWN"
        )

        execution_readiness = governance.get(
            "execution_readiness",
            "UNKNOWN"
        )

        risk_governance = governance.get(
            "risk_governance",
            "UNKNOWN"
        )

        override_status = governance.get(
            "override_status",
            "UNKNOWN"
        )

        confidence_score = self._normalize(
            governance.get(
                "confidence_score",
                final_decision.get(
                    "confidence_score",
                    0
                )
            )
        )

        validation_status = governance.get(
            "validation_status",
            final_decision.get(
                "validation_status",
                "UNKNOWN"
            )
        )

        validation_score = self._normalize(
            governance.get(
                "validation_score",
                final_decision.get(
                    "validation_score",
                    0
                )
            )
        )

        monitoring_policy = governance.get(
            "monitoring_policy",
            final_decision.get(
                "monitoring",
                "UNKNOWN"
            )
        )

        control_action = self._determine_control_action(
            governance_status,
            integrity_status,
            execution_readiness,
            risk_governance,
            execution_status,
            action,
            governance_score,
            confidence_score,
            validation_status,
            validation_score
        )

        control_status = self._determine_control_status(
            control_action
        )

        execution_mode = self._determine_execution_mode(
            control_action,
            monitoring_policy
        )

        control_risk = self._determine_control_risk(
            governance_status,
            integrity_status,
            risk_governance,
            governance_score,
            confidence_score,
            validation_score,
            control_action
        )

        control_reason = self._build_reason(
            control_action,
            governance_status,
            integrity_status,
            execution_readiness,
            risk_governance
        )

        summary = self._build_summary(
            decision,
            control_action,
            control_status,
            execution_mode,
            control_risk
        )

        return {
            "decision": decision,
            "action": action,
            "execution_status": execution_status,

            "governance_status": governance_status,
            "governance_score": governance_score,

            "integrity_status": integrity_status,
            "execution_readiness": execution_readiness,
            "risk_governance": risk_governance,
            "override_status": override_status,

            "confidence_score": confidence_score,

            "validation_status": validation_status,
            "validation_score": validation_score,

            "monitoring_policy": monitoring_policy,

            "control_action": control_action,
            "control_status": control_status,
            "execution_mode": execution_mode,
            "control_risk": control_risk,

            "control_reason": control_reason,
            "summary": summary
        }

    @staticmethod
    def _determine_control_action(
        governance_status,
        integrity_status,
        execution_readiness,
        risk_governance,
        execution_status,
        action,
        governance_score,
        confidence_score,
        validation_status,
        validation_score
    ):

        if governance_status == "REJECTED":
            return "BLOCK"

        if integrity_status == "COMPROMISED":
            return "BLOCK"

        if validation_status == "INVALID":
            return "BLOCK"

        if risk_governance in (
            "UNACCEPTABLE",
            "CRITICAL"
        ):
            return "BLOCK"

        if execution_status in (
            "BLOCKED",
            "PENDING_REVIEW"
        ):
            return "HOLD"

        if execution_readiness in (
            "NOT_READY",
            "BLOCKED"
        ):
            return "HOLD"

        if (
            governance_status == "APPROVED"
            and integrity_status == "INTACT"
            and execution_readiness == "READY"
            and risk_governance == "ACCEPTABLE"
            and governance_score >= 90
            and confidence_score >= 90
            and validation_score >= 90
            and validation_status == "VALID"
        ):

            if action == "PROCEED":
                return "EXECUTE"

            if action == "PROCEED_WITH_MONITORING":
                return "MONITOR"

        if confidence_score < 70:
            return "HOLD"

        if validation_score < 70:
            return "HOLD"

        return "MONITOR"

    @staticmethod
    def _determine_control_status(
        control_action
    ):

        if control_action == "EXECUTE":
            return "AUTHORIZED"

        if control_action == "MONITOR":
            return "AUTHORIZED_WITH_MONITORING"

        if control_action == "HOLD":
            return "ON_HOLD"

        if control_action == "BLOCK":
            return "BLOCKED"

        return "UNDETERMINED"

    @staticmethod
    def _determine_execution_mode(
        control_action,
        monitoring_policy
    ):

        if control_action == "EXECUTE":
            return "STANDARD_EXECUTION"

        if control_action == "MONITOR":
            return (
                f"CONTROLLED_EXECUTION_{monitoring_policy}"
            )

        if control_action == "HOLD":
            return "NO_EXECUTION"

        if control_action == "BLOCK":
            return "NO_EXECUTION"

        return "UNDETERMINED"

    @staticmethod
    def _determine_control_risk(
        governance_status,
        integrity_status,
        risk_governance,
        governance_score,
        confidence_score,
        validation_score,
        control_action
    ):

        if control_action == "BLOCK":
            return "CRITICAL"

        if (
            governance_status != "APPROVED"
            or integrity_status != "INTACT"
        ):
            return "HIGH"

        if risk_governance != "ACCEPTABLE":
            return "HIGH"

        if (
            governance_score < 80
            or confidence_score < 80
            or validation_score < 80
        ):
            return "MEDIUM"

        if control_action == "MONITOR":
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _build_reason(
        control_action,
        governance_status,
        integrity_status,
        execution_readiness,
        risk_governance
    ):

        if control_action == "EXECUTE":

            return (
                "Final AI decision is authorized for execution "
                "because governance is APPROVED, decision "
                "integrity is INTACT, execution readiness is "
                "READY, and risk governance is ACCEPTABLE."
            )

        if control_action == "MONITOR":

            return (
                "Final AI decision may proceed only under "
                "controlled monitoring because execution "
                "conditions require additional oversight."
            )

        if control_action == "HOLD":

            return (
                "Final AI decision is temporarily held because "
                "execution readiness or supporting intelligence "
                "does not satisfy the required execution threshold."
            )

        if control_action == "BLOCK":

            return (
                "Final AI decision execution is blocked because "
                "governance, integrity, validation, or risk "
                "conditions are not acceptable."
            )

        return (
            "Execution control could not be determined from "
            "the current final decision governance state."
        )

    @staticmethod
    def _build_summary(
        decision,
        control_action,
        control_status,
        execution_mode,
        control_risk
    ):

        return (
            f"Final AI decision {decision} received execution "
            f"control action {control_action}. Control status is "
            f"{control_status}, execution mode is "
            f"{execution_mode}, and control risk is "
            f"{control_risk}."
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