"""
GPT Quant Platform

AI Final Decision Lifecycle Governance & Control Intelligence

Step5-3-95
"""


class AIFinalDecisionLifecycleGovernanceControl:

    def govern(
        self,
        final_decision=None,
        governance=None,
        execution_control=None,
        execution_assurance=None,
        execution_monitoring=None,
        execution_feedback=None,
        reassessment=None,
        lifecycle=None,
        decision_confidence=None,
        validation=None
    ):
        """
        Integrate final decision lifecycle intelligence and determine
        the final operational governance and control state.
        """

        final_decision = final_decision or {}
        governance = governance or {}
        execution_control = execution_control or {}
        execution_assurance = execution_assurance or {}
        execution_monitoring = execution_monitoring or {}
        execution_feedback = execution_feedback or {}
        reassessment = reassessment or {}
        lifecycle = lifecycle or {}
        decision_confidence = decision_confidence or {}
        validation = validation or {}

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

        monitoring_status = execution_monitoring.get(
            "monitoring_status",
            "UNKNOWN"
        )

        monitoring_risk = execution_monitoring.get(
            "monitoring_risk",
            "UNKNOWN"
        )

        feedback_status = execution_feedback.get(
            "feedback_status",
            "UNKNOWN"
        )

        feedback_risk = execution_feedback.get(
            "feedback_risk",
            "UNKNOWN"
        )

        reassessment_required = bool(
            reassessment.get(
                "reassessment_required",
                False
            )
        )

        reassessment_status = reassessment.get(
            "reassessment_status",
            "UNKNOWN"
        )

        reassessment_risk = reassessment.get(
            "reassessment_risk",
            "UNKNOWN"
        )

        validation_status = validation.get(
            "validation_status",
            final_decision.get(
                "validation_status",
                "UNKNOWN"
            )
        )

        validation_score = self._normalize(
            validation.get(
                "validation_score",
                final_decision.get(
                    "validation_score",
                    0
                )
            )
        )

        confidence_score = self._normalize(
            decision_confidence.get(
                "confidence_score",
                final_decision.get(
                    "confidence_score",
                    0
                )
            )
        )

        operational_status = self._determine_operational_status(
            lifecycle_status,
            governance_status,
            control_status,
            assurance_status,
            monitoring_status,
            feedback_status,
            reassessment_required,
            validation_status
        )

        operational_risk = self._determine_operational_risk(
            lifecycle_risk,
            control_risk,
            assurance_risk,
            monitoring_risk,
            feedback_risk,
            reassessment_risk,
            confidence_score,
            validation_score
        )

        operational_score = self._calculate_score(
            lifecycle_score,
            governance_score,
            confidence_score,
            validation_score,
            operational_risk,
            reassessment_required
        )

        operational_grade = self._grade(
            operational_score
        )

        execution_authorization = self._determine_execution_authorization(
            operational_status,
            operational_risk,
            control_status,
            assurance_status,
            reassessment_required,
            validation_status
        )

        monitoring_policy = self._determine_monitoring_policy(
            operational_risk,
            lifecycle_action,
            reassessment_required
        )

        reassessment_policy = self._determine_reassessment_policy(
            operational_status,
            operational_risk,
            reassessment_required
        )

        control_signals = self._build_control_signals(
            lifecycle_status,
            lifecycle_risk,
            governance_status,
            governance_score,
            control_status,
            control_risk,
            assurance_status,
            assurance_risk,
            monitoring_status,
            monitoring_risk,
            feedback_status,
            feedback_risk,
            reassessment_required,
            reassessment_status,
            reassessment_risk,
            validation_status,
            validation_score,
            confidence_score
        )

        operational_action = self._determine_action(
            operational_status,
            operational_risk,
            execution_authorization,
            reassessment_required
        )

        operational_reason = self._build_reason(
            operational_status,
            operational_risk,
            execution_authorization,
            reassessment_required,
            control_signals
        )

        operational_summary = self._build_summary(
            decision,
            action,
            operational_status,
            operational_action,
            operational_risk,
            operational_score,
            operational_grade,
            execution_authorization
        )

        return {
            "decision": decision,
            "action": action,

            "lifecycle_status": lifecycle_status,
            "lifecycle_action": lifecycle_action,
            "lifecycle_risk": lifecycle_risk,
            "lifecycle_score": lifecycle_score,
            "lifecycle_grade": lifecycle_grade,

            "governance_status": governance_status,
            "governance_score": governance_score,

            "control_status": control_status,
            "control_risk": control_risk,

            "assurance_status": assurance_status,
            "assurance_risk": assurance_risk,

            "monitoring_status": monitoring_status,
            "monitoring_risk": monitoring_risk,

            "feedback_status": feedback_status,
            "feedback_risk": feedback_risk,

            "reassessment_required": reassessment_required,
            "reassessment_status": reassessment_status,
            "reassessment_risk": reassessment_risk,

            "validation_status": validation_status,
            "validation_score": validation_score,

            "confidence_score": confidence_score,

            "operational_status": operational_status,
            "operational_action": operational_action,
            "operational_risk": operational_risk,
            "operational_score": operational_score,
            "operational_grade": operational_grade,

            "execution_authorization": execution_authorization,
            "monitoring_policy": monitoring_policy,
            "reassessment_policy": reassessment_policy,

            "control_signals": control_signals,
            "operational_reason": operational_reason,
            "operational_summary": operational_summary
        }

    @staticmethod
    def _determine_operational_status(
        lifecycle_status,
        governance_status,
        control_status,
        assurance_status,
        monitoring_status,
        feedback_status,
        reassessment_required,
        validation_status
    ):

        if reassessment_required:
            return "REASSESSMENT_REQUIRED"

        if validation_status in (
            "INVALID",
            "FAILED"
        ):
            return "VALIDATION_BLOCKED"

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
            return "ASSURANCE_BLOCKED"

        if lifecycle_status in (
            "MONITORING_CRITICAL",
            "FEEDBACK_UNSTABLE"
        ):
            return "CONTROLLED_MONITORING"

        if lifecycle_status == "HEALTHY":
            if (
                governance_status == "APPROVED"
                and control_status == "AUTHORIZED"
                and assurance_status == "ASSURED"
                and monitoring_status == "STANDARD_MONITORING"
                and feedback_status == "STABLE"
            ):
                return "OPERATIONALLY_HEALTHY"

        return "MONITORING"

    @staticmethod
    def _determine_operational_risk(
        lifecycle_risk,
        control_risk,
        assurance_risk,
        monitoring_risk,
        feedback_risk,
        reassessment_risk,
        confidence_score,
        validation_score
    ):

        risks = {
            lifecycle_risk,
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

        if confidence_score < 80 or validation_score < 80:
            return "MEDIUM"

        if "MEDIUM" in risks:
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _calculate_score(
        lifecycle_score,
        governance_score,
        confidence_score,
        validation_score,
        operational_risk,
        reassessment_required
    ):

        score = (
            lifecycle_score * 0.40
            + governance_score * 0.20
            + confidence_score * 0.20
            + validation_score * 0.20
        )

        if reassessment_required:
            score -= 10

        if operational_risk == "MEDIUM":
            score -= 5

        if operational_risk == "HIGH":
            score -= 10

        if operational_risk == "CRITICAL":
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
    def _determine_execution_authorization(
        operational_status,
        operational_risk,
        control_status,
        assurance_status,
        reassessment_required,
        validation_status
    ):

        if validation_status in (
            "INVALID",
            "FAILED"
        ):
            return "DENIED"

        if reassessment_required:
            return "SUSPENDED"

        if operational_risk == "CRITICAL":
            return "DENIED"

        if operational_risk == "HIGH":
            return "REVIEW_REQUIRED"

        if (
            operational_status == "OPERATIONALLY_HEALTHY"
            and control_status == "AUTHORIZED"
            and assurance_status == "ASSURED"
        ):
            return "AUTHORIZED"

        if operational_risk == "MEDIUM":
            return "CONDITIONAL"

        return "MONITORING_ONLY"

    @staticmethod
    def _determine_monitoring_policy(
        operational_risk,
        lifecycle_action,
        reassessment_required
    ):

        if reassessment_required:
            return "INTENSIVE"

        if operational_risk == "CRITICAL":
            return "CONTINUOUS"

        if operational_risk == "HIGH":
            return "ENHANCED"

        if operational_risk == "MEDIUM":
            return "ELEVATED"

        if lifecycle_action == "CONTINUE":
            return "STANDARD"

        return "STANDARD"

    @staticmethod
    def _determine_reassessment_policy(
        operational_status,
        operational_risk,
        reassessment_required
    ):

        if reassessment_required:
            return "IMMEDIATE"

        if operational_risk == "CRITICAL":
            return "IMMEDIATE"

        if operational_risk == "HIGH":
            return "REQUIRED"

        if operational_risk == "MEDIUM":
            return "CONDITIONAL"

        if operational_status == "OPERATIONALLY_HEALTHY":
            return "NOT_REQUIRED"

        return "MONITOR"

    @staticmethod
    def _determine_action(
        operational_status,
        operational_risk,
        execution_authorization,
        reassessment_required
    ):

        if reassessment_required:
            return "REASSESS"

        if execution_authorization == "DENIED":
            return "HALT"

        if execution_authorization == "SUSPENDED":
            return "SUSPEND"

        if execution_authorization == "REVIEW_REQUIRED":
            return "REVIEW"

        if operational_status == "OPERATIONALLY_HEALTHY":
            return "CONTINUE"

        if operational_risk == "MEDIUM":
            return "MONITOR"

        return "CONTINUE_MONITORING"

    @staticmethod
    def _build_control_signals(
        lifecycle_status,
        lifecycle_risk,
        governance_status,
        governance_score,
        control_status,
        control_risk,
        assurance_status,
        assurance_risk,
        monitoring_status,
        monitoring_risk,
        feedback_status,
        feedback_risk,
        reassessment_required,
        reassessment_status,
        reassessment_risk,
        validation_status,
        validation_score,
        confidence_score
    ):

        signals = []

        if lifecycle_status != "HEALTHY":
            signals.append({
                "name": "Lifecycle Status",
                "value": lifecycle_status
            })

        if lifecycle_risk not in (
            "LOW",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Lifecycle Risk",
                "value": lifecycle_risk
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

        if confidence_score < 80:
            signals.append({
                "name": "Confidence Score",
                "value": confidence_score
            })

        return signals

    @staticmethod
    def _build_reason(
        operational_status,
        operational_risk,
        execution_authorization,
        reassessment_required,
        control_signals
    ):

        if operational_status == "OPERATIONALLY_HEALTHY":
            return (
                "Final AI decision lifecycle governance is operating "
                "normally with authorized execution, stable monitoring, "
                "valid assurance, and acceptable risk."
            )

        if reassessment_required:
            return (
                "Operational control requires reassessment because the "
                "final AI decision lifecycle contains signals requiring "
                "renewed evaluation."
            )

        if execution_authorization == "DENIED":
            return (
                "Execution authorization is denied because operational "
                "risk or validation conditions do not support continued "
                "execution."
            )

        if execution_authorization == "REVIEW_REQUIRED":
            return (
                "Execution requires review because operational risk is "
                "elevated and continued execution should not proceed "
                "without additional control."
            )

        if control_signals:
            names = ", ".join(
                signal["name"]
                for signal in control_signals[:4]
            )

            return (
                "Operational governance remains under control monitoring "
                f"because attention signals were detected in {names}."
            )

        return (
            "Final AI decision remains operational with continued "
            "governance and control monitoring recommended."
        )

    @staticmethod
    def _build_summary(
        decision,
        action,
        operational_status,
        operational_action,
        operational_risk,
        operational_score,
        operational_grade,
        execution_authorization
    ):

        return (
            f"Final AI decision {decision} with action {action} has "
            f"operational status {operational_status}. Operational "
            f"action is {operational_action}, operational risk is "
            f"{operational_risk}, operational score is "
            f"{operational_score}/100, operational grade is "
            f"{operational_grade}, and execution authorization is "
            f"{execution_authorization}."
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

