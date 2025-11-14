import sqlite3
import json
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from src.contracts.events import LogEvent, MetricEvent, TraceEvent

DATABASE_PATH = "/app/data/logs.db"


def init_db():
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
    cursor.execute(
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
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS traces (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            service TEXT NOT NULL,
            trace_id TEXT NOT NULL,
            span_id TEXT NOT NULL,
            parent_span_id TEXT,
            name TEXT NOT NULL,
            duration REAL NOT NULL,
            tags TEXT
        )
    """
    )
    conn.commit()
    conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/save/log")
async def save_log(log_event: LogEvent):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO logs (id, timestamp, service, level, message, details)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                str(log_event.id),
                log_event.timestamp.isoformat(),
                log_event.service,
                log_event.level,
                log_event.message,
                json.dumps(log_event.details) if log_event.details else None,
            ),
        )
        conn.commit()
        conn.close()
        return {"message": "Log event saved successfully"}
    except Exception as e:
        print("ERROR AL GUARDAR LOG:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/save/metric")
async def save_metric(metric_event: MetricEvent):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO metrics (id, timestamp, service, name, value, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                str(metric_event.id),
                metric_event.timestamp.isoformat(),
                metric_event.service,
                metric_event.name,
                metric_event.value,
                json.dumps(metric_event.tags),
            ),
        )
        conn.commit()
        conn.close()
        return {"message": "Metric event saved successfully"}
    except Exception as e:
        print("ERROR AL GUARDAR METRICA:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/save/trace")
async def save_trace(trace_event: TraceEvent):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO traces (
                id,
                timestamp,
                service,
                trace_id,
                span_id,
                parent_span_id,
                name,
                duration,
                tags
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(trace_event.id),
                trace_event.timestamp.isoformat(),
                trace_event.service,
                str(trace_event.trace_id),
                str(trace_event.span_id),
                str(trace_event.parent_span_id) if trace_event.parent_span_id else None,
                trace_event.name,
                trace_event.duration,
                json.dumps(trace_event.tags) if trace_event.tags else None,
            ),
        )

        conn.commit()
        conn.close()

        return {"message": "Trace event saved successfully"}

    except Exception as e:
        print("ERROR AL GUARDAR TRACE:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))
