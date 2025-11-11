import sqlite3
import json
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from src.contracts.events import LogEvent

DATABASE_PATH = "/app/data/logs.db"

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            service TEXT,
            level TEXT,
            message TEXT,
            details TEXT
        )
    """)
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
        cursor.execute("""
            INSERT INTO logs (id, timestamp, service, level, message, details)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(log_event.id),
            log_event.timestamp.isoformat(),
            log_event.service,
            log_event.level,
            log_event.message,
            json.dumps(log_event.details) if log_event.details else None
        ))
        conn.commit()
        conn.close()
        return {"message": "Log event saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
