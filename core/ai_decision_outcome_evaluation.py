"""
GPT Quant Platform

AI Decision Outcome Evaluation Engine

Phase 6
Step6-4

Evaluates actual outcomes against the stored AI decision snapshot
and generates decision-performance learning signals.
"""


class AIDecisionOutcomeEvaluation:

    def evaluate(
        self,
        outcome_snapshot=None,
        actual_outcome=None
    ):
        """
        Evaluate an AI decision outcome.

        Step6-4 does not invent performance results.
        When actual outcome data is unavailable, the evaluation
        remains in a waiting state.
        """

        outcome_snapshot = outcome_snapshot or {}
        actual_outcome = actual_outcome or {}

        decision = self._first(
            outcome_snapshot.get("decision"),
            "UNKNOWN"
        )

        action = self._first(
            outcome_snapshot.get("action"),
            "REVIEW"
        )

        strategy = self._first(
            outcome_snapshot.get("strategy"),
            "UNKNOWN"
        )

        snapshot_status = self._first(
            outcome_snapshot.get("snapshot_status"),
            "UNKNOWN"
        )

        snapshot_purpose = self._first(
            outcome_snapshot.get("snapshot_purpose"),
            "FUTURE_OUTCOME_EVALUATION"
        )

        actual_outcome_available = bool(
            actual_outcome
        )

        if not actual_outcome_available:
            return {
                "evaluation_status": "WAITING_FOR_OUTCOME",
                "outcome_status": "PENDING",
                "outcome_score": 0.0,
                "outcome_grade": "N/A",
                "decision_effectiveness": "PENDING",
                "strategy_effectiveness": "PENDING",
                "market_response": "PENDING",
                "portfolio_response": "PENDING",
                "learning_status": "WAITING_FOR_OUTCOME",
                "learning_signal": "NONE",
                "learning_signal_strength": 0.0,
                "actual_outcome_available": False,
                "decision": decision,
                "action": action,
                "strategy": strategy,
                "snapshot_status": snapshot_status,
                "snapshot_purpose": snapshot_purpose,
                "summary": (
                    "Actual outcome data is not yet available. "
                    "Outcome evaluation and learning remain pending."
                ),
                "reason": (
                    f"Decision {decision} with action {action} and "
                    f"strategy {strategy} has a stored outcome snapshot, "
                    "but no actual performance outcome is available."
                )
            }

        outcome_score = self._calculate_outcome_score(
            actual_outcome
        )

        outcome_grade = self._grade(
            outcome_score
        )

        decision_effectiveness = self._effectiveness(
            outcome_score
        )

        strategy_effectiveness = self._effectiveness(
            outcome_score
        )

        market_response = self._first(
            actual_outcome.get("market_response"),
            "EVALUATED"
        )

        portfolio_response = self._first(
            actual_outcome.get("portfolio_response"),
            "EVALUATED"
        )

        learning_signal = self._learning_signal(
            outcome_score
        )

        learning_signal_strength = round(
            abs(outcome_score - 50.0) * 2.0,
            1
        )

        return {
            "evaluation_status": "EVALUATED",
            "outcome_status": "EVALUATED",
            "outcome_score": outcome_score,
            "outcome_grade": outcome_grade,
            "decision_effectiveness": decision_effectiveness,
            "strategy_effectiveness": strategy_effectiveness,
            "market_response": market_response,
            "portfolio_response": portfolio_response,
            "learning_status": "LEARNING_AVAILABLE",
            "learning_signal": learning_signal,
            "learning_signal_strength": learning_signal_strength,
            "actual_outcome_available": True,
            "decision": decision,
            "action": action,
            "strategy": strategy,
            "snapshot_status": snapshot_status,
            "snapshot_purpose": snapshot_purpose,
            "summary": (
                f"Decision {decision} was evaluated with an "
                f"outcome score of {outcome_score:.1f} "
                f"({outcome_grade})."
            ),
            "reason": (
                "Actual outcome data is available and has been "
                "converted into a decision-performance learning signal."
            )
        }


    @staticmethod
    def _calculate_outcome_score(actual_outcome):
        """
        Calculate the normalized outcome score.

        Primary input:
        - portfolio_return

        Portfolio return normalization:
        - 0% return = 50 score
        - +10% return = 100 score
        - -10% return = 0 score

        The normalized score is bounded to 0~100.

        Backward-compatible inputs:
        - outcome_score
        - performance_score
        - return_score

        portfolio_return is treated as the primary
        real portfolio performance signal.
        """

        portfolio_return = actual_outcome.get(
            "portfolio_return"
        )

        if portfolio_return is not None:
            try:
                portfolio_return = float(
                    portfolio_return
                )
            except (TypeError, ValueError):
                portfolio_return = None

        if portfolio_return is not None:
            value = (
                50.0
                + (
                    portfolio_return * 5.0
                )
            )

            return round(
                max(
                    0.0,
                    min(
                        100.0,
                        value
                    )
                ),
                1
            )

        value = (
            actual_outcome.get("outcome_score")
            if actual_outcome.get("outcome_score") is not None
            else actual_outcome.get("performance_score")
        )

        if value is None:
            value = actual_outcome.get("return_score")

        if value is None:
            return 0.0

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

    @staticmethod
    def _grade(score):

        if score >= 90.0:
            return "A"

        if score >= 80.0:
            return "B"

        if score >= 70.0:
            return "C"

        if score >= 60.0:
            return "D"

        return "F"


    @staticmethod
    def _effectiveness(score):

        if score >= 80.0:
            return "EFFECTIVE"

        if score >= 60.0:
            return "NEUTRAL"

        return "INEFFECTIVE"


    @staticmethod
    def _learning_signal(score):

        if score >= 80.0:
            return "POSITIVE"

        if score >= 60.0:
            return "STABLE"

        return "NEGATIVE"


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
