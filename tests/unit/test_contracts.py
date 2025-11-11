import pytest
from datetime import datetime
from uuid import uuid4
from pydantic import ValidationError

from src.contracts.events import (
    LogEvent,
    MetricEvent,
    TraceEvent,
)


def test_log_event_creation():
    log_id = uuid4()
    timestamp = datetime.now()
    log = LogEvent(
        id=log_id,
        timestamp=timestamp,
        service="test_service",
        level="INFO",
        message="This is a test log message",
        details={"key": "value"},
    )
    assert log.id == log_id
    assert log.level == "INFO"
    assert log.message == "This is a test log message"


def test_metric_event_creation():
    metric_id = uuid4()
    timestamp = datetime.now()
    metric = MetricEvent(
        id=metric_id,
        timestamp=timestamp,
        service="test_service",
        name="test.metric",
        value=1.23,
        tags={"tag1": "value1"},
    )
    assert metric.id == metric_id
    assert metric.name == "test.metric"
    assert metric.value == 1.23


def test_trace_event_creation():
    trace_id = uuid4()
    span_id = uuid4()
    timestamp = datetime.now()
    trace = TraceEvent(
        id=uuid4(),
        timestamp=timestamp,
        service="test_service",
        trace_id=trace_id,
        span_id=span_id,
        name="test_trace",
        duration=0.123,  #
        tags={"tag1": "value1"},
    )
    assert trace.trace_id == trace_id
    assert trace.name == "test_trace"
    assert trace.duration == 0.123


def test_log_event_failures():
    """Prueba que LogEvent falla con datos incorrectos."""

    with pytest.raises(ValidationError):
        LogEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            service="test",
            level="INVALID_LEVEL",
            message="Test",
        )

    with pytest.raises(ValidationError):
        LogEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            service="",
            level="INFO",
            message="Test",
        )

    with pytest.raises(ValidationError):
        LogEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            service="test",
            level="INFO",
            message="",
        )


def test_metric_event_failures():
    """Prueba que MetricEvent falla con valores negativos o nombres inválidos."""

    with pytest.raises(ValidationError):
        MetricEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            service="test",
            name="test.metric",
            value=-1.0,
            tags={},
        )

    with pytest.raises(ValidationError):
        MetricEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            service="test",
            name="invalid-metric-name!",
            value=1.0,
            tags={},
        )

    with pytest.raises(ValidationError):
        MetricEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            service="test",
            name=".test.metric",
            value=1.0,
            tags={},
        )


def test_trace_event_failures():
    """Prueba que TraceEvent falla con duración negativa."""

    with pytest.raises(ValidationError):
        TraceEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            service="test",
            trace_id=uuid4(),
            span_id=uuid4(),
            name="test",
            duration=-1.0,
            tags={},
        )

    with pytest.raises(ValidationError):
        TraceEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            service="test",
            trace_id=uuid4(),
            span_id=uuid4(),
            name="",
            duration=1.0,
            tags={},
        )
