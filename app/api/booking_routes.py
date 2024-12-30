from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from app.services.booking_service import BookingService
from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter()

# Route to create a new booking
@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create a new booking for the current user
    try:
        created_booking = BookingService.create_booking(db, booking, current_user)
        return created_booking
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Route to retrieve a booking by ID
@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Retrieve a booking by ID
    booking = BookingService.get_booking(db, booking_id)
    if not booking or booking.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found or unauthorized")
    return booking

# Route to retrieve all bookings of a specific user
@router.get("/user/{user_id}", response_model=list[BookingResponse])
async def get_user_bookings(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Retrieve all bookings for the current user
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view other users' bookings")
    bookings = BookingService.get_user_bookings(db, user_id)
    return bookings

# Route to update the status of a booking
@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking_status(
    booking_id: int,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Update booking status (e.g., confirmed, cancelled)
    updated_booking = BookingService.update_booking_status(db, booking_id, booking_update)
    if not updated_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return updated_booking

# Route to cancel a booking
@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Cancel a booking for the current user
    success = BookingService.cancel_booking(db, booking_id, current_user)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return {"message": "Booking cancelled successfully"}
