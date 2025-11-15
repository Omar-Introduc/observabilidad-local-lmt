from unittest.mock import patch, MagicMock
from src.adapter.main import TelemetryAdapter
from uuid import uuid4


def test_send_log():
    adapter = TelemetryAdapter(service_name="test_service")
    with patch("httpx.Client") as mock_client:
        mock_post = MagicMock()
        mock_client.return_value.__enter__.return_value.post = mock_post
        adapter.log("INFO", "test message")
        mock_post.assert_called_once()


def test_send_metric():
    adapter = TelemetryAdapter(service_name="test_service")
    with patch("httpx.Client") as mock_client:
        mock_post = MagicMock()
        mock_client.return_value.__enter__.return_value.post = mock_post
        adapter.metric("test.metric", 1.0)
        mock_post.assert_called_once()


def test_send_trace():
    adapter = TelemetryAdapter(service_name="test_service")
    with patch("httpx.Client") as mock_client:
        mock_post = MagicMock()
        mock_client.return_value.__enter__.return_value.post = mock_post
        adapter.trace(uuid4(), uuid4(), "test.trace", 0.1)
        mock_post.assert_called_once()
