from fastapi import FastAPI
from src.contracts.events import LogEvent
import os
import logging
import httpx

app = FastAPI()

@app.get("/")
def home():
    """
    Root del viewer
    """
    return {"message": "Usted esta en el Viewer"}