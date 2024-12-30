from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from app.services.user_service import UserService
from app.database import get_db
from app.core.security import get_current_user, create_access_token
from app.models.user import User
from datetime import timedelta

# Define the router for user-related routes
router = APIRouter()

# Sign-up route for user creation
@router.post("/signup", response_model=UserResponse)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = UserService.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Create the new user
    created_user = UserService.create_user(db, user)
    return created_user

# Login route to get a JWT token
@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # Verify if the user exists and validate credentials
    db_user = UserService.get_user_by_email(db, user.email)
    if not db_user or not UserService.verify_user_password(db, user.email, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generate a JWT token
    access_token_expires = timedelta(minutes=30)  # Token expires in 30 minutes
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Get the current user's details
@router.get("/me", response_model=UserResponse)
async def get_user_details(current_user: User = Depends(get_current_user)):
    # Return the current user's details
    return current_user

# Update current user's details
@router.put("/me", response_model=UserResponse)
async def update_user_details(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Update the current user's details
    updated_user = UserService.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user
