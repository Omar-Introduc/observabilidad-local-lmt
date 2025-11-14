import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

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
        assert response.json() == {"count": 1 ,"logs": fake_logs}


@pytest.mark.parametrize("fake_logs", [
    [],
    None,
])
def test_get_logs_edge_cases(fake_logs):
    with patch("src.viewer.main.read_logs", autospec=True, return_value=fake_logs):
        response = client.get("/logs")
        assert response.status_code == 200