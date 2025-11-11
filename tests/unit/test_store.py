import pytest
from fastapi.testclient import TestClient
from src.store.main import app, DATABASE_PATH
import sqlite3
import os
import uuid
from datetime import datetime

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    # Creamos una base de datos temporal para el test
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            service TEXT,
            level TEXT,
            message TEXT,
            details TEXT
        )
    """
    )
    conn.commit()
    conn.close()

    yield

    # Nos aseguramos de mantener limpio el test
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)


def test_save_log_success(setup_database):
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

    # Verificamos que lo datos sean guardado o modificaciones
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs WHERE id=?", (log_data["id"],))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == log_data["id"]


def test_save_log_invalid_data():
    invalid_log_data = {
        "id": str(uuid.uuid4()),
        "timestamp": "invalid-timestamp",
        "service": "test-service",
        "level": "INFO",
        "message": "This is a test log message",
    }

    response = client.post("/save/log", json=invalid_log_data)

    assert response.status_code == 422
