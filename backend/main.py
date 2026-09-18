from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.wardrobe import router as wardrobe_router

from api.profile import router as profile_router

from api.outfit import router as outfit_router

from api.finance import router as finance_router

from api.feedback import router as feedback_router

from api.notification import router as notification_router

from services.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: begin the local notification scheduler
    # (APScheduler). Contains no business logic itself - it only
    # triggers orchestrator.graph.run_notification_check on a
    # schedule for every user.
    start_scheduler()

    yield

    # Shutdown
    stop_scheduler()


app = FastAPI(
    title="WardrobeWise API",
    description="Agentic AI Wardrobe and Purchase Decision System",
    version="1.0.0",
    lifespan=lifespan,
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

app.include_router(outfit_router)

app.include_router(finance_router)

app.include_router(feedback_router)

app.include_router(notification_router)


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
