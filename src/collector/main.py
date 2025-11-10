from fastapi import FastAPI
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
    return {"status": "ok"}
