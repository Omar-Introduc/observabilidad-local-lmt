from fastapi import FastAPI, HTTPException
from src.contracts.events import LogEvent

app = FastAPI()

@app.get("/")
def home():
    """
    Root del collector
    """
    return {"message": "Usted esta en el Collector"}

@app.get("/health")
def health_check():
    """
    Si app esta viva, devuelve ok
    """
    return {"status": "ok"}

@app.post("/ingest/log")
def ingest_log(event: LogEvent):
    """
    Recibe un LogEvent, valida automáticamente el esquema y responde 200 OK.
    """
    try:
        # Pydantic ya validó el JSON automáticamente al parsear
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))