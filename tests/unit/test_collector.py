from fastapi.testclient import TestClient
from src.collector.main import app
from uuid import uuid4
from datetime import datetime as Datetime
import pytest
import datetime
from unittest.mock import patch, MagicMock

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


def test_home_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Usted esta en el Collector"}


def test_health_check_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


client = TestClient(app)


def valid_log_payload():
    return {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "demo",
        "level": "INFO",
        "message": "Test log",
        "details": {"foo": "bar"},
    }


@patch("src.collector.main.httpx.Client")
def test_ingest_log_success(mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client

    mock_response = MagicMock()
    mock_response.json.return_value = {"saved": True}
    mock_response.raise_for_status.return_value = None
    mock_client.post.return_value = mock_response

    payload = valid_log_payload()

    res = client.post("/ingest/log", json=payload)

    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    assert res.json()["store_response"] == {"saved": True}

    mock_client.post.assert_called_once()


@patch("src.collector.main.httpx.Client")
def test_ingest_log_store_down(mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client

    mock_client.post.side_effect = Exception("boom")

    payload = valid_log_payload()
    res = client.post("/ingest/log", json=payload)

    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


METRICAS_INVALIDAS = [
    {},
    {
        "id": str(uuid4()),
        "timestamp": "2025/11/09",
        "service": "api",
        "name": "metric.a",
        "value": 1.2,
        "tags": {"env": "test"},
    },
    {
        "id": "12345678",
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "name": "metric.b",
        "value": 3.4,
        "tags": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "",
        "name": "metric.c",
        "value": 5.6,
        "tags": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "name": ".metric.d",
        "value": 7.8,
        "tags": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "name": "metric.e.",
        "value": 9.0,
        "tags": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "name": "metric.f",
        "value": -1.0,
        "tags": {"env": "test"},
    },
]


METRICAS_VALIDAS = [
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "name": "metric.g",
        "value": 1.23,
        "tags": {"env": "test"},
    },
    {
        "id": str(uuid4()),
        "timestamp": Datetime.now(datetime.UTC).isoformat(),
        "service": "api",
        "name": "metric.h",
        "value": 4.56,
        "tags": {},
    },
]


@pytest.mark.parametrize("payload", METRICAS_VALIDAS)
def test_valid_metric_returns_200(payload):
    response = client.post("/ingest/metric", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.parametrize("payload", METRICAS_INVALIDAS)
def test_invalid_metric_returns_422(payload):
    response = client.post("/ingest/metric", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "exc",
    [
        Exception("network down"),
        ValueError("bad value"),
        RuntimeError("unexpected"),
    ],
)
@patch("src.collector.main.httpx.Client")
def test_ingest_log_parametrized_errors(mock_client_cls, exc):
    mock_client = MagicMock()
    mock_client_cls.return_value.__enter__.return_value = mock_client

    mock_client.post.side_effect = exc

    payload = valid_log_payload()
    res = client.post("/ingest/log", json=payload)

    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
