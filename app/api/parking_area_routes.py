# app/api/parking_area_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.parking_area import ParkingAreaCreate, ParkingAreaUpdate, ParkingAreaResponse
from app.services.parking_area_service import ParkingAreaService
from app.database import get_db
from app.models.parking_area import ParkingArea

router = APIRouter()

@router.post("/", response_model=ParkingAreaResponse, status_code=status.HTTP_201_CREATED)
async def create_parking_area(parking_area: ParkingAreaCreate, db: Session = Depends(get_db)):
    # Create a new parking area
    created_parking_area = ParkingAreaService.create_parking_area(db, parking_area)
    return created_parking_area

@router.get("/{parking_area_id}", response_model=ParkingAreaResponse)
async def get_parking_area(parking_area_id: int, db: Session = Depends(get_db)):
    # Retrieve a parking area by ID
    parking_area = ParkingAreaService.get_parking_area(db, parking_area_id)
    if not parking_area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parking area not found")
    return parking_area

@router.get("/", response_model=list[ParkingAreaResponse])
async def get_all_parking_areas(db: Session = Depends(get_db)):
    # Retrieve all parking areas
    parking_areas = ParkingAreaService.get_all_parking_areas(db)
    return parking_areas

@router.put("/{parking_area_id}", response_model=ParkingAreaResponse)
async def update_parking_area(parking_area_id: int, parking_area_update: ParkingAreaUpdate, db: Session = Depends(get_db)):
    # Update an existing parking area
    updated_parking_area = ParkingAreaService.update_parking_area(db, parking_area_id, parking_area_update)
    if not updated_parking_area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parking area not found")
    return updated_parking_area

@router.delete("/{parking_area_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parking_area(parking_area_id: int, db: Session = Depends(get_db)):
    # Delete a parking area
    success = ParkingAreaService.delete_parking_area(db, parking_area_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parking area not found")
    return {"message": "Parking area deleted successfully"}
