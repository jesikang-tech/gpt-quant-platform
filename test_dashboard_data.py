"""Dashboard ranking/intelligence join on synthetic records."""
from price_test_support import isolated_price_db, synthetic_ranking_db


def test_dashboard_data_join(synthetic_ranking_db):
    from ranking_analyzer import get_intelligence_dashboard_data, get_universe_enhanced_ranking

    rows = get_intelligence_dashboard_data()
    intelligence = {row["ticker"]: row for row in get_universe_enhanced_ranking()}
    assert [row["ticker"] for row in rows] == ["111111", "222222", "333333"]
    for rank, row in enumerate(rows, 1):
        source = intelligence[row["ticker"]]
        assert row["rank"] == rank
        assert row["score"] == synthetic_ranking_db.scores[row["ticker"]][-1]
        for key in ("return_score", "trend_score", "slope_score", "enhanced_score", "grade", "prediction"):
            assert row[key] == source[key]
        assert row["stability"] == source["stability_score"]


def test_dashboard_data_empty(isolated_price_db):
    from ranking_analyzer import get_intelligence_dashboard_data
    assert get_intelligence_dashboard_data() == []
