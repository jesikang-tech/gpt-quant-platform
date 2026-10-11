"""JSON serialization contract using synthetic dashboard data."""
from price_test_support import isolated_price_db, synthetic_ranking_db


def test_dashboard_json_roundtrip(synthetic_ranking_db):
    import json
    from ranking_analyzer import get_intelligence_dashboard_json, get_intelligence_dashboard_data
    assert json.loads(get_intelligence_dashboard_json(limit=2)) == get_intelligence_dashboard_data(limit=2)


def test_dashboard_json_empty(isolated_price_db):
    import json
    from ranking_analyzer import get_intelligence_dashboard_json
    assert json.loads(get_intelligence_dashboard_json()) == []
