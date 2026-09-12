import os
import shutil
import sqlite3
import tempfile
from pathlib import Path

import config
import database


def run_test():
    source_db = Path(r".\database\g7_10_18_integration_test.db")

    fd, db_path = tempfile.mkstemp(
        prefix="decision_intelligence_read_only_",
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

        client = api_server.app.test_client()

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_outcome_history"
        )
        history_before = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
        )
        snapshot_before = cursor.fetchone()[0]

        conn.close()

        response_1 = client.get(
            "/api/portfolio/decision-intelligence"
        )

        assert response_1.status_code == 200
        assert response_1.is_json

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_outcome_history"
        )
        history_after_first = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
        )
        snapshot_after_first = cursor.fetchone()[0]

        conn.close()

        response_2 = client.get(
            "/api/portfolio/decision-intelligence"
        )

        assert response_2.status_code == 200
        assert response_2.is_json

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_outcome_history"
        )
        history_after_second = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM ai_decision_portfolio_snapshot"
        )
        snapshot_after_second = cursor.fetchone()[0]

        conn.close()

        assert history_after_first == history_before, (
            "GET must not create Outcome History"
        )

        assert snapshot_after_first == snapshot_before, (
            "GET must not create Portfolio Snapshot"
        )

        assert history_after_second == history_before, (
            "Repeated GET must not create Outcome History"
        )

        assert snapshot_after_second == snapshot_before, (
            "Repeated GET must not create Portfolio Snapshot"
        )

        print("CASE 1 FIRST GET HISTORY: PASS")
        print("CASE 2 FIRST GET SNAPSHOT: PASS")
        print("CASE 3 SECOND GET HISTORY: PASS")
        print("CASE 4 SECOND GET SNAPSHOT: PASS")
        print("")
        print("OVERALL RESULT: PASS")

    finally:
        config.DATABASE_PATH = original_config_path
        database.DATABASE_PATH = original_database_path

        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass


run_test()
