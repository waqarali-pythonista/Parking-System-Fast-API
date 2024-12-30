# app/models/user.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base  # Import Base from app.models.base
from datetime import datetime

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="user")
    
    # Using DateTime for created_at and updated_at for better timestamp management
    created_at = Column(DateTime, default=datetime.utcnow)  # Automatically set to current UTC time
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Updated on changes
    
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, role={self.role})"

    # Implement password hashing
    def set_password(self, password: str) -> None:
        """
        Set the password for the user, hashed before storing.
        """
        from app.core.security import hash_password
        self.password_hash = hash_password(password)
    
    # Check if the password matches the hashed password
    def check_password(self, password: str) -> bool:
        """
        Verify if the given password matches the stored hashed password.
        """
        from app.core.security import verify_password
        return verify_password(password, self.password_hash)
