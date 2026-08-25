from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.wardrobe import router as wardrobe_router

from api.profile import router as profile_router


app = FastAPI(
    title="WardrobeWise API",
    description="Agentic AI Wardrobe and Purchase Decision System",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(wardrobe_router)

app.include_router(profile_router)

@app.get("/")
def root():
    return {
        "message": "WardrobeWise backend is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api/test")
def test_connection():
    return {
        "success": True,
        "message": "React and FastAPI are connected!"
    }