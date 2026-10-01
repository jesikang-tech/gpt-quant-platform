import os
import shutil
import sqlite3
import tempfile
from pathlib import Path

import config
import database


def test_portfolio_history_persistence_contract():
    source_db = Path(r".\database\g7_10_18_integration_test.db")

    fd, db_path = tempfile.mkstemp(
        prefix="portfolio_history_contract_",
        suffix=".db"
    )
    os.close(fd)

    shutil.copy2(source_db, db_path)

    original_config_path = config.DATABASE_PATH
    original_database_path = database.DATABASE_PATH

    try:
        test_db_path = Path(db_path)

        config.DATABASE_PATH = test_db_path
        database.DATABASE_PATH = test_db_path

        import api_server
        from testing_helpers import authenticated_client

        client = authenticated_client(api_server.app)

        conn = sqlite3.connect(test_db_path)

        before = conn.execute(
            "SELECT COUNT(*) FROM portfolio_history"
        ).fetchone()[0]

        conn.close()

        response = client.get(
            "/api/portfolio?mode=balanced&save=true"
        )

        assert response.status_code == 200
        assert response.is_json

        conn = sqlite3.connect(test_db_path)

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

    finally:
        config.DATABASE_PATH = original_config_path
        database.DATABASE_PATH = original_database_path

        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass
