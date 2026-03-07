from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import setup_logging
from fastapi.middleware.cors import CORSMiddleware

setup_logging()

app = FastAPI(
    title="TravelGenie AI",
    description="Intelligent Travel Orchestration Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Welcome to TravelGenie AI Travel Planner API",
        "docs": "/docs"
    }