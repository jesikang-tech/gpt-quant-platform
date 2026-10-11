"""Intelligence summary for a synthetic leading ETF and empty data."""
from price_test_support import isolated_price_db, synthetic_ranking_db


def test_intelligence_summary(synthetic_ranking_db):
    from ranking_analyzer import get_dashboard_intelligence_summary, get_dashboard_api_data, generate_ai_insight
    top = get_dashboard_api_data()["data"][0]
    result = get_dashboard_intelligence_summary()
    assert result["success"] is True
    assert result["ticker"] == top["ticker"] == "111111"
    for key in ("score", "enhanced_score", "grade", "prediction", "stability"):
        assert result[key] == top[key]
    insight = generate_ai_insight(top["ticker"])
    for key in ("trend", "risk", "opinion"):
        assert result[key] == insight[key]
        assert isinstance(result[key], str) and result[key]


def test_intelligence_summary_empty(isolated_price_db):
    from ranking_analyzer import get_dashboard_intelligence_summary
    assert get_dashboard_intelligence_summary() == {"success": False, "message": "No ETF data"}
