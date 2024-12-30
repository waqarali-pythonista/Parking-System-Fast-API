# app/services/parking_area_service.py

from sqlalchemy.orm import Session
from app.models.parking_area import ParkingArea
from app.schemas.parking_area import ParkingAreaCreate, ParkingAreaUpdate

class ParkingAreaService:

    @staticmethod
    def create_parking_area(db: Session, parking_area: ParkingAreaCreate) -> ParkingArea:
        db_parking_area = ParkingArea(
            name=parking_area.name,
            location=parking_area.location,
            available_slots=parking_area.available_slots
        )
        db.add(db_parking_area)
        db.commit()
        db.refresh(db_parking_area)
        return db_parking_area

    @staticmethod
    def get_parking_area(db: Session, parking_area_id: int) -> ParkingArea:
        return db.query(ParkingArea).filter(ParkingArea.id == parking_area_id).first()

    @staticmethod
    def get_all_parking_areas(db: Session) -> list[ParkingArea]:
        return db.query(ParkingArea).all()

    @staticmethod
    def update_parking_area(db: Session, parking_area_id: int, parking_area_update: ParkingAreaUpdate) -> ParkingArea:
        db_parking_area = db.query(ParkingArea).filter(ParkingArea.id == parking_area_id).first()
        if db_parking_area:
            for field, value in parking_area_update.dict(exclude_unset=True).items():
                setattr(db_parking_area, field, value)
            db.commit()
            db.refresh(db_parking_area)
        return db_parking_area

    @staticmethod
    def delete_parking_area(db: Session, parking_area_id: int) -> bool:
        db_parking_area = db.query(ParkingArea).filter(ParkingArea.id == parking_area_id).first()
        if db_parking_area:
            db.delete(db_parking_area)
            db.commit()
            return True
        return False
