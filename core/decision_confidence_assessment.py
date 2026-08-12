"""
GPT Quant Platform

AI Decision Confidence Assessment Engine

Step5-3-82
"""


class DecisionConfidenceAssessment:

    def assess(
        self,
        explainability
    ):
        """
        Assess AI Decision Confidence Explainability.

        Converts confidence explainability signals
        into an overall confidence assessment.
        """

        explainability = (
            explainability or {}
        )

        confidence_score = self._normalize(
            explainability.get(
                "confidence_score",
                0
            )
        )

        positive_signals = (
            explainability.get(
                "positive_signals",
                []
            )
            or []
        )

        supporting_signals = (
            explainability.get(
                "supporting_signals",
                []
            )
            or []
        )

        risk_signals = (
            explainability.get(
                "risk_signals",
                []
            )
            or []
        )

        strongest_signals = (
            self._sort_signals(
                positive_signals
            )
        )

        supporting_strength = (
            self._sort_signals(
                supporting_signals
            )
        )

        attention_signals = (
            self._sort_signals(
                risk_signals
            )
        )

        assessment = (
            self._determine_assessment(
                confidence_score,
                strongest_signals,
                attention_signals
            )
        )

        assessment_summary = (
            self._build_summary(
                assessment,
                confidence_score,
                strongest_signals,
                supporting_strength,
                attention_signals
            )
        )

        return {
            "assessment":
                assessment,

            "confidence_score":
                confidence_score,

            "strongest_signals":
                strongest_signals,

            "supporting_signals":
                supporting_strength,

            "attention_signals":
                attention_signals,

            "assessment_summary":
                assessment_summary
        }

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
    def _sort_signals(signals):

        normalized = []

        for signal in signals:

            if not isinstance(
                signal,
                dict
            ):
                continue

            normalized.append(
                {
                    "name":
                        signal.get(
                            "name",
                            "-"
                        ),

                    "score":
                        DecisionConfidenceAssessment._normalize(
                            signal.get(
                                "score",
                                0
                            )
                        )
                }
            )

        return sorted(
            normalized,
            key=lambda item:
                item["score"],
            reverse=True
        )

    @staticmethod
    def _determine_assessment(
        confidence_score,
        strongest_signals,
        attention_signals
    ):

        if (
            confidence_score >= 90
            and strongest_signals
            and not attention_signals
        ):

            return "VERY_STRONG"

        if (
            confidence_score >= 80
            and not attention_signals
        ):

            return "STRONG"

        if confidence_score >= 70:

            return "MODERATE"

        return "NEEDS_ATTENTION"

    @staticmethod
    def _build_summary(
        assessment,
        confidence_score,
        strongest_signals,
        supporting_signals,
        attention_signals
    ):

        if assessment == "VERY_STRONG":

            base = (
                "Decision confidence is very strong "
                "with multiple high-quality intelligence signals."
            )

        elif assessment == "STRONG":

            base = (
                "Decision confidence is strong "
                "with supportive intelligence signals."
            )

        elif assessment == "MODERATE":

            base = (
                "Decision confidence is moderate "
                "and should continue to be monitored."
            )

        else:

            base = (
                "Decision confidence requires attention "
                "because one or more supporting signals are weak."
            )

        if strongest_signals:

            strongest = ", ".join(
                signal["name"]
                for signal in strongest_signals
                if signal["score"] >= 90
            )

            if strongest:

                base += (
                    f" Strongest signals are {strongest}."
                )

        if supporting_signals:

            base += (
                " Supporting signals remain "
                "within an acceptable range."
            )

        if attention_signals:

            attention = ", ".join(
                signal["name"]
                for signal in attention_signals
            )

            base += (
                f" Attention is recommended for {attention}."
            )

        return (
            f"{base} "
            f"Overall confidence score is "
            f"{confidence_score}/100."
        )
