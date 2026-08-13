"""
GPT Quant Platform

AI Final Decision Operational Intelligence

Step5-3-96
"""


class AIFinalDecisionOperationalIntelligence:

    def analyze(
        self,
        final_decision=None,
        governance_control=None
    ):
        """
        Analyze the final AI decision operational state
        using lifecycle governance and control intelligence.
        """

        final_decision = final_decision or {}
        governance_control = governance_control or {}

        decision = self._first_value(
            governance_control.get("decision"),
            final_decision.get("decision"),
            "UNKNOWN"
        )

        action = self._first_value(
            governance_control.get("action"),
            final_decision.get("action"),
            "UNKNOWN"
        )

        operational_status = governance_control.get(
            "operational_status",
            "UNKNOWN"
        )

        operational_action = governance_control.get(
            "operational_action",
            "UNKNOWN"
        )

        operational_risk = governance_control.get(
            "operational_risk",
            "UNKNOWN"
        )

        operational_score = self._normalize(
            governance_control.get(
                "operational_score",
                0
            )
        )

        operational_grade = governance_control.get(
            "operational_grade",
            "F"
        )

        execution_authorization = governance_control.get(
            "execution_authorization",
            "UNKNOWN"
        )

        monitoring_policy = governance_control.get(
            "monitoring_policy",
            "UNKNOWN"
        )

        reassessment_policy = governance_control.get(
            "reassessment_policy",
            "UNKNOWN"
        )

        validation_status = governance_control.get(
            "validation_status",
            final_decision.get(
                "validation_status",
                "UNKNOWN"
            )
        )

        validation_score = self._normalize(
            governance_control.get(
                "validation_score",
                final_decision.get(
                    "validation_score",
                    0
                )
            )
        )

        confidence_score = self._normalize(
            governance_control.get(
                "confidence_score",
                final_decision.get(
                    "confidence_score",
                    0
                )
            )
        )

        execution_status = governance_control.get(
            "control_status",
            final_decision.get(
                "execution_status",
                "UNKNOWN"
            )
        )

        intelligence_status = self._determine_intelligence_status(
            operational_status,
            operational_risk,
            execution_authorization,
            validation_status
        )

        intelligence_action = self._determine_action(
            intelligence_status,
            operational_action,
            execution_authorization,
            operational_risk
        )

        intelligence_score = self._calculate_score(
            operational_score,
            confidence_score,
            validation_score
        )

        intelligence_grade = self._grade(
            intelligence_score
        )

        priority = self._determine_priority(
            operational_risk,
            execution_authorization,
            reassessment_policy
        )

        signals = self._build_signals(
            operational_status,
            operational_risk,
            operational_score,
            execution_authorization,
            validation_status,
            validation_score,
            confidence_score,
            reassessment_policy
        )

        summary = self._build_summary(
            decision,
            action,
            intelligence_status,
            intelligence_action,
            operational_risk,
            intelligence_score,
            intelligence_grade,
            execution_authorization
        )

        return {
            "decision": decision,
            "action": action,

            "operational_status": operational_status,
            "operational_action": operational_action,
            "operational_risk": operational_risk,
            "operational_score": operational_score,
            "operational_grade": operational_grade,

            "execution_authorization": execution_authorization,
            "execution_status": execution_status,

            "monitoring_policy": monitoring_policy,
            "reassessment_policy": reassessment_policy,

            "validation_status": validation_status,
            "validation_score": validation_score,
            "confidence_score": confidence_score,

            "intelligence_status": intelligence_status,
            "intelligence_action": intelligence_action,
            "intelligence_risk": operational_risk,
            "intelligence_score": intelligence_score,
            "intelligence_grade": intelligence_grade,

            "priority": priority,
            "signals": signals,

            "summary": summary
        }

    @staticmethod
    def _determine_intelligence_status(
        operational_status,
        operational_risk,
        execution_authorization,
        validation_status
    ):

        if validation_status in (
            "INVALID",
            "FAILED"
        ):
            return "BLOCKED"

        if execution_authorization == "DENIED":
            return "BLOCKED"

        if execution_authorization in (
            "SUSPENDED",
            "REVIEW_REQUIRED"
        ):
            return "CONTROLLED"

        if operational_risk in (
            "CRITICAL",
            "HIGH"
        ):
            return "CONTROLLED"

        if operational_status == "OPERATIONALLY_HEALTHY":
            return "HEALTHY"

        if operational_risk == "MEDIUM":
            return "MONITORING"

        return "MONITORING"

    @staticmethod
    def _determine_action(
        intelligence_status,
        operational_action,
        execution_authorization,
        operational_risk
    ):

        if intelligence_status == "BLOCKED":
            return "HALT"

        if execution_authorization == "SUSPENDED":
            return "SUSPEND"

        if execution_authorization == "REVIEW_REQUIRED":
            return "REVIEW"

        if intelligence_status == "HEALTHY":
            return "PROCEED"

        if operational_risk == "MEDIUM":
            return "MONITOR"

        if operational_action == "REASSESS":
            return "REASSESS"

        return "MONITOR"

    @staticmethod
    def _calculate_score(
        operational_score,
        confidence_score,
        validation_score
    ):

        score = (
            operational_score * 0.60
            + confidence_score * 0.20
            + validation_score * 0.20
        )

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
    def _determine_priority(
        operational_risk,
        execution_authorization,
        reassessment_policy
    ):

        if execution_authorization == "DENIED":
            return "CRITICAL"

        if execution_authorization == "SUSPENDED":
            return "HIGH"

        if reassessment_policy == "IMMEDIATE":
            return "HIGH"

        if operational_risk == "HIGH":
            return "HIGH"

        if operational_risk == "MEDIUM":
            return "MEDIUM"

        return "NORMAL"

    @staticmethod
    def _build_signals(
        operational_status,
        operational_risk,
        operational_score,
        execution_authorization,
        validation_status,
        validation_score,
        confidence_score,
        reassessment_policy
    ):

        signals = []

        if operational_status != "OPERATIONALLY_HEALTHY":
            signals.append({
                "name": "Operational Status",
                "value": operational_status
            })

        if operational_risk not in (
            "LOW",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Operational Risk",
                "value": operational_risk
            })

        if operational_score < 80:
            signals.append({
                "name": "Operational Score",
                "value": operational_score
            })

        if execution_authorization not in (
            "AUTHORIZED",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Execution Authorization",
                "value": execution_authorization
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

        if reassessment_policy not in (
            "NOT_REQUIRED",
            "UNKNOWN"
        ):
            signals.append({
                "name": "Reassessment Policy",
                "value": reassessment_policy
            })

        return signals

    @staticmethod
    def _build_summary(
        decision,
        action,
        intelligence_status,
        intelligence_action,
        operational_risk,
        intelligence_score,
        intelligence_grade,
        execution_authorization
    ):

        return (
            f"Final AI decision {decision} with action {action} has "
            f"operational intelligence status {intelligence_status}. "
            f"Recommended intelligence action is {intelligence_action}, "
            f"operational risk is {operational_risk}, intelligence score "
            f"is {intelligence_score}/100, intelligence grade is "
            f"{intelligence_grade}, and execution authorization is "
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
