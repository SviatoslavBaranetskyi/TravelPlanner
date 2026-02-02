from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService
from app.api.dependencies import get_db_session

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate, db: Session = get_db_session()):
    service = ProjectService(db)
    try:
        project = service.create_project(project_in)
        return project
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[ProjectRead])
def list_projects(db: Session = get_db_session()):
    service = ProjectService(db)
    return service.list_projects()

@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = get_db_session()):
    service = ProjectService(db)
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, project_in: ProjectUpdate, db: Session = get_db_session()):
    service = ProjectService(db)
    project = service.update_project(project_id, project_in)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = get_db_session()):
    service = ProjectService(db)
    try:
        service.delete_project(project_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
