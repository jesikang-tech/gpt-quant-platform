"""
GPT Quant Platform

AI Final Decision Lifecycle Governance Engine

Step5-3-95
"""


class AIFinalDecisionLifecycleGovernance:

    def govern(
        self,
        final_decision=None,
        lifecycle=None
    ):
        """
        Evaluate the final AI decision lifecycle and determine
        final operational governance status.
        """

        final_decision = final_decision or {}
        lifecycle = lifecycle or {}

        decision = self._first_value(
            lifecycle.get("decision"),
            final_decision.get("decision"),
            "UNKNOWN"
        )

        action = self._first_value(
            lifecycle.get("action"),
            final_decision.get("action"),
            "UNKNOWN"
        )

        lifecycle_status = lifecycle.get(
            "lifecycle_status",
            "UNKNOWN"
        )

        lifecycle_action = lifecycle.get(
            "lifecycle_action",
            "UNKNOWN"
        )

        lifecycle_risk = lifecycle.get(
            "lifecycle_risk",
            "UNKNOWN"
        )

        lifecycle_score = self._normalize(
            lifecycle.get(
                "lifecycle_score",
                0
            )
        )

        lifecycle_grade = lifecycle.get(
            "lifecycle_grade",
            "F"
        )

        validation_status = lifecycle.get(
            "validation_status",
            "UNKNOWN"
        )

        governance_status = lifecycle.get(
            "governance_status",
            "UNKNOWN"
        )

        control_status = lifecycle.get(
            "control_status",
            "UNKNOWN"
        )

        assurance_status = lifecycle.get(
            "assurance_status",
            "UNKNOWN"
        )

        monitoring_status = lifecycle.get(
            "monitoring_status",
            "UNKNOWN"
        )

        feedback_status = lifecycle.get(
            "feedback_status",
            "UNKNOWN"
        )

        reassessment_status = lifecycle.get(
            "reassessment_status",
            "UNKNOWN"
        )

        reassessment_required = bool(
            lifecycle.get(
                "reassessment_required",
                False
            )
        )

        attention_signals = lifecycle.get(
            "attention_signals",
            []
        )

        governance_status_final = self._determine_governance_status(
            lifecycle_status,
            lifecycle_risk,
            lifecycle_score,
            validation_status,
            governance_status,
            control_status,
            assurance_status,
            monitoring_status,
            feedback_status,
            reassessment_status,
            reassessment_required
        )

        governance_action = self._determine_action(
            governance_status_final,
            lifecycle_action,
            lifecycle_risk,
            reassessment_required
        )

        governance_risk = self._determine_risk(
            governance_status_final,
            lifecycle_risk
        )

        governance_score = self._calculate_score(
            lifecycle_score,
            governance_status_final,
            governance_risk,
            reassessment_required
        )

        governance_grade = self._grade(
            governance_score
        )

        execution_authorized = (
            governance_status_final == "APPROVED"
            and governance_action == "CONTINUE"
            and governance_risk == "LOW"
        )

        monitoring_required = (
            governance_status_final in (
                "APPROVED",
                "MONITOR"
            )
        )

        override_status = self._determine_override(
            lifecycle_status,
            lifecycle_action,
            governance_status_final
        )

        operational_status = governance_status_final

        operational_action = governance_action

        operational_risk = governance_risk

        operational_score = governance_score

        operational_grade = governance_grade

        governance_reason = self._build_reason(
            governance_status_final,
            governance_action,
            governance_risk,
            lifecycle_status,
            lifecycle_score,
            reassessment_required,
            attention_signals
        )

        summary = self._build_summary(
            decision,
            action,
            operational_status,
            operational_action,
            operational_risk,
            operational_score,
            operational_grade
        )

        return {
            "decision": decision,
            "action": action,

            "lifecycle_status": lifecycle_status,
            "lifecycle_action": lifecycle_action,
            "lifecycle_risk": lifecycle_risk,
            "lifecycle_score": lifecycle_score,
            "lifecycle_grade": lifecycle_grade,

            "validation_status": validation_status,
            "governance_status": governance_status,
            "control_status": control_status,
            "assurance_status": assurance_status,
            "monitoring_status": monitoring_status,
            "feedback_status": feedback_status,
            "reassessment_status": reassessment_status,
            "reassessment_required": reassessment_required,

            "governance_status_final":
                governance_status_final,
            "governance_action":
                governance_action,
            "governance_risk":
                governance_risk,
            "governance_score":
                governance_score,
            "governance_grade":
                governance_grade,

            "execution_authorized":
                execution_authorized,
            "monitoring_required":
                monitoring_required,
            "override_status":
                override_status,

            "operational_status":
                operational_status,
            "operational_action":
                operational_action,
            "operational_risk":
                operational_risk,
            "operational_score":
                operational_score,
            "operational_grade":
                operational_grade,

            "attention_signals":
                attention_signals,

            "governance_reason":
                governance_reason,

            "summary":
                summary
        }

    @staticmethod
    def _determine_governance_status(
        lifecycle_status,
        lifecycle_risk,
        lifecycle_score,
        validation_status,
        governance_status,
        control_status,
        assurance_status,
        monitoring_status,
        feedback_status,
        reassessment_status,
        reassessment_required
    ):

        if reassessment_required:
            return "REASSESS"

        if lifecycle_status in (
            "VALIDATION_FAILED",
            "GOVERNANCE_BLOCKED",
            "EXECUTION_BLOCKED",
            "ASSURANCE_FAILED",
            "MONITORING_CRITICAL",
            "FEEDBACK_UNSTABLE",
            "REASSESSMENT_REQUIRED"
        ):
            return "BLOCKED"

        if lifecycle_risk == "CRITICAL":
            return "BLOCKED"

        if lifecycle_risk == "HIGH":
            return "REVIEW"

        if validation_status in (
            "INVALID",
            "FAILED"
        ):
            return "BLOCKED"

        if governance_status in (
            "REJECTED",
            "BLOCKED"
        ):
            return "BLOCKED"

        if control_status in (
            "BLOCKED",
            "REJECTED"
        ):
            return "BLOCKED"

        if assurance_status in (
            "FAILED",
            "BLOCKED"
        ):
            return "BLOCKED"

        if monitoring_status in (
            "CRITICAL_MONITORING",
            "BLOCKED_MONITORING"
        ):
            return "BLOCKED"

        if feedback_status in (
            "CRITICAL",
            "UNSTABLE"
        ):
            return "REVIEW"

        if reassessment_status in (
            "CRITICAL_REASSESSMENT",
            "UNSTABLE_REASSESSMENT"
        ):
            return "REASSESS"

        if lifecycle_score < 80:
            return "REVIEW"

        if (
            lifecycle_status == "HEALTHY"
            and lifecycle_risk == "LOW"
        ):
            return "APPROVED"

        return "MONITOR"

    @staticmethod
    def _determine_action(
        governance_status,
        lifecycle_action,
        lifecycle_risk,
        reassessment_required
    ):

        if governance_status == "APPROVED":
            return "CONTINUE"

        if governance_status == "REASSESS":
            return "REASSESS"

        if governance_status == "BLOCKED":
            return "HALT"

        if governance_status == "REVIEW":
            return "REVIEW"

        if reassessment_required:
            return "REASSESS"

        if lifecycle_risk == "MEDIUM":
            return "MONITOR"

        if lifecycle_action == "CONTINUE":
            return "CONTINUE"

        return "MONITOR"

    @staticmethod
    def _determine_risk(
        governance_status,
        lifecycle_risk
    ):

        if governance_status == "BLOCKED":
            return "CRITICAL"

        if governance_status == "REASSESS":
            return "HIGH"

        if governance_status == "REVIEW":
            return "HIGH"

        if lifecycle_risk in (
            "CRITICAL",
            "HIGH",
            "MEDIUM"
        ):
            return lifecycle_risk

        return "LOW"

    @staticmethod
    def _calculate_score(
        lifecycle_score,
        governance_status,
        governance_risk,
        reassessment_required
    ):

        score = lifecycle_score

        if governance_status == "APPROVED":
            score += 0

        elif governance_status == "MONITOR":
            score -= 5

        elif governance_status == "REVIEW":
            score -= 10

        elif governance_status == "REASSESS":
            score -= 15

        elif governance_status == "BLOCKED":
            score -= 25

        if governance_risk == "HIGH":
            score -= 5

        if governance_risk == "CRITICAL":
            score -= 15

        if reassessment_required:
            score -= 5

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
    def _grade(score):

        if score >= 95:
            return "A+"

        if score >= 90:
            return "A"

        if score >= 85:
            return "B+"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        if score >= 60:
            return "D"

        return "F"

    @staticmethod
    def _determine_override(
        lifecycle_status,
        lifecycle_action,
        governance_status
    ):

        if governance_status in (
            "BLOCKED",
            "REASSESS"
        ):
            return "ACTIVE"

        if (
            lifecycle_status == "HEALTHY"
            and lifecycle_action == "CONTINUE"
        ):
            return "NONE"

        return "NONE"

    @staticmethod
    def _build_reason(
        governance_status,
        governance_action,
        governance_risk,
        lifecycle_status,
        lifecycle_score,
        reassessment_required,
        attention_signals
    ):

        if governance_status == "APPROVED":
            return (
                "Final AI decision lifecycle governance is approved "
                "because lifecycle health, risk, and supporting execution "
                "signals remain within acceptable operating ranges."
            )

        if governance_status == "BLOCKED":
            return (
                "Final AI decision lifecycle governance is blocked because "
                "one or more critical lifecycle conditions prevent "
                "continued execution."
            )

        if governance_status == "REASSESS":
            return (
                "Final AI decision lifecycle governance requires "
                "reassessment before continued execution."
            )

        if governance_status == "REVIEW":
            return (
                "Final AI decision lifecycle governance requires review "
                "because lifecycle risk or supporting signals are elevated."
            )

        if attention_signals:
            names = ", ".join(
                signal.get("name", "Unknown")
                for signal in attention_signals[:4]
            )

            return (
                "Final AI decision lifecycle governance remains under "
                f"monitoring because attention signals were detected in "
                f"{names}."
            )

        return (
            "Final AI decision lifecycle governance remains operational "
            "with continued monitoring."
        )

    @staticmethod
    def _build_summary(
        decision,
        action,
        operational_status,
        operational_action,
        operational_risk,
        operational_score,
        operational_grade
    ):

        return (
            f"Final AI decision {decision} with action {action} has "
            f"operational status {operational_status}. Operational "
            f"action is {operational_action}, operational risk is "
            f"{operational_risk}, operational score is "
            f"{operational_score}/100, and operational grade is "
            f"{operational_grade}."
        )

    @staticmethod
    def _first_value(*values):

        for value in values:
            if value not in (
                None,
                "",
                "UNKNOWN"
            ):
                return value

        return "UNKNOWN"

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
