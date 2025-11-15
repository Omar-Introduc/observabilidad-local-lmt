from fastapi import FastAPI
from src.contracts.events import LogEvent, MetricEvent, TraceEvent
import os
import logging
import httpx

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


@app.post("/ingest/metric")
def ingest_metric(event: MetricEvent):
    """
    Recibe un MetricEvent, valida automáticamente el esquema usando Pydantic.
    """
    store_base = os.getenv("STORE_URL", "http://store:8000")
    store_endpoint = f"{store_base.rstrip('/')}/save/metric"

    logger = logging.getLogger("collector")
    payload = event.model_dump(mode="json")
    try:
        with httpx.Client(timeout=2.0) as client:
            resp = client.post(store_endpoint, json=payload)
            resp.raise_for_status()
            return {"status": "ok", "store_response": resp.json()}
    except httpx.RequestError as e:
        logger.warning("No se pudo conectar al Store (%s): %s", store_endpoint, e)
    except httpx.HTTPStatusError as e:
        logger.warning(
            "El Store respondió con error %s: %s",
            e.response.status_code,
            e.response.text,
        )
    except Exception as e:
        logger.exception("Error inesperado al reenviar métrica al store: %s", e)

    return {"status": "ok"}


@app.post("/ingest/log")
def ingest_log(event: LogEvent):
    """
    Recibe un LogEvent, valida automáticamente el esquema usando Pydantic
    """
    store_base = os.getenv("STORE_URL", "http://store:8000")
    store_endpoint = f"{store_base.rstrip('/')}/save/log"

    logger = logging.getLogger("collector")
    payload = event.model_dump(mode="json")
    try:
        with httpx.Client(timeout=2.0) as client:
            resp = client.post(store_endpoint, json=payload)
            resp.raise_for_status()
            return {"status": "ok", "store_response": resp.json()}
    except httpx.RequestError as e:
        logger.warning("No se pudo conectar al Store (%s): %s", store_endpoint, e)
    except httpx.HTTPStatusError as e:
        logger.warning(
            "El Store respondió con error %s: %s",
            e.response.status_code,
            e.response.text,
        )
    except Exception as e:
        logger.exception("Error inesperado al reenviar log al store: %s", e)

    return {"status": "ok"}


@app.post("/ingest/trace")
def ingest_trace(event: TraceEvent):
    """
    Recibe un TraceEvent, valida automáticamente el esquema usando Pydantic
    """
    store_base = os.getenv("STORE_URL", "http://store:8000")
    store_endpoint = f"{store_base.rstrip('/')}/save/trace"

    logger = logging.getLogger("collector")
    payload = event.model_dump(mode="json")
    try:
        with httpx.Client(timeout=2.0) as client:
            resp = client.post(store_endpoint, json=payload)
            resp.raise_for_status()
            return {"status": "ok", "store_response": resp.json()}
    except httpx.RequestError as e:
        logger.warning("No se pudo conectar al Store (%s): %s", store_endpoint, e)
    except httpx.HTTPStatusError as e:
        logger.warning(
            "El Store respondió con error %s: %s",
            e.response.status_code,
            e.response.text,
        )
    except Exception as e:
        logger.exception("Error inesperado al reenviar trace al store: %s", e)

    return {"status": "ok"}
