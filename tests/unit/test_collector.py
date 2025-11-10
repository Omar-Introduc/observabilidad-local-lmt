from fastapi.testclient import TestClient
from src.collector.main import app
from uuid import uuid4
from datetime import datetime as Datetime
import pytest
import datetime

client = TestClient(app)

LOGS_INVALIDOS = [
    {},
    {
        "id": str(uuid4()),
        "timestamp": "2025/11/09",
        "service": "api",
        "level": "INFO",
        "message": "Log con fecha en formato incorrecto",
        "details": {"env": "test"},
    },
    {
        "id": "12345678",
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "level": "INFO",
        "message": "Log con UUID incorrecto",
        "details": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "",
        "level": "INFO",
        "message": "Log con nombre de servicio vacio",
        "details": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "level": "TRACE",
        "message": "Log con level incorrecto",
        "details": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "level": "",
        "message": "Log con level vacio",
        "details": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "level": "INFO",
        "message": "",
        "details": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "level": "INFO",
        "message": "Log con campo details inválido",
        "details": {"number": 1},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "level": "INFO",
        "message": "Log con campo obligatorio faltante (service)",
        "details": {"env": "test"},
    },
]

LOGS_VALIDOS = [
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "level": "INFO",
        "message": "Log válido",
        "details": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "level": "INFO",
        "message": "Log válido sin campo opcionaldetails",
    },
]


@pytest.mark.parametrize("payload", LOGS_VALIDOS)
def test_valid_log_returns_200(payload):
    response = client.post("/ingest/log", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.parametrize("payload", LOGS_INVALIDOS)
def test_invalid_log_returns_422(payload):
    response = client.post("/ingest/log", json=payload)
    assert response.status_code == 422
