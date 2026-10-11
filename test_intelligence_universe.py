"""Universe selection by analysis date using synthetic scores."""
from price_test_support import isolated_price_db, synthetic_ranking_db


def test_intelligence_universe_dates(synthetic_ranking_db):
    from ranking_analyzer import get_all_intelligence_universe
    assert get_all_intelligence_universe() == ["111111", "222222", "333333", "444444"]
    assert get_all_intelligence_universe(synthetic_ranking_db.dates[0]) == ["333333", "222222", "111111"]
    assert get_all_intelligence_universe("1999-01-01") == []


def test_intelligence_universe_empty(isolated_price_db):
    from ranking_analyzer import get_all_intelligence_universe
    assert get_all_intelligence_universe() == []
