"""Enhanced ranking components and ordering from synthetic histories."""
from price_test_support import isolated_price_db, synthetic_ranking_db


def test_multi_ranking_components(synthetic_ranking_db):
    from ranking_analyzer import get_enhanced_ranking
    rows = get_enhanced_ranking()
    assert [row["ticker"] for row in rows] == ["111111", "222222", "333333"]
    for row in rows:
        ticker = row["ticker"]
        assert row["base_score"] == synthetic_ranking_db.scores[ticker][-1]
        assert row["trend_score"] == synthetic_ranking_db.ranks[ticker][-2] - synthetic_ranking_db.ranks[ticker][-1]
        assert row["momentum_score"] == synthetic_ranking_db.scores[ticker][-1] - synthetic_ranking_db.scores[ticker][-2]
        assert row["enhanced_score"] == sum(row[key] for key in
            ("base_score", "trend_score", "momentum_score", "grade_bonus", "stability_score"))
    assert rows[1]["prediction_bonus"] > rows[2]["prediction_bonus"]


def test_multi_ranking_empty(isolated_price_db):
    from ranking_analyzer import get_enhanced_ranking
    assert get_enhanced_ranking() == []
