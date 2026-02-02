from sqlalchemy.orm import Session
from app.core.constants import MAX_PLACES_PER_PROJECT
from app.db.models.project import Project
from app.db.models.place import Place
from app.schemas.project import ProjectCreate, ProjectUpdate, PlaceCreate
from app.utils.artic_api import validate_place_exists


class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, project_in: ProjectCreate):
        if len(project_in.places) > MAX_PLACES_PER_PROJECT:
            raise ValueError(f"Cannot have more than {MAX_PLACES_PER_PROJECT} places in a project")

        project = Project(
            name=project_in.name,
            description=project_in.description,
            start_date=project_in.start_date,
        )
        self.db.add(project)
        self.db.flush()

        for place_in in project_in.places:
            if not validate_place_exists(place_in.external_id):
                raise ValueError(f"Place {place_in.external_id} does not exist in Art Institute API")
            place = Place(
                external_id=place_in.external_id,
                notes=place_in.notes,
                project_id=project.id
            )
            self.db.add(place)

        self.db.commit()
        self.db.refresh(project)
        return project

    def get_project(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id).first()

    def list_projects(self):
        return self.db.query(Project).all()

    def update_project(self, project_id: int, project_in: ProjectUpdate):
        project = self.get_project(project_id)
        if not project:
            return None
        for field, value in project_in.dict(exclude_unset=True).items():
            setattr(project, field, value)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete_project(self, project_id: int):
        project = self.get_project(project_id)
        if not project:
            return None
        if any(p.visited for p in project.places):
            raise ValueError("Cannot delete project with visited places")
        self.db.delete(project)
        self.db.commit()
        return True
