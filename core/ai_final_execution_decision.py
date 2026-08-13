class AIFinalExecutionDecision:

    """
    Step5-3-99
    AI Final Execution Decision
    """

    def analyze(
        self,
        final_decision,
        orchestration,
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence
    ):

        final_decision = final_decision or {}
        orchestration = orchestration or {}
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
            orchestration.get("decision"),
            integrated_intelligence.get("decision"),
            "UNKNOWN"
        )

        action = self._first_value(
            orchestration.get("orchestration_action"),
            final_decision.get("action"),
            integrated_intelligence.get("action"),
            "HOLD"
        )

        orchestration_status = self._first_value(
            orchestration.get("orchestration_status"),
            "UNKNOWN"
        )

        orchestration_risk = self._first_value(
            orchestration.get("orchestration_risk"),
            "UNKNOWN"
        )

        execution_authorization = self._first_value(
            orchestration.get("execution_authorization"),
            integrated_intelligence.get(
                "execution_authorization"
            ),
            lifecycle_governance_control.get(
                "execution_authorization"
            ),
            final_decision.get("execution_status"),
            "UNAUTHORIZED"
        )

        reassessment_policy = self._first_value(
            orchestration.get("reassessment_policy"),
            lifecycle_governance_control.get(
                "reassessment_policy"
            ),
            "REQUIRED"
        )

        confidence_score = self._score(
            orchestration.get("confidence_score"),
            integrated_intelligence.get(
                "confidence_score"
            ),
            final_decision.get("confidence_score")
        )

        orchestration_score = self._score(
            orchestration.get("orchestration_score")
        )

        integrated_score = self._score(
            orchestration.get("integrated_score"),
            integrated_intelligence.get(
                "integrated_score"
            )
        )

        governance_score = self._score(
            orchestration.get("governance_score"),
            lifecycle_governance_control.get(
                "governance_score"
            )
        )

        lifecycle_score = self._score(
            orchestration.get("lifecycle_score")
        )

        operational_score = self._score(
            orchestration.get("operational_score"),
            operational_intelligence.get(
                "operational_score"
            )
        )

        scores = [
            orchestration_score,
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

        execution_score = (
            round(
                sum(valid_scores) / len(valid_scores),
                1
            )
            if valid_scores
            else 0.0
        )

        execution_status = self._determine_execution_status(
            orchestration_status,
            orchestration_risk,
            execution_authorization,
            reassessment_policy
        )

        execution_decision = self._determine_execution_decision(
            execution_status,
            action
        )

        execution_risk = self._determine_risk(
            orchestration_risk,
            integrated_intelligence,
            lifecycle_governance_control,
            operational_intelligence
        )

        execution_grade = self._grade(
            execution_score
        )

        signals = []

        self._append_signal(
            signals,
            "Orchestration Status",
            orchestration_status,
            "ORCHESTRATION_READY"
        )

        self._append_signal(
            signals,
            "Execution Authorization",
            execution_authorization,
            "AUTHORIZED"
        )

        self._append_signal(
            signals,
            "Reassessment Policy",
            reassessment_policy,
            "NOT_REQUIRED"
        )

        self._append_signal(
            signals,
            "Execution Risk",
            execution_risk,
            "LOW"
        )

        reason = self._build_reason(
            decision,
            action,
            execution_status,
            execution_decision,
            execution_risk,
            execution_score,
            execution_grade,
            execution_authorization
        )

        summary = self._build_summary(
            decision,
            execution_status,
            execution_decision,
            execution_risk,
            execution_score,
            execution_grade
        )

        return {
            "decision": decision,
            "action": action,
            "execution_decision":
                execution_decision,
            "execution_status":
                execution_status,
            "execution_risk":
                execution_risk,
            "execution_score":
                execution_score,
            "execution_grade":
                execution_grade,
            "execution_authorization":
                execution_authorization,
            "orchestration_status":
                orchestration_status,
            "orchestration_risk":
                orchestration_risk,
            "reassessment_policy":
                reassessment_policy,
            "confidence_score":
                confidence_score,
            "orchestration_score":
                orchestration_score,
            "integrated_score":
                integrated_score,
            "governance_score":
                governance_score,
            "lifecycle_score":
                lifecycle_score,
            "operational_score":
                operational_score,
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
    def _determine_execution_status(
        orchestration_status,
        orchestration_risk,
        execution_authorization,
        reassessment_policy
    ):

        if orchestration_status in (
            "ORCHESTRATION_BLOCKED",
            "CRITICAL",
            "FAILED"
        ):
            return "EXECUTION_BLOCKED"

        if orchestration_risk in (
            "CRITICAL",
            "HIGH"
        ):
            return "EXECUTION_BLOCKED"

        if execution_authorization != "AUTHORIZED":
            return "EXECUTION_REVIEW"

        if reassessment_policy not in (
            "NOT_REQUIRED",
            "NONE"
        ):
            return "EXECUTION_REVIEW"

        if orchestration_status == "ORCHESTRATION_REVIEW":
            return "EXECUTION_REVIEW"

        return "EXECUTION_READY"

    @staticmethod
    def _determine_execution_decision(
        execution_status,
        action
    ):

        if execution_status == "EXECUTION_BLOCKED":
            return "HALT"

        if execution_status == "EXECUTION_REVIEW":
            return "REVIEW"

        return AIFinalExecutionDecision._first_value(
            action,
            "PROCEED"
        )

    @staticmethod
    def _determine_risk(
        orchestration_risk,
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence
    ):

        risks = [
            orchestration_risk,
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
        execution_decision,
        risk,
        score,
        grade,
        execution_authorization
    ):

        return (
            f"Final AI decision {decision} with action "
            f"{action} reached execution status {status}. "
            f"Final execution decision is "
            f"{execution_decision}, risk is {risk}, "
            f"score is {score}/100, grade is {grade}, "
            f"and execution authorization is "
            f"{execution_authorization}."
        )

    @staticmethod
    def _build_summary(
        decision,
        status,
        execution_decision,
        risk,
        score,
        grade
    ):

        return (
            f"Final AI decision {decision} has execution "
            f"status {status}. Execution decision is "
            f"{execution_decision}, risk is {risk}, "
            f"score is {score}/100, and grade is {grade}."
        )
