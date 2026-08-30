class AIFinalDecisionCertification:

    """
    Step5-3-100
    AI Final Decision Certification
    """

    def analyze(
        self,
        final_decision,
        validation,
        governance,
        lifecycle,
        operational_intelligence,
        integrated_intelligence,
        orchestration,
        execution_decision
    ):

        final_decision = final_decision or {}
        validation = validation or {}
        governance = governance or {}
        lifecycle = lifecycle or {}
        operational_intelligence = (
            operational_intelligence or {}
        )
        integrated_intelligence = (
            integrated_intelligence or {}
        )
        orchestration = orchestration or {}
        execution_decision = execution_decision or {}

        decision = self._first_value(
            final_decision.get("decision"),
            execution_decision.get("decision"),
            "UNKNOWN"
        )

        action = self._first_value(
            final_decision.get("action"),
            execution_decision.get("action"),
            "HOLD"
        )

        validation_status = self._first_value(
            validation.get("validation_status"),
            "UNKNOWN"
        )

        governance_status = self._first_value(
            governance.get("governance_status"),
            "UNKNOWN"
        )

        lifecycle_status = self._first_value(
            lifecycle.get("lifecycle_status"),
            "UNKNOWN"
        )

        operational_status = self._first_value(
            operational_intelligence.get(
                "operational_status"
            ),
            "UNKNOWN"
        )

        integrated_status = self._first_value(
            integrated_intelligence.get(
                "integrated_status"
            ),
            "UNKNOWN"
        )

        orchestration_status = self._first_value(
            orchestration.get(
                "orchestration_status"
            ),
            "UNKNOWN"
        )

        execution_status = self._first_value(
            execution_decision.get(
                "execution_status"
            ),
            "UNKNOWN"
        )

        execution_authorization = self._first_value(
            execution_decision.get(
                "execution_authorization"
            ),
            governance.get(
                "execution_status"
            ),
            "UNAUTHORIZED"
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
            operational_intelligence.get(
                "operational_score"
            )
        )

        integrated_score = self._score(
            integrated_intelligence.get(
                "integrated_score"
            )
        )

        orchestration_score = self._score(
            orchestration.get(
                "orchestration_score"
            )
        )

        execution_score = self._score(
            execution_decision.get(
                "execution_score"
            )
        )

        confidence_score = self._score(
            execution_decision.get(
                "confidence_score"
            ),
            final_decision.get(
                "confidence_score"
            )
        )

        scores = [
            validation_score,
            governance_score,
            lifecycle_score,
            operational_score,
            integrated_score,
            orchestration_score,
            execution_score,
            confidence_score
        ]

        valid_scores = [
            score for score in scores
            if score is not None
        ]

        certification_score = (
            round(
                sum(valid_scores) / len(valid_scores),
                1
            )
            if valid_scores
            else 0.0
        )

        statuses = {
            "Decision Validation": validation_status,
            "Governance": governance_status,
            "Lifecycle": lifecycle_status,
            "Operational Intelligence": operational_status,
            "Integrated Intelligence": integrated_status,
            "Orchestration": orchestration_status,
            "Execution Decision": execution_status,
            "Execution Authorization":
                execution_authorization
        }

        certification_status = (
            self._determine_certification_status(
                statuses
            )
        )

        certification_action = (
            self._determine_action(
                certification_status,
                action
            )
        )

        certification_risk = (
            self._determine_risk(
                statuses
            )
        )

        execution_readiness = (
            "READY"
            if (
                certification_status == "CERTIFIED"
                and execution_status == "EXECUTION_READY"
                and execution_authorization == "AUTHORIZED"
            )
            else "NOT_READY"
        )

        decision_integrity = (
            "INTACT"
            if (
                certification_status == "CERTIFIED"
                and certification_risk == "LOW"
            )
            else "REVIEW_REQUIRED"
        )

        signals = []

        self._append_signal(
            signals,
            "Decision Validation",
            validation_status,
            "VALID"
        )

        self._append_signal(
            signals,
            "Governance",
            governance_status,
            "APPROVED"
        )

        self._append_signal(
            signals,
            "Lifecycle",
            lifecycle_status,
            "HEALTHY"
        )

        self._append_signal(
            signals,
            "Operational Intelligence",
            operational_status,
            "OPERATIONALLY_HEALTHY"
        )

        self._append_signal(
            signals,
            "Integrated Intelligence",
            integrated_status,
            "INTEGRATED_HEALTHY"
        )

        self._append_signal(
            signals,
            "Orchestration",
            orchestration_status,
            "ORCHESTRATION_READY"
        )

        self._append_signal(
            signals,
            "Execution Decision",
            execution_status,
            "EXECUTION_READY"
        )

        self._append_signal(
            signals,
            "Execution Authorization",
            execution_authorization,
            "AUTHORIZED"
        )

        certification_grade = self._grade(
            certification_score
        )

        reason = self._build_reason(
            decision,
            action,
            certification_status,
            certification_action,
            certification_risk,
            certification_score,
            certification_grade,
            execution_readiness,
            decision_integrity
        )

        summary = self._build_summary(
            decision,
            certification_status,
            certification_action,
            certification_risk,
            certification_score,
            certification_grade,
            execution_readiness
        )

        return {
            "decision": decision,
            "action": action,
            "certification_status":
                certification_status,
            "certification_score":
                certification_score,
            "certification_grade":
                certification_grade,
            "certification_action":
                certification_action,
            "certification_risk":
                certification_risk,
            "execution_readiness":
                execution_readiness,
            "decision_integrity":
                decision_integrity,
            "validation_status":
                validation_status,
            "governance_status":
                governance_status,
            "lifecycle_status":
                lifecycle_status,
            "operational_status":
                operational_status,
            "integrated_status":
                integrated_status,
            "orchestration_status":
                orchestration_status,
            "execution_status":
                execution_status,
            "execution_authorization":
                execution_authorization,
            "validation_score":
                validation_score,
            "governance_score":
                governance_score,
            "lifecycle_score":
                lifecycle_score,
            "operational_score":
                operational_score,
            "integrated_score":
                integrated_score,
            "orchestration_score":
                orchestration_score,
            "execution_score":
                execution_score,
            "confidence_score":
                confidence_score,
            "certification_signals":
                signals,
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

        return "UNKNOWN"

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
    def _determine_certification_status(
        statuses
    ):

        blocked_states = {
            "CRITICAL",
            "INTEGRATION_CRITICAL",
            "FAILED",
            "BLOCKED",
            "REJECTED",
            "UNAUTHORIZED",
            "EXECUTION_BLOCKED"
        }

        review_states = {
            "ATTENTION",
            "WARNING",
            "DEGRADED",
            "REASSESS_REQUIRED",
            "UNKNOWN"
        }

        normalized = [
            str(value).upper()
            for value in statuses.values()
            if value is not None
        ]

        if any(
            value in blocked_states
            for value in normalized
        ):
            return "CERTIFICATION_BLOCKED"

        if any(
            value in review_states
            for value in normalized
        ):
            return "CERTIFICATION_REVIEW"

        required = [
            "VALID",
            "APPROVED",
            "HEALTHY",
            "OPERATIONALLY_HEALTHY",
            "INTEGRATED_HEALTHY",
            "ORCHESTRATION_READY",
            "EXECUTION_READY",
            "AUTHORIZED"
        ]

        if all(
            value in normalized
            for value in required
        ):
            return "CERTIFIED"

        return "CERTIFICATION_REVIEW"

    @staticmethod
    def _determine_action(
        certification_status,
        action
    ):

        if certification_status == (
            "CERTIFICATION_BLOCKED"
        ):
            return "HALT"

        if certification_status == (
            "CERTIFICATION_REVIEW"
        ):
            return "REVIEW"

        return AIFinalDecisionCertification._first_value(
            action,
            "PROCEED"
        )

    @staticmethod
    def _determine_risk(statuses):

        normalized = [
            str(value).upper()
            for value in statuses.values()
            if value
        ]

        if any(
            value in (
                "CRITICAL",
                "FAILED",
                "BLOCKED",
                "REJECTED",
                "UNAUTHORIZED"
            )
            for value in normalized
        ):
            return "CRITICAL"

        if any(
            value in (
                "WARNING",
                "DEGRADED",
                "ATTENTION",
                "REASSESS_REQUIRED"
            )
            for value in normalized
        ):
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def _build_reason(
        decision,
        action,
        status,
        certification_action,
        risk,
        score,
        grade,
        readiness,
        integrity
    ):

        return (
            f"Final AI decision {decision} with action "
            f"{action} received certification status "
            f"{status}. Certification action is "
            f"{certification_action}, risk is {risk}, "
            f"score is {score}/100, grade is {grade}, "
            f"execution readiness is {readiness}, and "
            f"decision integrity is {integrity}."
        )

    @staticmethod
    def _build_summary(
        decision,
        status,
        action,
        risk,
        score,
        grade,
        readiness
    ):

        return (
            f"Final AI decision {decision} has "
            f"certification status {status}. "
            f"Certification action is {action}, "
            f"risk is {risk}, score is {score}/100, "
            f"grade is {grade}, and execution readiness "
            f"is {readiness}."
        )
