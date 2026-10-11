"""Trend, grade and stability contracts using synthetic rank histories."""
import pytest
from price_test_support import isolated_price_db, synthetic_ranking_db


@pytest.mark.parametrize("ticker,direction,grade", [("111111", "RISING", "A"),
    ("222222", "STABLE", "B"), ("333333", "FALLING", "C")])
def test_ranking_analytics(synthetic_ranking_db, ticker, direction, grade):
    import ranking_analyzer as analyzer
    ranks = synthetic_ranking_db.ranks[ticker]
    scores = synthetic_ranking_db.scores[ticker]
    trend = analyzer.analyze_ranking_trend(ticker)
    assert trend["current_rank"] == ranks[-1]
    assert trend["previous_rank"] == ranks[-2]
    assert trend["rank_change"] == ranks[-2] - ranks[-1]
    analytics = analyzer.get_ranking_analytics(ticker)
    assert analytics["current_score"] == scores[-1]
    assert analytics["score_change"] == scores[-1] - scores[0]
    assert analyzer.calculate_rank_direction(ticker) == direction
    assert analyzer.calculate_analytics_grade(ticker) == grade
    assessment = analyzer.generate_ranking_assessment(ticker)
    assert assessment["direction"] == direction and assessment["grade"] == grade
    stability = analyzer.get_stability_analytics(ticker)
    assert stability["history_count"] == len(ranks)
    assert stability["average_rank_change"] == sum(abs(b-a) for a,b in zip(ranks, ranks[1:])) / (len(ranks)-1)
    assert stability["stability_score"] == analyzer.calculate_stability_score(ticker)
    assert assessment["stability_grade"] == stability["stability_grade"]


def test_ranking_analytics_empty(isolated_price_db):
    import ranking_analyzer as analyzer
    assert analyzer.get_ranking_analytics("missing")["message"] == "No ranking history"
    assert analyzer.calculate_rank_direction("missing") == "UNKNOWN"
    assert analyzer.calculate_stability_score("missing") == 0
