"""Universe enrichment including an ETF without ranking history."""
from price_test_support import isolated_price_db, synthetic_ranking_db


def test_universe_ranking(synthetic_ranking_db):
    from ranking_analyzer import get_universe_enhanced_ranking
    rows = get_universe_enhanced_ranking()
    assert [row["ticker"] for row in rows] == ["111111", "222222", "333333", "444444"]
    assert all(0 <= row["enhanced_score"] <= 100 for row in rows)
    for row in rows[:3]:
        score = synthetic_ranking_db.scores[row["ticker"]][-1]
        assert row["base_score"] == row["final_score"] == score
        assert row["return_score"] == score / 2
    history_free = rows[-1]
    assert history_free["grade"] == "N/A"
    assert history_free["prediction"] == "UNCERTAIN"
    assert history_free["enhanced_score"] == history_free["final_score"] == 30


def test_universe_ranking_empty(isolated_price_db):
    from ranking_analyzer import get_universe_enhanced_ranking
    assert get_universe_enhanced_ranking() == []
