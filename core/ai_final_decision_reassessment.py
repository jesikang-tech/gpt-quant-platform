"""
GPT Quant Platform

AI Final Decision Reassessment Intelligence Engine

Step5-3-93
"""


class AIFinalDecisionReassessment:

    def reassess(
        self,
        final_decision=None,
        governance=None,
        execution_control=None,
        execution_assurance=None,
        execution_feedback=None,
        execution_monitoring=None
    ):
        """
        Evaluate final AI decision execution state and determine
        whether a decision reassessment is required.
        """

        final_decision = final_decision or {}
        governance = governance or {}
        execution_control = execution_control or {}
        execution_assurance = execution_assurance or {}
        execution_feedback = execution_feedback or {}
        execution_monitoring = execution_monitoring or {}

        decision = self._first_value(
            execution_feedback.get("decision"),
            execution_monitoring.get("decision"),
            execution_assurance.get("decision"),
            execution_control.get("decision"),
            final_decision.get("decision"),
            "UNKNOWN"
        )

        action = self._first_value(
            execution_feedback.get("action"),
            execution_monitoring.get("action"),
            execution_assurance.get("action"),
            execution_control.get("action"),
            final_decision.get("action"),
            "UNKNOWN"
        )

        feedback_status = execution_feedback.get(
            "feedback_status",
            "UNKNOWN"
        )

        feedback_action = execution_feedback.get(
            "feedback_action",
            "UNKNOWN"
        )

        feedback_risk = execution_feedback.get(
            "feedback_risk",
            "UNKNOWN"
        )

        feedback_score = self._normalize(
            execution_feedback.get(
                "feedback_score",
                0
            )
        )

        monitoring_status = execution_monitoring.get(
            "monitoring_status",
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

        assurance_status = execution_assurance.get(
            "assurance_status",
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

        control_status = execution_control.get(
            "control_status",
            "UNKNOWN"
        )

        control_risk = execution_control.get(
            "control_risk",
            "UNKNOWN"
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

        validation_status = self._first_value(
            execution_feedback.get("validation_status"),
            execution_assurance.get("validation_status"),
            final_decision.get("validation_status"),
            "UNKNOWN"
        )

        validation_score = self._normalize(
            execution_feedback.get(
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

        reassessment_required = self._determine_reassessment(
            feedback_status,
            feedback_risk,
            feedback_action,
            monitoring_status,
            monitoring_risk,
            monitoring_score,
            assurance_status,
            assurance_risk,
            assurance_score,
            control_status,
            control_risk,
            governance_status,
            governance_score,
            validation_status,
            validation_score
        )

        reassessment_status = self._determine_status(
            reassessment_required,
            feedback_status,
            feedback_risk
        )

        reassessment_action = self._determine_action(
            reassessment_required,
            feedback_action,
            feedback_status,
            feedback_risk
        )

        reassessment_risk = self._determine_risk(
            reassessment_required,
            feedback_risk,
            monitoring_risk,
            assurance_risk,
            control_risk
        )

        reassessment_score = self._calculate_score(
            feedback_score,
            monitoring_score,
            assurance_score,
            governance_score,
            validation_score,
            reassessment_required,
            reassessment_risk
        )

        attention_signals = self._build_attention_signals(
            feedback_status,
            feedback_risk,
            monitoring_risk,
            monitoring_score,
            assurance_status,
            assurance_risk,
            assurance_score,
            control_status,
            control_risk,
            governance_status,
            governance_score,
            validation_status,
            validation_score
        )

        reassessment_reason = self._build_reason(
            reassessment_required,
            reassessment_status,
            attention_signals
        )

        summary = self._build_summary(
            decision,
            action,
            reassessment_required,
            reassessment_status,
            reassessment_action,
            reassessment_risk,
            reassessment_score
        )

        return {
            "decision": decision,
            "action": action,

            "feedback_status": feedback_status,
            "feedback_action": feedback_action,
            "feedback_risk": feedback_risk,
            "feedback_score": feedback_score,

            "monitoring_status": monitoring_status,
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

            "reassessment_required": reassessment_required,
            "reassessment_status": reassessment_status,
            "reassessment_action": reassessment_action,
            "reassessment_risk": reassessment_risk,
            "reassessment_score": reassessment_score,

            "attention_signals": attention_signals,
            "reassessment_reason": reassessment_reason,
            "summary": summary
        }

    @staticmethod
    def _determine_reassessment(
        feedback_status,
        feedback_risk,
        feedback_action,
        monitoring_status,
        monitoring_risk,
        monitoring_score,
        assurance_status,
        assurance_risk,
        assurance_score,
        control_status,
        control_risk,
        governance_status,
        governance_score,
        validation_status,
        validation_score
    ):

        if feedback_status in (
            "CRITICAL",
            "UNSTABLE",
            "REQUIRES_ATTENTION"
        ):
            return True

        if feedback_action in (
            "HALT",
            "REASSESS"
        ):
            return True

        if feedback_risk in (
            "HIGH",
            "CRITICAL"
        ):
            return True

        if monitoring_risk in (
            "HIGH",
            "CRITICAL"
        ):
            return True

        if assurance_risk in (
            "HIGH",
            "CRITICAL"
        ):
            return True

        if control_risk in (
            "HIGH",
            "CRITICAL"
        ):
            return True

        if assurance_status in (
            "BLOCKED",
            "FAILED"
        ):
            return True

        if control_status in (
            "BLOCKED",
            "REJECTED"
        ):
            return True

        if governance_status in (
            "REJECTED",
            "BLOCKED"
        ):
            return True

        if validation_status in (
            "INVALID",
            "FAILED"
        ):
            return True

        if (
            monitoring_status == "CRITICAL_MONITORING"
            or monitoring_status == "BLOCKED_MONITORING"
        ):
            return True

        if monitoring_score < 80:
            return True

        if assurance_score < 80:
            return True

        if governance_score < 80:
            return True

        if validation_score < 80:
            return True

        return False

    @staticmethod
    def _determine_status(
        reassessment_required,
        feedback_status,
        feedback_risk
    ):

        if reassessment_required:
            if feedback_status == "CRITICAL":
                return "CRITICAL_REASSESSMENT"

            if feedback_status == "UNSTABLE":
                return "UNSTABLE_REASSESSMENT"

            return "REASSESSMENT_REQUIRED"

        if (
            feedback_status == "STABLE"
            and feedback_risk == "LOW"
        ):
            return "NOT_REQUIRED"

        return "MONITOR"

    @staticmethod
    def _determine_action(
        reassessment_required,
        feedback_action,
        feedback_status,
        feedback_risk
    ):

        if reassessment_required:
            if feedback_action == "HALT":
                return "HALT_AND_REASSESS"

            if feedback_status == "CRITICAL":
                return "HALT_AND_REASSESS"

            return "REASSESS"

        if (
            feedback_status == "STABLE"
            and feedback_risk == "LOW"
        ):
            return "CONTINUE"

        return "CONTINUE_MONITORING"

    @staticmethod
    def _determine_risk(
        reassessment_required,
        feedback_risk,
        monitoring_risk,
        assurance_risk,
        control_risk
    ):

        risks = {
            feedback_risk,
            monitoring_risk,
            assurance_risk,
            control_risk
        }

        if "CRITICAL" in risks:
            return "CRITICAL"

        if "HIGH" in risks:
            return "HIGH"

        if reassessment_required:
            return "MEDIUM"

        if "MEDIUM" in risks:
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _calculate_score(
        feedback_score,
        monitoring_score,
        assurance_score,
        governance_score,
        validation_score,
        reassessment_required,
        reassessment_risk
    ):

        score = (
            feedback_score * 0.30
            + monitoring_score * 0.20
            + assurance_score * 0.20
            + governance_score * 0.15
            + validation_score * 0.15
        )

        if reassessment_required:
            score -= 10

        if reassessment_risk == "HIGH":
            score -= 5

        if reassessment_risk == "CRITICAL":
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
    def _build_attention_signals(
        feedback_status,
        feedback_risk,
        monitoring_risk,
        monitoring_score,
        assurance_status,
        assurance_risk,
        assurance_score,
        control_status,
        control_risk,
        governance_status,
        governance_score,
        validation_status,
        validation_score
    ):

        signals = []

        if feedback_status not in (
            "STABLE",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Feedback Status",
                "value": feedback_status
            })

        if feedback_risk not in (
            "LOW",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Feedback Risk",
                "value": feedback_risk
            })

        if monitoring_risk not in (
            "LOW",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Monitoring Risk",
                "value": monitoring_risk
            })

        if monitoring_score < 80:
            signals.append({
                "name": "Monitoring Score",
                "value": monitoring_score
            })

        if assurance_status not in (
            "ASSURED",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Assurance Status",
                "value": assurance_status
            })

        if assurance_risk not in (
            "LOW",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Assurance Risk",
                "value": assurance_risk
            })

        if assurance_score < 80:
            signals.append({
                "name": "Assurance Score",
                "value": assurance_score
            })

        if control_status not in (
            "AUTHORIZED",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Control Status",
                "value": control_status
            })

        if control_risk not in (
            "LOW",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Control Risk",
                "value": control_risk
            })

        if governance_status not in (
            "APPROVED",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Governance Status",
                "value": governance_status
            })

        if governance_score < 80:
            signals.append({
                "name": "Governance Score",
                "value": governance_score
            })

        if validation_status not in (
            "VALID",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Validation Status",
                "value": validation_status
            })

        if validation_score < 80:
            signals.append({
                "name": "Validation Score",
                "value": validation_score
            })

        return signals

    @staticmethod
    def _build_reason(
        reassessment_required,
        reassessment_status,
        attention_signals
    ):

        if not reassessment_required:
            return (
                "No reassessment is required because execution feedback, "
                "monitoring, assurance, governance, control, and validation "
                "signals remain within acceptable operating ranges."
            )

        if reassessment_status == "CRITICAL_REASSESSMENT":
            return (
                "Immediate reassessment is required because critical "
                "execution or monitoring conditions were detected."
            )

        if reassessment_status == "UNSTABLE_REASSESSMENT":
            return (
                "Reassessment is required because the final AI decision "
                "execution state is unstable and supporting intelligence "
                "signals require renewed evaluation."
            )

        if attention_signals:
            signal_names = ", ".join(
                signal["name"]
                for signal in attention_signals[:4]
            )

            return (
                "Reassessment is required because attention signals were "
                f"detected in {signal_names}."
            )

        return (
            "Reassessment is required because one or more final AI decision "
            "execution conditions are outside the expected operating range."
        )

    @staticmethod
    def _build_summary(
        decision,
        action,
        reassessment_required,
        reassessment_status,
        reassessment_action,
        reassessment_risk,
        reassessment_score
    ):

        return (
            f"Final AI decision {decision} with action {action} has "
            f"reassessment status {reassessment_status}. Reassessment "
            f"action is {reassessment_action}, reassessment risk is "
            f"{reassessment_risk}, reassessment score is "
            f"{reassessment_score}/100, and reassessment required is "
            f"{reassessment_required}."
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
