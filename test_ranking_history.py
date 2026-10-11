"""Repository ranking history order and filtering on synthetic records."""
from price_test_support import isolated_price_db, synthetic_ranking_db


def test_ranking_history(synthetic_ranking_db):
    from repository import get_ranking_history
    expected = list(reversed(list(zip(synthetic_ranking_db.ranks["111111"],
                                     synthetic_ranking_db.scores["111111"], synthetic_ranking_db.dates))))
    assert get_ranking_history("111111") == expected
    assert get_ranking_history("missing") == []
