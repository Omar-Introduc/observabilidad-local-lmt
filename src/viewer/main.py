from fastapi import FastAPI, HTTPException
import sqlite3
from pathlib import Path
import json

app = FastAPI()

DB_PATH = Path("/app/data/logs.db")


@app.get("/health")
def health_check():
    """
    Si app esta viva, devuelve ok
    """
    return {"status": "ok"}


@app.get("/")
def home():
    """
    Root del viewer
    """
    return {"message": "Usted esta en el Viewer"}


def read_logs():
    if not DB_PATH.exists():
        return []

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, timestamp, service, level, message, details FROM logs"
        )
        raw_logs = cursor.fetchall()

        conn.close()

        logs = []
        for log_info in raw_logs:

            details_as_dict = json.loads(log_info[5]) if log_info[5] else None

            logs.append(
                {
                    "id": log_info[0],
                    "timestamp": log_info[1],
                    "service": log_info[2],
                    "level": log_info[3],
                    "message": log_info[4],
                    "details": details_as_dict,
                }
            )
        return logs

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs")
def get_logs():
    logs = read_logs() or []
    logs = list(logs)
    return {"count": len(logs), "logs": logs}

def read_metrics():
    if not DB_PATH.exists():
        return []

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        """
        CREATE TABLE IF NOT EXISTS metrics (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            service TEXT,
            name TEXT,
            value REAL,
            tags TEXT
        )
        """

        cursor.execute(
            "SELECT id, timestamp, service, name, value, tags FROM metrics"
        )
        raw_metrics = cursor.fetchall()

        conn.close()

        metrics = []
        for metric_info in raw_metrics:

            tags_as_dict = json.loads(metric_info[5]) if metric_info[5] else None

            metrics.append(
                {
                    "id": metric_info[0],
                    "timestamp": metric_info[1],
                    "service": metric_info[2],
                    "name": metric_info[3],
                    "value": metric_info[4],
                    "tags": tags_as_dict,
                }
            )
        return metrics

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def get_metrics():
    metrics = read_metrics() or []
    metrics = list(metrics)
    return {"count": len(metrics), "metrics": metrics}

def read_traces():
    if not DB_PATH.exists():
        return []

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        """
        id: UUID
        timestamp: datetime
        service: str = Field(..., min_length=1)
        trace_id: UUID
        span_id: UUID
        parent_span_id: Optional[UUID] = None
        name: str = Field(..., min_length=1)
        duration: float
        tags: Dict[str, str]
        """

        cursor.execute(
            "SELECT id, timestamp, service, trace_id, span_id, parent_span_id, name, duration, tags FROM traces"
        )
        raw_traces = cursor.fetchall()

        conn.close()

        traces = []
        for trace_info in raw_traces:

            tags_as_dict = json.loads(trace_info[8]) if trace_info[8] else {}
            parent_span_id = trace_info[5] if trace_info[5] else None

            traces.append(
                {
                    "id": trace_info[0],
                    "timestamp": trace_info[1],
                    "service": trace_info[2],
                    "trace_id": trace_info[3],
                    "span_id": trace_info[4],
                    "parent_span_id": parent_span_id,
                    "name": trace_info[6],
                    "duration": trace_info[7],
                    "tags": tags_as_dict,
                }
            )
        return traces

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/traces")
def get_traces():
    traces = read_traces() or []
    traces = list(traces)
    return {"count": len(traces), "traces": traces}
