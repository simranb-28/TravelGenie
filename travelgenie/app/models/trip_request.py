from pydantic import BaseModel
from typing import Optional


class TripRequest(BaseModel):
    destination: str
    duration: int
    budget: str
    preferences: Optional[str] = None