# app/schemas/parking_area.py

from pydantic import BaseModel
from typing import Optional

# Pydantic schema for creating a parking area (used for input validation)
class ParkingAreaCreate(BaseModel):
    name: str
    location: str
    available_slots: int

    class Config:
        orm_mode = True  # Tells Pydantic to work with ORM models (SQLAlchemy)

# Pydantic schema for updating a parking area (e.g., change available slots or location)
class ParkingAreaUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    available_slots: Optional[int] = None

    class Config:
        orm_mode = True

# Pydantic schema for representing parking area data (used for output responses)
class ParkingAreaResponse(BaseModel):
    id: int
    name: str
    location: str
    available_slots: int

    class Config:
        orm_mode = True
