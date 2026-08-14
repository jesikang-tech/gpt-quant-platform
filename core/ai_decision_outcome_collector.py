"""
GPT Quant Platform

AI Decision Outcome Data Collector

Phase 6
Step6-2

Collects a snapshot of the final AI portfolio decision
for future outcome evaluation and learning.
"""


class AIDecisionOutcomeDataCollector:

    def collect(
        self,
        final_decision=None,
        final_decision_master_control=None,
        final_decision_certification=None,
        final_execution_decision=None,
        final_decision_execution_feedback=None,
        final_decision_execution_monitoring=None,
        final_decision_execution_reassessment=None,
        final_decision_governance=None,
        final_decision_lifecycle=None,
        final_decision_operational_intelligence=None,
        final_decision_orchestration=None,
        final_decision_integrated_intelligence=None,
        intelligence=None,
        intelligence_score=None,
        decision_confidence=None
    ):
        """
        Collect the current final AI decision state.

        Step6-2 does not evaluate performance yet.
        It only creates a structured decision snapshot
        that can later be compared with actual outcomes.
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
        final_decision_governance = (
            final_decision_governance or {}
        )
        final_decision_lifecycle = (
            final_decision_lifecycle or {}
        )
        final_decision_operational_intelligence = (
            final_decision_operational_intelligence or {}
        )
        final_decision_orchestration = (
            final_decision_orchestration or {}
        )
        final_decision_integrated_intelligence = (
            final_decision_integrated_intelligence or {}
        )
        intelligence = intelligence or {}
        intelligence_score = intelligence_score or {}
        decision_confidence = decision_confidence or {}

        decision = self._first(
            final_decision.get("decision"),
            final_decision_master_control.get("decision"),
            "UNKNOWN"
        )

        action = self._first(
            final_decision.get("action"),
            final_decision_master_control.get(
                "master_control_action"
            ),
            "REVIEW"
        )

        strategy = self._first(
            final_decision.get("strategy"),
            intelligence.get("final_strategy"),
            intelligence.get("strategy_mode"),
            "UNKNOWN"
        )

        market_view = self._first(
            final_decision.get("market_view"),
            intelligence.get("market_view"),
            "UNKNOWN"
        )

        risk_level = self._first(
            final_decision.get("risk_level"),
            final_decision_certification.get(
                "certification_risk"
            ),
            "UNKNOWN"
        )

        confidence_score = self._score(
            decision_confidence.get("confidence_score")
        )

        intelligence_value = self._score(
            intelligence_score.get("intelligence_score")
        )

        validation_score = self._score(
            final_decision.get("validation_score")
        )

        certification_score = self._score(
            final_decision_certification.get(
                "certification_score"
            )
        )

        execution_score = self._score(
            final_execution_decision.get(
                "execution_score"
            )
        )

        governance_score = self._score(
            final_decision_governance.get(
                "governance_score"
            )
        )

        lifecycle_score = self._score(
            final_decision_lifecycle.get(
                "lifecycle_score"
            )
        )

        operational_score = self._score(
            final_decision_operational_intelligence.get(
                "operational_score"
            )
        )

        orchestration_score = self._score(
            final_decision_orchestration.get(
                "orchestration_score"
            )
        )

        integrated_score = self._score(
            final_decision_integrated_intelligence.get(
                "integrated_score"
            )
        )

        return {
            "snapshot_status": "COLLECTED",

            "decision": decision,
            "action": action,
            "strategy": strategy,
            "market_view": market_view,
            "risk_level": risk_level,

            "confidence_score": confidence_score,
            "intelligence_score": intelligence_value,
            "validation_score": validation_score,

            "certification_score": certification_score,
            "execution_score": execution_score,
            "governance_score": governance_score,
            "lifecycle_score": lifecycle_score,
            "operational_score": operational_score,
            "orchestration_score": orchestration_score,
            "integrated_score": integrated_score,

            "execution_status": self._first(
                final_execution_decision.get(
                    "execution_status"
                ),
                "UNKNOWN"
            ),

            "execution_authorization": self._first(
                final_execution_decision.get(
                    "execution_authorization"
                ),
                "UNKNOWN"
            ),

            "certification_status": self._first(
                final_decision_certification.get(
                    "certification_status"
                ),
                "UNKNOWN"
            ),

            "governance_status": self._first(
                final_decision_governance.get(
                    "governance_status"
                ),
                "UNKNOWN"
            ),

            "monitoring_status": self._first(
                final_decision_execution_monitoring.get(
                    "monitoring_status"
                ),
                "UNKNOWN"
            ),

            "feedback_status": self._first(
                final_decision_execution_feedback.get(
                    "feedback_status"
                ),
                "UNKNOWN"
            ),

            "reassessment_status": self._first(
                final_decision_execution_reassessment.get(
                    "reassessment_status"
                ),
                "UNKNOWN"
            ),

            "reassessment_required": bool(
                final_decision_execution_reassessment.get(
                    "reassessment_required",
                    False
                )
            ),

            "snapshot_purpose": (
                "FUTURE_OUTCOME_EVALUATION"
            ),

            "outcome_status": "PENDING"
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
