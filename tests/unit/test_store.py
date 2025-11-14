import pytest
from fastapi.testclient import TestClient

from src.store.main import app, DATABASE_PATH
import uuid
from datetime import datetime
import json


@pytest.fixture
def client(mocker):
    """
    prepara el cliente de prueba
    """
    mocker.patch("src.store.main.sqlite3.connect")

    test_client = TestClient(app)
    yield test_client


def test_save_log_success(client, mocker):
    """
    Prueba que el endpoint
    """
    mock_connect = mocker.patch("src.store.main.sqlite3.connect")

    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value

    log_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "service": "test-service",
        "level": "INFO",
        "message": "This is a test log message",
        "details": {"key": "value"},
    }

    response = client.post("/save/log", json=log_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Log event saved successfully"}

    mock_connect.assert_called_with(DATABASE_PATH)

    mock_conn.cursor.assert_called_once()

    expected_params = (
        log_data["id"],
        log_data["timestamp"],
        log_data["service"],
        log_data["level"],
        log_data["message"],
        json.dumps(log_data["details"]),
    )
    mock_cursor.execute.assert_called_once_with(
        mocker.ANY,
        expected_params,
    )

    mock_conn.commit.assert_called_once()

    mock_conn.close.assert_called_once()


def test_save_log_invalid_data(client):
    """
    Prueba que el endpoint devuelve 422 con datos malos
    """
    invalid_log_data = {
        "id": str(uuid.uuid4()),
        "timestamp": "invalid-timestamp",
        "service": "test-service",
        "level": "INFO",
        "message": "This is a test log message",
    }

    response = client.post("/save/log", json=invalid_log_data)

    assert response.status_code == 422


def test_save_metric_success(client, mocker):
    """
    Prueba que el endpoint guarda una métrica correctamente
    """
    mock_connect = mocker.patch("src.store.main.sqlite3.connect")
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value

    metric_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "service": "test-service",
        "name": "test.metric",
        "value": 123.45,
        "tags": {"env": "test"},
    }

    response = client.post("/save/metric", json=metric_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Metric event saved successfully"}

    mock_connect.assert_called_with(DATABASE_PATH)
    mock_conn.cursor.assert_called_once()

    expected_params = (
        metric_data["id"],
        metric_data["timestamp"],
        metric_data["service"],
        metric_data["name"],
        metric_data["value"],
        json.dumps(metric_data["tags"]),
    )
    mock_cursor.execute.assert_called_once_with(
        mocker.ANY,
        expected_params,
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_save_metric_invalid_data(client):
    """
    Prueba que el endpoint devuelve 422 con datos de métrica inválidos
    """
    invalid_metric_data = {
        "id": str(uuid.uuid4()),
        "timestamp": "invalid-timestamp",
        "service": "test-service",
        "name": "test.metric",
        "value": 123.45,
        "tags": {"env": "test"},
    }

    response = client.post("/save/metric", json=invalid_metric_data)

    assert response.status_code == 422


def test_init_db(mocker):
    """
    Prueba que la función init_db crea las tablas de la base de datos
    """
    mock_connect = mocker.patch("src.store.main.sqlite3.connect")
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value

    from src.store.main import init_db

    init_db()

    mock_connect.assert_called_with(DATABASE_PATH)
    mock_conn.cursor.assert_called_once()
    assert mock_cursor.execute.call_count == 2
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_save_log_db_error(client, mocker):
    """
    Prueba que el endpoint maneja errores de la base de datos
    """
    mock_connect = mocker.patch("src.store.main.sqlite3.connect")
    mock_conn = mock_connect.return_value
    mock_conn.cursor.side_effect = Exception("DB error")

    log_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "service": "test-service",
        "level": "INFO",
        "message": "This is a test log message",
        "details": {"key": "value"},
    }

    response = client.post("/save/log", json=log_data)

    assert response.status_code == 500


def test_save_metric_db_error(client, mocker):
    """
    Prueba que el endpoint maneja errores de la base de datos
    """
    mock_connect = mocker.patch("src.store.main.sqlite3.connect")
    mock_conn = mock_connect.return_value
    mock_conn.cursor.side_effect = Exception("DB error")

    metric_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "service": "test-service",
        "name": "test.metric",
        "value": 123.45,
        "tags": {"env": "test"},
    }

    response = client.post("/save/metric", json=metric_data)

    assert response.status_code == 500
