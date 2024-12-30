# app/services/user_service.py

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password, get_current_user
from fastapi import HTTPException, status

class UserService:

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """
        Create a new user and hash the password before saving to the database.
        """
        db_user = User(username=user.username, email=user.email, role=user.role)
        db_user.password_hash = hash_password(user.password)  # Hash the password before saving
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """
        Retrieve a user by their ID.
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """
        Retrieve a user by their email address.
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
        """
        Update the details of an existing user.
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            # Update only the fields that are provided
            for field, value in user_update.dict(exclude_unset=True).items():
                setattr(db_user, field, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def verify_user_password(db: Session, email: str, password: str) -> bool:
        """
        Verify the user's password by comparing the hashed password.
        """
        db_user = db.query(User).filter(User.email == email).first()
        if db_user and verify_password(password, db_user.password_hash):
            return True
        return False

    @staticmethod
    def get_user_by_token(db: Session, token: str) -> User:
        """
        Retrieve the current user from the token.
        This method should verify the JWT token and get the associated user.
        """
        user = get_current_user(token)  # Extract current user from token
        if user:
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
