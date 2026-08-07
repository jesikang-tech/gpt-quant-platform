"""
AI Portfolio Optimization Scoring Engine
Step5-3-65
"""


class OptimizationScoringEngine:

    def __init__(self):

        pass


    def calculate_score(
        self,
        return_score,
        trend_score,
        slope_score,
        market_confidence=50,
        diversification=50
    ):
        """
        Optimization Score 계산
        """

        score = (
            return_score * 0.30 +
            trend_score * 0.25 +
            slope_score * 0.20 +
            market_confidence * 0.15 +
            diversification * 0.10
        )

        return round(score, 2)


    def analyze_factors(
        self,
        return_score,
        trend_score,
        slope_score
    ):
        """
        AI Factor Intelligence Analysis
        Step5-3-65-12
        """

        def classify_score(score):

            if score >= 90:
                return "Excellent"

            elif score >= 80:
                return "Strong"

            elif score >= 70:
                return "Good"

            elif score >= 60:
                return "Moderate"

            else:
                return "Weak"


        return {
            "return": classify_score(return_score),
            "trend": classify_score(trend_score),
            "slope": classify_score(slope_score)
        }    



if __name__ == "__main__":

    engine = OptimizationScoringEngine()

    score = engine.calculate_score(
        return_score=92,
        trend_score=88,
        slope_score=84,
        market_confidence=82,
        diversification=90
    )

    print()
    print("Optimization Score")
    print(score)