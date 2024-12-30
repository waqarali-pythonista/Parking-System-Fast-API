# app/models/parking_area.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base  # Import Base from app.models.base

class ParkingArea(Base):
    __tablename__ = 'parking_areas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    available_slots = Column(Integer)

    bookings = relationship("Booking", back_populates="parking_area")

    def __repr__(self):
        return f"ParkingArea(id={self.id}, name={self.name}, location={self.location}, available_slots={self.available_slots})"
