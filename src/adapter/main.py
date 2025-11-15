import httpx
import os
import logging
from uuid import uuid4
from datetime import datetime, timezone
from src.contracts.events import LogEvent, MetricEvent, TraceEvent

logger = logging.getLogger(__name__)


class TelemetryAdapter:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.collector_base_url = os.getenv("COLLECTOR_URL", "http://collector:8000")

    def _send_event(self, endpoint: str, payload: dict):
        url = f"{self.collector_base_url.rstrip('/')}{endpoint}"
        try:
            with httpx.Client(timeout=2.0) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                logger.info(f"Event sent to {url}: {resp.json()}")
        except httpx.RequestError as e:
            logger.warning(f"Could not connect to Collector ({url}): {e}")
        except httpx.HTTPStatusError as e:
            logger.warning(
                f"Collector responded with error {e.response.status_code}: {e.response.text}"
            )
        except Exception as e:
            logger.exception(f"Unexpected error sending event to collector: {e}")

    def log(self, level: str, message: str, details: dict = None):
        event = LogEvent(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            service=self.service_name,
            level=level,
            message=message,
            details=details,
        )
        self._send_event("/ingest/log", event.model_dump(mode="json"))

    def metric(self, name: str, value: float, tags: dict = None):
        event = MetricEvent(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            service=self.service_name,
            name=name,
            value=value,
            tags=tags or {},
        )
        self._send_event("/ingest/metric", event.model_dump(mode="json"))

    def trace(
        self,
        trace_id: str,
        span_id: str,
        name: str,
        duration: float,
        parent_span_id: str = None,
        tags: dict = None,
    ):
        event = TraceEvent(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            service=self.service_name,
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=name,
            duration=duration,
            tags=tags or {},
        )
        self._send_event("/ingest/trace", event.model_dump(mode="json"))
