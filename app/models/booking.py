from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base  # Import Base from app.models.base
from datetime import datetime

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    parking_area_id = Column(Integer, ForeignKey("parking_areas.id"))
    status = Column(String, default="pending")
    booking_time = Column(DateTime, default=datetime.utcnow)  # When the booking was made
    created_at = Column(DateTime, default=datetime.utcnow)  # Automatically set when a record is created
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Automatically updated

    # Define relationships
    user = relationship("User", back_populates="bookings")
    parking_area = relationship("ParkingArea", back_populates="bookings")

    def __repr__(self):
        return f"Booking(id={self.id}, user_id={self.user_id}, parking_area_id={self.parking_area_id}, status={self.status})"
