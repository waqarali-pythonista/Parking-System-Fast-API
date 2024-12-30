# app/schemas/user.py

from pydantic import BaseModel
from datetime import datetime

# Schema for creating a new user
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"  # Default role is "user"

    class Config:
        from_attributes = True  # Pydantic V2 compatibility for working with ORM models

# Schema for logging in (used for user login)
class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True  # Pydantic V2 compatibility for working with ORM models

# Schema for updating a user
class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    role: str | None = None

    class Config:
        from_attributes = True  # Pydantic V2 compatibility for working with ORM models

# Schema for returning user data in response (used for user info)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic V2 compatibility for working with ORM models
