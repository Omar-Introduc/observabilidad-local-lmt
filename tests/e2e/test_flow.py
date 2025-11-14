import os
import subprocess
import time
import uuid
from datetime import datetime, timezone
import httpx
import pytest

# Generate a unique run ID for this test session
run_id = uuid.uuid4()


@pytest.fixture(scope="session", autouse=True)
def manage_docker_compose(request):
    """
    Fixture to automatically start and stop Docker Compose services for the
    entire test session.
    """
    # Using a unique project name to avoid conflicts in parallel test runs
    project_name = f"test_project_{run_id}"
    compose_file = "docker-compose.yml"

    # Command to start services
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
    # Command to stop services
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

    # Start services
    subprocess.check_call(start_command)
    print("Docker-compose services started.")

    # Allow time for services to initialize
    time.sleep(5)

    # Yield control to the tests
    yield

    # Teardown: stop services after all tests have run
    subprocess.check_call(stop_command)
    print("Docker-compose services stopped and volumes removed.")


def wait_for_service(url, timeout=30):
    """
    Waits for a service to become available by repeatedly polling its health
    check endpoint.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with httpx.Client() as client:
                response = client.get(url)
                if response.status_code == 200:
                    print(f"Service at {url} is up.")
                    return
        except httpx.RequestError:
            pass
        time.sleep(1)
    pytest.fail(f"Service at {url} did not become available in {timeout} seconds.")


@pytest.fixture(scope="session")
def service_urls():
    """
    Provides the URLs for the services under test. Waits for each service to
    be healthy before returning.
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
    Tests the full data flow from Collector to Viewer, ensuring data is
    correctly processed and persisted.
    """
    collector_url = service_urls["collector"]
    viewer_url = service_urls["viewer"]

    # 1. Inject a log event into the Collector
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

    # Allow a moment for the data to be processed and stored
    time.sleep(2)

    # 2. Query the Viewer to retrieve the log
    with httpx.Client() as client:
        response = client.get(f"{viewer_url}/logs/find/{log_id}")
    assert response.status_code == 200, "Log should be found in the viewer"

    # 3. Validate the retrieved data
    retrieved_log = response.json()
    assert retrieved_log["id"] == str(log_id)
    assert retrieved_log["message"] == f"Test log message {run_id}"
    assert retrieved_log["details"]["run_id"] == str(run_id)

    # 4. Verify persistence by querying again (optional but good practice)
    with httpx.Client() as client:
        response_persistent = client.get(f"{viewer_url}/logs/find/{log_id}")
    assert response_persistent.status_code == 200
    assert response_persistent.json()["id"] == str(log_id)
