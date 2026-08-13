class AIFinalDecisionOrchestration:

    """
    Step5-3-98
    AI Final Decision Orchestration
    """

    def analyze(
        self,
        final_decision,
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence
    ):

        final_decision = final_decision or {}
        integrated_intelligence = (
            integrated_intelligence or {}
        )
        lifecycle_governance_control = (
            lifecycle_governance_control or {}
        )
        operational_intelligence = (
            operational_intelligence or {}
        )

        decision = self._first_value(
            final_decision.get("decision"),
            integrated_intelligence.get("decision"),
            "UNKNOWN"
        )

        action = self._first_value(
            final_decision.get("action"),
            integrated_intelligence.get("action"),
            "HOLD"
        )

        integrated_score = self._score(
            integrated_intelligence.get(
                "integrated_score"
            )
        )

        governance_score = self._score(
            integrated_intelligence.get(
                "governance_score"
            ),
            lifecycle_governance_control.get(
                "governance_score"
            )
        )

        lifecycle_score = self._score(
            integrated_intelligence.get(
                "lifecycle_score"
            )
        )

        operational_score = self._score(
            integrated_intelligence.get(
                "operational_score"
            ),
            operational_intelligence.get(
                "operational_score"
            )
        )

        confidence_score = self._score(
            integrated_intelligence.get(
                "confidence_score"
            ),
            final_decision.get(
                "confidence_score"
            )
        )

        scores = [
            integrated_score,
            governance_score,
            lifecycle_score,
            operational_score,
            confidence_score
        ]

        valid_scores = [
            score for score in scores
            if score is not None
        ]

        orchestration_score = (
            round(
                sum(valid_scores) / len(valid_scores),
                1
            )
            if valid_scores
            else 0.0
        )

        orchestration_status = (
            self._determine_status(
                integrated_intelligence,
                lifecycle_governance_control,
                operational_intelligence
            )
        )

        orchestration_action = (
            self._determine_action(
                orchestration_status,
                integrated_intelligence,
                final_decision
            )
        )

        orchestration_risk = (
            self._determine_risk(
                integrated_intelligence,
                lifecycle_governance_control,
                operational_intelligence
            )
        )

        execution_authorization = self._first_value(
            integrated_intelligence.get(
                "execution_authorization"
            ),
            lifecycle_governance_control.get(
                "execution_authorization"
            ),
            final_decision.get(
                "execution_status"
            ),
            "UNAUTHORIZED"
        )

        monitoring_policy = self._first_value(
            integrated_intelligence.get(
                "monitoring_policy"
            ),
            lifecycle_governance_control.get(
                "monitoring_policy"
            ),
            "STANDARD"
        )

        reassessment_policy = self._first_value(
            integrated_intelligence.get(
                "reassessment_policy"
            ),
            lifecycle_governance_control.get(
                "reassessment_policy"
            ),
            "REQUIRED"
        )

        signals = []

        self._append_signal(
            signals,
            "Integrated Intelligence",
            integrated_intelligence.get(
                "integrated_status"
            ),
            "INTEGRATED_HEALTHY"
        )

        self._append_signal(
            signals,
            "Operational Intelligence",
            operational_intelligence.get(
                "intelligence_status"
            ),
            "HEALTHY"
        )

        self._append_signal(
            signals,
            "Operational Governance",
            lifecycle_governance_control.get(
                "operational_status"
            ),
            "OPERATIONALLY_HEALTHY"
        )

        self._append_signal(
            signals,
            "Execution Authorization",
            execution_authorization,
            "AUTHORIZED"
        )

        orchestration_grade = self._grade(
            orchestration_score
        )

        reason = self._build_reason(
            decision,
            action,
            orchestration_status,
            orchestration_action,
            orchestration_risk,
            orchestration_score,
            orchestration_grade,
            execution_authorization
        )

        summary = self._build_summary(
            decision,
            action,
            orchestration_status,
            orchestration_action,
            orchestration_risk,
            orchestration_score,
            orchestration_grade
        )

        return {
            "decision": decision,
            "action": action,
            "orchestration_status":
                orchestration_status,
            "orchestration_action":
                orchestration_action,
            "orchestration_risk":
                orchestration_risk,
            "orchestration_score":
                orchestration_score,
            "orchestration_grade":
                orchestration_grade,
            "execution_authorization":
                execution_authorization,
            "monitoring_policy":
                monitoring_policy,
            "reassessment_policy":
                reassessment_policy,
            "integrated_score":
                integrated_score,
            "governance_score":
                governance_score,
            "lifecycle_score":
                lifecycle_score,
            "operational_score":
                operational_score,
            "confidence_score":
                confidence_score,
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
    def _score(*values):

        for value in values:

            if value is None:
                continue

            try:
                return float(value)
            except (
                TypeError,
                ValueError
            ):
                continue

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
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence
    ):

        statuses = [
            integrated_intelligence.get(
                "integrated_status"
            ),
            lifecycle_governance_control.get(
                "operational_status"
            ),
            operational_intelligence.get(
                "intelligence_status"
            )
        ]

        if any(
            status in (
                "INTEGRATION_CRITICAL",
                "CRITICAL",
                "FAILED",
                "BLOCKED",
                "REJECTED"
            )
            for status in statuses
        ):
            return "ORCHESTRATION_BLOCKED"

        if any(
            status in (
                "INTEGRATION_ATTENTION",
                "WARNING",
                "ATTENTION",
                "DEGRADED",
                "REASSESS_REQUIRED"
            )
            for status in statuses
        ):
            return "ORCHESTRATION_REVIEW"

        return "ORCHESTRATION_READY"

    @staticmethod
    def _determine_action(
        orchestration_status,
        integrated_intelligence,
        final_decision
    ):

        if orchestration_status == (
            "ORCHESTRATION_BLOCKED"
        ):
            return "HALT"

        if orchestration_status == (
            "ORCHESTRATION_REVIEW"
        ):
            return "REVIEW"

        return AIFinalDecisionOrchestration._first_value(
            integrated_intelligence.get(
                "integrated_action"
            ),
            final_decision.get(
                "action"
            ),
            "PROCEED"
        )

    @staticmethod
    def _determine_risk(
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence
    ):

        risks = [
            integrated_intelligence.get(
                "integrated_risk"
            ),
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
        orchestration_action,
        risk,
        score,
        grade,
        execution_authorization
    ):

        return (
            f"Final AI decision {decision} with action "
            f"{action} is orchestrated across integrated "
            f"intelligence, lifecycle governance, and "
            f"operational intelligence. Orchestration status "
            f"is {status}, orchestration action is "
            f"{orchestration_action}, risk is {risk}, "
            f"score is {score}/100, grade is {grade}, "
            f"and execution authorization is "
            f"{execution_authorization}."
        )

    @staticmethod
    def _build_summary(
        decision,
        action,
        status,
        orchestration_action,
        risk,
        score,
        grade
    ):

        return (
            f"Final AI decision {decision} with action "
            f"{action} has orchestration status {status}. "
            f"Orchestration action is "
            f"{orchestration_action}, risk is {risk}, "
            f"score is {score}/100, and grade is {grade}."
        )
