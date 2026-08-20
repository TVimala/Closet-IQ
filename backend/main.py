"""Application entry point for the Closet-IQ backend."""

from fastapi import FastAPI

from backend.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to Closet-IQ backend"}
