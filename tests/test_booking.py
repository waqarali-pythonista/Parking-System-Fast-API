# test/test_booking.py

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.booking import BookingCreate, BookingUpdate
from app.database import SessionLocal, engine, get_db
from app.models.booking import Booking
from app.models.user import User
from app.models.parking_area import ParkingArea
import pytest

# Setup the TestClient
client = TestClient(app)

# Test creating a booking
def test_create_booking():
    # Prepare user data
    user_data = {
        "username": "bookinguser",
        "email": "bookinguser@example.com",
        "password": "testpassword"
    }
    # Create the user
    user_response = client.post("/users/signup", json=user_data)
    user = user_response.json()

    # Prepare parking area data
    parking_area_data = {
        "name": "Park Central",
        "location": "Central City",
        "available_slots": 10
    }
    # Create the parking area
    parking_area_response = client.post("/parking-areas/", json=parking_area_data)
    parking_area = parking_area_response.json()

    # Prepare booking data
    booking_data = {
        "user_id": user["id"],
        "parking_area_id": parking_area["id"],
        "status": "pending"
    }
    
    # Make a POST request to create the booking
    response = client.post("/bookings/", json=booking_data)
    
    # Check the response status and booking data
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user["id"]
    assert data["parking_area_id"] == parking_area["id"]
    assert data["status"] == "pending"
    assert "id" in data  # Ensure the booking ID is included

# Test retrieving a booking by ID
def test_get_booking():
    # Prepare user data
    user_data = {
        "username": "bookinguser2",
        "email": "bookinguser2@example.com",
        "password": "testpassword"
    }
    # Create the user
    user_response = client.post("/users/signup", json=user_data)
    user = user_response.json()

    # Prepare parking area data
    parking_area_data = {
        "name": "Park East",
        "location": "East City",
        "available_slots": 5
    }
    # Create the parking area
    parking_area_response = client.post("/parking-areas/", json=parking_area_data)
    parking_area = parking_area_response.json()

    # Create the booking
    booking_data = {
        "user_id": user["id"],
        "parking_area_id": parking_area["id"],
        "status": "pending"
    }
    booking_response = client.post("/bookings/", json=booking_data)
    booking = booking_response.json()

    # Retrieve the booking by ID
    response = client.get(f"/bookings/{booking['id']}")
    
    # Check the response status and data
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == booking["id"]
    assert data["user_id"] == user["id"]
    assert data["parking_area_id"] == parking["id"]
    assert data["status"] == "pending"

# Test updating a booking status
def test_update_booking_status():
    # Prepare user data
    user_data = {
        "username": "bookinguser3",
        "email": "bookinguser3@example.com",
        "password": "testpassword"
    }
    # Create the user
    user_response = client.post("/users/signup", json=user_data)
    user = user_response.json()

    # Prepare parking area data
    parking_area_data = {
        "name": "Park West",
        "location": "West City",
        "available_slots": 3
    }
    # Create the parking area
    parking_area_response = client.post("/parking-areas/", json=parking_area_data)
    parking_area = parking_area_response.json()

    # Create the booking
    booking_data = {
        "user_id": user["id"],
        "parking_area_id": parking_area["id"],
        "status": "pending"
    }
    booking_response = client.post("/bookings/", json=booking_data)
    booking = booking_response.json()

    # Prepare the update data
    update_data = {
        "status": "confirmed"
    }
    
    # Update the booking status
    response = client.put(f"/bookings/{booking['id']}", json=update_data)
    
    # Check the response status and updated data
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"

# Test cancelling a booking
def test_cancel_booking():
    # Prepare user data
    user_data = {
        "username": "bookinguser4",
        "email": "bookinguser4@example.com",
        "password": "testpassword"
    }
    # Create the user
    user_response = client.post("/users/signup", json=user_data)
    user = user_response.json()

    # Prepare parking area data
    parking_area_data = {
        "name": "Park South",
        "location": "South City",
        "available_slots": 20
    }
    # Create the parking area
    parking_area_response = client.post("/parking-areas/", json=parking_area_data)
    parking_area = parking_area_response.json()

    # Create the booking
    booking_data = {
        "user_id": user["id"],
        "parking_area_id": parking_area["id"],
        "status": "pending"
    }
    booking_response = client.post("/bookings/", json=booking_data)
    booking = booking_response.json()

    # Cancel the booking
    response = client.delete(f"/bookings/{booking['id']}")
    
    # Check the response status
    assert response.status_code == 204
    
    # Try to retrieve the cancelled booking
    response = client.get(f"/bookings/{booking['id']}")
    assert response.status_code == 404  # Booking should not exist after cancellation

# Test booking with no available slots
def test_create_booking_no_slots():
    # Prepare user data
    user_data = {
        "username": "bookinguser5",
        "email": "bookinguser5@example.com",
        "password": "testpassword"
    }
    # Create the user
    user_response = client.post("/users/signup", json=user_data)
    user = user_response.json()

    # Prepare parking area data with no available slots
    parking_area_data = {
        "name": "Full Park",
        "location": "Downtown",
        "available_slots": 0
    }
    # Create the parking area
    parking_area_response = client.post("/parking-areas/", json=parking_area_data)
    parking_area = parking_area_response.json()

    # Try to create a booking for the full parking area
    booking_data = {
        "user_id": user["id"],
        "parking_area_id": parking_area["id"],
        "status": "pending"
    }
    
    response = client.post("/bookings/", json=booking_data)
    
    # Check the response status and error message
    assert response.status_code == 400
    assert response.json()["detail"] == "No available slots in this parking area"
