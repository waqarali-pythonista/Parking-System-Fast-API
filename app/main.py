# app/main.py

from fastapi import FastAPI
from app.api.user_routes import router as user_router  # Ensure correct import of user router
from app.api.parking_area_routes import router as parking_area_router  # Correct import
from app.api.booking_routes import router as booking_router  # Correct import
from app.database import engine, Base
from app.core.config import SECRET_KEY, ALGORITHM
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI(
    title="Real-time Parking Booking System",
    description="A system to view parking areas, check space availability, and book parking slots.",
    version="1.0.0"
)

# Add CORS middleware to allow requests from all origins (useful for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the API routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(parking_area_router, prefix="/parking-areas", tags=["Parking Areas"])
app.include_router(booking_router, prefix="/bookings", tags=["Bookings"])

# Initialize the database
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Real-time Parking Booking System!"}
