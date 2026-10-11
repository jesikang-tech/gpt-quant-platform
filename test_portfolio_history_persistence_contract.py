"""Synthetic isolated API contract; no source database copy or import-time execution."""
from contextlib import ExitStack, closing
from price_test_support import (isolated_price_db, isolated_evaluation_api,
                                synthetic_ranking_db, synthetic_ready_api)


def test_portfolio_history_persistence_contract(synthetic_ready_api):
    client = synthetic_ready_api.client
    with ExitStack() as stack:

        conn = stack.enter_context(closing(synthetic_ready_api.db.connect()))

        # The persistence contract uses metadata columns absent from init_database.
        # Build that schema only in this guarded synthetic DB.
        with conn:
            conn.execute("ALTER TABLE portfolio_history ADD COLUMN health_score REAL")
            conn.execute("ALTER TABLE portfolio_history ADD COLUMN confidence TEXT")
            conn.execute("ALTER TABLE portfolio_history ADD COLUMN market_condition TEXT")

        before = conn.execute(
            "SELECT COUNT(*) FROM portfolio_history"
        ).fetchone()[0]

        conn.close()

        response = client.get(
            "/api/portfolio?mode=balanced&save=true"
        )

        assert response.status_code == 200
        assert response.is_json

        conn = stack.enter_context(closing(synthetic_ready_api.db.connect()))

        after = conn.execute(
            "SELECT COUNT(*) FROM portfolio_history"
        ).fetchone()[0]

        rows = conn.execute(
            """
            SELECT
                mode,
                ticker,
                weight,
                score,
                created_at,
                health_score,
                confidence,
                market_condition
            FROM portfolio_history
            ORDER BY id DESC
            LIMIT 4
            """
        ).fetchall()

        conn.close()

        assert after - before == 4, (
            "Balanced portfolio must persist exactly four constituent rows"
        )

        assert len(rows) == 4

        assert {row[0] for row in rows} == {"balanced"}

        assert len({row[4] for row in rows}) == 1, (
            "One portfolio snapshot must share one created_at value"
        )

        assert sum(float(row[2]) for row in rows) == 100.0, (
            "Persisted portfolio weights must total 100 percent"
        )

        assert all(
            row[5] is not None
            and row[6] is not None
            and row[7] is not None
            for row in rows
        ), (
            "Portfolio history metadata must be persisted"
        )

        assert len({row[5] for row in rows}) == 1
        assert len({row[6] for row in rows}) == 1
        assert len({row[7] for row in rows}) == 1
