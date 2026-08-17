"""
GPT Quant Platform

AI Decision Outcome Intelligence Engine

Phase 6
Step6-1

Tracks the expected outcome state of the final AI portfolio decision
and provides a foundation for future decision-performance feedback.
"""


class AIDecisionOutcomeIntelligence:

    def analyze(
        self,
        final_decision=None,
        final_decision_master_control=None,
        final_decision_certification=None,
        final_execution_decision=None,
        final_decision_execution_feedback=None,
        final_decision_execution_monitoring=None,
        final_decision_execution_reassessment=None,
        intelligence=None,
        intelligence_score=None,
        decision_confidence=None,
        outcome_evaluation=None
    ):
        """
        Analyze the outcome state of the final AI portfolio decision.

        Step6-1 intentionally does not assume a successful or failed
        outcome before actual performance data becomes available.
        """

        final_decision = final_decision or {}
        final_decision_master_control = (
            final_decision_master_control or {}
        )
        final_decision_certification = (
            final_decision_certification or {}
        )
        final_execution_decision = (
            final_execution_decision or {}
        )
        final_decision_execution_feedback = (
            final_decision_execution_feedback or {}
        )
        final_decision_execution_monitoring = (
            final_decision_execution_monitoring or {}
        )
        final_decision_execution_reassessment = (
            final_decision_execution_reassessment or {}
        )
        intelligence = intelligence or {}
        intelligence_score = intelligence_score or {}
        decision_confidence = decision_confidence or {}
        outcome_evaluation = outcome_evaluation or {}

        decision = self._first(
            final_decision.get("decision"),
            final_decision_master_control.get("decision"),
            final_execution_decision.get("decision"),
            "UNKNOWN"
        )

        action = self._first(
            final_decision.get("action"),
            final_decision_master_control.get(
                "master_control_action"
            ),
            final_execution_decision.get("action"),
            "REVIEW"
        )

        execution_status = self._first(
            final_execution_decision.get("execution_status"),
            final_decision_master_control.get("execution_status"),
            final_decision.get("execution_status"),
            "UNKNOWN"
        )

        execution_authorization = self._first(
            final_decision_master_control.get(
                "execution_authorization"
            ),
            final_execution_decision.get(
                "execution_authorization"
            ),
            "UNAUTHORIZED"
        )

        master_control_status = self._first(
            final_decision_master_control.get(
                "master_control_status"
            ),
            "UNKNOWN"
        )

        certification_status = self._first(
            final_decision_certification.get(
                "certification_status"
            ),
            "UNKNOWN"
        )

        feedback_status = self._first(
            final_decision_execution_feedback.get(
                "feedback_status"
            ),
            "UNKNOWN"
        )

        monitoring_status = self._first(
            final_decision_execution_monitoring.get(
                "monitoring_status"
            ),
            "UNKNOWN"
        )

        reassessment_status = self._first(
            final_decision_execution_reassessment.get(
                "reassessment_status"
            ),
            "UNKNOWN"
        )

        reassessment_required = bool(
            final_decision_execution_reassessment.get(
                "reassessment_required",
                False
            )
        )

        intelligence_value = self._score(
            intelligence_score.get(
                "intelligence_score"
            )
        )

        confidence_value = self._score(
            decision_confidence.get(
                "confidence_score"
            )
        )

        outcome_status = self._first(
            outcome_evaluation.get(
                "outcome_status"
            ),
            "PENDING"
        )

        outcome_score = self._score(
            outcome_evaluation.get(
                "outcome_score"
            )
        )

        if outcome_score is None:
            outcome_score = 0.0

        outcome_learning_status = self._first(
            outcome_evaluation.get(
                "learning_status"
            ),
            "WAITING_FOR_OUTCOME"
        )

        outcome_learning_signal = self._first(
            outcome_evaluation.get(
                "learning_signal"
            ),
            "NONE"
        )

        outcome_learning_signal_strength = self._score(
            outcome_evaluation.get(
                "learning_signal_strength"
            )
        )

        if outcome_learning_signal_strength is None:
            outcome_learning_signal_strength = 0.0

        outcome_grade = self._first(
            outcome_evaluation.get(
                "outcome_grade"
            ),
            "N/A"
        )

        decision_effectiveness = self._first(
            outcome_evaluation.get(
                "decision_effectiveness"
            ),
            "PENDING"
        )

        strategy_effectiveness = self._first(
            outcome_evaluation.get(
                "strategy_effectiveness"
            ),
            "PENDING"
        )

        market_response = self._first(
            outcome_evaluation.get(
                "market_response"
            ),
            "PENDING"
        )

        portfolio_response = self._first(
            outcome_evaluation.get(
                "portfolio_response"
            ),
            "PENDING"
        )

        if (
            master_control_status == "MASTER_BLOCKED"
            or execution_authorization == "UNAUTHORIZED"
        ):
            learning_status = "BLOCKED"
            feedback_state = "BLOCKED"

        elif reassessment_required:
            learning_status = "REASSESSMENT_REQUIRED"
            feedback_state = "REASSESSMENT_REQUIRED"

        elif (
            execution_status == "EXECUTION_READY"
            and master_control_status == "MASTER_READY"
            and certification_status == "CERTIFIED"
        ):
            learning_status = "WAITING_FOR_OUTCOME"
            feedback_state = "COLLECTING"

        else:
            learning_status = "WAITING_FOR_OUTCOME"
            feedback_state = "COLLECTING"

        adaptive_learning_required = (
            reassessment_required
            or feedback_status in {
                "FAILED",
                "DEGRADED",
                "WARNING"
            }
        )

        summary = (
            f"Final AI decision {decision} has outcome status "
            f"{outcome_status}. Actual performance outcome data "
            f"is not yet available, so decision effectiveness and "
            f"strategy effectiveness remain pending. Learning "
            f"status is {learning_status}."
        )

        reason = (
            f"Decision {decision} is currently tracked as "
            f"{outcome_status}. Execution status is "
            f"{execution_status}, master control status is "
            f"{master_control_status}, certification status is "
            f"{certification_status}, and feedback status is "
            f"{feedback_status}. The system will evaluate actual "
            f"portfolio and market outcomes when outcome data "
            f"becomes available."
        )

        return {
            "decision": decision,
            "action": action,
            "outcome_status": outcome_status,
            "outcome_score": outcome_score,
            "outcome_grade": outcome_grade,
            "outcome_learning_status": outcome_learning_status,
            "outcome_learning_signal": outcome_learning_signal,
            "outcome_learning_signal_strength": outcome_learning_signal_strength,
            "decision_effectiveness": decision_effectiveness,
            "strategy_effectiveness": strategy_effectiveness,
            "market_response": market_response,
            "portfolio_response": portfolio_response,
            "execution_status": execution_status,
            "execution_authorization": execution_authorization,
            "master_control_status": master_control_status,
            "certification_status": certification_status,
            "feedback_status": feedback_status,
            "monitoring_status": monitoring_status,
            "reassessment_status": reassessment_status,
            "reassessment_required": reassessment_required,
            "intelligence_score": intelligence_value,
            "confidence_score": confidence_value,
            "learning_status": learning_status,
            "feedback_state": feedback_state,
            "adaptive_learning_required": adaptive_learning_required,
            "summary": summary,
            "reason": reason
        }

    @staticmethod
    def _first(*values):

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
    def _score(value):

        if value is None:
            return None

        try:
            return round(
                max(
                    0.0,
                    min(
                        100.0,
                        float(value)
                    )
                ),
                1
            )

        except (TypeError, ValueError):
            return None
