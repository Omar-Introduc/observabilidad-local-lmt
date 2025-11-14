import subprocess
import time
import uuid
from datetime import datetime, timezone
import httpx
import pytest

run_id = uuid.uuid4()


@pytest.fixture(scope="session", autouse=True)
def manage_docker_compose(request):
    """
    iniciar y detener automáticamente los servicios
    """
    project_name = f"test_project_{run_id}"
    compose_file = "docker-compose.yml"

    start_command = [
        "docker",
        "compose",
        "-f",
        compose_file,
        "-p",
        project_name,
        "up",
        "--build",
        "-d",
    ]
    stop_command = [
        "docker",
        "compose",
        "-f",
        compose_file,
        "-p",
        project_name,
        "down",
        "--volumes",
    ]

    subprocess.check_call(start_command)
    print("Servicios de Docker-compose iniciados.")

    time.sleep(5)

    yield

    subprocess.check_call(stop_command)
    print("Servicios de Docker-compose detenidos y volúmenes eliminados.")


def wait_for_service(url, timeout=30):
    """
    Espera a que un servicio esté disponible
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with httpx.Client() as client:
                response = client.get(url)
                if response.status_code == 200:
                    print(f"Servicio en {url} está activo.")
                    return
        except httpx.RequestError:
            pass
        time.sleep(1)
    pytest.fail(f"Servicio en {url} no estuvo disponible en {timeout} segundos.")


@pytest.fixture(scope="session")
def service_urls():
    """
    Provee las URLs de los servicios bajo prueba
    """
    urls = {
        "collector": "http://localhost:8000",
        "viewer": "http://localhost:8002",
    }
    wait_for_service(f"{urls['collector']}/health")
    wait_for_service(f"{urls['viewer']}/health")
    return urls


def test_full_flow(service_urls):
    """
    Prueba el flujo de datos completo (Collector -> Viewer)
    """
    collector_url = service_urls["collector"]
    viewer_url = service_urls["viewer"]

    log_id = uuid.uuid4()
    event_data = {
        "id": str(log_id),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "test_service",
        "level": "INFO",
        "message": f"Test log message {run_id}",
        "details": {"run_id": str(run_id)},
    }
    with httpx.Client() as client:
        response = client.post(f"{collector_url}/ingest/log", json=event_data)
    assert response.status_code == 200
    assert response.json().get("status") == "ok"

    time.sleep(2)

    with httpx.Client() as client:
        response = client.get(f"{viewer_url}/logs")

    assert response.status_code == 200, "El viewer debería responder en /logs"

    response_data = response.json()
    assert "logs" in response_data

    retrieved_log = None
    for log in response_data["logs"]:
        if log["id"] == str(log_id):
            retrieved_log = log
            break

    assert retrieved_log is not None, "El log enviado no se encontró en el viewer"

    assert retrieved_log["message"] == f"Test log message {run_id}"
    assert retrieved_log["details"]["run_id"] == str(run_id)
