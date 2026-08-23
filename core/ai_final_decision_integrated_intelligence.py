class AIFinalDecisionIntegratedIntelligence:
    """
    Step5-3-97
    AI Final Decision Integrated Intelligence
    """

    def analyze(
        self,
        final_decision,
        validation,
        governance,
        execution_control,
        execution_assurance,
        execution_monitoring,
        execution_feedback,
        reassessment,
        lifecycle,
        lifecycle_governance_control,
        operational_intelligence
    ):

        final_decision = final_decision or {}
        validation = validation or {}
        governance = governance or {}
        execution_control = execution_control or {}
        execution_assurance = execution_assurance or {}
        execution_monitoring = execution_monitoring or {}
        execution_feedback = execution_feedback or {}
        reassessment = reassessment or {}
        lifecycle = lifecycle or {}
        lifecycle_governance_control = (
            lifecycle_governance_control or {}
        )
        operational_intelligence = (
            operational_intelligence or {}
        )

        decision = self._first_value(
            final_decision.get("decision"),
            validation.get("decision"),
            governance.get("decision")
        )

        action = self._first_value(
            final_decision.get("action"),
            validation.get("action"),
            governance.get("action")
        )

        validation_score = self._score(
            validation.get("validation_score")
        )

        governance_score = self._score(
            governance.get("governance_score")
        )

        lifecycle_score = self._score(
            lifecycle.get("lifecycle_score")
        )

        operational_score = self._score(
            lifecycle_governance_control.get(
                "operational_score"
            )
        )

        operational_intelligence_score = self._score(
            operational_intelligence.get(
                "intelligence_score"
            )
        )

        confidence_score = self._score(
            final_decision.get("confidence_score")
        )

        scores = [
            validation_score,
            governance_score,
            lifecycle_score,
            operational_score,
            operational_intelligence_score,
            confidence_score
        ]

        valid_scores = [
            score for score in scores
            if score is not None
        ]

        integrated_score = (
            round(sum(valid_scores) / len(valid_scores), 1)
            if valid_scores
            else 0.0
        )

        integrated_status = self._determine_status(
            validation,
            governance,
            execution_control,
            execution_assurance,
            execution_monitoring,
            execution_feedback,
            reassessment,
            lifecycle,
            lifecycle_governance_control,
            operational_intelligence
        )

        integrated_action = self._determine_action(
            integrated_status,
            final_decision,
            lifecycle,
            lifecycle_governance_control,
            operational_intelligence
        )

        integrated_risk = self._determine_risk(
            validation,
            governance,
            execution_control,
            execution_assurance,
            execution_monitoring,
            execution_feedback,
            reassessment,
            lifecycle,
            lifecycle_governance_control,
            operational_intelligence
        )

        execution_authorization = self._first_value(
            lifecycle_governance_control.get(
                "execution_authorization"
            ),
            execution_control.get(
                "execution_status"
            ),
            final_decision.get(
                "execution_status"
            ),
            "UNAUTHORIZED"
        )

        monitoring_policy = self._first_value(
            lifecycle_governance_control.get(
                "monitoring_policy"
            ),
            execution_monitoring.get(
                "monitoring_policy"
            ),
            "STANDARD"
        )

        reassessment_policy = self._first_value(
            lifecycle_governance_control.get(
                "reassessment_policy"
            ),
            "REQUIRED"
            if reassessment.get("reassessment_required")
            else "NOT_REQUIRED"
        )

        signals = []

        self._append_signal(
            signals,
            "Validation",
            validation.get("validation_status"),
            "VALID"
        )

        self._append_signal(
            signals,
            "Governance",
            governance.get("governance_status"),
            "APPROVED"
        )

        self._append_signal(
            signals,
            "Execution Control",
            execution_control.get("control_status"),
            "AUTHORIZED"
        )

        self._append_signal(
            signals,
            "Execution Assurance",
            execution_assurance.get("assurance_status"),
            "ASSURED"
        )

        self._append_signal(
            signals,
            "Execution Feedback",
            execution_feedback.get("feedback_status"),
            "STABLE"
        )

        self._append_signal(
            signals,
            "Reassessment",
            reassessment.get("reassessment_status"),
            "NOT_REQUIRED"
        )

        self._append_signal(
            signals,
            "Lifecycle",
            lifecycle.get("lifecycle_status"),
            "HEALTHY"
        )

        self._append_signal(
            signals,
            "Operational Intelligence",
            operational_intelligence.get(
                "intelligence_status"
            ),
            "HEALTHY"
        )

        integrated_grade = self._grade(integrated_score)

        reason = self._build_reason(
            decision,
            action,
            integrated_status,
            integrated_risk,
            integrated_score,
            integrated_grade,
            execution_authorization
        )

        summary = self._build_summary(
            decision,
            action,
            integrated_status,
            integrated_action,
            integrated_risk,
            integrated_score,
            integrated_grade
        )

        return {
            "decision": decision,
            "action": action,
            "integrated_status": integrated_status,
            "integrated_action": integrated_action,
            "integrated_risk": integrated_risk,
            "integrated_score": integrated_score,
            "integrated_grade": integrated_grade,
            "execution_authorization": execution_authorization,
            "monitoring_policy": monitoring_policy,
            "reassessment_policy": reassessment_policy,
            "validation_score": validation_score,
            "governance_score": governance_score,
            "lifecycle_score": lifecycle_score,
            "operational_score": operational_score,
            "operational_intelligence_score":
                operational_intelligence_score,
            "confidence_score": confidence_score,
            "signals": signals,
            "reason": reason,
            "summary": summary
        }

    @staticmethod
    def _first_value(*values):

        for value in values:

            if value not in (
                None,
                "",
                "UNKNOWN",
                "N/A"
            ):
                return value

        return None

    @staticmethod
    def _score(value):

        if value is None:
            return None

        try:
            return float(value)
        except (
            TypeError,
            ValueError
        ):
            return None

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
    def _append_signal(
        signals,
        name,
        value,
        expected
    ):

        if value is None:
            return

        if value != expected:

            signals.append(
                {
                    "name": name,
                    "status": "ATTENTION",
                    "value": value,
                    "expected": expected
                }
            )

    @staticmethod
    def _determine_status(
        validation,
        governance,
        execution_control,
        execution_assurance,
        execution_monitoring,
        execution_feedback,
        reassessment,
        lifecycle,
        lifecycle_governance_control,
        operational_intelligence
    ):

        statuses = [
            validation.get("validation_status"),
            governance.get("governance_status"),
            execution_control.get("control_status"),
            execution_assurance.get("assurance_status"),
            execution_feedback.get("feedback_status"),
            reassessment.get("reassessment_status"),
            lifecycle.get("lifecycle_status"),
            lifecycle_governance_control.get(
                "operational_status"
            ),
            operational_intelligence.get(
                "intelligence_status"
            )
        ]

        if any(
            status in (
                "INVALID",
                "REJECTED",
                "BLOCKED",
                "FAILED",
                "CRITICAL"
            )
            for status in statuses
        ):
            return "INTEGRATION_CRITICAL"

        if any(
            status in (
                "WARNING",
                "ATTENTION",
                "DEGRADED",
                "REASSESS_REQUIRED",
                "REASSESSMENT_REQUIRED"
            )
            for status in statuses
        ):
            return "INTEGRATION_ATTENTION"

        return "INTEGRATED_HEALTHY"

    @staticmethod
    def _determine_action(
        integrated_status,
        final_decision,
        lifecycle,
        lifecycle_governance_control,
        operational_intelligence
    ):

        if integrated_status == "INTEGRATION_CRITICAL":
            return "HALT"

        if integrated_status == "INTEGRATION_ATTENTION":
            return "REVIEW"

        return AIFinalDecisionIntegratedIntelligence._first_value(
            operational_intelligence.get(
                "intelligence_action"
            ),
            lifecycle_governance_control.get(
                "operational_action"
            ),
            lifecycle.get("lifecycle_action"),
            final_decision.get("action"),
            "CONTINUE"
        )

    @staticmethod
    def _determine_risk(
        validation,
        governance,
        execution_control,
        execution_assurance,
        execution_monitoring,
        execution_feedback,
        reassessment,
        lifecycle,
        lifecycle_governance_control,
        operational_intelligence
    ):

        risks = [
            validation.get("risk_level"),
            governance.get("risk_governance"),
            execution_control.get("control_risk"),
            execution_assurance.get("assurance_risk"),
            execution_monitoring.get("monitoring_risk"),
            execution_feedback.get("feedback_risk"),
            reassessment.get("reassessment_risk"),
            lifecycle.get("lifecycle_risk"),
            lifecycle_governance_control.get(
                "operational_risk"
            ),
            operational_intelligence.get(
                "intelligence_risk"
            )
        ]

        normalized = [
            str(risk).upper()
            for risk in risks
            if risk
        ]

        if "CRITICAL" in normalized:
            return "CRITICAL"

        if "HIGH" in normalized:
            return "HIGH"

        if "MEDIUM" in normalized:
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _build_reason(
        decision,
        action,
        status,
        risk,
        score,
        grade,
        execution_authorization
    ):

        return (
            f"Final AI decision {decision} with action {action} "
            f"is integrated across validation, governance, "
            f"execution, lifecycle, and operational intelligence. "
            f"Integrated status is {status}, risk is {risk}, "
            f"integrated score is {score}/100, grade is {grade}, "
            f"and execution authorization is "
            f"{execution_authorization}."
        )

    @staticmethod
    def _build_summary(
        decision,
        action,
        status,
        integrated_action,
        risk,
        score,
        grade
    ):

        return (
            f"Final AI decision {decision} with action {action} "
            f"has integrated status {status}. Integrated action "
            f"is {integrated_action}, integrated risk is {risk}, "
            f"integrated score is {score}/100, and integrated "
            f"grade is {grade}."
        )
