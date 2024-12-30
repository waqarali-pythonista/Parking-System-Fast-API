from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Pydantic schema for creating a booking (used for input validation)
class BookingCreate(BaseModel):
    user_id: int
    parking_area_id: int
    booking_time: Optional[datetime] = None  # Can be specified, otherwise defaults to now
    status: Optional[str] = "pending"  # Default status is 'pending'

    class Config:
        orm_mode = True  # Tells Pydantic to work with ORM models (SQLAlchemy)

# Pydantic schema for updating a booking (e.g., changing status)
class BookingUpdate(BaseModel):
    status: Optional[str] = None

    class Config:
        orm_mode = True

# Pydantic schema for representing booking data (used for output responses)
class BookingResponse(BaseModel):
    id: int
    user_id: int
    parking_area_id: int
    booking_time: datetime
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
