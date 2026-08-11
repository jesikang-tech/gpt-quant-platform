"""
AI Decision Trend & Stability Engine
Step5-3-72

Analyze AI decision score trends, stability,
momentum, grade stability, and decision consistency.
"""


class AIDecisionTrend:

    def analyze(self, history):
        """
        Analyze AI Decision history.

        history:
            List of dictionaries containing:
            decision_score, grade, decision, created_at
        """

        if not history:
            return self._empty_result()

        scores = [
            self._normalize(item.get("decision_score", 0))
            for item in history
            if item.get("decision_score") is not None
        ]

        if not scores:
            return self._empty_result()

        latest_score = scores[0]

        previous_score = (
            scores[1]
            if len(scores) > 1
            else latest_score
        )

        score_change = round(
            latest_score - previous_score,
            1
        )

        direction = self._get_direction(
            score_change
        )

        stability = self._get_stability(
            scores
        )

        momentum = self._get_momentum(
            scores
        )

        latest_grade = history[0].get(
            "grade",
            "UNKNOWN"
        )

        grade_stability = self._get_grade_stability(
            history
        )

        latest_decision = history[0].get(
            "decision",
            "UNKNOWN"
        )

        consistency = self._get_decision_consistency(
            history
        )

        summary = self._generate_summary(
            direction,
            stability,
            momentum,
            latest_grade,
            latest_decision
        )

        return {
            "latest_score": latest_score,
            "previous_score": previous_score,
            "score_change": score_change,
            "direction": direction,
            "stability": stability,
            "momentum": momentum,
            "grade": latest_grade,
            "grade_stability": grade_stability,
            "decision": latest_decision,
            "consistency": consistency,
            "summary": summary
        }


    def _get_direction(self, change):

        if change > 0.1:
            return "UP"

        if change < -0.1:
            return "DOWN"

        return "STABLE"


    def _get_stability(self, scores):

        if len(scores) < 2:
            return "HIGH"

        recent_scores = scores[:5]

        average = sum(recent_scores) / len(
            recent_scores
        )

        variance = sum(
            (score - average) ** 2
            for score in recent_scores
        ) / len(recent_scores)

        deviation = variance ** 0.5

        if deviation <= 1.0:
            return "HIGH"

        if deviation <= 3.0:
            return "MEDIUM"

        return "LOW"


    def _get_momentum(self, scores):

        if len(scores) < 3:
            return "NEUTRAL"

        latest = scores[0]
        previous = scores[1]
        older = scores[2]

        recent_change = latest - previous
        previous_change = previous - older

        if (
            recent_change > 0.1
            and previous_change > 0.1
        ):
            return "POSITIVE"

        if (
            recent_change < -0.1
            and previous_change < -0.1
        ):
            return "NEGATIVE"

        return "NEUTRAL"


    def _get_grade_stability(self, history):

        grades = [
            item.get("grade")
            for item in history[:5]
            if item.get("grade")
        ]

        if not grades:
            return "UNKNOWN"

        if len(set(grades)) == 1:
            return "STABLE"

        return "CHANGING"


    def _get_decision_consistency(self, history):

        decisions = [
            item.get("decision")
            for item in history[:5]
            if item.get("decision")
        ]

        if not decisions:
            return "UNKNOWN"

        if len(set(decisions)) == 1:
            return "HIGH"

        if len(set(decisions)) <= 2:
            return "MEDIUM"

        return "LOW"


    def _generate_summary(
        self,
        direction,
        stability,
        momentum,
        grade,
        decision
    ):

        if direction == "UP":
            trend_text = (
                "AI decision score is improving."
            )

        elif direction == "DOWN":
            trend_text = (
                "AI decision score is declining."
            )

        else:
            trend_text = (
                "AI decision score remains stable."
            )

        return (
            f"{trend_text} "
            f"Stability is {stability.lower()}, "
            f"momentum is {momentum.lower()}, "
            f"and the current grade is {grade}. "
            f"The latest decision is {decision}."
        )


    @staticmethod
    def _normalize(value):

        try:
            return round(float(value), 1)

        except (
            TypeError,
            ValueError
        ):
            return 0.0


    @staticmethod
    def _empty_result():

        return {
            "latest_score": 0,
            "previous_score": 0,
            "score_change": 0,
            "direction": "STABLE",
            "stability": "UNKNOWN",
            "momentum": "NEUTRAL",
            "grade": "UNKNOWN",
            "grade_stability": "UNKNOWN",
            "decision": "UNKNOWN",
            "consistency": "UNKNOWN",
            "summary": (
                "AI decision trend data is unavailable."
            )
        }
