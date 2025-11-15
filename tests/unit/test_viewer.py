import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import json
import sqlite3

from src.viewer.main import app, read_logs, read_metrics, read_traces

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


# ---metrics


def test_get_metrics_ok():
    fake_metrics = [
        {
            "id": "123",
            "timestamp": "2024-10-10T10:00:00",
            "service": "api",
            "name": "metric.g",
            "value": 1.23,
            "tags": {"env": "test"},
        }
    ]

    with patch(
        "src.viewer.main.read_metrics", autospec=True, return_value=fake_metrics
    ):
        response = client.get("/metrics")

        assert response.status_code == 200
        assert response.json() == {"count": 1, "metrics": fake_metrics}


@pytest.mark.parametrize(
    "fake_metrics",
    [
        [],
        None,
    ],
)
def test_get_metrics_edge_cases(fake_metrics):
    with patch(
        "src.viewer.main.read_metrics", autospec=True, return_value=fake_metrics
    ):
        response = client.get("/metrics")
        assert response.status_code == 200


def test_read_metrics_returns_empty_if_db_not_exists(tmp_path, monkeypatch):
    fake_db = tmp_path / "no_db.db"
    monkeypatch.setattr("src.viewer.main.DB_PATH", fake_db)

    result = read_metrics()
    assert result == []


def test_read_metrics_success(tmp_path, monkeypatch):
    db_file = tmp_path / "metrics.db"
    monkeypatch.setattr("src.viewer.main.DB_PATH", db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE metrics (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            service TEXT,
            name TEXT,
            value REAL,
            tags TEXT
        )
        """
    )
    cursor.execute(
        """
            INSERT INTO metrics (id, timestamp, service, name, value, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "123",
            "2024-10-10T10:00:00",
            "svc",
            "ejemplo",
            12.3,
            json.dumps({"a": "b"}),
        ),
    )
    conn.commit()
    conn.close()

    # Ejecutar
    metrics = read_metrics()

    assert isinstance(metrics, list)
    assert len(metrics) == 1
    assert metrics[0]["id"] == "123"
    assert metrics[0]["tags"] == {"a": "b"}


# ---traces


def test_get_traces_ok():
    fake_traces = [
        {
            "id": "123",
            "timestamp": "2024-10-10T10:00:00",
            "service": "servicio-ejemplo",
            "trace_id": "456",
            "span_id": "789",
            "parent_span_id": "159",  # opcional
            "name": "ejemplo",
            "duration": 67.67,
            "tags": {"status": "ok"},
        }
    ]

    with patch("src.viewer.main.read_traces", autospec=True, return_value=fake_traces):
        response = client.get("/traces")

        assert response.status_code == 200
        assert response.json() == {"count": 1, "traces": fake_traces}


@pytest.mark.parametrize(
    "fake_traces",
    [
        [],
        None,
    ],
)
def test_get_traces_edge_cases(fake_traces):
    with patch("src.viewer.main.read_traces", autospec=True, return_value=fake_traces):
        response = client.get("/traces")
        assert response.status_code == 200


def test_read_traces_returns_empty_if_db_not_exists(tmp_path, monkeypatch):
    fake_db = tmp_path / "no_db.db"
    monkeypatch.setattr("src.viewer.main.DB_PATH", fake_db)

    result = read_traces()
    assert result == []


def test_read_traces_success(tmp_path, monkeypatch):
    db_file = tmp_path / "traces.db"
    monkeypatch.setattr("src.viewer.main.DB_PATH", db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE traces (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            service TEXT NOT NULL,
            trace_id TEXT NOT NULL,
            span_id TEXT NOT NULL,
            parent_span_id TEXT,
            name TEXT NOT NULL,
            duration REAL NOT NULL,
            tags TEXT
        )
        """
    )
    cursor.execute(
        """
            INSERT INTO traces (
                id,
                timestamp,
                service,
                trace_id,
                span_id,
                parent_span_id,
                name,
                duration,
                tags
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
        (
            "123",
            "2024-10-10T10:00:00",
            "svc",
            "456",
            "789",
            "159",
            "ejemplo",
            12.3,
            json.dumps({"a": "b"}),
        ),
    )
    conn.commit()
    conn.close()

    # Ejecutar
    traces = read_traces()

    assert isinstance(traces, list)
    assert len(traces) == 1
    assert traces[0]["id"] == "123"
    assert traces[0]["trace_id"] == "456"
    assert traces[0]["span_id"] == "789"
    assert traces[0]["parent_span_id"] == "159"
    assert traces[0]["tags"] == {"a": "b"}
