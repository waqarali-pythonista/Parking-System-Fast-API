# test/test_parking_area.py

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.parking_area import ParkingAreaCreate, ParkingAreaUpdate
from app.database import SessionLocal, engine, get_db
from app.models.parking_area import ParkingArea
import pytest

# Setup the TestClient
client = TestClient(app)

# Test the creation of a parking area
def test_create_parking_area():
    # Prepare parking area data
    parking_area_data = {
        "name": "Central Park",
        "location": "Downtown",
        "available_slots": 50
    }
    
    # Make a POST request to create the parking area
    response = client.post("/parking-areas/", json=parking_area_data)
    
    # Check the response status and parking area data
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == parking_area_data["name"]
    assert data["location"] == parking_area_data["location"]
    assert data["available_slots"] == parking_area_data["available_slots"]
    assert "id" in data  # Ensure the parking area ID is included

# Test retrieving a parking area by ID
def test_get_parking_area():
    # Prepare parking area data
    parking_area_data = {
        "name": "Park Plaza",
        "location": "Uptown",
        "available_slots": 30
    }
    
    # Create the parking area
    response = client.post("/parking-areas/", json=parking_area_data)
    created_parking_area = response.json()
    
    # Get the parking area by ID
    response = client.get(f"/parking-areas/{created_parking_area['id']}")
    
    # Check the response status and data
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_parking_area["id"]
    assert data["name"] == parking_area_data["name"]

# Test retrieving all parking areas
def test_get_all_parking_areas():
    # Prepare parking area data
    parking_area_data_1 = {
        "name": "Park West",
        "location": "West End",
        "available_slots": 25
    }
    parking_area_data_2 = {
        "name": "Park East",
        "location": "East End",
        "available_slots": 40
    }
    
    # Create two parking areas
    client.post("/parking-areas/", json=parking_area_data_1)
    client.post("/parking-areas/", json=parking_area_data_2)
    
    # Get all parking areas
    response = client.get("/parking-areas/")
    
    # Check the response status and data
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # There should be at least two parking areas
    assert any(area["name"] == "Park West" for area in data)
    assert any(area["name"] == "Park East" for area in data)

# Test updating a parking area
def test_update_parking_area():
    # Prepare parking area data
    parking_area_data = {
        "name": "Park North",
        "location": "North Side",
        "available_slots": 20
    }
    
    # Create the parking area
    response = client.post("/parking-areas/", json=parking_area_data)
    created_parking_area = response.json()
    
    # Prepare updated data
    updated_data = {
        "name": "Park North Updated",
        "location": "North Side (Updated)",
        "available_slots": 35
    }
    
    # Update the parking area
    response = client.put(f"/parking-areas/{created_parking_area['id']}", json=updated_data)
    
    # Check the response status and updated data
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["location"] == updated_data["location"]
    assert data["available_slots"] == updated_data["available_slots"]

# Test deleting a parking area
def test_delete_parking_area():
    # Prepare parking area data
    parking_area_data = {
        "name": "Park South",
        "location": "South Side",
        "available_slots": 10
    }
    
    # Create the parking area
    response = client.post("/parking-areas/", json=parking_area_data)
    created_parking_area = response.json()
    
    # Delete the parking area
    response = client.delete(f"/parking-areas/{created_parking_area['id']}")
    
    # Check the response status
    assert response.status_code == 204
    
    # Try to get the deleted parking area
    response = client.get(f"/parking-areas/{created_parking_area['id']}")
    assert response.status_code == 404  # Should return "Not Found" after deletion

# Test for duplicate parking area creation (e.g., same name)
def test_create_parking_area_duplicate_name():
    # Prepare parking area data
    parking_area_data = {
        "name": "Duplicate Park",
        "location": "City Center",
        "available_slots": 15
    }
    
    # Create the first parking area
    client.post("/parking-areas/", json=parking_area_data)
    
    # Try creating the same parking area again
    response = client.post("/parking-areas/", json=parking_area_data)
    
    # Check that it returns a conflict status code
    assert response.status_code == 400
    assert response.json()["detail"] == "Parking area with this name already exists"
