"""
GPT Quant Platform

AI Final Decision Integration Engine

Step5-3-87
"""


class AIFinalDecisionIntegration:

    def integrate(
        self,
        intelligence=None,
        intelligence_score=None,
        decision_confidence=None,
        decision_confidence_assessment=None,
        decision_confidence_recommendation=None,
        ai_decision_validation=None,
        ai_decision_validation_explainability=None,
        ai_decision_validation_action=None
    ):
        """
        Integrate the complete AI portfolio decision pipeline
        into one final decision object.
        """

        intelligence = intelligence or {}
        intelligence_score = intelligence_score or {}
        decision_confidence = decision_confidence or {}
        decision_confidence_assessment = (
            decision_confidence_assessment or {}
        )
        decision_confidence_recommendation = (
            decision_confidence_recommendation or {}
        )
        ai_decision_validation = (
            ai_decision_validation or {}
        )
        ai_decision_validation_explainability = (
            ai_decision_validation_explainability or {}
        )
        ai_decision_validation_action = (
            ai_decision_validation_action or {}
        )

        decision = self._first(
            ai_decision_validation_action.get("decision"),
            ai_decision_validation.get("decision"),
            intelligence.get("decision"),
            "UNKNOWN"
        )

        action = self._first(
            ai_decision_validation_action.get("action"),
            decision_confidence_recommendation.get(
                "recommendation"
            ),
            "REVIEW_REQUIRED"
        )

        execution_status = self._first(
            ai_decision_validation_action.get(
                "execution_status"
            ),
            "UNDETERMINED"
        )

        confidence_score = self._normalize(
            self._first(
                decision_confidence.get(
                    "confidence_score"
                ),
                ai_decision_validation_action.get(
                    "confidence_score"
                ),
                ai_decision_validation.get(
                    "confidence_score"
                ),
                0
            )
        )

        confidence_level = self._first(
            decision_confidence.get(
                "confidence_level"
            ),
            ai_decision_validation_action.get(
                "confidence_level"
            ),
            "UNKNOWN"
        )

        confidence_grade = self._first(
            decision_confidence.get(
                "confidence_grade"
            ),
            "UNKNOWN"
        )

        validation_status = self._first(
            ai_decision_validation_action.get(
                "validation_status"
            ),
            ai_decision_validation.get(
                "validation_status"
            ),
            ai_decision_validation.get(
                "validation"
            ),
            "UNKNOWN"
        )

        validation_score = self._normalize(
            self._first(
                ai_decision_validation_action.get(
                    "validation_score"
                ),
                ai_decision_validation.get(
                    "validation_score"
                ),
                0
            )
        )

        recommendation = self._first(
            ai_decision_validation_action.get(
                "recommendation"
            ),
            decision_confidence_recommendation.get(
                "recommendation"
            ),
            "REVIEW"
        )

        risk_level = self._first(
            ai_decision_validation_action.get(
                "risk_level"
            ),
            "UNKNOWN"
        )

        monitoring = self._first(
            ai_decision_validation_action.get(
                "monitoring"
            ),
            decision_confidence_recommendation.get(
                "monitoring"
            ),
            "HIGH"
        )

        intelligence_value = self._normalize(
            intelligence_score.get(
                "intelligence_score",
                0
            )
        )

        intelligence_grade = self._first(
            intelligence_score.get(
                "grade"
            ),
            "UNKNOWN"
        )

        strategy = self._first(
            intelligence.get(
                "final_strategy"
            ),
            intelligence.get(
                "strategy_mode"
            ),
            ai_decision_validation_action.get(
                "strategy_mode"
            ),
            "UNKNOWN"
        )

        market_view = self._first(
            intelligence.get(
                "market_view"
            ),
            "UNKNOWN"
        )

        adaptive_action = self._first(
            ai_decision_validation_action.get(
                "adaptive_action"
            ),
            intelligence.get(
                "adaptive_action"
            ),
            "UNKNOWN"
        )

        decision_alignment = self._first(
            ai_decision_validation_action.get(
                "decision_alignment"
            ),
            ai_decision_validation.get(
                "decision_alignment"
            ),
            intelligence.get(
                "decision_alignment"
            ),
            "UNKNOWN"
        )

        decision_consistency = self._first(
            ai_decision_validation_action.get(
                "decision_consistency"
            ),
            ai_decision_validation.get(
                "decision_consistency"
            ),
            intelligence.get(
                "decision_consistency"
            ),
            "UNKNOWN"
        )

        reliability = self._first(
            ai_decision_validation_action.get(
                "reliability"
            ),
            ai_decision_validation.get(
                "reliability"
            ),
            intelligence.get(
                "reliability"
            ),
            "UNKNOWN"
        )

        optimization_status = self._first(
            ai_decision_validation_action.get(
                "optimization_status"
            ),
            ai_decision_validation.get(
                "optimization_status"
            ),
            intelligence.get(
                "optimization_status"
            ),
            "UNKNOWN"
        )

        summary = self._build_summary(
            decision,
            action,
            execution_status,
            confidence_score,
            validation_status,
            risk_level,
            strategy
        )

        rationale = self._first(
            ai_decision_validation_explainability.get(
                "explanation"
            ),
            ai_decision_validation_action.get(
                "action_reason"
            ),
            intelligence.get(
                "summary"
            ),
            "Final AI decision is based on the available portfolio intelligence."
        )

        return {
            "decision": decision,
            "action": action,
            "execution_status": execution_status,
            "confidence_score": confidence_score,
            "confidence_level": confidence_level,
            "confidence_grade": confidence_grade,
            "validation_status": validation_status,
            "validation_score": validation_score,
            "recommendation": recommendation,
            "risk_level": risk_level,
            "monitoring": monitoring,
            "intelligence_score": intelligence_value,
            "intelligence_grade": intelligence_grade,
            "strategy": strategy,
            "market_view": market_view,
            "adaptive_action": adaptive_action,
            "decision_alignment": decision_alignment,
            "decision_consistency": decision_consistency,
            "reliability": reliability,
            "optimization_status": optimization_status,
            "summary": summary,
            "rationale": rationale
        }

    @staticmethod
    def _first(*values):

        for value in values:

            if value is not None and value != "":
                return value

        return None

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

    @staticmethod
    def _build_summary(
        decision,
        action,
        execution_status,
        confidence_score,
        validation_status,
        risk_level,
        strategy
    ):

        return (
            f"Final AI portfolio decision is {decision} "
            f"with action {action}. Execution status is "
            f"{execution_status}, confidence is "
            f"{confidence_score}/100, validation status is "
            f"{validation_status}, risk level is "
            f"{risk_level}, and strategy is {strategy}."
        )