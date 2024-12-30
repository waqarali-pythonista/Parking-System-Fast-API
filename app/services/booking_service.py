# app/services/booking_service.py

from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.parking_area import ParkingArea
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingUpdate
from datetime import datetime

class BookingService:

    @staticmethod
    def create_booking(db: Session, booking_data: BookingCreate, user: User) -> Booking:
        # Check if the parking area exists
        parking_area = db.query(ParkingArea).filter(ParkingArea.id == booking_data.parking_area_id).first()
        if not parking_area:
            raise ValueError("Parking area not found")

        # Check if there are available slots
        if parking_area.available_slots <= 0:
            raise ValueError("No available slots in this parking area")

        # Create the booking
        booking = Booking(
            user_id=user.id,
            parking_area_id=booking_data.parking_area_id,
            booking_time=booking_data.booking_time or datetime.utcnow(),
            status=booking_data.status
        )
        db.add(booking)
        
        # Decrease available slots for the parking area
        parking_area.available_slots -= 1
        
        # Commit changes
        db.commit()
        db.refresh(booking)
        db.refresh(parking_area)
        
        return booking

    @staticmethod
    def get_booking(db: Session, booking_id: int) -> Booking:
        # Retrieve a booking by id
        return db.query(Booking).filter(Booking.id == booking_id).first()

    @staticmethod
    def cancel_booking(db: Session, booking_id: int, user: User) -> bool:
        # Retrieve the booking by id
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        
        if not booking:
            raise ValueError("Booking not found")
        
        # Check if the booking belongs to the user
        if booking.user_id != user.id:
            raise ValueError("You cannot cancel someone else's booking")
        
        # Change booking status to 'cancelled'
        booking.status = "cancelled"
        
        # Revert the available slots in the parking area
        parking_area = db.query(ParkingArea).filter(ParkingArea.id == booking.parking_area_id).first()
        if parking_area:
            parking_area.available_slots += 1
        
        # Commit the changes
        db.commit()
        db.refresh(booking)
        db.refresh(parking_area)
        
        return True

    @staticmethod
    def update_booking_status(db: Session, booking_id: int, booking_update: BookingUpdate) -> Booking:
        # Retrieve the booking by id
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        
        if not booking:
            raise ValueError("Booking not found")
        
        # Update the booking status
        if booking_update.status:
            booking.status = booking_update.status
        
        # Commit the changes
        db.commit()
        db.refresh(booking)
        
        return booking

    @staticmethod
    def get_user_bookings(db: Session, user_id: int) -> list[Booking]:
        # Retrieve all bookings for a specific user
        return db.query(Booking).filter(Booking.user_id == user_id).all()
