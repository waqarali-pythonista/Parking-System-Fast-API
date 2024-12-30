# test/test_user.py

from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.schemas.user import UserCreate
from app.database import SessionLocal, engine, get_db
from app.core.security import hash_password
import pytest

# Setup the TestClient
client = TestClient(app)

# Test the user creation (signup)
def test_create_user():
    # Prepare user data
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    
    # Make a POST request to the signup route
    response = client.post("/users/signup", json=user_data)
    
    # Check the response status and user data
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data  # Ensure the user ID is included

# Test user login (authentication)
def test_login_user():
    # Prepare login credentials
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    
    # Make a POST request to the login route
    response = client.post("/users/login", json=login_data)
    
    # Check the response status and access token
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# Test the retrieval of current user details (protected route)
def test_get_current_user():
    # First, create a user to test with
    user_data = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "testpassword"
    }
    response = client.post("/users/signup", json=user_data)
    user = response.json()

    # Get the access token for the created user
    login_data = {
        "email": "testuser2@example.com",
        "password": "testpassword"
    }
    login_response = client.post("/users/login", json=login_data)
    access_token = login_response.json()["access_token"]
    
    # Make a GET request to retrieve the current user details
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    
    # Check that the response matches the user's details
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]

# Test user update
def test_update_user():
    # Prepare user data
    user_data = {
        "username": "testuser3",
        "email": "testuser3@example.com",
        "password": "testpassword"
    }
    response = client.post("/users/signup", json=user_data)
    user = response.json()
    
    # Prepare new update data
    update_data = {
        "username": "updateduser3",
        "email": "updateduser3@example.com",
        "password": "updatedpassword"
    }
    
    # Get the access token
    login_data = {
        "email": "testuser3@example.com",
        "password": "testpassword"
    }
    login_response = client.post("/users/login", json=login_data)
    access_token = login_response.json()["access_token"]
    
    # Make a PUT request to update user data
    response = client.put("/users/me", json=update_data, headers={"Authorization": f"Bearer {access_token}"})
    
    # Check the updated response data
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == update_data["username"]
    assert data["email"] == update_data["email"]

# Test for duplicate user registration (signup)
def test_create_user_duplicate_email():
    # Prepare user data
    user_data = {
        "username": "testuser",
        "email": "duplicate@example.com",
        "password": "testpassword"
    }
    # Create the user for the first time
    client.post("/users/signup", json=user_data)
    
    # Try creating the same user again
    response = client.post("/users/signup", json=user_data)
    
    # Check that it returns a conflict status code
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
