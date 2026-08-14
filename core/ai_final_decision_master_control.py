class AIFinalDecisionMasterControl:

    """
    Step5-3-101
    AI Final Decision Master Control
    """

    def analyze(
        self,
        final_decision,
        certification,
        execution_decision,
        governance,
        lifecycle,
        operational_intelligence,
        orchestration,
        integrated_intelligence,
        validation
    ):

        final_decision = final_decision or {}
        certification = certification or {}
        execution_decision = execution_decision or {}
        governance = governance or {}
        lifecycle = lifecycle or {}
        operational_intelligence = operational_intelligence or {}
        orchestration = orchestration or {}
        integrated_intelligence = integrated_intelligence or {}
        validation = validation or {}

        decision = self._first_value(
            final_decision.get("decision"),
            certification.get("decision"),
            execution_decision.get("decision"),
            "UNKNOWN"
        )

        action = self._first_value(
            certification.get("certification_action"),
            execution_decision.get("action"),
            final_decision.get("action"),
            "HOLD"
        )

        certification_status = self._first_value(
            certification.get("certification_status"),
            "UNKNOWN"
        )

        certification_risk = self._first_value(
            certification.get("certification_risk"),
            "UNKNOWN"
        )

        execution_status = self._first_value(
            execution_decision.get("execution_status"),
            certification.get("execution_status"),
            "UNKNOWN"
        )

        execution_authorization = self._first_value(
            execution_decision.get("execution_authorization"),
            certification.get("execution_authorization"),
            "UNAUTHORIZED"
        )

        execution_readiness = self._first_value(
            certification.get("execution_readiness"),
            execution_decision.get("execution_status"),
            "NOT_READY"
        )

        decision_integrity = self._first_value(
            certification.get("decision_integrity"),
            "REVIEW_REQUIRED"
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
            operational_intelligence.get("operational_status"),
            "UNKNOWN"
        )

        orchestration_status = self._first_value(
            orchestration.get("orchestration_status"),
            "UNKNOWN"
        )

        integrated_status = self._first_value(
            integrated_intelligence.get("integrated_status"),
            "UNKNOWN"
        )

        validation_status = self._first_value(
            validation.get("validation_status"),
            "UNKNOWN"
        )

        reassessment_required = bool(
            lifecycle.get("reassessment_required", False)
        )

        scores = [
            self._score(certification.get("certification_score")),
            self._score(execution_decision.get("execution_score")),
            self._score(governance.get("governance_score")),
            self._score(lifecycle.get("lifecycle_score")),
            self._score(
                operational_intelligence.get("operational_score")
            ),
            self._score(
                orchestration.get("orchestration_score")
            ),
            self._score(
                integrated_intelligence.get("integrated_score")
            ),
            self._score(validation.get("validation_score"))
        ]

        valid_scores = [
            score for score in scores
            if score is not None
        ]

        master_control_score = (
            round(min(valid_scores), 1)
            if valid_scores
            else 0.0
        )

        blocked = {
            "CERTIFICATION_BLOCKED",
            "FAILED",
            "BLOCKED",
            "REJECTED",
            "UNAUTHORIZED",
            "EXECUTION_BLOCKED",
            "CRITICAL"
        }

        review = {
            "CERTIFICATION_REVIEW",
            "ATTENTION",
            "WARNING",
            "DEGRADED",
            "REASSESS_REQUIRED",
            "UNKNOWN"
        }

        statuses = [
            certification_status,
            execution_status,
            governance_status,
            lifecycle_status,
            operational_status,
            orchestration_status,
            integrated_status,
            validation_status,
            execution_authorization,
            decision_integrity
        ]

        normalized = [
            str(value).upper()
            for value in statuses
            if value is not None
        ]

        if any(value in blocked for value in normalized):
            master_control_status = "MASTER_BLOCKED"
            master_control_action = "HALT"
            master_control_risk = "CRITICAL"

        elif (
            reassessment_required
            or any(value in review for value in normalized)
        ):
            master_control_status = "MASTER_REVIEW"
            master_control_action = "REVIEW"
            master_control_risk = "MEDIUM"

        elif (
            certification_status == "CERTIFIED"
            and execution_status == "EXECUTION_READY"
            and execution_authorization == "AUTHORIZED"
            and execution_readiness == "READY"
            and decision_integrity == "INTACT"
            and governance_status == "APPROVED"
            and lifecycle_status == "HEALTHY"
            and operational_status == "OPERATIONALLY_HEALTHY"
            and orchestration_status == "ORCHESTRATION_READY"
            and integrated_status == "INTEGRATED_HEALTHY"
            and validation_status == "VALID"
        ):
            master_control_status = "MASTER_READY"
            master_control_action = "PROCEED"
            master_control_risk = "LOW"

        else:
            master_control_status = "MASTER_REVIEW"
            master_control_action = "REVIEW"
            master_control_risk = "MEDIUM"

        master_control_grade = self._grade(
            master_control_score
        )

        execution_control = (
            "EXECUTE"
            if master_control_status == "MASTER_READY"
            else "HOLD"
        )

        reason = (
            f"Final AI decision {decision} received "
            f"master control status {master_control_status}. "
            f"Master control action is {master_control_action}, "
            f"risk is {master_control_risk}, score is "
            f"{master_control_score}/100, grade is "
            f"{master_control_grade}, and execution control "
            f"is {execution_control}."
        )

        summary = (
            f"Final AI decision {decision} has master control "
            f"status {master_control_status}. Master control "
            f"action is {master_control_action}, risk is "
            f"{master_control_risk}, score is "
            f"{master_control_score}/100, grade is "
            f"{master_control_grade}, and execution control "
            f"is {execution_control}."
        )

        return {
            "decision": decision,
            "action": action,
            "master_control_status": master_control_status,
            "master_control_action": master_control_action,
            "master_control_risk": master_control_risk,
            "master_control_score": master_control_score,
            "master_control_grade": master_control_grade,
            "execution_control": execution_control,
            "execution_status": execution_status,
            "execution_authorization": execution_authorization,
            "execution_readiness": execution_readiness,
            "decision_integrity": decision_integrity,
            "certification_status": certification_status,
            "certification_risk": certification_risk,
            "governance_status": governance_status,
            "lifecycle_status": lifecycle_status,
            "operational_status": operational_status,
            "orchestration_status": orchestration_status,
            "integrated_status": integrated_status,
            "validation_status": validation_status,
            "reassessment_required": reassessment_required,
            "certification_score": self._score(
                certification.get("certification_score")
            ),
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
        except (TypeError, ValueError):
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
