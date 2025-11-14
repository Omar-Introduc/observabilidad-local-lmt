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
