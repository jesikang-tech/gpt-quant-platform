"""
GPT Quant Platform

AI Final Decision Execution Assurance Engine

Step5-3-90
"""


class AIFinalDecisionExecutionAssurance:

    def assure(
        self,
        final_decision=None,
        governance=None,
        execution_control=None
    ):
        """
        Determine the final execution assurance state
        from the governed and execution-controlled AI decision.
        """

        final_decision = final_decision or {}
        governance = governance or {}
        execution_control = execution_control or {}

        decision = execution_control.get(
            "decision",
            final_decision.get(
                "decision",
                "UNKNOWN"
            )
        )

        action = execution_control.get(
            "action",
            final_decision.get(
                "action",
                "UNKNOWN"
            )
        )

        execution_status = execution_control.get(
            "execution_status",
            final_decision.get(
                "execution_status",
                "UNDETERMINED"
            )
        )

        control_action = execution_control.get(
            "control_action",
            "UNKNOWN"
        )

        control_status = execution_control.get(
            "control_status",
            "UNKNOWN"
        )

        execution_mode = execution_control.get(
            "execution_mode",
            "UNKNOWN"
        )

        control_risk = execution_control.get(
            "control_risk",
            "UNKNOWN"
        )

        governance_status = execution_control.get(
            "governance_status",
            governance.get(
                "governance_status",
                "UNKNOWN"
            )
        )

        governance_score = self._normalize(
            execution_control.get(
                "governance_score",
                governance.get(
                    "governance_score",
                    0
                )
            )
        )

        integrity_status = execution_control.get(
            "integrity_status",
            governance.get(
                "integrity_status",
                "UNKNOWN"
            )
        )

        execution_readiness = execution_control.get(
            "execution_readiness",
            governance.get(
                "execution_readiness",
                "UNKNOWN"
            )
        )

        risk_governance = execution_control.get(
            "risk_governance",
            governance.get(
                "risk_governance",
                "UNKNOWN"
            )
        )

        confidence_score = self._normalize(
            execution_control.get(
                "confidence_score",
                final_decision.get(
                    "confidence_score",
                    0
                )
            )
        )

        validation_status = execution_control.get(
            "validation_status",
            final_decision.get(
                "validation_status",
                "UNKNOWN"
            )
        )

        validation_score = self._normalize(
            execution_control.get(
                "validation_score",
                final_decision.get(
                    "validation_score",
                    0
                )
            )
        )

        monitoring_policy = execution_control.get(
            "monitoring_policy",
            final_decision.get(
                "monitoring",
                "UNKNOWN"
            )
        )

        assurance_status = self._determine_assurance_status(
            control_action,
            control_status,
            governance_status,
            integrity_status,
            execution_readiness,
            risk_governance,
            control_risk,
            governance_score,
            confidence_score,
            validation_status,
            validation_score
        )

        assurance_level = self._determine_assurance_level(
            assurance_status,
            control_action,
            control_risk
        )

        monitoring_status = self._determine_monitoring_status(
            control_action,
            monitoring_policy
        )

        assurance_risk = self._determine_assurance_risk(
            assurance_status,
            control_risk,
            governance_score,
            confidence_score,
            validation_score
        )

        assurance_score = self._calculate_assurance_score(
            governance_score,
            confidence_score,
            validation_score,
            assurance_status,
            control_risk
        )

        assurance_reason = self._build_reason(
            assurance_status,
            control_action,
            governance_status,
            integrity_status,
            execution_readiness,
            risk_governance
        )

        summary = self._build_summary(
            decision,
            action,
            assurance_status,
            assurance_level,
            monitoring_status,
            assurance_risk,
            assurance_score
        )

        return {
            "decision": decision,
            "action": action,
            "execution_status": execution_status,

            "control_action": control_action,
            "control_status": control_status,
            "execution_mode": execution_mode,
            "control_risk": control_risk,

            "governance_status": governance_status,
            "governance_score": governance_score,
            "integrity_status": integrity_status,
            "execution_readiness": execution_readiness,
            "risk_governance": risk_governance,

            "confidence_score": confidence_score,
            "validation_status": validation_status,
            "validation_score": validation_score,

            "monitoring_policy": monitoring_policy,

            "assurance_status": assurance_status,
            "assurance_level": assurance_level,
            "monitoring_status": monitoring_status,
            "assurance_risk": assurance_risk,
            "assurance_score": assurance_score,

            "assurance_reason": assurance_reason,
            "summary": summary
        }

    @staticmethod
    def _determine_assurance_status(
        control_action,
        control_status,
        governance_status,
        integrity_status,
        execution_readiness,
        risk_governance,
        control_risk,
        governance_score,
        confidence_score,
        validation_status,
        validation_score
    ):

        if control_action == "BLOCK":
            return "BLOCKED"

        if control_status == "BLOCKED":
            return "BLOCKED"

        if governance_status == "REJECTED":
            return "BLOCKED"

        if integrity_status == "COMPROMISED":
            return "BLOCKED"

        if validation_status == "INVALID":
            return "BLOCKED"

        if risk_governance in (
            "UNACCEPTABLE",
            "CRITICAL"
        ):
            return "BLOCKED"

        if control_action == "HOLD":
            return "PENDING"

        if execution_readiness in (
            "NOT_READY",
            "BLOCKED"
        ):
            return "PENDING"

        if (
            control_action == "EXECUTE"
            and control_status == "AUTHORIZED"
            and governance_status == "APPROVED"
            and integrity_status == "INTACT"
            and execution_readiness == "READY"
            and risk_governance == "ACCEPTABLE"
            and validation_status == "VALID"
            and governance_score >= 90
            and confidence_score >= 90
            and validation_score >= 90
            and control_risk == "LOW"
        ):
            return "ASSURED"

        return "MONITORED"

    @staticmethod
    def _determine_assurance_level(
        assurance_status,
        control_action,
        control_risk
    ):

        if assurance_status == "ASSURED":
            return "HIGH"

        if assurance_status == "BLOCKED":
            return "NONE"

        if assurance_status == "PENDING":
            return "LOW"

        if control_action == "MONITOR":
            return "MEDIUM"

        if control_risk == "MEDIUM":
            return "MEDIUM"

        return "MEDIUM"

    @staticmethod
    def _determine_monitoring_status(
        control_action,
        monitoring_policy
    ):

        if control_action == "EXECUTE":
            if monitoring_policy == "STANDARD":
                return "STANDARD_MONITORING"

            return "ENHANCED_MONITORING"

        if control_action == "MONITOR":
            return "ACTIVE_MONITORING"

        if control_action == "HOLD":
            return "PRE_EXECUTION_MONITORING"

        if control_action == "BLOCK":
            return "MONITORING_SUSPENDED"

        return "UNDETERMINED"

    @staticmethod
    def _determine_assurance_risk(
        assurance_status,
        control_risk,
        governance_score,
        confidence_score,
        validation_score
    ):

        if assurance_status == "BLOCKED":
            return "CRITICAL"

        if assurance_status == "PENDING":
            return "HIGH"

        if control_risk == "HIGH":
            return "HIGH"

        if (
            governance_score < 80
            or confidence_score < 80
            or validation_score < 80
        ):
            return "MEDIUM"

        if control_risk == "MEDIUM":
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _calculate_assurance_score(
        governance_score,
        confidence_score,
        validation_score,
        assurance_status,
        control_risk
    ):

        score = (
            governance_score * 0.40
            + confidence_score * 0.30
            + validation_score * 0.30
        )

        if assurance_status == "ASSURED":
            score += 2

        if control_risk == "HIGH":
            score -= 5

        if control_risk == "CRITICAL":
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
        assurance_status,
        control_action,
        governance_status,
        integrity_status,
        execution_readiness,
        risk_governance
    ):

        if assurance_status == "ASSURED":

            return (
                "Final AI decision execution is fully assured "
                "because execution control is authorized, "
                "governance is APPROVED, decision integrity is "
                "INTACT, execution readiness is READY, and risk "
                "governance is ACCEPTABLE."
            )

        if assurance_status == "MONITORED":

            return (
                "Final AI decision execution remains available "
                "under monitored assurance because execution "
                "conditions require additional oversight."
            )

        if assurance_status == "PENDING":

            return (
                "Final AI decision execution assurance is pending "
                "because execution readiness or control conditions "
                "have not reached the required threshold."
            )

        if assurance_status == "BLOCKED":

            return (
                "Final AI decision execution assurance is blocked "
                "because governance, integrity, validation, risk, "
                "or execution control conditions are unacceptable."
            )

        return (
            "Final AI decision execution assurance could not be "
            "determined from the current execution state."
        )

    @staticmethod
    def _build_summary(
        decision,
        action,
        assurance_status,
        assurance_level,
        monitoring_status,
        assurance_risk,
        assurance_score
    ):

        return (
            f"Final AI decision {decision} with action {action} "
            f"received execution assurance status "
            f"{assurance_status}. Assurance level is "
            f"{assurance_level}, monitoring status is "
            f"{monitoring_status}, assurance risk is "
            f"{assurance_risk}, and assurance score is "
            f"{assurance_score}/100."
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
