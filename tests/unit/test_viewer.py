import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import json
import sqlite3

from src.viewer.main import app, read_logs

client = TestClient(app)


def test_get_logs_ok():
    fake_logs = [
        {
            "id": "1",
            "timestamp": "2024-01-01T10:00:00",
            "service": "demo",
            "level": "INFO",
            "message": "hello",
            "details": {"a": 1},
        }
    ]

    with patch("src.viewer.main.read_logs", autospec=True, return_value=fake_logs):
        response = client.get("/logs")

        assert response.status_code == 200
        assert response.json() == {"count": 1, "logs": fake_logs}


@pytest.mark.parametrize(
    "fake_logs",
    [
        [],
        None,
    ],
)
def test_get_logs_edge_cases(fake_logs):
    with patch("src.viewer.main.read_logs", autospec=True, return_value=fake_logs):
        response = client.get("/logs")
        assert response.status_code == 200


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_read_logs_returns_empty_if_db_not_exists(tmp_path, monkeypatch):
    fake_db = tmp_path / "no_db.db"
    monkeypatch.setattr("src.viewer.main.DB_PATH", fake_db)

    result = read_logs()
    assert result == []


def test_read_logs_success(tmp_path, monkeypatch):
    db_file = tmp_path / "logs.db"
    monkeypatch.setattr("src.viewer.main.DB_PATH", db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE logs (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            service TEXT,
            level TEXT,
            message TEXT,
            details TEXT
        )
        """
    )
    cursor.execute(
        """
        INSERT INTO logs (id, timestamp, service, level, message, details)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "123",
            "2024-10-10T10:00:00",
            "svc",
            "INFO",
            "hola",
            json.dumps({"a": "b"}),
        ),
    )
    conn.commit()
    conn.close()

    # Ejecutar
    logs = read_logs()

    assert isinstance(logs, list)
    assert len(logs) == 1
    assert logs[0]["id"] == "123"
    assert logs[0]["details"] == {"a": "b"}
