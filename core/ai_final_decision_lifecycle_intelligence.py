"""
GPT Quant Platform

AI Final Decision Lifecycle Intelligence Engine

Step5-3-94
"""


class AIFinalDecisionLifecycleIntelligence:

    def analyze(
        self,
        final_decision=None,
        governance=None,
        execution_control=None,
        execution_assurance=None,
        execution_monitoring=None,
        execution_feedback=None,
        reassessment=None
    ):
        """
        Integrate the complete AI final decision lifecycle
        and determine its overall operational health.
        """

        final_decision = final_decision or {}
        governance = governance or {}
        execution_control = execution_control or {}
        execution_assurance = execution_assurance or {}
        execution_monitoring = execution_monitoring or {}
        execution_feedback = execution_feedback or {}
        reassessment = reassessment or {}

        decision = self._first_value(
            final_decision.get("decision"),
            governance.get("decision"),
            execution_control.get("decision"),
            "UNKNOWN"
        )

        action = self._first_value(
            final_decision.get("action"),
            governance.get("action"),
            execution_control.get("action"),
            "UNKNOWN"
        )

        validation_status = self._first_value(
            final_decision.get("validation_status"),
            execution_feedback.get("validation_status"),
            "UNKNOWN"
        )

        validation_score = self._normalize(
            final_decision.get(
                "validation_score",
                execution_feedback.get("validation_score", 0)
            )
        )

        governance_status = governance.get(
            "governance_status",
            "UNKNOWN"
        )

        governance_score = self._normalize(
            governance.get("governance_score", 0)
        )

        control_status = execution_control.get(
            "control_status",
            "UNKNOWN"
        )

        control_risk = execution_control.get(
            "control_risk",
            "UNKNOWN"
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
            execution_assurance.get("assurance_score", 0)
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
            execution_monitoring.get("monitoring_score", 0)
        )

        feedback_status = execution_feedback.get(
            "feedback_status",
            "UNKNOWN"
        )

        feedback_risk = execution_feedback.get(
            "feedback_risk",
            "UNKNOWN"
        )

        feedback_score = self._normalize(
            execution_feedback.get("feedback_score", 0)
        )

        reassessment_status = reassessment.get(
            "reassessment_status",
            "UNKNOWN"
        )

        reassessment_required = bool(
            reassessment.get(
                "reassessment_required",
                False
            )
        )

        reassessment_risk = reassessment.get(
            "reassessment_risk",
            "UNKNOWN"
        )

        reassessment_score = self._normalize(
            reassessment.get("reassessment_score", 0)
        )

        lifecycle_status = self._determine_status(
            validation_status,
            governance_status,
            control_status,
            assurance_status,
            monitoring_status,
            feedback_status,
            reassessment_status,
            reassessment_required
        )

        lifecycle_risk = self._determine_risk(
            control_risk,
            assurance_risk,
            monitoring_risk,
            feedback_risk,
            reassessment_risk
        )

        lifecycle_score = self._calculate_score(
            validation_score,
            governance_score,
            assurance_score,
            monitoring_score,
            feedback_score,
            reassessment_score,
            lifecycle_risk,
            reassessment_required
        )

        lifecycle_grade = self._grade(lifecycle_score)

        attention_signals = self._build_attention_signals(
            validation_status,
            validation_score,
            governance_status,
            governance_score,
            control_status,
            control_risk,
            assurance_status,
            assurance_risk,
            assurance_score,
            monitoring_status,
            monitoring_risk,
            monitoring_score,
            feedback_status,
            feedback_risk,
            feedback_score,
            reassessment_status,
            reassessment_required,
            reassessment_risk,
            reassessment_score
        )

        lifecycle_action = self._determine_action(
            lifecycle_status,
            lifecycle_risk,
            reassessment_required
        )

        lifecycle_summary = self._build_summary(
            decision,
            action,
            lifecycle_status,
            lifecycle_action,
            lifecycle_risk,
            lifecycle_score,
            lifecycle_grade
        )

        lifecycle_reason = self._build_reason(
            lifecycle_status,
            lifecycle_risk,
            reassessment_required,
            attention_signals
        )

        return {
            "decision": decision,
            "action": action,

            "validation_status": validation_status,
            "validation_score": validation_score,

            "governance_status": governance_status,
            "governance_score": governance_score,

            "control_status": control_status,
            "control_risk": control_risk,

            "assurance_status": assurance_status,
            "assurance_risk": assurance_risk,
            "assurance_score": assurance_score,

            "monitoring_status": monitoring_status,
            "monitoring_risk": monitoring_risk,
            "monitoring_score": monitoring_score,

            "feedback_status": feedback_status,
            "feedback_risk": feedback_risk,
            "feedback_score": feedback_score,

            "reassessment_status": reassessment_status,
            "reassessment_required": reassessment_required,
            "reassessment_risk": reassessment_risk,
            "reassessment_score": reassessment_score,

            "lifecycle_status": lifecycle_status,
            "lifecycle_action": lifecycle_action,
            "lifecycle_risk": lifecycle_risk,
            "lifecycle_score": lifecycle_score,
            "lifecycle_grade": lifecycle_grade,

            "attention_signals": attention_signals,
            "lifecycle_reason": lifecycle_reason,
            "lifecycle_summary": lifecycle_summary
        }

    @staticmethod
    def _determine_status(
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
            return "REASSESSMENT_REQUIRED"

        if validation_status in (
            "INVALID",
            "FAILED"
        ):
            return "VALIDATION_FAILED"

        if governance_status in (
            "REJECTED",
            "BLOCKED"
        ):
            return "GOVERNANCE_BLOCKED"

        if control_status in (
            "BLOCKED",
            "REJECTED"
        ):
            return "EXECUTION_BLOCKED"

        if assurance_status in (
            "FAILED",
            "BLOCKED"
        ):
            return "ASSURANCE_FAILED"

        if monitoring_status in (
            "CRITICAL_MONITORING",
            "BLOCKED_MONITORING"
        ):
            return "MONITORING_CRITICAL"

        if feedback_status in (
            "CRITICAL",
            "UNSTABLE"
        ):
            return "FEEDBACK_UNSTABLE"

        if reassessment_status in (
            "CRITICAL_REASSESSMENT",
            "UNSTABLE_REASSESSMENT"
        ):
            return "REASSESSMENT_REQUIRED"

        if (
            validation_status == "VALID"
            and governance_status == "APPROVED"
            and control_status == "AUTHORIZED"
            and assurance_status == "ASSURED"
            and feedback_status == "STABLE"
        ):
            return "HEALTHY"

        return "MONITORING"

    @staticmethod
    def _determine_risk(
        control_risk,
        assurance_risk,
        monitoring_risk,
        feedback_risk,
        reassessment_risk
    ):

        risks = {
            control_risk,
            assurance_risk,
            monitoring_risk,
            feedback_risk,
            reassessment_risk
        }

        if "CRITICAL" in risks:
            return "CRITICAL"

        if "HIGH" in risks:
            return "HIGH"

        if "MEDIUM" in risks:
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _calculate_score(
        validation_score,
        governance_score,
        assurance_score,
        monitoring_score,
        feedback_score,
        reassessment_score,
        lifecycle_risk,
        reassessment_required
    ):

        score = (
            validation_score * 0.15
            + governance_score * 0.15
            + assurance_score * 0.15
            + monitoring_score * 0.15
            + feedback_score * 0.20
            + reassessment_score * 0.20
        )

        if reassessment_required:
            score -= 10

        if lifecycle_risk == "MEDIUM":
            score -= 5

        if lifecycle_risk == "HIGH":
            score -= 10

        if lifecycle_risk == "CRITICAL":
            score -= 20

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
    def _determine_action(
        lifecycle_status,
        lifecycle_risk,
        reassessment_required
    ):

        if lifecycle_status == "HEALTHY":
            return "CONTINUE"

        if reassessment_required:
            return "REASSESS"

        if lifecycle_risk == "CRITICAL":
            return "HALT"

        if lifecycle_risk == "HIGH":
            return "REVIEW"

        if lifecycle_risk == "MEDIUM":
            return "MONITOR"

        return "CONTINUE_MONITORING"

    @staticmethod
    def _build_attention_signals(
        validation_status,
        validation_score,
        governance_status,
        governance_score,
        control_status,
        control_risk,
        assurance_status,
        assurance_risk,
        assurance_score,
        monitoring_status,
        monitoring_risk,
        monitoring_score,
        feedback_status,
        feedback_risk,
        feedback_score,
        reassessment_status,
        reassessment_required,
        reassessment_risk,
        reassessment_score
    ):

        signals = []

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

        if monitoring_status not in (
            "STANDARD_MONITORING",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Monitoring Status",
                "value": monitoring_status
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

        if feedback_score < 80:
            signals.append({
                "name": "Feedback Score",
                "value": feedback_score
            })

        if reassessment_required:
            signals.append({
                "name": "Reassessment Required",
                "value": True
            })

        if reassessment_status not in (
            "NOT_REQUIRED",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Reassessment Status",
                "value": reassessment_status
            })

        if reassessment_risk not in (
            "LOW",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Reassessment Risk",
                "value": reassessment_risk
            })

        if reassessment_score < 80:
            signals.append({
                "name": "Reassessment Score",
                "value": reassessment_score
            })

        return signals

    @staticmethod
    def _build_reason(
        lifecycle_status,
        lifecycle_risk,
        reassessment_required,
        attention_signals
    ):

        if lifecycle_status == "HEALTHY":
            return (
                "The final AI decision lifecycle is operating normally "
                "with validation, governance, execution, monitoring, "
                "feedback, and reassessment signals within acceptable "
                "operating ranges."
            )

        if reassessment_required:
            return (
                "The final AI decision lifecycle requires reassessment "
                "because the execution lifecycle contains signals that "
                "require renewed evaluation."
            )

        if lifecycle_risk == "CRITICAL":
            return (
                "The final AI decision lifecycle is critical and requires "
                "immediate intervention."
            )

        if lifecycle_risk == "HIGH":
            return (
                "The final AI decision lifecycle has elevated risk and "
                "requires review before continued execution."
            )

        if attention_signals:
            names = ", ".join(
                signal["name"]
                for signal in attention_signals[:4]
            )

            return (
                "The final AI decision lifecycle remains under monitoring "
                f"because attention signals were detected in {names}."
            )

        return (
            "The final AI decision lifecycle remains operational with "
            "continued monitoring recommended."
        )

    @staticmethod
    def _build_summary(
        decision,
        action,
        lifecycle_status,
        lifecycle_action,
        lifecycle_risk,
        lifecycle_score,
        lifecycle_grade
    ):

        return (
            f"Final AI decision {decision} with action {action} has "
            f"lifecycle status {lifecycle_status}. Lifecycle action is "
            f"{lifecycle_action}, lifecycle risk is {lifecycle_risk}, "
            f"lifecycle score is {lifecycle_score}/100, and lifecycle "
            f"grade is {lifecycle_grade}."
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
