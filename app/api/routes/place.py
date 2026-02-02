from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.place import PlaceUpdate
from app.schemas.project import PlaceRead
from app.services.place_service import PlaceService
from app.db.session import get_db

router = APIRouter(prefix="/places", tags=["Places"])

@router.post("/{project_id}", response_model=PlaceRead, status_code=status.HTTP_201_CREATED)
def add_place(project_id: int, external_id: str, notes: str = None, db: Session = Depends(get_db)):
    service = PlaceService(db)
    try:
        place = service.add_place(project_id, external_id, notes)
        return place
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{place_id}", response_model=PlaceRead)
def update_place(place_id: int, place_in: PlaceUpdate, db: Session = Depends(get_db)):
    service = PlaceService(db)
    place = service.update_place(place_id, place_in)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    return place

@router.get("/{place_id}", response_model=PlaceRead)
def get_place(place_id: int, db: Session = Depends(get_db)):
    service = PlaceService(db)
    place = service.get_place(place_id)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    return place
