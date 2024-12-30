# app/core/config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configuration values
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Secret key for JWT token signing
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Algorithm for JWT encoding
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Token expiration time in minutes

# Database configuration
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Email configuration (if you plan to use email for sending notifications)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "your-email@example.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-email-password")
