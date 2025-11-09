from fastapi import FastAPI

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