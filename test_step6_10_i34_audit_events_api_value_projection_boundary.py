import os
import sqlite3
import tempfile
from pathlib import Path

import config
import database
import api_server


def run_test():
    fd, db_path = tempfile.mkstemp(
        prefix="step6_10_i34_",
        suffix=".db"
    )
    os.close(fd)

    original_config_path = config.DATABASE_PATH
    original_database_path = database.DATABASE_PATH

    try:
        test_db_path = Path(db_path)

        config.DATABASE_PATH = test_db_path
        database.DATABASE_PATH = test_db_path
        database.init_database()

        conn = database.get_connection()
        cursor = conn.cursor()

        events = [
            (
                "OUTCOME_EVALUATION_STARTED",
                "2026-08-31T16:01:00+09:00",
                "portfolio_outcome_evaluation",
                "STARTED",
                501,
                "outcome:501",
                '{"evaluation_date": null, "actual_outcome_gate": true}',
            ),
            (
                "OUTCOME_EVALUATED",
                "2026-08-31T16:02:00+09:00",
                "portfolio_outcome_evaluation",
                "EVALUATED",
                501,
                "outcome:501",
                '{"portfolio_return": 0.05}',
            ),
            (
                "LEARNING_SIGNAL_GENERATED",
                "2026-08-31T16:03:00+09:00",
                "outcome_intelligence",
                "AVAILABLE",
                501,
                "outcome:501",
                '{"learning_signal": "POSITIVE", "learning_signal_strength": 0.8}',
            ),
            (
                "REASSESSMENT_REQUIRED",
                "2026-08-31T16:04:00+09:00",
                "outcome_intelligence",
                "REQUIRED",
                501,
                "outcome:501",
                "not-valid-json",
            ),
            (
                "ADAPTIVE_STRATEGY_GENERATED",
                "2026-08-31T16:05:00+09:00",
                "adaptive_strategy",
                "GENERATED",
                501,
                "outcome:501",
                "",
            ),
        ]

        for event in events:
            cursor.execute(
                """
                INSERT INTO audit_event
                (
                    audit_event_id,
                    event_type,
                    event_time,
                    source,
                    status,
                    outcome_history_id,
                    correlation_key,
                    details
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"{event[0]}:{event[5]}:{event[1]}",
                    event[0],
                    event[1],
                    event[2],
                    event[3],
                    event[4],
                    event[5],
                    event[6],
                ),
            )

        conn.commit()

        cursor.execute(
            """
            SELECT
                id,
                audit_event_id,
                event_type,
                event_time,
                source,
                status,
                outcome_history_id,
                correlation_key,
                details
            FROM audit_event
            WHERE outcome_history_id = 501
            ORDER BY event_time ASC, id ASC
            """
        )

        expected_rows = cursor.fetchall()
        conn.close()

        client = api_server.app.test_client()

        print("=" * 60)
        print("Step6-10-I-34 Audit Events API Value Projection Boundary")
        print("=" * 60)

        print("")
        print("CASE 1 RAW VALUE PROJECTION")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=501&limit=5"
        )

        assert response.status_code == 200

        payload = response.get_json()

        assert payload["success"] is True
        assert len(payload["events"]) == 5

        print("CASE 1: PASS")

        print("")
        print("CASE 2 IDENTIFIER VALUE PRESERVATION")

        api_events = payload["events"]

        for row, event in zip(expected_rows, api_events):
            assert event["id"] == row[0]
            assert event["audit_event_id"] == row[1]
            assert event["outcome_history_id"] == row[6]
            assert event["correlation_key"] == row[7]

        print("CASE 2: PASS")

        print("")
        print("CASE 3 EVENT METADATA VALUE PRESERVATION")

        for row, event in zip(expected_rows, api_events):
            assert event["event_type"] == row[2]
            assert event["event_time"] == row[3]
            assert event["source"] == row[4]
            assert event["status"] == row[5]

        print("CASE 3: PASS")

        print("")
        print("CASE 4 DETAILS RAW STRING PRESERVATION")

        for row, event in zip(expected_rows, api_events):
            assert event["details"] == row[8]
            assert isinstance(event["details"], str)

        assert api_events[0]["details"] == (
            '{"evaluation_date": null, "actual_outcome_gate": true}'
        )
        assert api_events[1]["details"] == (
            '{"portfolio_return": 0.05}'
        )
        assert api_events[2]["details"] == (
            '{"learning_signal": "POSITIVE", "learning_signal_strength": 0.8}'
        )
        assert api_events[3]["details"] == "not-valid-json"
        assert api_events[4]["details"] == ""

        print("CASE 4: PASS")

        print("")
        print("CASE 5 NO TIMELINE STYLE TRANSFORMATION")

        assert isinstance(api_events[0]["details"], str)
        assert isinstance(api_events[1]["details"], str)
        assert isinstance(api_events[2]["details"], str)
        assert api_events[3]["details"] == "not-valid-json"
        assert api_events[4]["details"] == ""

        print("CASE 5: PASS")

        print("")
        print("CASE 6 FILTERED VALUE PROJECTION")

        response = client.get(
            "/api/ai-decision/audit-events"
            "?correlation_key=outcome:501&limit=2"
        )

        assert response.status_code == 200

        filtered_payload = response.get_json()

        assert filtered_payload["success"] is True
        assert len(filtered_payload["events"]) == 2

        assert [
            event["event_type"]
            for event in filtered_payload["events"]
        ] == [
            "OUTCOME_EVALUATION_STARTED",
            "OUTCOME_EVALUATED",
        ]

        assert [
            event["details"]
            for event in filtered_payload["events"]
        ] == [
            '{"evaluation_date": null, "actual_outcome_gate": true}',
            '{"portfolio_return": 0.05}',
        ]

        print("CASE 6: PASS")

        print("")
        print("CASE 7 READ-ONLY AUDIT SOURCE")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                audit_event_id,
                event_type,
                event_time,
                source,
                status,
                outcome_history_id,
                correlation_key,
                details
            FROM audit_event
            ORDER BY event_time ASC, id ASC
            """
        )

        before = cursor.fetchall()
        conn.close()

        client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=501&limit=5"
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                audit_event_id,
                event_type,
                event_time,
                source,
                status,
                outcome_history_id,
                correlation_key,
                details
            FROM audit_event
            ORDER BY event_time ASC, id ASC
            """
        )

        after = cursor.fetchall()
        conn.close()

        assert before == after

        print("CASE 7: PASS")

        print("")
        print("CASE 8 NO SYNTHETIC EVENT CREATION")

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            """
        )

        before_count = cursor.fetchone()[0]
        conn.close()

        client.get(
            "/api/ai-decision/audit-events"
            "?outcome_history_id=501&limit=5"
        )

        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM audit_event
            """
        )

        after_count = cursor.fetchone()[0]
        conn.close()

        assert before_count == after_count

        print("CASE 8: PASS")

        print("")
        print("=" * 60)
        print("OVERALL RESULT: PASS")
        print("=" * 60)

    finally:
        config.DATABASE_PATH = original_config_path
        database.DATABASE_PATH = original_database_path

        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass


run_test()
