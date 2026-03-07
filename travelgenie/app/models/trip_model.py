from pydantic import BaseModel, Field
from typing import List


class TripRequest(BaseModel):
    destination: str = Field(..., example="Paris")
    duration: int = Field(..., example=5)
    budget: int = Field(..., example=1500)
    preferences: List[str] = Field(
        default=[],
        example=["romantic", "low walking"]
    )


class TripResponse(BaseModel):
    destination: str
    duration: int
    budget: str
    budget_allocation: dict
    recommended_experiences: List[dict]
    weather: str
    itinerary: List[str]