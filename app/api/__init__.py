# app/api/__init__.py

# This file can be left empty or used to import API routes to make them accessible at the package level.
# By importing routes here, we can use `from app.api import user_routes, parking_area_routes, booking_routes` elsewhere in the application.

from .user_routes import router as user_router
from .parking_area_routes import router as parking_area_router
from .booking_routes import router as booking_router
