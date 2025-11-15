from fastapi import FastAPI
from src.adapter.main import TelemetryAdapter
from uuid import uuid4

app = FastAPI()
adapter = TelemetryAdapter(service_name="demo_service_1")

@app.get("/")
def home():
    """
    Root of the demo service 1
    """
    return {"message": "Demo Service 1"}

@app.get("/log")
def send_log():
    adapter.log("INFO", "This is a test log from Demo Service 1")
    return {"status": "log sent"}

@app.get("/metric")
def send_metric():
    adapter.metric("test.metric", 123.45, {"tag": "demo"})
    return {"status": "metric sent"}

@app.get("/trace")
def send_trace():
    trace_id = uuid4()
    span_id = uuid4()
    adapter.trace(trace_id=trace_id, span_id=span_id, name="test.trace", duration=0.123)
    return {"status": "trace sent"}
