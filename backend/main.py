from fastapi import FastAPI
from api.outfit import router as outfit_router


app = FastAPI(
    title="Closet-IQ",
    description="Agentic AI Personal Wardrobe System"
)


app.include_router(outfit_router)


@app.get("/")
def home():
    return {
        "message": "Closet-IQ backend is running"
    }