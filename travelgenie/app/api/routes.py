from fastapi import APIRouter
from app.models.trip_request import TripRequest
from app.services.trip_service import generate_trip

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "healthy"}


@router.post("/generate-trip")
async def create_trip(request: TripRequest):
    return await generate_trip(request)