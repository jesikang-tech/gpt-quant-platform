"""Dashboard envelope and metadata from synthetic SQLite data."""
from price_test_support import isolated_price_db, synthetic_ranking_db


def test_dashboard_api_metadata_and_limit(synthetic_ranking_db):
    from ranking_analyzer import get_dashboard_api_data

    result = get_dashboard_api_data(limit=2)
    assert result["success"] is True
    assert result["count"] == len(result["data"]) == 2
    assert [row["ticker"] for row in result["data"]] == ["111111", "222222"]
    assert result["metadata"] == {"market_data_date": synthetic_ranking_db.dates[-1],
                                  "ranking_date": synthetic_ranking_db.dates[-1]}


def test_dashboard_api_empty(isolated_price_db):
    from ranking_analyzer import get_dashboard_api_data

    assert get_dashboard_api_data() == {"success": True, "count": 0, "data": [],
                                       "metadata": {"market_data_date": None, "ranking_date": None}}
