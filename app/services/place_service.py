from sqlalchemy.orm import Session
from app.core.constants import MAX_PLACES_PER_PROJECT
from app.db.models.place import Place
from app.schemas.place import PlaceUpdate
from app.utils.artic_api import artic_client


class PlaceService:
    def __init__(self, db: Session):
        self.db = db

    def add_place(self, project_id: int, external_id: str, notes: str = None):
        from app.db.models.project import Project

        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")

        if len(project.places) >= MAX_PLACES_PER_PROJECT:
            raise ValueError(f"Cannot have more than {MAX_PLACES_PER_PROJECT} places in a project")

        if any(p.external_id == external_id for p in project.places):
            raise ValueError("This place is already added to the project")

        if not artic_client.validate_place_exists(external_id):
            raise ValueError("Place does not exist in Art Institute API")

        place = Place(
            external_id=external_id,
            notes=notes,
            project_id=project.id
        )
        self.db.add(place)
        self.db.commit()
        self.db.refresh(place)
        return place

    def update_place(self, place_id: int, place_in: PlaceUpdate):
        place = self.db.query(Place).filter(Place.id == place_id).first()
        if not place:
            return None
        
        for field, value in place_in.dict(exclude_unset=True).items():
            setattr(place, field, value)
        
        self.db.commit()
        self.db.refresh(place)
        return place

    def get_place(self, place_id: int):
        return self.db.query(Place).filter(Place.id == place_id).first()
